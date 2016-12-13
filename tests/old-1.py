import gevent
import zmq.green as zmq
from inet.client import backend
from inet.messaging.types import Request
from inet import sockets
from tests import Sockets

server = 'tcp://*:9999'
client = 'tcp://localhost:9999'


class ClientBackend(Sockets):

    def test_send(self):
        cl = self.create(zmq.REQ)
        sv = self.create(zmq.REP)

        sockets.connect(client, cl)
        gevent.spawn(self.server, server, sv)

        req = Request('1', 'admin.users', {'a': 5})
        backend.send(cl, req)
        assert sockets.recv(cl) == req
        sockets.disconnect(client, cl)



def test_recv():
    pass


def test_confirm_status():
    pass
