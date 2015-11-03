import gipc
import logging
import plac
import zmq.green as zmq


def fork(service, frontend, backend, daemon=False):
    """Create a proxy."""
    with gipc.pipe():
        gipc.start_process(target=mediate, args=(service, frontend, backend), daemon=daemon)


def main():
    logging.basicConfig(level=logging.ERROR)
    try:
        plac.call(mediate)
    except KeyboardInterrupt:
        logging.error('Exiting proxy....')


def mediate(service, front, back):
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
