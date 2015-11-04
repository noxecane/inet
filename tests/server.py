import logging
from inet.proxy import InetClient
from inet.server import RoutableServer

logging.basicConfig(level=logging.DEBUG)

proxy = InetClient('tcp://127.0.0.1:3014')
server = RoutableServer('testservice', proxy, 'tcp://127.0.0.1:4001',
                        'ipc:///tmp/inet.testservice.sock')


@server.route('hello/world')
def hello(req, resp):
    resp.data['greeting'] = 'World'
    return resp

server.setup(localproxy=False)
server.spawnworkers()
server.loopforever()
