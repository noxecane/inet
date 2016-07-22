from collections import namedtuple
from functools import wraps
from inet.errors import InvalidType

Contact = namedtuple('Contact', ['address', 'services'])
Request = namedtuple('Request', ['origin',  'data'])
Response = namedtuple('Response', ['origin', 'source', 'status', 'data'])


def __raise_invalid_type(fn):
    @wraps(fn)
    def decorated(msg):
        try:
            fn(msg)
        except KeyError:
            raise InvalidType('The type passed in is invalid')
    return decorated


@__raise_invalid_type
def to_request(msg):
    '''
    Converts a dict to a request tuple
    @sig to_request :: Dict -> Request
    '''
    return Request(origin=msg['origin'], data=msg['data'])


@__raise_invalid_type
def to_response(msg):
    '''
    Converts a dict to a response tuple
    @sig to_response :: Dict -> Response
    '''
    return Response(origin=msg['origin'], source=msg['source'],
                    status=msg['status'], data=msg['data'])


@__raise_invalid_type
def to_contact(msg):
    '''
    Converts a dict to a contact tuple
    @sig to_contact :: Dict -> Contact
    '''
    return Contact(address=msg['address'], services=msg['services'])


def from_type(mtype):
    return mtype._as_dict()
