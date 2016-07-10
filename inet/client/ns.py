from inet import NS_PORT
from inet.sockets import udp
from pyfunk.misc import fid


addresses = {}


class NoSuchMethod(Exception):
    pass


def get_address(path):
    address = addresses.get(path)
    if address is None:
        NoSuchMethod('This given %s does not exist' % path)
    return address


def save(info):
    pass


def autoupdate(addresses):
    # create socket
    socket = udp.broadcast(udp.create()) \
        .chain(udp.shared) \
        .chain(udp.bind('', NS_PORT)) \
        .chain(udp.pollable).unsafeIO()

    # listen
    while True:
        try:
            udp.wait(1024, 3, socket).fork(fid, save)
        except KeyboardInterrupt:
            break
