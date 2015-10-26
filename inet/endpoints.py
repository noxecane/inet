from . import (
    sockets, message, inet_db
)
from .constants import INET_COMMAND_INIT, INET_COMMAND_LOOKUP


services = {}
endserver = sockets.get_address(inet_db['endserver']['host'],
                                inet_db['endserver']['port'])


def query(service):
    sock, poller = sockets.create_reliable_req_socket()
    sock.connect(endserver)
    req = message.message()

    # build the request
    req.meta('method', 'endpoint')
    req.data('command', INET_COMMAND_LOOKUP)
    req.data('service', service)

    # query the dns server
    sock.send(req.raw())
    resp = sockets.reliably_recv_req(sock, poller, endserver)
    # clean up the mess
    sockets.destroy_reliable_req_socket(sock, poller)

    # return nothing if server was not found
    resp = message.from_raw(resp)
    if resp.meta('status') == 200:
        services[service] = resp.data()
        return resp.data()


def init(service):
    sock, poller = sockets.create_reliable_req_socket()
    sock.connect(endserver)
    req = message.message()

    # build the request
    req.meta('method', 'endpoint')
    req.data('command', INET_COMMAND_INIT)
    req.data('service', service)

    # query the dns server
    sock.send(req.raw())
    resp = sockets.reliably_recv_req(sock, poller, endserver)
    # clean up the mess
    sockets.destroy_reliable_req_socket(sock, poller)
    return message.from_raw(resp).data()
