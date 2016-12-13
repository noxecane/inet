import gevent

from tests import Sockets
from inet.sockets import udp, pollable, bind
from pyfunk.combinators import compose
from pyfunk.misc import trace


class UDPTestCase(Sockets):

    def test_send(self):
        create_server = compose(trace('Creating sender'), udp.reuse, udp.broadcast, udp.create)
        data = b'Hello world'

        g = gevent.spawn(self.receiver, ('', 8009), udp.create(), self.assertTrue)
        gevent.spawn(udp.send, ('localhost', 8009), create_server(), data)
        g.join()

    def test_recv(self):
        create_server = compose(udp.reuse, udp.broadcast, udp.create)
        create_client = compose(bind(('', 8009)), udp.reuse, udp.create)
        data = b'Hello world'

        sock = create_client()
        poller = pollable(sock)

        gevent.spawn(udp.send, ('localhost', 8009), create_server(), data)
        assert udp.recv(poller, sock)._value[1] == data
