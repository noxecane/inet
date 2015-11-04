import gipc
import logging
import plac
import zmq.green as zmq

from .errors import ConnectionError
from .router import Router
from .sockets import ReliableSocket


logger = logging.getLogger('inet.service.client')
service_doc = "Name of the service that'll be proxied."
frontend_doc = "Address for clients to connect to."
backend_doc = "Address for server workers."


def fork(service, frontend, backend, daemon=False):
    """Create a proxy."""
    with gipc.pipe():
        gipc.start_process(target=mediate, args=(service, frontend, backend), daemon=daemon)


def main():
    logging.basicConfig(level=logging.DEBUG)
    try:
        plac.call(mediate)
    except KeyboardInterrupt:
        logging.error('Exiting proxy....')


def mediate(service: service_doc, front: frontend_doc, back: backend_doc):
    context = zmq.Context()
    logger = logging.getLogger('inet.proxy.%s' % service)

    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    frontend.bind(front)
    backend.bind(back)

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    logger.debug('Starting proxy %s => %s', front, back)

    while True:
        events = dict(poller.poll())

        if events.get(frontend) == zmq.POLLIN:
            msg = frontend.recv_multipart()
            backend.send_multipart(msg)
        elif events.get(backend) == zmq.POLLIN:
            msg = backend.recv_multipart()
            frontend.send_multipart(msg)


class InetClient(object):

    """Link to the Inet server."""

    def __init__(self, address):
        self.address = address
        self.socket = ReliableSocket(address)
        self.cache = {}

    def query(self, service):
        """Look for a service's address in its cache or Inet server.

        The cache can never have invalid addresses as Inet registerations
        are permanent.
        """
        if service in self.cache:
            return self.cache[service]

        # create and connect
        self.socket.connect()

        # make dns request
        _, req = Router.transform('inet://endpoint/get')
        req.data = {'service': service}
        logger.debug('Sending inet query for %s', service)
        self.socket.sendmsg(req)

        resp = self.socket.recvmsg()
        self.socket.destroy()

        if resp.meta['status'] == 200:
            address = resp.data['frontend']
            self.cache[service] = address
            logger.debug('Found %s at %s', service, address)
            return address
        else:
            raise ConnectionError('(%d) (%s)' % (resp.meta['status'], resp.data['message']))

    def register(self, service, frontend, backend):
        """Register a service to the Inet server.

        Note that whatever address is returned is permanent.
        """
        self.socket.connect()

        logger.debug('Trying to register %s', service)
        _, req = Router.transform('inet://endpoint/post')
        req.data = {
            'service': service,
            'frontend': frontend,
            'backend': backend
        }
        self.socket.sendmsg(req)

        # ensure message is sent before destroying socket
        resp = self.socket.recvmsg()
        self.socket.destroy()
        return resp.data

    def fork(self, service, frontend, backend):
        """Create a proxy in inet host."""
        self.socket.connect()

        _, req = Router.transform('inet://proxy/fork')
        req.data = {
            'service': service,
            'frontend': frontend,
            'backend': backend
        }
        self.socket.sendmsg(req)

        # ensure message is sent before destroying socket
        self.socket.recvmsg()
        self.socket.destroy()

    def unregister(self, service):
        """Remove a service permanently from inet."""
        self.socket.connect()

        logger.debug('Removing %s', service)
        _, req = Router.transform('inet://endpoint/delete')
        req.data = {'service': service}
        self.socket.sendmsg(req)

        # ensure message is sent before destroying socket
        self.socket.recvmsg()
        self.socket.destroy()

        if service in self.cache:
            del self.cache[service]
