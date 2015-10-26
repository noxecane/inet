from . import inet_db


class Counter(object):
    counterdb = None
    cache = {}

    def __init__(self, name, start, stop):
        self.name = name
        self.start = start
        self.stop = stop

    def __iter__(self):
        if self.name not in self.cache:
            self.cache[self.name] = self.start
        return self

    def __next__(self):
        if self.cache[self.name] == self.stop:
            raise StopIteration
        self.cache[self.name] += 1
        inet_db['counters'] = self.cache
        return self.cache[self.name] - 1


def counter(name, start, stop):
    return iter(Counter(name, start, stop))
