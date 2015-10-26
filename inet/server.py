import functools
import gevent
import logging
import zmq.green as zmq

from . import (
    sockets, endpoints,
    message
)


def spawn_server(service, handler):
    return gevent.spawn(__server, service, handler)


def __server(service, handler):
    logger = logging.getLogger('inet.server.%s' % service)
    backend = endpoints.init(service)
    socket = sockets.create_socket(zmq.REP)
    socket.connect(backend['address'])

    def __send(socket, resp):
        logger.debug('get response:%s', resp.asdict())
        socket.send(resp.raw())

    while True:
        logger.debug('Serving on %s as backend', backend['address'])
        req = message.from_raw(socket.recv())
        if req.meta('method') == 'get':
            # create response with ability to send itself
            resp = message.message()
            setattr(resp, 'send', functools.partial(__send, socket, resp))
            handler(req, resp)
        else:
            # immediately send
            resp = message.message({'status', 201})
            logger.debug('post response:%s', resp.asdict())
            socket.send(resp.raw())
            handler(req)
    sockets.destroy_socket(socket)
