from pyfunk import combinators as cm


def __name(err):
    return type(err).__name__


def __message(err):
    return str(err)


def as_dict(err):
    return {'name': __name(err), 'message': __message(err)}


def create(name):
    return type(name, (Exception, ), {})
