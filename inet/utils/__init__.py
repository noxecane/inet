from functools import wraps


def breakable_loop(fn):  # noqa
    @wraps(fn)
    def loop(*args, **kwargs):
        while True:
            try:
                fn(*args, **kwargs)
            except KeyboardInterrupt:
                break
    return loop


def once(fn):
    called = False
    result = None

    @wraps(fn)
    def called_once(*args, **kwargs):
        if not called:
            nonlocal called, result
            called = True
            result = fn(*args, **kwargs)
        return result
    return called_once
