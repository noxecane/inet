import gevent
import logging
from inet import sockets
from inet.errors import MethodNotFound
from inet.messaging.codec import decode
from inet.messaging.types import to_contact
from inet.sockets import udp
from inet.utils import breakable_loop, once
from pyfunk.combinators import curry, compose
from pyfunk.monads import fmap

logger = logging.getLogger('inet.client.ns')
NS_PORT = 9999


def __listen(host, sock):
    return sockets.bind((host, NS_PORT), sock)


@curry
def __recvFn(poller, sock):
    return lambda: udp.recv(poller, sock)


def __setup_receiver(host):
    return __listen(host, __create_receiver())


def __remove_address(response):
    _, contact = response
    return contact


@curry
def __get_address(servicebook, path):
    try:
        return servicebook[path]
    except KeyError:
        raise MethodNotFound('The given path "%s" was not found' % path)


@curry
def __update_book(servicebook, contact):
    # use the service paths as keys
    logger.debug('Adding services for %s', contact.address)
    for s in contact.services:
        servicebook[s] = contact.address

__create_receiver = compose(udp.reuse, udp.create)
__get_response = compose(to_contact, decode, __remove_address)


@once
def start_receiver(host):
    '''
    Setups up a gevent greenlet to listen for server broadcasts so as
    to update the nameservice address map. It returns a function for
    accessing such map. This function will riase a MethodNotFound
    exception if the service is not in its address book.
    @sig start_receiver :: Str -> (Str -> Str)
    '''
    servicebook = {}
    receiver = __setup_receiver(host)
    poller = sockets.pollable(receiver)

    contact_reload = compose(fmap(__update_book(servicebook)), fmap(__get_response),
                             __recvFn(poller, receiver))
    gevent.spawn(breakable_loop(contact_reload))

    # return getter function
    return __get_address(servicebook)
