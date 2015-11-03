import logging

from .router import Router
from .sockets import ReliableSocket


logger = logging.getLogger('inet.client')


class Client(object):

    """Represents an actual client."""

    def __init__(self, proxy_client):
        self.socket = ReliableSocket()
        self.proxy = proxy_client

    def get(self, url, data=None):
        """Hide the process needed to make a request."""
        service, req = Router.transform(url)
        if data is not None:
            req.data = data
        return self.sendrequest(service, req)

    def sendrequest(self, service, req):
        """Send a :class:message.`_Message`.

        It doesn't bother to catch any errors involved with sending the request though
        """
        address = self.proxy.query(service)

        logger.debug('Connecting to server at %s', address)
        self.socket.address = address
        self.socket.connect()

        logger.debug('Sending request......')
        self.socket.sendmsg(req)
        return self.socket.recvmsg()
