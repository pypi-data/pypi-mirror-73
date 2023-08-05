# coding=utf-8
from __future__ import absolute_import, print_function

from suanpan.app.modules.base import Module
from suanpan.storage import storage

module = Module()


@module.stream("storage.create")
def createStorage(context):
    args = context.args
    stream = context.stream
    path = args.path or storage.getPathInTempStore(args.key)
    stream.pipe(path)
    storage.upload(args.key, path)


@module.on("storage.remove")
def removeStrorage(context):
    args = context.args
    storage.remove(args.key)
