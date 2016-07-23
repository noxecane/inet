import logging
import uuid
from inet import sockets
from inet.client import ns, backend
from inet.utils.path import Path

logger = logging.getLogger('inet.client')


def create_uuid():
    return uuid.uuid4().hex


class InetPath(Path):

    def __call__(self, data):
        # create a socket
        # set uuid of client

        # get address of the path
        # connect 
        address = ns.get_address(self.path)
