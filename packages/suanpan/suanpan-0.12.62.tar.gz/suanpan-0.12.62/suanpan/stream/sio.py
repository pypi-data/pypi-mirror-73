# coding=utf-8
from __future__ import absolute_import, print_function

import datetime
import io
import traceback
import uuid

from suanpan import path, runtime
from suanpan.log import logger
from suanpan.stream import handlers
from suanpan.stream.interfaces import HasHandlers


class Event(object):
    TEMPLATE = "__{keyword}_::{event}::{data}__"

    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._kwargs.setdefault("keyword", "akuma")

    def __call__(self, event, *args, **kwargs):
        kwargs.update(event=event)
        return self.format(*args, **kwargs)

    def format(self, *args, **kwargs):
        return self.TEMPLATE.format(*self._args, *args, **self._kwargs, **kwargs)

    def new(self):
        return self.format(event="new", data="id")

    def resume(self, id=""):
        return self.format(event="resume", data=id)

    def data(self, id):
        return self.format(event="data", data=id)

    def more(self, id):
        return self.format(event="more", data=id)

    def stop(self):
        return self.format(event="stop", data="")


class Stream(object):
    def __init__(self, id):
        self.record = {
            "id": id,
            "event": None,
            "uploadedChunks": 0,
            "paused": False,
            "dirty": False,
            "expire": self._addExipre(new=True),
            "active": True,
        }
        self.buffer = io.BytesIO()

    def _addExipre(self, expire=None, new=False):
        expire = expire or self.now
        if new:
            return expire + datetime.timedelta(minutes=5)
        if (self.now - expire).seconds <= 60:
            return expire + datetime.timedelta(milliseconds=60)
        return expire

    @property
    def now(self):
        return datetime.datetime.now()

    @property
    def uploadedChunks(self):
        return self.record["uploadedChunks"]

    @property
    def dirty(self):
        return self.record["dirty"]

    @property
    def expire(self):
        return self.record["expire"]

    @property
    def expired(self):
        return self.now > self.expire

    def update(self, *args, **kwargs):
        return self.record.update(*args, **kwargs)

    def read(self):
        self.buffer.seek(0)
        data = self.buffer.read()
        self.buffer.truncate(0)
        return data

    def write(self, chunks):
        self.update(
            active=True,
            uploadedChunks=self.uploadedChunks + len(chunks),
            expire=self._addExipre(self.expire),
        )
        return self.buffer.write(chunks)

    def pipe(self, file):
        if isinstance(file, str):
            path.mkdirs(file, parent=True)
            file = open(file, "ab")
        with file:
            file.write(self.read())


class Cleaner(object):
    def __init__(self, delta, handler):
        self.delta = delta
        self.handler = handler
        self.expire = self.now + delta

    @property
    def now(self):
        return datetime.datetime.now()

    @property
    def expired(self):
        return self.now > self.expire

    def clean(self, *args, **kwargs):
        if self.expired:
            self.handler(*args, **kwargs)


class StreamServer(HasHandlers):
    DEFAULT_HANDLER_CLASS = handlers.SIOStreamHandler

    def __init__(self, stream, sio):
        super(StreamServer, self).__init__()
        self.stream = stream
        self.sio = sio
        self.streams = {}
        self.event = Event()
        self.cleaner = Cleaner(datetime.timedelta(seconds=10), self._clean)
        self.init()

    def init(self):
        self.sio.on(self.event.new(), self.onNew)
        self.sio.on(self.event.resume(), self.onResume)

    @property
    def now(self):
        return datetime.datetime.now()

    def _addTime(self, date, new=False):
        if new:
            return date + datetime.timedelta(minutes=5)
        if (self.now - date).seconds <= 60:
            return date + datetime.timedelta(milliseconds=60)
        return date

    def _genid(self):
        id = uuid.uuid4().hex
        while id in self.streams:
            id = uuid.uuid4().hex
        return id

    def _createNew(self, id):
        self._listener(id)
        return id

    def _listener(self, id):
        self.sio.on(self.event.data(id), lambda sid, data: self.onData(sid, id, data))

    def _done(self, id):
        self.streams.pop(id)

    def _clean(self):
        for id, stream in self.streams.items():
            if stream.expired:
                self.streams.pop(id)

    def _handle(self, key, handler):
        def _dec(sid, data, stream):
            title = f"{sid} - sio:{key}"
            _run = runtime.costrun(title)(handler.run)
            try:
                return _run(self.stream, data, sid, stream)
            except Exception:  # pylint: disable=broad-except
                logger.error(traceback.format_exc())

        return _dec

    def getHandler(self, key):
        if not self.hasHandler(key):
            super(StreamServer, self).setHandler(key, self.DEFAULT_HANDLER_CLASS())
        return super(StreamServer, self).getHandler(key)

    def setHandler(self, key, handler):
        return self.getHandler(key).use(handler)

    def clean(self, *args, **kwargs):
        self.cleaner.clean(*args, **kwargs)

    def onNew(self, sid):  # pylint: disable=unused-argument
        return self._createNew(self._genid())

    def onData(self, sid, id, data):
        chunk = data["chunk"]
        info = data["info"]
        event = data["event"]
        self.clean()

        stream = self.streams.get(id)
        if not stream:
            stream = self.streams[id] = Stream(id)
        uploadedChunks = stream.write(chunk)

        if self.hasHandler(event):
            self._handle(event, self.getHandler(event))(sid, info["data"], stream)

        if stream.uploadedChunks < info["size"]:
            self.more(id, uploadedChunks)
        else:
            self._done(id)

    def onStop(self, sid, id):  # pylint: disable=unused-argument
        if id in self.streams:
            self._done(id)

    def onResume(self, sid, id):  # pylint: disable=unused-argument
        stream = self.streams.get(id)
        if stream:
            self.resume(id, stream.uploadedChunks)
        else:
            self._createNew(id)
            self.resume(id)

    def more(self, id, *args, **kwargs):
        self.sio.emit(self.event.more(id), *args, **kwargs)

    def resume(self, id, *args, **kwargs):
        self.sio.emit(self.event.resume(id), *args, **kwargs)
