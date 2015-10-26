# inet

A simple library built on top of zeromq to enable different python
programs make requests over tcp. It works using three components
*server*, *dns* and *client* and they are connected using service
names

### Server
The server is a function to respond to requests

```python
from inet import server
def hello_world_server(req, resp):
    if req.data('message') == 'Hello':
        resp.data('message', 'World')
        resp.send()

server.spawn_server('hello', hello_world_server)
```

### Client
```python
from inet import client

resp = client.get('hello', {'message', 'Hello'})
print(resp.data('message')) # "World"
```

### DNS
```
from inet import endserver

endserver.start_server()
```

*N.B*: Notes that it uses gevent for managing workers