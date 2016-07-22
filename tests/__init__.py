from inet.sockets import close, create_brutal, bind
from unittest import TestCase
import zmq.green as zmq

SERVER = 'tcp://localhost:9999'
TIMEOUT = 1000


class InetTestCase(TestCase):

    def setUp(self):
        self.context = zmq.Context.instance()
        self.poller = zmq.Poller()
        self.sockets = []

    def tearDown(self):
        while self.sockets:
            s = self.sockets.pop()
            if not s.closed:
                close(s)

    def assertFn(self, fn):
        def function(v):
            assert not fn(v)
        return function

    def create(self, sockettype):
        s = create_brutal(self.context, sockettype)
        self.sockets.append(s)
        return s

    def server(self, addr, socket, req=1):
        bind(addr, socket)
        while req != 0:
            socket.send(socket.recv())
            req -= 1
