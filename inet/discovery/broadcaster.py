import logging

from inet.discovery import NS_PORT
from inet.messaging import from_type
from inet.sockets import udp, codec
from pyfunk.combinators import compose, curry

logger = logging.getLogger('inet.discovery.broadcaster')

__encode_contact = compose(codec.encode, from_type)


@curry
def broadcast_fn(host, sock):
    '''
    Creates a function for  distributing contact information
    using UDP broadcasts.
    @sig broadcast_fn :: String -> UDPSocket -> (Contact -> _)
    '''
    broadcast = udp.send((host, NS_PORT), sock)
    return compose(broadcast, __encode_contact)
