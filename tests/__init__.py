from inet import sockets
from inet.sockets import udp
from unittest import TestCase
import zmq.green as zmq

SERVER = 'tcp://localhost:9999'
TIMEOUT = 1000


class Sockets(TestCase):

    def setUp(self):
        self.context = zmq.Context.instance()
        self.poller = zmq.Poller()
        self.sockets = []

    def tearDown(self):
        while self.sockets:
            s = self.sockets.pop()
            if not s.closed:
                sockets.close(s)

    def assertFn(self, fn):
        def function(*args, **kwargs):
            assert not fn(*args, **kwargs)
        return function

    def assertTrue(x):
        assert True

    def create(self, sockettype):
        s = sockets.create_brutal(self.context, sockettype)
        self.sockets.append(s)
        return s

    def server(self, addr, sock, req=1):
        sockets.bind(addr, sock)
        while req != 0:
            sock.send(sock.recv())
            req -= 1

    def receiver(self, addr, sock, asserter, req=1):
        sockets.bind(addr, sock)
        mresult = udp.recv(sockets.pollable(sock), sock)
        if mresult.nothing():
            assert False
        else:
            asserter(mresult._value)
