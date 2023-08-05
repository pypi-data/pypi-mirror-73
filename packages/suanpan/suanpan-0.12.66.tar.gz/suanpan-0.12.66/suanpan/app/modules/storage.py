# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan import path
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
        path.copy(debugfile, filepath)
        storage.upload(args.key, filepath)


@module.on("storage.remove")
def removeStrorage(context):
    args = context.args
    file = os.path.basename(args.key)
    debugfile = app.sio.static("debug", file)
    path.remove(debugfile)
    storage.remove(args.key)
    if args.path:
        path.remove(args.path)


@module.on("storage.list")
def listStorages(context):
    args = context.args
    return (
        [_pathmeta(file) for file in path.listFiles(args.path)]
        if args.path
        else [_keymeta(file) for file in storage.listFiles(args.key)]
    )


@module.on("storage.meta.get")
def getStorageMeta(context):
    args = context.args
    return _pathmeta(args.path) if args.path else _keymeta(args.key)


@module.fn
def notifyStorageMeta(key=None, path=None):
    meta = _pathmeta(path) if path else _keymeta(key)
    app.sio.emit("storage.meta.notify", meta)


def _pathmeta(filepath):
    return {"src": f"debug/{os.path.basename(filepath)}", "path": filepath}


def _keymeta(filekey):
    return {"src": f"debug/{os.path.basename(filekey)}", "path": filekey}
