import logging
import zmq.green as zmq
from inet import sockets
from inet.client import ns
from inet.utils.path import Path

logger = logging.getLogger('inet.client')


class InetPath(Path):

    def __call__(self, data):
        address = ns.get_address(self.path)


def module(name):
    context = zmq.Context.instance()
    return InetPath(name, sockets.create(context, zmq.REQ))
