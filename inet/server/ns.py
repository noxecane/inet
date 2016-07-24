from inet.sockets import udp
from inet.client.ns import NS_PORT
from inet.messaging.codec import encode
from inet.messaging.types import from_type
from inet.utils import breakable_loop, once
from pyfunk.combinators import compose


__create_broadcaster = compose(udp.reuse, udp.broadcast, udp.create)
__encode_contact = compose(encode, from_type)


@once
def start_broadcaster(address, contact):
    # create udp socket
    # fork process
    udp.send(address, __create_broadcaster())
    # start loop in process
