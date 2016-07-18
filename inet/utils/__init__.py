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
