import gevent
import pytest
from inet.client import ns
from inet.errors import MethodNotFound
from inet.messaging.codec import encode
from inet.messaging.types import from_type, Contact
from inet.sockets import udp
from pyfunk.combinators import compose


create_server = compose(udp.reuse, udp.broadcast, udp.create)


def server(sock, contact, wait=1):
    udp.send(('localhost', ns.NS_PORT), sock, encode(from_type(contact)))


def test_startup_process():
    get_address = ns.start_receiver('')
    address = 'tcp://localhost:9980'
    services = [
        'admin.tokens.decode',
        'admin.users.get'
    ]
    
    gevent.spawn(server, create_server(), Contact(address=address, services=services))
    gevent.sleep(3)
    assert get_address('admin.tokens.decode') == address
    assert get_address('admin.users.get') == address
    with pytest.raises(MethodNotFound):
        assert get_address('hello.world')
#
