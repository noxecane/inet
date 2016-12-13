from collections import namedtuple
from inet import messaging as msg, sockets
from inet.sockets import codec
from pyfunk import combinators as cm


Request = namedtuple('Request', ['origin', 'path', 'data'])
__encode = cm.compose(codec.encode, msg.from_type)


@msg.invalid_type
def to_request(msg):
    '''
    Converts a dict to a request tuple
    @sig to_request :: Dict -> Request
    '''
    return Request(**msg)


@cm.curry
def send(sock, req):
    '''
    Encodes the request before sending it using zeromq
    @sig send :: Socket -> Request -> Byte
    '''
    return sockets.send(sock, __encode(req))


__recv = cm.compose(to_request, codec.decode, sockets.recv)


def recv(sock):
    '''
    Acts as recv on the Request layer
    @sig recv :: Socket -> Request
    '''
    return __recv(sock)
