import gevent
from inet.sockets import udp
from inet.client.ns import NS_PORT
from inet.messaging.codec import encode
from inet.messaging.types import from_type
from inet.utils import breakable_loop, once
from pyfunk.combinators import compose


__create_broadcaster = compose(udp.reuse, udp.broadcast, udp.create)
__encode_contact = compose(encode, from_type)


@once
def start_broadcaster(host, contact):
    broadcast = breakable_loop(udp.send((host, NS_PORT), __create_broadcaster()))
    return gevent.spawn(broadcast, __encode_contact(contact))
