import logging
import zmq.green as zmq

from . import message
from .errors import ConnectionError


logger = logging.getLogger('inet.socket')


class Socket(object):

    """Simple cover over :class:`zmq.Socket`."""

    context = zmq.Context(1)

    def __init__(self, stype, address=None):
        """Set up data needed to create and destroy a socket."""
        self.stype = stype
        self.address = address
        self.socket = None
        self.closed = True
        self._context = Socket.context

    def instantiate(self):
        """Create a new socket. Ensure you destroy when you are done with the socket."""
        self.socket = self._context.socket(self.stype)
        self.closed = False

    def destroy(self):
        """Shutdown a socket.

        All messages that are in its queue will be cleared so use carefully.
        """
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.closed = True

    def restart(self):
        """Destroy and recreate a socket/."""
        self.destroy()
        self.instantiate()

    def sendraw(self, raw):
        """Proxy to ``zmq.Socket.send``."""
        self.socket.send(raw)

    def sendmsg(self, msg):
        """Make it possible to send :class:`inet._Message`."""
        self.sendraw(msg.raw)

    def recvraw(self):
        """Proxy to ``zmq.Socket.recv``."""
        return self.socket.recv()

    def recvmsg(self):
        """Same as sendmsg."""
        return message.from_raw(self.recvraw())


class ClientSocket(Socket):

    """Represents a socket that only connects, not necessarily a REQ socket."""

    def connect(self):
        if self.closed:
            self.instantiate()
        self.socket.connect(self.address)

    def disconnect(self):
        if self.closed:
            self.instantiate()
        self.socket.disconnect(self.address)


class ServerSocket(Socket):

    """Represents a socket that binds."""

    def bind(self):
        if self.closed:
            self.instantiate()
        self.socket.bind(self.address)

    def unbind(self):
        if self.closed:
            self.instantiate()
        self.socket.unbind(self.address)


class ReliableSocket(ClientSocket):

    """It's called reliable because it's sure to notify if doesn't receive a reply.

    Unlike other sockets it's a defined REQ socket(which can be changed but don't
    unless you know what you are doing).
    """

    def __init__(self, address=None):
        super().__init__(zmq.REQ, address=address)
        self.poller = zmq.Poller()

    def instantiate(self):
        super().instantiate()
        self.poller.register(self.socket, zmq.POLLIN)

    def destroy(self):
        super().destroy()
        self.poller.unregister(self.socket)

    def recvraw(self, retries=3, timeout=3000):
        """Wait reliably for a response.

        Unlike normal recv, this ensures that a response is received
        within the specified timeout and after at least the number of
        retries given.
        """
        events = dict(self.poller.poll(timeout))
        if events.get(self.socket) == zmq.POLLIN:
            logger.debug('Received reply after %s tries', 4 - retries)
            return super().recvraw()
        elif retries:
            logger.debug('Retrying request.....(%s)', 4 - retries)
            # restart and reconnect
            self.restart()
            self.connect()
            return self.recvraw(retries=retries - 1)
        else:
            logger.debug('Ran out steam, abandoning request')
            self.destroy()
            raise ConnectionError('Connection to server at %s refused' % self.address)
