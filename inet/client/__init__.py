import logging
import uuid
import zmq.green as zmq
from inet import sockets
from inet.client import ns, backend
from inet.utils.path import Path, Root

logger = logging.getLogger('inet.client')
RECV_HOST = ''


class InetPath(Path):

    def __call__(self, data):
        addr = self.root.get_address(self.path)
        sockets.connect(addr, self.root.socket)
        self.root.send(data)
        result = self.root.recv()
        sockets.disconnect(addr, self.root.socket)
        return result


class InetClient(Root):

    path_cls = InetPath

    def __init__(self, name, context):
        super().__init__(name)
        self.socket = sockets.create_brutal(context, zmq.REQ)
        self.uuid = uuid.uuid4().hex
        self.get_address = ns.start_receiver(RECV_HOST)
        self.send = backend.send(self.uuid, self.socket)
        self.recv = lambda: backend.recv(self.socket)
