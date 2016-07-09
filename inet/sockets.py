import json
import logging
import zmq.green as zmq
from pyfunk.collections import freduce
from pyfunk.combinators import curry
from pyfunk.functors.io import IO
from pyfunk.functors.task import Task

logger = logging.getLogger('inet.socket')
TIMEOUT = 3000


@curry
def create(context, socktype):
    '''
    Create a new socket
    @sig create :: Context -> Int -> Socket
    '''
    return context.socket(socktype)


def destroy(socket):
    '''
    Shutdown a socket. All messages that are in its queue will be
    cleared so use carefully.
    @sig destroy :: Socket -> IO Socket
    '''
    def close_sock():
        socket.close(0)
        return socket
    return IO(close_sock)


@curry
def connect(address, socket):
    '''
    Connect a socket to a particular address
    @sig connect :: Str -> Socket -> IO Socket
    '''
    def io_connect():
        socket.connect(address)
        return socket
    return IO(io_connect)


@curry
def disconnect(address, socket):
    '''
    Disconnect a socket from a particular address
    @sig disconnect :: Str -> Socket -> IO Socket
    '''
    def io_disconnect():
        socket.disconnect(address)
        return socket
    return IO(io_disconnect)


@curry
def bind(address, socket):
    '''
    Bind a socket to a particular port or address
    @sig bind :: Str -> Socket -> IO Socket
    '''
    def io_bind():
        socket.bind(address)
        return socket
    return IO(io_bind)


@curry
def unbind(address, socket):
    '''
    Unbind a socket from a particular port or address
    @sig unbind :: Str -> Socket -> IO Socket
    '''
    def io_unbind():
        socket.unbind(address)
        return socket
    return IO(io_unbind)


@curry
def pollable(poller, socket):
    '''
    Registers the socket to the given poller. This should
    be used when creating a reliable socket.
    @sig pollable :: Poller -> Socket -> IO Socket
    '''
    def io_pollable():
        poller.register(socket, zmq.POLLIN)
        return socket
    return IO(io_pollable)


@curry
def unpollable(poller, socket):
    '''
    Registers the socket to the given poller. This should
    be used when cleaning up a socket that was made pollable
    @sig unpollable :: Poller -> Socket -> IO Socket
    '''
    def io_unpollable():
        poller.unregister(socket)
        return socket
    return IO(io_unpollable)


@curry
def send(poller, socket, data):
    '''
    Performs the two way connection between client and a server
    socket.The given socket must be pollable and connected for this
    function to work. The return error string must be formatted with
    a key value `address`.
    @sig send :: Poller -> Socket -> Dict -> Task Str Dict
    '''
    def task_send(reject, resolve):
        socket.send(bytes(json.dumps(data), 'utf8'))
        events = dict(poller.poll(TIMEOUT))
        if events.get(socket) == zmq.POLLIN:
            resolve(json.loads(socket.recv().decode('utf8')))
        else:
            reject('Connection to server at {address} refused')
    return Task(task_send)


@curry
def reliable_send(poller, sockets, data):
    '''
    Works the same way as send except that it can send using another
    socket when one fails.
    @sig reliable_send :: Poller -> [Socket] ->  Dict -> Task Str Dict
    '''
    inner_send = send(poller)
    return freduce(lambda lt, sk: lt.or_else(lambda _: inner_send(sk, data)),
                   inner_send(sockets[0], data), sockets[1:])
