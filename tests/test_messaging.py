import pytest
from inet.messaging import InvalidType, from_type
from inet.messaging.request import Request, to_request


def test_from_type():
    req = from_type(Request(origin='1', path='admin.encode', data={'a': 12}))
    assert 'origin' in req
    assert req['data'] == {'a': 12}


def test_raise_invalid_type():
    with pytest.raises(InvalidType):
        to_request({})
