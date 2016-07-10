import socket
import zmq.green as zmq

from pyfunk.combinators import curry
from pyfunk.functors.io import IO
from pyfunk.functors.task import Task

__poller = zmq.Poller()


def create():
    '''
    Creates a UDP socket
    @sig socket :: _ -> UDPSocket
    '''
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


def shared(s):
    '''
    Enables this socket bind to an address already bound to another
    socket. This should be used before binding.
    @sig shared :: UDPSocket -> IO UDPSocket
    '''
    def share_socket():
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s
    return IO(share_socket)


def broadcast(s):
    '''
    Ask the OS for permission to broadcast. This should be used as soon
    as one creates a socket
    @sig broadcast :: UDPSocket -> IO UDPSocket
    '''
    def broadcast_socket():
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        return s
    return IO(broadcast_socket)


@curry
def bind(url, port, s):
    '''
    Binds a socket to a specific address(url, port combination).
    @sig bind :: Str -> Int -> UDPSocket -> IO UDPSocket
    '''
    def share_socket():
        s.bind((url, port))
        return s
    return IO(share_socket)


def pollable(s):
    '''
    Gives the library the ability to listen for activity on the socket.
    Must be called to use wait
    @sig pollable :: UDPSocket -> IO UDPSocket
    '''
    def poll_socket():
        __poller.register(s, zmq.POLLIN)
        return s
    return IO(poll_socket)


@curry
def wait(size, interval, s):
    '''
    Listens for activity on the UDP socket then returns the message
    and the source of such activity.
    @sig wait :: Int -> Int -> UDPSocket -> Task Str (Str, (Str, Int))
    '''
    def listen(reject, resolve):
        events = dict(__poller.poll(interval * 1000))
        if s.fileno() in events:
            resolve(s.recvfrom(size))
        else:
            reject('No activity noticed')
    return Task(listen)
