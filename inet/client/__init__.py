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
        sock = self.root.new_socket()
        addr = self.root.get_address(self.path)

        sockets.connect(addr, sock)
        self.root.send(sock, data)
        result = backend.recv(sock)

        sockets.disconnect(addr, sock)
        sockets.close(sock)
        return result


class InetClient(Root):

    path_cls = InetPath

    def __init__(self, name, context):
        super().__init__(name)
        self.new_socket = lambda: sockets.create_brutal(context, zmq.REQ)
        self.uuid = uuid.uuid4().hex
        self.get_address = ns.start_receiver(RECV_HOST)
        self.send = backend.send(self.uuid)
