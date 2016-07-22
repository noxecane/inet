import gevent

from tests import InetTestCase
from inet.sockets import udp, pollable, bind
from pyfunk.combinators import compose
from pyfunk.misc import trace


class UDPTestCase(InetTestCase):

    def udp_server(self, address, sock, req=1):
        bind(address, sock)
        poller = pollable(sock)
        while req != 0:
            events = dict(poller.poll(udp.UDP_TIMEOUT))
            if sock.fileno() in events:
                data, _ = sock.recvfrom(udp.UDP_SIZE)
                setattr(self, 'udata', True)
                req -= 1
            else:
                setattr(self, 'udata', False)
                return

    def test_send(self):
        create_server = compose(trace('Creating sender'), udp.reuse, udp.broadcast, udp.create)
        data = b'Hello world'

        g = gevent.spawn(self.udp_server, ('', 8009), udp.create())
        gevent.spawn(udp.send, ('localhost', 8009), create_server(), data)
        g.join()
        assert self.udata

    def test_recv(self):
        create_server = compose(udp.reuse, udp.broadcast, udp.create)
        create_client = compose(bind(('', 8009)), udp.reuse, udp.create)
        data = b'Hello world'

        sock = create_client()
        poller = pollable(sock)

        gevent.spawn(udp.send, ('localhost', 8009), create_server(), data)
        assert udp.recv(poller, sock)._value[1] == data
