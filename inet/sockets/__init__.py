import logging
import zmq.green as zmq
from pyfunk.combinators import curry, compose

logger = logging.getLogger('inet.sockets')
REQ_TIMEOUT = 3000


class ConnectionTimeout(ConnectionError):
    pass


@curry
def create(context, stype):
    '''
    Creates a socket of the given type
    @sig create :: ZMQContext -> Int -> Socket
    '''
    return context.socket(stype)


def nolinger(sock):
    '''
    Sets the linger socket option to 0. This way calls to close
    and disconnect work as expected, immediately
    @sig nolinger :: Socket -> Socket
    '''
    sock.setsockopt(zmq.LINGER, 0)
    return sock

__create_brutal = compose(nolinger, create)


def create_brutal(context, stype):
    '''
    Creates a socket that can close/disconnect immediately. Basically
    creates a socket with linger option at 0.
    @sig create_brutal :: ZMQContext -> Int -> Socket
    '''
    return __create_brutal(context, stype)


def close(sock):
    '''
    Calls socket.close
    @sig close :: Socket -> Socket
    '''
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
    logger.debug('Connecting to  %s......', add_str)
    return sock


@curry
def disconnect(address, sock):
    '''
    Composable version of ZMQ's disconnect
    @sig disconnect :: Address -> Socket -> Socket
    '''
    sock.disconnect(address)
    add_str = address if isinstance(address, str) else '%s:%d' % address
    logger.debug('Disconnected from %s....', add_str)
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
    with encoding on-top. It only works with zeromq sockets
    @sig send :: Socket -> Byte -> Byte
    '''
    logger.debug('Sending message out to connected peer')
    sock.send(msg)
    return msg


def recv(sock):
    '''
    Extends the zmq_recv function by polling within a specified
    timeout. Like send it only works with zeromq sockets
    @sig recv :: Socket -> Byte
    '''
    if sock.poll(REQ_TIMEOUT) == 1:
        logger.debug('Received response from peer')
        return sock.recv()
    raise ConnectionTimeout('Connection to server timedout')
