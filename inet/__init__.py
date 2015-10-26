# import atexit
# from .constants import INET_DB_FILENAME
import logging

logging.basicConfig(level=logging.DEBUG)

inet_db = {}
inet_db['endserver'] = {
    'host': '127.0.0.1',
    'port': 3004
}


# def __close_db():
#     inet_db.close()


# atexit.register(__close_db)
