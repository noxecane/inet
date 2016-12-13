import gevent
import pytest
import zmq.green as zmq
from inet.client import ns
from inet.error import MethodNotFound
from inet.messaging import codec
from inet.messaging.types import Contact
from inet.sockets import udp


def test_receive_pair():
    pair = ns.receiver_pair('')
    assert len(pair) == 2
    poller, sock = pair
    assert isinstance(poller, zmq.Poller)
    assert sock.recvfrom


def test_get_contact():
    address = ns.get_contact({'admin.users': 'tcp://localhost:8009'}, 'admin.users')
    assert address == 'tcp://localhost:8009'


def test_get_contact_fail():
    with pytest.raises(MethodNotFound):
        ns.get_contact({}, 'admin.users')


def test_add_contact():
    contacts = {}
    ns.add_contact(contacts, Contact('tcp://localhost:9009', ['admin.users', 'admin.tokens']))
    assert len(contacts) == 2
    assert contacts['admin.tokens'] == 'tcp://localhost:9009'


def serve_contact(contact):
    server_address = ('127.0.0.1', ns.NS_PORT)
    server = udp.broadcaster()
    udp.send(server_address, server, codec.encode(contact))


def test_recv():
    poller, sock = ns.receiver_pair('')
    contact = dict(address='tcp://localhost:8009', services=['admin.tokens', 'admin.users'])
    gevent.spawn(serve_contact, contact)

    mcontact = ns.recv(poller, sock)
    assert isinstance(mcontact._value, Contact)
    assert mcontact._value.address == contact['address']
