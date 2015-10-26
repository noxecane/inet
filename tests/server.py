from .. import server


def user(req, resp):
    assert req.data('message') == 'ping'
    resp.meta('status', 200)
    resp.data('message', 'pong')
    resp.send()

user_server = server.spawn_server('user', user)
user_server.join()
