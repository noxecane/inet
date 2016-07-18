import gevent
import logging
from inet.errors import MethodNotFound
from inet import sockets
from inet.sockets import udp
from inet.utils import breakable_loop
from pyfunk.combinators import curry, compose
from pyfunk.monads import fmap

logger = logging.getLogger('inet.client.ns')
NS_PORT = 9999


@curry
def get_address(amap, path):
    '''
    Get the address of a particular path. If the path is not
    offered by any node a MethodNotFound error will be thrown
    @sig get_address :: Str -> Str
    '''
    try:
        return amap[path]
    except KeyError:
        raise MethodNotFound('The given path "%s" was not found' % path)


@curry
def update_amap(amap, broadcast):
    '''
    Updates mapping for service names to addresses with a service
    broadcast
    @sig update_amap :: Dict -> Dict -> _
    '''
    services, address = broadcast['services'], broadcast['address']
    # use the service paths as keys
    logger.debug('Adding services for %s', address)
    for s in services:
        amap[s] = address


def discard_address(response):
    '''
    Removes the address from a UDP response
    @sig discard_address :: Maybe ((Str, Int), Dict) -> Dict
    '''
    _, broadcast = response
    return broadcast


def start_receiver(host):
    '''
    Setups up a gevent greenlet to listen for server broadcasts so as
    to update the nameservice address map. It returns a function for
    accessing such map.
    @sig start_receiver :: Str -> (Str -> Str)
    '''
    amap = {}
    create_receiver = compose(udp.reuse, udp.create)
    setup_socket = compose(sockets.bind((host, NS_PORT)), create_receiver)
    # create socket and make it pollable
    sock = setup_socket()
    poller = sockets.pollable(sock)

    # setup the receiver to update the amap
    recv = compose(fmap(discard_address), lambda: udp.recv(poller, sock))
    areload = compose(fmap(update_amap(amap)), recv)
    gevent.spawn(breakable_loop(areload))

    # return getter function
    return get_address(amap)
