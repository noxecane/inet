# inet

**v0.2.4 has bug so you'll have to clone the head**

A simple library built on top of zeromq to enable different python
programs talk over sockets. It works using three components
*server*, *name service* and *client*. The main feature(or use) of this
library is its persistent name service


### Name Service
Start the inet server on command line
```shell
$ inetserver
```

### Server
The server is a function to respond to requests

```python
from inet.inetclient import InetClient
from inet.server import RoutableServer

# talks with the inet server
proxy = InetClient('tcp://127.0.0.1:3014')

# frontend address is what clients connect to while backend address(unix socket)
# is what workers connect to
server = RoutableServer('testservice', proxy, 'tcp://127.0.0.1:4001',
                        'ipc:///tmp/inet.testservice.sock')


@server.route('hello/world')
def hello(req, resp):
    resp.data['greeting'] = 'World'
    return resp

server.setup(localproxy=False)
# spawn default(3) number of workers
server.spawnworkers()
server.loopforever()
```

### Client

```python
from inet.inetclient import InetClient
from inet.client import Client

proxy = InetClient('tcp://127.0.0.1:3014')
client = Client(proxy)

# service name acts as protocol
resp = client.get('testservice://hello/world')
print(resp.meta['status'])  # 200
print(resp.data['greeting']) # 'World'
```


*N.B*: Notes that it uses gevent for managing workers