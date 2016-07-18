import logging
import socket
from inet.sockets.message import encode, decode
from pyfunk.combinators import curry
from pyfunk.monads import Maybe

logger = logging.getLogger('inet.sockets.udp')
UDP_TIMEOUT = 3000
UDP_SIZE = 8192


def create():
    '''
    Creates a UDP Socket
    @sig create :: _ -> UDPSocket
    '''
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


def broadcast(sock):
    '''
    Ask for permission to do broadcasts
    @sig broadcast :: Socket -> Socket
    '''
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return sock


def reuse(sock):
    '''
    Ask for permission to share the same port with others
    @sig reuse :: Socket -> Socket
    '''
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    return sock


@curry
def recv(poller, sock):
    '''
    A recv with the ability to timeout. It uses UDP_TIMEOUT
    for its waiting period and UDP_SIZE for its buffer size
    @sig recv :: Poller -> Socket -> Maybe ((Str, Int) Dict)
    '''
    events = dict(poller.poll(UDP_TIMEOUT))
    if sock.fileno() in events:
        msg, address = sock.recvfrom(UDP_SIZE)
        logger.debug('Received request from %s:%d', *address)
        return Maybe.of((address, decode(msg)))
    return Maybe.of(None)


@curry
def send(address, sock, data):
    '''
    Sends a encoded data over the given address.
    @sig send :: (Str, Int) -> Socket -> Dict
    '''
    logger.debug('Sending to %s:%d', *address)
    sock.sendto(encode(data), 0, address)
