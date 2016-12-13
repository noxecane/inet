import gevent
import zmq.green as zmq

from inet import sockets
from inet.sockets import ConnectionTimeout
from tests import Sockets

server = 'tcp://*:9999'
client = 'tcp://localhost:9999'


class TestSockets(Sockets):

    def test_send(self):
        cl = self.create(zmq.REQ)
        sv = self.create(zmq.REP)

        sockets.connect(client, cl)
        gevent.spawn(self.server, server, sv, 6)

        req = b'Hello World'
        sockets.send(cl, req)
        assert sockets.recv(cl) == req
        sockets.disconnect(client, cl)

    def test_send_timeout(self):
        cl = self.create(zmq.REQ)
        sockets.connect(client, cl)

        req = b'Hello World'

        with self.assertRaises(ConnectionTimeout):
            sockets.send(cl, req)
            sockets.recv(cl)

    def test_multi_send(self):
        cl = self.create(zmq.REQ)
        sv = self.create(zmq.REP)

        cl = sockets.nolinger(cl)
        gevent.spawn(self.server, server, sv, 2000)

        for i in range(2000):
            req = bytes('Hello %s' % i, 'utf8')
            sockets.connect(client, cl)
            sockets.send(cl, req)
            assert sockets.recv(cl) == req
            sockets.disconnect(client, cl)
