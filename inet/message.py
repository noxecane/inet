import json


class _Message(object):

    def __init__(self, meta, data):
        self._data = data or {}
        self._meta = meta or {}

    def raw(self):
        message = json.dumps(self.asdict())
        return message.encode('utf-8')

    def asdict(self):
        return dict(meta=self._meta, data=self._data)

    def data(self, key=None, val=None):
        if key is None and val is None:
            return self._data
        elif isinstance(key, dict) and val is None:
            self._data = key
        elif val is None:
            return self._data[key]
        elif key is not None and val is not None:
            self._data[key] = val
        else:
            raise ValueError('What are you doing')

    def meta(self, key=None, val=None):
        if key is None and val is None:
            return self._meta
        elif isinstance(key, dict) and val is None:
            self._meta = key
        elif val is None:
            return self._meta[key]
        elif key is not None and val is not None:
            self._meta[key] = val
        else:
            raise ValueError('What are you doing')


def from_raw(raw):
    raw = raw.decode('utf-8')
    return _Message(**json.loads(raw))


def message(meta=None, data=None):
    return _Message(meta, data)
