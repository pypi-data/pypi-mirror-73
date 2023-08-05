# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan import path as upath
from suanpan.app import app
from suanpan.app.modules.base import Module
from suanpan.storage import storage

module = Module()


@module.stream("storage.create")
def createStorage(context):
    args = context.args
    stream = context.stream
    filepath = storage.getPathInTempStore(args.key)
    debugfile = app.sio.static("debug", args.key)
    stream.pipe(filepath)
    if stream.done:
        upath.symlink(filepath, debugfile)
        storage.upload(args.key, filepath)


@module.on("storage.remove")
def removeStrorage(context):
    args = context.args
    filepath = storage.getPathInTempStore(args.key)
    debugfile = app.sio.static("debug", args.key)
    storage.remove(args.key)
    upath.remove(filepath)
    upath.remove(debugfile)


@module.on("storage.list")
def listStorage(context):
    args = context.args
    return [meta(key) for key in storage.listFiles(args.key)]


@module.on("storage.meta.get")
def getStorageMeta(context):
    args = context.args
    return meta(args.key)


@module.fn
def notifyStorageMeta(key):
    app.sio.emit("storage.meta.notify", meta(key))


@module.fn
def meta(key):
    return {"src": f"debug/{key}", "key": key}
