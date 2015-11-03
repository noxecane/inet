import logging

from inet.client import Client
from inet.proxy import InetClient

logging.basicConfig(level=logging.DEBUG)

proxy = InetClient('tcp://127.0.0.1:3014')
client = Client(proxy)

resp = client.get('testservice://hello/world')
assert resp.meta['status'] == 200
assert resp.data['greeting'] == 'World'
