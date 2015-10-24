import json
import logging
import zmq.green as zmq

logging.basicConfig(level=logging.DEBUG)


logger = logging.getLogger('client')
DNSHOST = '127.0.0.1'
DNSPORT = 3004
SETUPCMD = 6
HOSTNAME = 'user'

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://%s:%s' % (DNSHOST, DNSPORT))


def make_message():
    return {'meta': {}, 'data': {}}


def decode_message(message):
    message = message.decode('utf-8')
    return json.loads(message)


def encode_message(message):
    message =  json.dumps(message)
    return message.encode('utf-8')

def meta(message, key, val=None):
    if val is None:
        return message['meta'][key]
    else:
        message['meta'][key] = val


def data(message, key=None, val=None):
    if key is None:
        if val is not None:
            message['data'] = val
        else:
            return message['data']
    if val is None:
        return message['data'][key]
    else:
        message['data'][key] = val


if __name__ == '__main__':
    logger.debug('Connected to tcp://%s:%s', DNSHOST, DNSPORT)
    logger.debug('Sending dns setup query for %s', HOSTNAME)
    
    dns_request = make_message()
    meta(dns_request, 'command', SETUPCMD)
    data(dns_request, 'hostname', HOSTNAME)
    socket.send(encode_message(dns_request))
    
    logger.debug('Waiting for response')
    dns_response = socket.recv()
    dns_response = decode_message(dns_response)
    dnsinfo = data(dns_response)
    socket.close()
    
    socket = context.socket(zmq.REP)
    socket.connect('tcp://%s:%s' % (dnsinfo['localhost'], dnsinfo['pout']))

    while True:
        logger.debug('Serving on tcp://%s:%s as backend',
                 dnsinfo['localhost'], dnsinfo['pout'])
        request = socket.recv()
        request = decode_message(request)
        logger.debug('Request from client:%s', request)

        response = make_message()
        meta(response, 'status', 200)
        data(response, 'message', 'Pong')
        response = encode_message(response)
        socket.send(response)
    socket.close()

    




