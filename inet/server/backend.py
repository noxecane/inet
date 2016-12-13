import socket
from inet import sockets
from inet.messaging.codec import encode, decode
from inet.messaging.types import from_type, to_request
from pyfunk.combinators import curry, compose


def get_address():
    '''
    Returns the IP of the host. It's correctness is determined by the prescence
    of internet access.
    @sig get_address :: _ -> Str
    '''
    try:
        ip, _ = __precise_address()
        return ip
    except socket.gaierror:
        return __lucky_address()


def __precise_address():
    sock = socket.socket()
    sock.connect(('www.google.com', 80))
    return sock.getsockname()


def __lucky_address():
    return socket.gethostbyname(socket.gethostname())
