import msgpack


def encode(data):
    '''
    Encodes the given data as a msgpack string
    @sig encode :: Dict -> String
    '''
    return msgpack.dumps(data)


def decode(msg):
    '''
    Decodes zeromq messages to dict objects
    @sig decode :: String -> Dict
    '''
    return msgpack.loads(msg)
