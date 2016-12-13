from collections import namedtuple
from inet import messaging as msg, sockets
from pyfunk import combinators as cm
from inet.error import exceptions
from inet.sockets import codec


Response = namedtuple('Response', ['origin', 'source', 'status', 'data'])
__encode = cm.compose(codec.encode, msg.from_type)


@msg.invalid_type
def to_response(msg):
    '''
    Converts a dict to a response tuple
    @sig to_response :: Dict -> Response
    '''
    return Response(**msg)


@cm.curry
def send(sock, response):
    '''
    Encodes the given response and sends it over the wire
    @sig send :: Socket -> Request -> Bytes
    '''
    return sockets.send(sock, __encode(response))

__recv = cm.compose(to_response, codec.decode, sockets.recv)


def recv(sock):
    '''
    Removes response data from the response envelope and decodes
    it in the process.
    @sig recv :: Socket -> Response
    '''
    response = recv(sock)
    confirm_status(response.status, response.data)
    return response


@cm.curry
def confirm_status(response):
    '''
    Propagates exceptions from based on the given status
    @sig confirm_status :: Response -> Bool
    '''
    if response.status == 'error':
        exc = exceptions.create(response.data['name'])
        raise exc(response.data['message'])
    return True
