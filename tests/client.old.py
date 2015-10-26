import json
import logging
import zmq.green as zmq

logging.basicConfig(level=logging.DEBUG)


logger = logging.getLogger('client')
DNSHOST = '127.0.0.1'
DNSPORT = 3004
LOOKUPCMD = 4
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
    logger.debug('Sending dns query for %s', HOSTNAME)
    
    dns_request = make_message()
    meta(dns_request, 'command', LOOKUPCMD)
    data(dns_request, 'hostname', HOSTNAME)
    socket.send(encode_message(dns_request))
    
    logger.debug('Waiting for response')
    dns_response = socket.recv()
    dns_response = decode_message(dns_response)
    serverinfo = data(dns_response)
    socket.close()

    socket = context.socket(zmq.REQ)
    socket.connect('tcp://%s:%s' % (serverinfo['localhost'], serverinfo['pin']))

    logger.debug('Sending request to tcp://%s:%s',
                 serverinfo['localhost'], serverinfo['pin'])

    request = make_message()
    data(request, 'message', 'Ping')
    request = encode_message(request)
    socket.send(request)

    response = socket.recv()
    response = decode_message(response)
    logger.debug('Response from server: %s', response)
    socket.close()




