import socket

from inet import POLL_TIMEOUT
from pyfunk.combinators import curry
from pyfunk.functors.io import IO
from pyfunk.functors.task import Task


def create():
    '''
    Creates a UDP socket
    @sig socket :: _ -> UDPSocket
    '''
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


def same_address(s):
    '''
    Enables this socket bind to an address already bound to another
    socket. This should be used before binding.
    @sig same_address :: UDPSocket -> IO UDPSocket
    '''
    def share_socket():
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s
    return IO(share_socket)


def can_broadcast(s):
    '''
    Ask the OS for permission to broadcast. This should be used as soon
    as one creates a socket
    @sig can_broadcast :: UDPSocket -> IO UDPSocket
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


# def recv(size, poller, s):


@curry
def wait(size, poller, s):
    '''
    Listens for activity on the UDP socket then returns the message
    and the source of such activity.
    @sig wait :: Int -> Poller -> UDPSocket -> Task Str (Str, (Str, Int))
    '''
    def listen(reject, resolve):
        events = dict(poller.poll(POLL_TIMEOUT))
        if s.fileno() in events:
            resolve(s.recvfrom(size))
        else:
            reject('No activity noticed')
    return Task(listen)
