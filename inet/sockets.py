import logging
import zmq.green as zmq

from .constants import INET_REQUEST_TIMEOUT
from .errors import ConnectionError

logger = logging.getLogger('inet.socket')


def get_address(host, port):
    return 'tcp://%s:%s' % (host, port)


def create_socket(type, ctx=None):
    ctx = ctx or zmq.Context(1)
    socket = ctx.socket(type)
    return socket


def create_reliable_req_socket(poller=None, ctx=None):
    socket = create_socket(zmq.REQ, ctx)
    poller = poller or zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    return (socket, poller)


def destroy_socket(socket):
    socket.setsockopt(zmq.LINGER, 0)
    socket.close()


def destroy_reliable_req_socket(socket, poller):
    destroy_socket(socket)
    poller.unregister(socket)


def reliably_recv_req(socket, poller, address, retries=3):
    events = dict(poller.poll(INET_REQUEST_TIMEOUT))
    if events.get(socket) == zmq.POLLIN:
        logger.debug('Received reply after %s tries', 4 - retries)
        return socket.recv()
    elif retries:
        logger.debug('Retrying request.....(%s)', 4 - retries)
        destroy_reliable_req_socket(socket, poller)
        socket, poller = create_reliable_req_socket(poller)
        socket.connect(address)
        return reliably_recv_req(socket, poller, address, retries - 1)
    else:
        logger.debug('Ran out steam, abandoning request')
        destroy_reliable_req_socket(socket, poller)
        raise ConnectionError('Connection to server at %s refused' % address)
