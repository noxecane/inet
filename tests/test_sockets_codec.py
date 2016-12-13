from inet.sockets import codec


def test_encode_byte():
    val = codec.encode(dict(name='Arewa'))
    assert isinstance(val, bytes)


def test_decode_dict():
    data = codec.encode(dict(name='Arewa'))
    val = codec.decode(data)
    assert isinstance(val, dict)

