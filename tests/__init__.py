from inet.sockets import destroy, create, bind
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
            destroy(s).unsafeIO()

    def socket(self, sockettype):
        s = create(self.context, sockettype)
        self.sockets.append(s)
        return s

    def server(self, addr, socket, req=1):
        bind(addr, socket).unsafeIO()
        while req != 0:
            socket.send(socket.recv())
            req -= 1

    def assertFn(self, f):
        def fn(res):
            assert f(res)
        return fn

    def assertError(self, address):
        def fn(err):
            print('Error:', err.format(address=address))
            assert False
        return fn
