import logging

from inet import sockets
from pyfunk import combinators as cm, monads
from inet.discovery import NS_PORT, contact
from inet.sockets import udp, codec

logger = logging.getLogger('inet.discovery.receiver')


def __listen(host, sock):
    return sockets.bind((host, NS_PORT), sock)


def __setup_receiver(host):
    return __listen(host, udp.receiver())


def receiver_pair(host):
    '''
    Creates a receiver bound to the given host and it's poller.
    @sig receiver_pair :: Str -> (ZMQPoller, UDPSocket)
    '''
    sock = __setup_receiver(host)
    return sockets.pollable(sock), sock


def __remove_address(response):
    _, contact = response
    return contact


__response = cm.compose(contact.to_contact, codec.decode, __remove_address)
__recv = cm.compose(monads.fmap(__response), udp.recv)


@cm.curry
def recv(poller, sock):
    '''
    Blocks for a period to receive and decode contact information from
    the servers.
    @sig recv :: ZMQPoller -> UDPSocket -> Maybe Contact
    '''
    return __recv(poller, sock)


@cm.curry
def receive_fn(poller, sock, setter):
    '''
    Creates a function capable of updating a contacs map when called. This function
    blocks but with gevent blocking has been taking care of.
    @sig receive_fn :: ZMQPoller -> UDPSocket -> (Contact -> Bool) -> (_ -> _)
    '''
    return cm.compose(monads.fmap(setter), lambda: recv(poller, sock))
