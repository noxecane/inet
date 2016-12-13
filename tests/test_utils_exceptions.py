from inet.utils import exceptions as exc


def test_as_dict():
    assert exc.as_dict(ConnectionError('ConnectionError')) == {'name': 'ConnectionError', 'message': 'ConnectionError'}


def test_create():
    assert issubclass(exc.create('Arewa'), Exception)
