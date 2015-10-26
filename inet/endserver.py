import gipc
import logging
import zmq.green as zmq

from . import (
    sockets, message, counter,
    loadbalancer, inet_db
)
from .constants import INET_COMMAND_INIT, INET_COMMAND_LOOKUP


load_balancers = {}

pin_counter = counter.counter('pin', 4000, 5000)
pout_counter = counter.counter('pout', 5000, 6000)

host = inet_db['endserver']['host']
port = inet_db['endserver']['port']
address = sockets.get_address(host, port)
logger = logging.getLogger('inet.endserver')


def fork(service):
    lb = {
        'frontend': sockets.get_address(host, next(pin_counter)),
        'backend': sockets.get_address(host, next(pout_counter)),
        'service': service
    }
    with gipc.pipe() as (pipein, pipeout):
        logger.debug('Forking process to host %s load balancer', service)
        gipc.start_process(target=loadbalancer.mediate, args=(pipein, ))
        pipeout.put(lb)
        return lb


def start_server():
    socket = sockets.create_socket(zmq.REP)
    socket.bind(address)
    while True:
        logger.debug('Listening on %s for dns queries', address)
        req = message.from_raw(socket.recv())

        if req.meta('method') == 'endpoint':
            command = req.data('command')
            service = req.data('service')

            if command == INET_COMMAND_LOOKUP:
                if service in load_balancers:
                    resp = message.message({'status': 200})
                    resp.data('address', load_balancers[service]['frontend'])
                    logger.debug('Lookup -- Request:%s Response:%s',
                                 req.asdict(), resp.asdict())
                    socket.send(resp.raw())
                else:
                    resp = message.message({'status': 200})
                    resp.data('message', 'Server not found')
                    logger.debug('Lookup -- Request:%s Response:%s',
                                 service, resp.asdict())
                    socket.send(resp.raw())
            elif command == INET_COMMAND_INIT:
                if service not in load_balancers:
                    load_balancers[service] = fork(service)
                resp = message.message({'status': 200})
                resp.data('address', load_balancers[service]['backend'])
                logger.debug('Init -- Request:%s Response:%s',
                             req.asdict(), resp.asdict())
                socket.send(resp.raw())
    sockets.destroy_socket(socket)
