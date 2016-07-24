from inet import sockets
from inet.messaging.codec import encode, decode
from inet.messaging.types import Response, from_type, to_request
from pyfunk.combinators import curry, compose


def __as_response(uuid, req, status, data):
    return Response(origin=uuid, source=req.origin, status=status, data=data)

__create_respone = compose(encode, from_type, __as_response)
__xrecv = compose(to_request, decode, sockets.recv)


@curry
def send(uuid, sock, req, status, data):
    '''
    Envelopes and encodes the data as a response before sending
    it using zeromq
    @sig send :: Str -> Socket -> Request -> Status -> Dict -> Byte
    '''
    return sockets.send(sock, __create_respone(uuid, req, status, data))


def recv(sock):
    '''
    Removes request data from the request envelope and decodes
    it in the process.
    @sig recv :: Socket -> Dict
    '''
    return __xrecv(sock).data
