import pytest
from inet.errors import InvalidType
from inet.messaging import types


def test_from_type():
    req = types.from_type(types.Request(origin='1', data={'a': 12}))
    assert 'origin' in req
    assert req['data'] == {'a': 12}


def test_raise_invalid_type():
    with pytest.raises(InvalidType):
        types.to_contact({})


def test_to_request():
    req = types.to_request(dict(origin=1, data={'a': 12}))
    assert isinstance(req, types.Request)


def test_to_response():
    req = types.to_response(dict(origin=1, source=2, status='error', data={'a': 12}))
    assert isinstance(req, types.Response)


def test_to_contace():
    req = types.to_contact(dict(address='localhost', services=['admin.keys.encode']))
    assert isinstance(req, types.Contact)
