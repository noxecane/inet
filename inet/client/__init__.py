import logging
import uuid
import zmq.green as zmq

from collections import namedtuple
from inet import sockets
from inet.messaging.request import Request

logger = logging.getLogger('inet.client')
RECV_HOST = ''

Client = namedtuple('Client', ['context', 'uuid', 'send'])


def create_client(context=None):
    context = context or zmq.Context.instance()


def get(client, path):
    pass


class InetPath(Path):

    def __call__(self, data):
        addr = self.root.get_address(self.path)

        sock = sockets.create(self.root.context, zmq.REQ)
        sockets.connect(addr, sock)

        self.root.send(sock, Request(self.root.uuid, self.path, data))
        response = backend.recv(sock)

        sockets.disconnect(addr, sock)
        sockets.close(sock)
        return response.data
 

class InetClient(Root):

    path_cls = InetPath

    def __init__(self, name, context=None):
        super().__init__(name)
        self.context = 
        self.uuid = uuid.uuid4().hex
        self.get_address = backend.start_receiver(RECV_HOST)
