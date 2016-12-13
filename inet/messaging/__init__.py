import functools


class InvalidType(TypeError):
    pass


def invalid_type(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except (KeyError, TypeError):
            raise InvalidType('The type passed is invalid')
    return decorated


def from_type(mtype):
    return dict(mtype._asdict())
