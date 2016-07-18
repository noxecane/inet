import logging
import zmq.green as zmq
from inet.errors import ConnectionTimeout
from inet.sockets.message import encode, decode
from pyfunk.combinators import curry

logger = logging.getLogger('inet.sockets')
REQ_TIMEOUT = 3000


@curry
def create(context, stype):
    '''
    Creates a socket of the given type
    @sig create :: ZMQContext -> Int -> Socket
    '''
    return context.socket(stype)


def destroy(sock):
    '''
    Clears the socket queue then closes the socket. Use this when the socket
    is no longer needed at all.
    @sig destroy :: Socket -> Socket
    '''
    sock.setsockopt(zmq.LINGER, 0)
    sock.close()
    return sock


@curry
def connect(address, sock):
    '''
    Composable version of ZMQ's connect
    @sig connect :: Address -> Socket -> Socket
    '''
    sock.connect(address)
    add_str = address if isinstance(address, str) else '%s:%d' % address
    logger.debug('Connected succsessfully from %s', add_str)
    return sock


@curry
def diconnect(address, sock):
    '''
    Composable version of ZMQ's disconnect
    @sig disconnect :: Address -> Socket -> Socket
    '''
    sock.disconnect(address)
    add_str = address if isinstance(address, str) else '%s:%d' % address
    logger.debug('Disconnected succsessfully from %s', add_str)
    return sock


@curry
def bind(address, sock):
    '''
    Composable version of ZMQ's bind
    @sig bind :: Address -> Socket -> Socket
    '''
    sock.bind(address)
    add_str = address if isinstance(address, str) else '%s:%d' % address
    logger.debug('Now listening on %s', add_str)
    return sock


@curry
def unbind(address, sock):
    '''
    Composable version of ZMQ's unbind
    @sig unbind :: Address -> Socket -> Socket
    '''
    sock.unbind(address)
    add_str = address if isinstance(address, str) else '%s:%d' % address
    logger.debug('Stopped listening on %s', add_str)
    return sock


def pollable(sock):
    '''
    Creates and registers a ZMQ poller for this socket.
    @sig pollable :: Socket -> Poller
    '''
    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)
    return poller


@curry
def unpollable(poller, sock):
    '''
    Composable version of ZMQ Poller's unregister
    @sig connect :: Poller -> Socket -> Socket
    '''
    poller.unregister(sock)
    return sock


@curry
def send(sock, msg):
    '''
    Encodes and sends a message. It's basically a proxy to zeromq_send
    with encoding on-top
    @sig send :: Socket -> Dict -> Socket
    '''
    logger.debug('Sending message out to connected peer')
    sock.send(encode(msg))


@curry
def recv(sock, address):
    '''
    Extends the zmq_recv function by polling within a specified
    timeout.
    @sig recv :: Str -> Socket -> Dict
    '''
    if sock.poll(REQ_TIMEOUT) == 1:
        logger.debug('Received response from peer at %s', address)
        return decode(sock.recv())
    raise ConnectionTimeout('Connection to server at %s as timedout' % address)
