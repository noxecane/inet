import logging
import zmq.green as zmq


def mediate(pipein):
    balancer_info = pipein.get()
    context = zmq.Context()
    logger = logging.getLogger('inet.loadbalancer.%s' % balancer_info['service'])

    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    frontend.bind(balancer_info['frontend'])
    backend.bind(balancer_info['backend'])

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    logger.debug('Starting load balancer at %s in and %s out',
                 balancer_info['frontend'], balancer_info['backend'])

    while True:
        events = dict(poller.poll())

        if events.get(frontend) == zmq.POLLIN:
            msg = frontend.recv_multipart()
            backend.send_multipart(msg)
        elif events.get(backend) == zmq.POLLIN:
            msg = backend.recv_multipart()
            frontend.send_multipart(msg)
