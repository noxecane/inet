class MethodNotFound(AttributeError):
    pass


class ConnectionTimeout(ConnectionError):
    pass


class InvalidType(TypeError):
    pass


def exception(name):
    return type(name, (Exception, ), {})
