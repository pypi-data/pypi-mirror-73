# coding=utf-8
from __future__ import absolute_import, division, print_function

import functools
import math
import os

import oss2
from lostc import collection as lcc
from oss2.models import PartInfo
from oss2.resumable import ResumableDownloadStore, ResumableStore

from suanpan import api, asyncio, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.log import logger
from suanpan.storage import base
from suanpan.utils import pbar as spbar


class Storage(base.Storage):
    LARGE_FILE_SIZE = 1024 * 1024 * 1024  # 1GB
    PREFERRED_SIZE = 500 * 1024 * 1024  # 500MB

    def __init__(
        self,
        ossAccessId=None,
        ossAccessKey=None,
        ossBucketName="suanpan",
        ossEndpoint="http://oss-cn-beijing.aliyuncs.com",
        ossDelimiter="/",
        ossTempStore=base.Storage.DEFAULT_TEMP_DATA_STORE,
        ossGlobalStore=base.Storage.DEFAULT_GLOBAL_DATA_STORE,
        ossDownloadNumThreads=1,
        ossDownloadStoreName=".py-oss-download",
        ossUploadNumThreads=1,
        ossUploadStoreName=".py-oss-upload",
        **kwargs,
    ):
        super(Storage, self).__init__(
            delimiter=ossDelimiter,
            tempStore=ossTempStore,
            globalStore=ossGlobalStore,
            **kwargs,
        )

        self.bucketName = ossBucketName
        self.endpoint = ossEndpoint
        self.refreshAccessKey(accessId=ossAccessId, accessKey=ossAccessKey)

        self.downloadNumThreads = ossDownloadNumThreads
        self.downloadStoreName = ossDownloadStoreName
        self.downloadStore = ResumableDownloadStore(
            self.tempStore, self.downloadStoreName
        )

        self.uploadNumThreads = ossUploadNumThreads
        self.uploadStoreName = ossUploadStoreName
        self.uploadStore = ResumableStore(self.tempStore, self.uploadStoreName)

        self._removeOssLogger()

    def autoRefreshToken(self, func):
        @functools.wraps(func)
        def _dec(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except oss2.exceptions.OssError as e:
                if e.status != 403:
                    raise e
                logger.warning("Oss access denied, refreshing access key.")
                self.refreshAccessKey()
                return func(*args, **kwargs)

        return _dec

    def autoRefreshBucket(self, bucket):
        try:
            bucket.object_exists(f"studio/{g.userId}/permissions")
            return bucket
        except oss2.exceptions.OssError as e:
            if e.status != 403:
                raise e
            logger.warning("Oss access denied, refreshing access key.")
            self.refreshAccessKey()
            bucket = self.getBucketByName(bucket.bucket_name)
            return bucket

    def refreshAccessKey(self, accessId=None, accessKey=None):
        if accessId and accessKey:
            self.accessId = accessId
            self.accessKey = accessKey
            self.auth = oss2.Auth(self.accessId, self.accessKey)
        else:
            data = api.oss.getToken()
            self.accessId = data["Credentials"]["AccessKeyId"]
            self.accessKey = data["Credentials"]["AccessKeySecret"]
            self.securityToken = data["Credentials"]["SecurityToken"]
            self.auth = oss2.StsAuth(self.accessId, self.accessKey, self.securityToken)

        self.bucket = self.getBucket(self.bucketName)
        return self.accessId, self.accessKey

    def _removeOssLogger(self):
        ossLogger = getattr(oss2, "logger", None)
        if ossLogger:
            self._removeLoggerHandlers(ossLogger)

    def _removeLoggerHandlers(self, _logger):
        for handler in _logger.handlers[:]:
            _logger.removeHandler(handler)
        return _logger

    @runtime.retry(stop_max_attempt_number=3)
    def download(self, name, path, bucketOrBucketName=None, ignores=None):
        bucket = self.getBucket(bucketOrBucketName)
        ignores = ignores or self.DEFAULT_IGNORE_KEYWORDS
        downloadFunction = (
            self.downloadFile
            if self.isFile(name, bucketOrBucketName=bucket)
            else self.downloadFolder
        )
        return downloadFunction(name, path, bucketOrBucketName=bucket, ignores=ignores)

    def downloadFolder(
        self,
        folderName,
        folderPath,
        delimiter=None,
        bucketOrBucketName=None,
        ignores=None,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        ignores = ignores or self.DEFAULT_IGNORE_KEYWORDS
        delimiter = delimiter or self.delimiter
        storagePath = self.storageUrl(folderName, bucketOrBucketName=bucket)

        if folderPath in ignores:
            logger.debug(f"Ignore downloading folder: {folderPath} -> {storagePath}")
            return folderPath

        downloads = {
            file: self.localPathJoin(
                folderPath, self.storageRelativePath(file, folderName)
            )
            for _, _, files in self.walk(
                folderName, delimiter=delimiter, bucketOrBucketName=bucket
            )
            for file in files
        }

        logger.info(f"Downloading folder: {storagePath} -> {folderPath}")
        # Download from oss
        _run = functools.partial(
            self.downloadFile, bucketOrBucketName=bucket, ignores=ignores, quiet=True
        )
        asyncio.starmap(_run, downloads.items(), pbar="Downloading")
        # Remove ignores
        self.removeIgnores(folderPath, ignores=ignores)
        # Remove rest files and folders
        files = (
            os.path.join(root, file)
            for root, _, files in os.walk(folderPath)
            for file in files
        )
        restFiles = [file for file in files if file not in downloads.values()]
        asyncio.map(
            spath.remove, restFiles, pbar="Removing Rest Files" if restFiles else False,
        )
        spath.removeEmptyFolders(folderPath)
        logger.debug(f"Removed empty folders in: {folderPath}")
        # End
        logger.debug(f"Downloaded folder: {storagePath} -> {folderPath}")
        return folderPath

    def downloadFile(
        self, objectName, filePath, bucketOrBucketName=None, ignores=None, quiet=False
    ):
        bucket = self.getBucket(bucketOrBucketName)
        ignores = ignores or self.DEFAULT_IGNORE_KEYWORDS
        storagePath = self.storageUrl(objectName, bucketOrBucketName=bucket)
        fileSize = self.getStorageSize(objectName, bucketOrBucketName=bucket)

        if not quiet:
            logger.info(f"Downloading file: {storagePath} -> {filePath}")

        with spbar.one(total=fileSize, config=not quiet) as pbar:
            if filePath in ignores:
                pbar.update(fileSize)
                pbar.set_description("Ignored")
                return filePath

            fileMd5 = self.getLocalMd5(filePath)
            objectMd5 = self.getStorageMd5(objectName, bucketOrBucketName=bucket)
            if self.checkMd5(fileMd5, objectMd5):
                pbar.update(fileSize)
                pbar.set_description("Existed")
                return filePath

            def _percentage(consumed_bytes, total_bytes):
                if total_bytes:
                    pbar.update(consumed_bytes - pbar.n)
                    pbar.set_description("Downloading")

            spath.safeMkdirsForFile(filePath)
            self.autoRefreshToken(oss2.resumable_download)(
                bucket,
                objectName,
                filePath,
                num_threads=self.downloadNumThreads,
                store=self.downloadStore,
                progress_callback=_percentage,
            )

            pbar.set_description("Downloaded")

            return filePath

    @runtime.retry(stop_max_attempt_number=3)
    def upload(self, name, path, bucketOrBucketName=None, ignores=None):
        bucket = self.getBucket(bucketOrBucketName)
        ignores = ignores or self.DEFAULT_IGNORE_KEYWORDS
        uploadFunction = self.uploadFolder if os.path.isdir(path) else self.uploadFile
        return uploadFunction(name, path, bucketOrBucketName=bucket, ignores=ignores)

    def uploadFolder(
        self, folderName, folderPath, bucketOrBucketName=None, ignores=None,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        ignores = ignores or self.DEFAULT_IGNORE_KEYWORDS
        storagePath = self.storageUrl(folderName, bucketOrBucketName=bucket)

        if folderName in ignores:
            logger.debug(f"Ignore uploading folder: {folderName} -> {storagePath}")
            return folderPath

        filePaths = (
            os.path.join(root, file)
            for root, _, files in os.walk(folderPath)
            for file in files
        )
        uploads = {
            filePath: self.storagePathJoin(
                folderName, self.localRelativePath(filePath, folderPath)
            )
            for filePath in filePaths
        }

        if not uploads:
            logger.warning(f"Uploading empty folder: {folderPath}")
        else:
            logger.info(f"Uploading folder: {folderPath} -> {storagePath}")
            # Upload files to oss
            uploadItems = [
                (objectName, filePath) for filePath, objectName in uploads.items()
            ]
            _run = functools.partial(
                self.uploadFile, bucketOrBucketName=bucket, ignores=ignores, quiet=True
            )
            asyncio.starmap(_run, uploadItems, pbar="Uploading")

        # Remove rest files
        localFiles = set(
            self.localRelativePath(filePath, folderPath) for filePath in uploads.keys()
        )
        remoteFiles = set(
            self.storageRelativePath(objectName, folderName)
            for _, _, files in self.walk(folderName)
            for objectName in files
        )
        restFiles = [
            self.storagePathJoin(folderName, file) for file in remoteFiles - localFiles
        ]
        _run = functools.partial(self.remove, bucketOrBucketName=bucket, quiet=True)
        asyncio.map(
            _run, restFiles, pbar="Removing Rest Files" if restFiles else False,
        )
        # End
        logger.debug(f"Uploaded folder: {folderPath} -> {storagePath}")
        return folderPath

    def uploadFile(
        self, objectName, filePath, bucketOrBucketName=None, ignores=None, quiet=False
    ):
        bucket = self.getBucket(bucketOrBucketName)
        ignores = ignores or self.DEFAULT_IGNORE_KEYWORDS
        storagePath = self.storageUrl(objectName, bucketOrBucketName=bucket)
        fileSize = self.getLocalSize(filePath)

        if not quiet:
            logger.info(f"Uploading file: {filePath} -> {storagePath}")

        with spbar.one(total=fileSize, config=not quiet) as pbar:
            if filePath in ignores:
                pbar.update(fileSize)
                pbar.set_description("Ignored")
                return filePath

            fileMd5 = self.getLocalMd5(filePath)
            objectMd5 = self.getStorageMd5(objectName, bucketOrBucketName=bucket)
            if self.checkMd5(fileMd5, objectMd5):
                pbar.update(fileSize)
                pbar.set_description("Existed")
                return filePath

            def _percentage(consumed_bytes, total_bytes):
                if total_bytes:
                    pbar.update(consumed_bytes - pbar.n)
                    pbar.set_description("Uploading")

            self.autoRefreshToken(oss2.resumable_upload)(
                bucket,
                objectName,
                filePath,
                num_threads=self.uploadNumThreads,
                store=self.uploadStore,
                progress_callback=_percentage,
                headers={self.CONTENT_MD5: fileMd5},
            )

            pbar.set_description("Uploaded")

            return filePath

    @runtime.retry(stop_max_attempt_number=3)
    def copy(self, name, dist, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        copyFunction = (
            self.copyFile
            if self.isFile(name, bucketOrBucketName=bucket)
            else self.copyFolder
        )
        return copyFunction(name, dist, bucketOrBucketName=bucket)

    def copyFolder(
        self, folderName, distName, bucketOrBucketName=None, delimiter=None,
    ):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        folderName = self.completePath(folderName)
        distName = self.completePath(distName)
        logger.info(f"Copying folder: {folderName} -> {distName}")
        copyItems = [
            (file, file.replace(folderName, distName))
            for _, _, files in self.walk(
                folderName, delimiter=delimiter, bucketOrBucketName=bucket
            )
            for file in files
        ]
        _run = functools.partial(self.copyFile, bucketOrBucketName=bucket, quiet=True)
        asyncio.starmap(_run, copyItems, pbar="Copying")

    def copyFile(self, objectName, distName, bucketOrBucketName=None, quiet=False):
        bucket = self.getBucket(bucketOrBucketName)
        fileSize = self.getStorageSize(objectName, bucketOrBucketName=bucket)
        copyFunction = (
            self.copyLargeFile
            if fileSize >= self.LARGE_FILE_SIZE
            else self.copySmallFile
        )
        return copyFunction(
            objectName, distName, fileSize, bucketOrBucketName=bucket, quiet=quiet
        )

    def copySmallFile(
        self, objectName, distName, size, bucketOrBucketName=None, quiet=False
    ):
        bucket = self.getBucket(bucketOrBucketName)

        if not quiet:
            _src = self.storageUrl(objectName, bucketOrBucketName=bucket)
            _target = self.storageUrl(distName, bucketOrBucketName=bucket)
            logger.info(f"Copying file: {_src} -> {_target}")

        with spbar.one(total=size, config=not quiet) as pbar:
            objectMd5 = self.getStorageMd5(objectName, bucketOrBucketName=bucket)
            distMd5 = self.getStorageMd5(distName, bucketOrBucketName=bucket)
            if self.checkMd5(objectMd5, distMd5):
                pbar.update(size)
                pbar.set_description("Existed")
                return distName

            bucket.copy_object(bucket.bucket_name, objectName, distName)
            pbar.update(size)
            return distName

    def copyLargeFile(
        self, objectName, distName, size, bucketOrBucketName=None, quiet=False
    ):
        bucket = self.getBucket(bucketOrBucketName)

        if not quiet:
            _src = self.storageUrl(objectName, bucketOrBucketName=bucket)
            _target = self.storageUrl(distName, bucketOrBucketName=bucket)
            logger.info(f"Copying file: {_src} -> {_target}")

        with spbar.one(total=size, config=not quiet) as pbar:
            objectMd5 = self.getStorageMd5(objectName, bucketOrBucketName=bucket)
            distMd5 = self.getStorageMd5(objectName, bucketOrBucketName=bucket)
            if self.checkMd5(objectMd5, distMd5):
                pbar.update(size)
                pbar.set_description("Existed")
                return distName

            partSize = self.autoRefreshToken(oss2.determine_part_size)(
                size, preferred_size=self.PREFERRED_SIZE
            )
            uploadId = bucket.init_multipart_upload(distName).upload_id
            parts = math.ceil(size / partSize)
            parts = (
                (i + 1, i * partSize, min((i + 1) * partSize, size))
                for i in range(parts)
            )

            def _copy(part):
                partNumber, byteRange = part[0], part[-2:]
                result = bucket.upload_part_copy(
                    bucket.bucket_name,
                    objectName,
                    byteRange,
                    distName,
                    uploadId,
                    partNumber,
                )
                pbar.update(byteRange[1] - byteRange[0])
                return PartInfo(partNumber, result.etag)

            parts = [_copy(part) for part in parts]
            bucket.complete_multipart_upload(distName, uploadId, parts)
            return distName

    @runtime.retry(stop_max_attempt_number=3)
    def remove(
        self, objectName, delimiter=None, bucketOrBucketName=None, quiet=False,
    ):
        delimiter = delimiter or self.delimiter
        bucket = self.getBucket(bucketOrBucketName)
        removeFunc = (
            self.removeFile
            if self.isFile(objectName, bucketOrBucketName=bucket)
            else self.removeFolder
        )
        return removeFunc(
            objectName, delimiter=delimiter, bucketOrBucketName=bucket, quiet=quiet
        )

    def removeFolder(
        self, folderName, delimiter=None, bucketOrBucketName=None, quiet=False,
    ):
        delimiter = delimiter or self.delimiter
        bucket = self.getBucket(bucketOrBucketName)
        folderName = self.completePath(folderName)
        removes = [
            objectName for _, _, files in self.walk(folderName) for objectName in files
        ]
        _run = functools.partial(
            self.remove, delimiter=delimiter, bucketOrBucketName=bucket, quiet=True
        )
        asyncio.map(
            _run, removes, pbar="Removing" if removes and not quiet else False,
        )
        return folderName

    def removeFile(
        self, fileName, delimiter=None, bucketOrBucketName=None, quiet=False
    ):  # pylint: disable=unused-argument
        bucket = self.getBucket(bucketOrBucketName)
        bucket.delete_object(fileName)
        if not quiet:
            storagePath = self.storageUrl(fileName, bucketOrBucketName=bucket)
            logger.info(f"Removed file: {storagePath}")
        return fileName

    def walk(self, folderName, delimiter=None, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        root = self.completePath(folderName, delimiter=delimiter)
        objects = (
            obj
            for obj in runtime.saferun(self._listAll, default=iter(()))(
                folderName, delimiter=delimiter, bucketOrBucketName=bucket
            )
            if obj.key != root
        )
        folders, files = lcc.divide(objects, lambda obj: obj.is_prefix())
        folders, files = self._getObjectNames(folders), self._getObjectNames(files)
        yield root, folders, files
        for folder in folders:
            for item in self.walk(
                folder, delimiter=delimiter, bucketOrBucketName=bucket
            ):
                yield item

    def _listAll(self, folderName, delimiter=None, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        delimiter = delimiter or self.delimiter
        prefix = (
            folderName if folderName.endswith(delimiter) else folderName + delimiter
        )
        return (
            obj
            for obj in self.autoRefreshToken(oss2.ObjectIterator)(
                delimiter=delimiter, prefix=prefix, bucket=bucket
            )
        )

    def listAll(self, folderName, delimiter=None, bucketOrBucketName=None):
        return (
            obj.key
            for obj in self._listAll(
                folderName, delimiter=delimiter, bucketOrBucketName=bucketOrBucketName
            )
        )

    def listFolders(self, folderName, delimiter=None, bucketOrBucketName=None):
        return (
            obj.key
            for obj in self._listAll(
                folderName, delimiter=delimiter, bucketOrBucketName=bucketOrBucketName
            )
            if obj.is_prefix()
        )

    def listFiles(self, folderName, delimiter=None, bucketOrBucketName=None):
        return (
            obj.key
            for obj in self._listAll(
                folderName, delimiter=delimiter, bucketOrBucketName=bucketOrBucketName
            )
            if not obj.is_prefix()
        )

    def isFolder(self, folderName, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        return next(self.listAll(folderName, bucketOrBucketName=bucket), None)

    def isFile(self, objectName, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        return bucket.object_exists(objectName)

    def getStorageMd5(self, objectName, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        try:
            return bucket.head_object(objectName).headers.get(self.CONTENT_MD5)
        except oss2.exceptions.NotFound:
            return None

    def getStorageSize(self, objectName, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        return bucket.head_object(objectName).content_length

    def storageUrl(self, path, bucketOrBucketName=None):
        bucket = self.getBucket(bucketOrBucketName)
        return "oss:///" + self.storagePathJoin(bucket.bucket_name, path)

    def getBucket(self, bucketOrBucketName):
        return self.autoRefreshBucket(
            bucketOrBucketName
            if isinstance(bucketOrBucketName, oss2.Bucket)
            else self.getBucketByName(bucketOrBucketName)
        )

    def getBucketByName(self, bucketName=None):
        return (
            oss2.Bucket(self.auth, self.endpoint, bucketName)
            if bucketName
            else self.bucket
        )

    def _getObjectNames(self, objects):
        return (
            [obj.key for obj in objects]
            if isinstance(objects, (tuple, list))
            else objects.key
        )
