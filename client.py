import logging
import zmq.green as zmq

from . import (
    sockets, endpoints,
    message
)
from .constants import (
    INET_COMMAND_LOOKUP, INET_STATUS_OK,
    INET_STATUS_NOT_FOUND
)
from .errors import ConnectionError


logger = logging.getLogger('inet.client')


def request(service, req):
    frontend = endpoints.query(service)

    if frontend is None:
        raise ConnectionError('No server is available for %s' % service)

    socket, poller = sockets.create_reliable_req_socket()
    socket.connect(frontend['address'])
    socket.send(req.raw())
    return message.from_raw(sockets.reliably_recv_req(socket, poller, frontend))


def get(service, data):
    if isinstance(data, dict):
        req = message.message({'method': 'get'}, data)
        return request(service, req)
    else:
        raise ValueError('Expecting a dict found %s' % type(data))
