

class MethodNotFound(Exception):
    pass


class ConnectionTimeout(Exception):
    pass


class RegisterationError(Exception):
    pass


def exception(name):
    return type(name, (Exception, ), {})
