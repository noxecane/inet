import gipc
import json
import logging
import zmq.green as zmq


logging.basicConfig(level=logging.DEBUG)


logger = logging.getLogger('dns-server')
lb_balancer_map = {}
LOOKUP_CMD = 4
SETUP_CMD = 6
LAST_PIN = 4000 
LAST_POUT = 5000
LOCALHOST = '127.0.0.1'
LOCALPORT = 3004

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://%s:%s' % (LOCALHOST, LOCALPORT))


def make_message():
    return {'meta': {}, 'data': {}}


def decode_message(message):
    message = message.decode('utf-8')
    return json.loads(message)


def encode_message(message):
    message = json.dumps(message)
    return message.encode('utf-8')


def meta(req, key, val=None):
    if val is None:
        return req['meta'][key]
    else:
        req['meta'][key] = val


def data(message, key=None, val=None):
    if key is None:
        if val is not None:
            message['data'] = val
            return
        else:
            return message['data']
    if val is None:
        return message['data'][key]
    else:
        message['data'][key] = val


def create_lb(hostname):
    global LAST_PIN
    global LAST_POUT
    lb = {}    
    # create frontend port
    lb['pin'] = LAST_PIN
    LAST_PIN += 1
    # create backend port
    lb['pout'] = LAST_POUT
    LAST_POUT += 1
    # host info
    lb['hostname'] = hostname
    lb['localhost'] = LOCALHOST
    logger.debug('Created load balancer with hostname:%s port-in:%s port-out:%s',
                  hostname, LAST_PIN, LAST_POUT)
    return lb


def mediate(pipein):
    lb = pipein.get()
    context = zmq.Context()
    logger = logging.getLogger(lb['hostname'])

    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    frontend.bind('tcp://%s:%s' % (lb['localhost'], lb['pin']))
    backend.bind('tcp://%s:%s' % (lb['localhost'], lb['pout']))

    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    logger.debug('Starting load balancer at tcp://%s:%s in and tcp://%s:%s out',
                 lb['localhost'], lb['pin'], lb['localhost'], lb['pout'])
    while True:
        events = dict(poller.poll())

        if events.get(frontend) == zmq.POLLIN:
            msg = frontend.recv_multipart()
            backend.send_multipart(msg)
        elif events.get(backend) == zmq.POLLIN:
            msg = backend.recv_multipart()
            frontend.send_multipart(msg)


def fork(lb):
    with gipc.pipe() as (pipein, pipeout):
        logger.debug('Forking process to host %s load balancer', lb['hostname'])
        process = gipc.start_process(target=mediate, args=(pipein, ))
        pipeout.put(lb)


def make_response(status, d):
    response = make_message()
    meta(response, 'status', status)
    data(response, None, d)
    return encode_message(response)


if __name__ == '__main__':
    while True:
        logger.debug('Listening on %s:%s for dns queries', LOCALHOST, LOCALPORT)
        request = socket.recv()
        request = decode_message(request)

        cmd = meta(request, 'command')
        if cmd == LOOKUP_CMD:
            hostname = data(request, 'hostname')
            logger.debug('Received lookup command for %s', hostname)

            if hostname in lb_balancer_map:
                response = make_response(200, lb_balancer_map[hostname])
                socket.send(response)
                logger.debug('Sent 200 response')
            else:
                response = make_response(404, {
                    'message': 'Server not found'
                })
                socket.send(response)
                logger.debug('Sent 404 response')
        elif cmd == SETUP_CMD:
            hostname = data(request, 'hostname')
            logger.debug('Received setup command for %s', hostname)
            if hostname not in lb_balancer_map:
                lb = create_lb(hostname)
                fork(lb)
                lb_balancer_map[hostname] = lb
            response = make_response(200, lb_balancer_map[hostname])
            socket.send(response)
            logger.debug('Sent lb details for %s', hostname)

        

