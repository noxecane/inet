import logging
from inet.inetclient import InetClient
from inet.errors import ConnectionError


logging.basicConfig(level=logging.DEBUG)
proxy = InetClient('tcp://127.0.0.1:3014')


# query fail
try:
    proxy.query('fakeservice')
except ConnectionError:
    pass
except Exception:
    raise AssertionError("Didn't raise ConnectionError")


# register and query
proxy.register('fakeservice', 'loopin', 'loopout')
frontend = proxy.query('fakeservice')
assert frontend == 'loopin'

# duplicate_register
proxy.register('fakeservice', 'loopon', 'loopout')
frontend = proxy.query('fakeservice')
assert frontend == 'loopin'

# delete
proxy.unregister('fakeservice')
try:
    proxy.query('fakeservice')
except ConnectionError:
    pass
except Exception:
    raise AssertionError("Didn't raise ConnectionError")


# fork
proxy.fork('fakeservice', 'inproc://loopin', 'inproc://loopout')
