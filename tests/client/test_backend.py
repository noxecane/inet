import gevent
import json
import uuid
import zmq.green as zmq
from inet.client import backend
from inet.sockets import connect, bind
from inet.messaging import types, codec
from tests import InetTestCase

client = 'tcp://localhost:9999'
server = 'tcp://*:9999'


class ClientBackendTestCase(InetTestCase):

    def server(self, addr, sock, status='success'):
        bind(addr, sock)
        uid = uuid.uuid4()
        req = types.to_request(codec.decode(sock.recv()))
        resp = types.Response(origin=req.origin, source=uid.hex,
                              status=status, data=req.data)
        sock.send(codec.encode(types.from_type(resp)))

    def test_send_bytes(self):
        cl = self.create(zmq.REQ)
        sv = self.create(zmq.REP)

        connect(client, cl)
        gevent.spawn(self.server, server, sv, 1)

        uid = uuid.uuid4()
        data = dict(name='Arewa')

        reqraw = backend.send(uid.hex, cl, data)
        assert isinstance(reqraw, bytes)

    def test_send_json(self):
        cl = self.create(zmq.REQ)
        sv = self.create(zmq.REP)

        connect(client, cl)
        gevent.spawn(self.server, server, sv, 1)

        uid = uuid.uuid4()
        data = dict(name='Arewa')

        reqraw = backend.send(uid.hex, cl, data).decode('utf8')
        req = json.loads(reqraw)
        assert 'origin' in req
        assert data == req['data']

    def test_recv_json(self):
        cl = self.create(zmq.REQ)
        sv = self.create(zmq.REP)

        connect(client, cl)
        gevent.spawn(self.server, server, sv)

        uid = uuid.uuid4()
        data = dict(name='Arewa')

        backend.send(uid.hex, cl, data).decode('utf8')
        respdata = backend.recv(cl)
        assert data == respdata
