import logging
import socket
from pyfunk import combinators as cm
from pyfunk.monads.maybe import Maybe

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


__broadcaster = cm.compose(broadcast, reuse, create)


def broadcaster():
    '''
    Creates a UDP socket capable of broadcasting messages on an
    already bound address.
    @sig broadcaster :: _ -> UDPSocket
    '''
    return __broadcaster()

__receiver = cm.compose(reuse, create)


def receiver():
    '''
    Creates a UDP socket capable of receiving messages on an
    already bound address.
    @sig receiver :: _ -> UDPSocket
    '''
    return __receiver()


@cm.curry
def recv(poller, sock):
    '''
    A recv with the ability to timeout. It uses UDP_TIMEOUT
    for its waiting period and UDP_SIZE for its buffer size
    @sig recv :: Poller -> Socket -> Maybe ((Str, Int) Byte)
    '''
    events = dict(poller.poll(UDP_TIMEOUT))
    if sock.fileno() in events:
        msg, address = sock.recvfrom(UDP_SIZE)
        logger.debug('Received request from %s:%d', *address)
        return Maybe.of((address, msg))
    return Maybe.of(None)


@cm.curry
def send(address, sock, data):
    '''
    Sends a encoded data over the given address.
    @sig send :: (Str, Int) -> Socket -> Byte
    '''
    logger.debug('Sending to %s:%d', *address)
    sock.sendto(data, 0, address)
