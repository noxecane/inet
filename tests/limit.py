import gevent

from inet.proxy import InetClient


def interval(fn, delay, loops, *args, **kwargs):
    while loops != 0:
        gevent.sleep(delay)
        kwargs['loops'] = loops
        fn(*args, **kwargs)
        loops -= 1


proxy = InetClient('tcp://127.0.0.1:3014')


def query(service, loops):
    global proxy
    print(proxy.query(service), loops)


if __name__ == '__main__':
    interval(query, 5, 2000, 'testservice')
