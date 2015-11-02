import sqlite3


class Sqlite(object):

    def __init__(self, path):
        self.path = path
        self.db = None

    def connect(self):
        self.db = sqlite3.connect(self.path)
        self.db.row_factory = sqlite3.Row

    def query(self, query, *params):
        c = self.db.cursor()
        c.execute(query, tuple(params))
        return c

    def run(self, query, *params):
        c = self.query(query, *params)
        self.db.commit()
        return c

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def queryone(self, query, *params):
        result = self.query(query, *params).fetchone()
        if result is not None:
            result = dict(result)
        return result

    def queryall(self, query, *params):
        result = self.query(query, *params).fetchall()
        if result is not []:
            result = list(map(dict, result))
        return result

    def close(self):
        self.db.close()
