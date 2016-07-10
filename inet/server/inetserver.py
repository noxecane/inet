import logging
import plac

from .db import Sqlite, sqlite3
from .proxy import fork
from .server import Server

logger = logging.getLogger('inet.service.server')
server = Server('inet', None, 'ipc:///tmp/inet.inetserver.sock')
inetdb = Sqlite('/tmp/inetservices.db')
forked = []


logger.debug('Ensuring data exists in database')
inetdb.connect()
inetdb.run('''create table if not exists services (
    id integer primary key autoincrement,
    name text unique not null,
    frontend text unique not null,
    backend text unique not null,
    forked integer
);''')
inetdb.close()


@server.route('endpoint/get')
def query(req, resp):
    inetdb.connect()

    # retrieve important service info
    service = req.data['service']
    endpoint = inetdb.queryone('''
        select name, frontend, backend from services
        where name=?;
        ''', service)

    # return appropriate response
    if endpoint:
        logger.debug('Found endpoint %s at %s => %s', service,
                     endpoint['frontend'], endpoint['backend'])
        resp.data = endpoint
    else:
        logger.debug('%s has no record', service)
        resp.meta['status'] = 404
        resp.data['message'] = "The %s service doesn't exist" % service

    inetdb.close()
    return resp


@server.route('endpoint/post')
def register(req, resp):
    inetdb.connect()

    # retrieve important service info
    service = req.data['service']
    frontend = req.data['frontend']
    backend = req.data['backend']

    logger.debug('Creating record for %s', service)
    try:
        inetdb.run('''
            insert into services (name, frontend, backend, forked)
            values (?,?,?,?)''', service, frontend, backend, 0)
    except sqlite3.IntegrityError:
        # we assume only the service is being duplicated
        endpoint = inetdb.queryone('''
        select name, frontend, backend from services
        where name=?;
        ''', service)
        logger.debug('Found previous record %s => %s',
                     endpoint['frontend'], endpoint['backend'])
        resp.data = endpoint

    inetdb.close()
    return resp


@server.route('endpoint/delete')
def unregister(req, resp):
    inetdb.connect()

    # retrieve important service info
    service = req.data['service']

    logger.debug('Deleting record for %s', service)
    inetdb.run('delete from services where name=?', service)

    inetdb.close()
    return resp


@server.route('proxy/fork')
def fork_proxy(req, resp):
    inetdb.connect()
    service = req.data['service']

    if service in forked:
        resp.meta['status'] = 409
        resp.data['message'] = 'Proxy already forked'
        return resp

    forked.append(service)
    frontend = req.data['frontend']
    backend = req.data['backend']
    inetdb.run('update services set forked=? where frontend=? and backend=?',
               1, frontend, backend)

    logger.debug('Creating sub-process to route "%s" requests', service)
    fork(service, frontend, backend)
    inetdb.close()
    return resp


def startserver(address: 'Frontend address of the server'='tcp://127.0.0.1:3014',
                debug: 'Start server in debug mode'=True):
    inetdb.connect()
    server.frontend = address

    logger.debug('Forking proxy for inet server')
    fork(server.service, server.frontend, server.backend)

    # fork their proxies
    for service in inetdb.queryall('select * from services where forked=?', 1):
        fork(service['name'], service['frontend'], service['backend'])

    # start workers and wait
    server.spawnworkers()
    server.loopforever()
    inetdb.close()


def main():
    logging.basicConfig(level=logging.DEBUG)
    try:
        plac.call(startserver)
    except KeyboardInterrupt:
        logging.error('Exiting server')
