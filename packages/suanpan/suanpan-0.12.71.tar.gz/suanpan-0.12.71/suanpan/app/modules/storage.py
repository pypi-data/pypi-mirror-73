# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan import path as upath
from suanpan.app import app
from suanpan.app.modules.base import Module
from suanpan.storage import storage

module = Module()


@module.stream("storage.create")
def createStorage(context):
    args = context.args
    stream = context.stream
    file = os.path.basename(args.key)
    debugfile = app.sio.static("debug", file)
    filepath = args.path or storage.getPathInTempStore(args.key)
    stream.pipe(debugfile)
    if stream.done:
        upath.copy(debugfile, filepath)
        storage.upload(args.key, filepath)


@module.on("storage.remove")
def removeStrorage(context):
    args = context.args
    file = os.path.basename(args.key)
    debugfile = app.sio.static("debug", file)
    upath.remove(debugfile)
    storage.remove(args.key)
    if args.path:
        upath.remove(args.path)


@module.on("storage.list")
def listStorages(context):
    args = context.args
    files = upath.listFiles(args.path) if args.path else storage.listFiles(args.key)
    _meta = _pathmeta if args.path else _keymeta
    return [_meta(file) for file in files]


@module.on("storage.meta.get")
def getStorageMeta(context):
    args = context.args
    return meta(key=args.key, path=args.path)


@module.fn
def notifyStorageMeta(key=None, path=None):
    app.sio.emit("storage.meta.notify", meta(key=key, path=path))


@module.fn
def meta(key=None, path=None):
    return _pathmeta(path) if path else _keymeta(key)


def _keymeta(key):
    return {"src": f"debug/{os.path.basename(key)}", "key": key}


def _pathmeta(path):
    return {"src": f"debug/{os.path.basename(path)}", "path": path}
