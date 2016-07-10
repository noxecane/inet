import gevent
import zmq.green as zmq

from inet import sockets
from tests import InetTestCase

server = 'tcp://*:9999'
client = 'tcp://localhost:9999'
pair = zmq.REQ
pair2 = zmq.REP


def assertFn(f):
    def fn(res):
        assert f(res)
    return fn


def assertError(address):
    def fn(err):
        print('Error:', err.format(address=address))
        assert False
    return fn


class TestSockets(InetTestCase):

    def test_create(self):
        sock = self.socket(pair)
        assert not sock.closed

    def test_destroy(self):
        sock = self.socket(pair)
        sockets.destroy(sock).unsafeIO()
        assert sock.closed

    def test_connect(self):
        '''Needs a server'''
        sock = self.socket(pair)
        sockets.connect(client, sock).unsafeIO()

    def test_disconnect(self):
        sock = self.socket(pair)
        sockets.connect(client, sock).chain(sockets.disconnect(client)).unsafeIO()

    def test_bind(self):
        sock = self.socket(pair)
        sockets.bind(server, sock).unsafeIO()

    # def test_unbind(self):
    #     sock = self.socket(sockets.TSERVER)
    #     sockets.bind(server, sock).chain(sockets.unbind(server)).unsafeIO()

    def test_pollable(self):
        s1 = self.socket(pair)
        s2 = self.socket(pair2)
        sockets.pollable(self.poller, s1).unsafeIO()
        sockets.pollable(self.poller, s2).unsafeIO()

    def test_unpollable(self):
        sock = self.socket(pair)
        sockets.pollable(self.poller, sock).chain(sockets.unpollable(self.poller)).unsafeIO()

    def test_send(self):
        s1 = self.socket(pair)
        s2 = self.socket(pair2)
        sockets.connect(client, s1).chain(sockets.pollable(self.poller)).unsafeIO()
        gevent.spawn(self.server, server, s2)
        req = dict(id=12)
        resp = sockets.send(self.poller, s1, req)
        resp.fork(assertError(client), assertFn(lambda res: res == req))

    def test_reliable_send(self):
        for i in range(3):
            s1 = self.socket(pair)
            sockets.connect(client, s1).chain(sockets.pollable(self.poller)).unsafeIO()
        req = dict(id=12)
        resp = sockets.reliable_send(self.poller, self.sockets, req)
        resp.fork(assertFn(lambda res: True), assertFn(lambda res: res == req))

    def test_multi_send(self):
        s1 = self.socket(pair)
        s2 = self.socket(pair2)
        sockets.connect(client, s1).chain(sockets.pollable(self.poller)).unsafeIO()
        gevent.spawn(self.server, server, s2, 2000)
        for i in range(2000):
            req = dict(id=i)
            resp = sockets.send(self.poller, s1, req)
            print(i)
            resp.fork(assertError(client), assertFn(lambda res: res == req))
