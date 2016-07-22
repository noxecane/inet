from inet import sockets
from inet.errors import exception
from inet.messaging.codec import encode, decode
from inet.messaging.types import Request, from_type, to_response
from pyfunk.combinators import curry, compose


def __as_request(uuid, data):
    return Request(origin=uuid, data=data)

__create_request = curry(compose(encode, from_type, __as_request))
__xrecv = compose(to_response, decode, sockets.recv)


@curry
def send(uuid, sock, data):
    '''
    Envelopes and encodes the data as a request before sending
    it using zeromq
    @sig send :: Str -> Socket -> Dict -> Byte
    '''
    return sockets.send(sock, __create_request(uuid, data))


def recv(sock):
    '''
    Removes response data from the response envelope and decodes
    it in the process. Also raises propagated exceptions from the
    server it's receiving from.
    '''
    response = __xrecv(sock)
    if response.state == 'error':
        exc = exception(response.data['name'])
        raise exc(response.data['message'])
    return response.data
