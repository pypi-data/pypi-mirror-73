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
    stream.pipe(filepath)
    if stream.done:
        symlink(args.key)


@module.on("storage.remove")
def removeStrorage(context):
    args = context.args
    filepath = storage.getPathInTempStore(args.key)
    debugpath = app.sio.static("debug", args.key)
    storage.remove(args.key)
    upath.remove(filepath)
    upath.remove(debugpath)


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


@module.fn
def dowload(key):
    filepath = storage.getPathInTempStore(key)
    storage.dowload(key, filepath)
    symlink(key)
    return filepath


@module.fn
def remove(key):
    filepath = storage.getPathInTempStore(key)
    debugpath = app.sio.static("debug", key)
    storage.remove(key)
    upath.remove(filepath)
    upath.remove(debugpath)
    return key


@module.fn
def symlink(key):
    filepath = storage.getPathInTempStore(key)
    debugpath = app.sio.static("debug", key)
    return upath.symlink(filepath, debugpath)
