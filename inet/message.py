import json


class _Message(object):

    def __init__(self, meta=None, data=None):
        self.data = data or {}
        self.meta = meta or {}

    @property
    def raw(self):
        message = json.dumps(self.asdict())
        return message.encode('utf-8')

    def asdict(self):
        return dict(meta=self.meta, data=self.data)


def from_raw(raw):
    raw = raw.decode('utf-8')
    return _Message(**json.loads(raw))


def message(meta=None, data=None):
    return _Message(meta, data)
