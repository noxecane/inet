import gevent

from tests import InetTestCase
from inet.sockets import udp


def server(sock):
    pass


class UDPTestCase(InetTestCase):

    def test_create(self):
        assert udp.create()

    def test_same_address(self):
        s1 = udp.create()
        udp.same_address(s1).unsafeIO()

    def test_can_broadcast(self):
        s1 = udp.socket()
        udp.can_broadcast(s1).unsafeIO()

    def test_bind(self):
        s1 = udp.socket()
        udp.bind('', 9999, s1).unsafeIO()

    def test_wait(self):
        s1 = udp.socket()

