import functools
import gevent
import logging
import zmq.green as zmq

from . import message
from .proxy import fork
from .router import Router
from .sockets import ClientSocket


logger = logging.getLogger('inet.server')


class Server(object):

    def __init__(self, service, frontend, backend):
        self.service = service
        self.frontend = frontend
        self.backend = backend
        self.router = Router()
        self._workers = []

    def route(self, path):
        """Decorator to smoothen handling different request on the same server."""
        def decorator(f):
            self.router.register(path, f)
            return f
        return decorator

    def spawnworkers(self, workers=3):
        """Create a worker greenlet."""
        logger.debug('Launching %s worker(s) for %s', workers, self.service)
        for _ in range(workers):
            _ = gevent.spawn(ServerWorker(self.service, self.backend, self.router))
            self._workers.append(_)

    def loopforever(self, workers=3):
        """Blocking function to give the workers time to listen to requests."""
        if len(self._workers) == 0:
            self.spawnworkers(workers)
        gevent.joinall(self._workers)


class RoutableServer(Server):

    def __init__(self, service, proxy, frontend, backend):
        super().__init__(service, frontend, backend)
        self.proxy = proxy

    def setup(self, localproxy=False, daemon=False):
        """Create the actual server and its proxy."""
        endpoint = self.proxy.register(self.service, self.frontend, self.backend)

        # fork a proxy if the proxy type is local
        if localproxy:
            logger.debug('Forking sub-process to proxy worker requests for %s', self.service)
            fork(self.service, self.frontend, self.backend, daemon)
        elif not endpoint:
            # no need to fork if record exists as the proxy will still be on
            self.proxy.fork(self.service, self.frontend, self.backend)


class ServerWorker(object):

    def __init__(self, service, backend, router):
        self.service = service
        self.address = backend
        self.router = router
        self.socket = ClientSocket(zmq.REP, backend)

    def __call__(self):
        logger = logging.getLogger('inet.server.worker.%s' % self.service)
        self.socket.connect()

        # function used to respond
        def send(self, socket):
            socket.sendmsg(self)

        while True:
            logger.debug('Listening on %s', self.address)
            req = self.socket.recvmsg()
            resp = message.message({'status': 200})
            handler = self.router.route(req)

            # validate the request
            if handler is None:
                resp.meta['status'] = 404
                resp.data['message'] = 'The route does not exist on this server'
            elif handler is False:
                resp.meta['status'] = 400
                resp.data['message'] = 'Meta "path" not found in request'
            else:
                setattr(resp, 'send', functools.partial(send, resp, self.socket))
                try:
                    resp = handler(req, resp)
                except Exception as e:
                    resp.meta['status'] = 500
                    resp.data['message'] = str(e)

            if resp is not None:
                send(resp, self.socket)

        # destroy socket, we never truly get here
        self.socket.destroy()
