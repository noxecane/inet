import json


def encode(data):
    '''
    Encodes the given data as a json string
    @sig encode :: Dict -> String
    '''
    return bytes(json.dumps(data), 'utf8')


def decode(msg):
    '''
    Decodes zeromq messages to dict objects
    @sig decode :: String -> Dict
    '''
    return json.loads(msg.decode('utf8'))
