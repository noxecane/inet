from .. import client


resp = client.get('user', {'message': 'ping'})
assert resp.data('message') == 'pong'
