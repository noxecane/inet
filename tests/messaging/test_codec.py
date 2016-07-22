import json
from inet.messaging.codec import encode, decode


def test_encode_byte():
    val = encode(dict(name='Arewa'))
    assert isinstance(val, bytes)


def test_encode_json():
    data = dict(name='Arewa')
    val = encode(data)
    assert json.loads(val.decode('utf8')) == data


def test_decode():
    data = dict(name='Arewa')
    raw = bytes(json.dumps(data), 'utf8')
    assert decode(raw) == data
