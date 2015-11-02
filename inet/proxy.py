import click
import gipc
import logging
import zmq.green as zmq


def fork(service, frontend, backend):
    """Creates a proxy"""
    with gipc.pipe():
        gipc.start_process(target=mediate, args=(service, frontend, backend))


@click.command()
@click.option('--service')
@click.option('--frontend')
@click.option('--backend')
def main(service, frontend, backend):
    mediate(service, frontend, backend)


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
