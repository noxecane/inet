import pytest
from inet.errors import InvalidType
from inet.messaging import types


def test_raise_invalid_type():
    with pytest.raises(InvalidType):
        types.to_contact({})
