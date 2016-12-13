import functools


def breakable_loop(fn):
    '''
    Creates a function that continously loops till a keyboard
    interrupt exception is thrown
    @sig breakable_loop :: (* -> _) -> (* -> _)
    '''
    @functools.wraps(fn)
    def loop(*args, **kwargs):
        while True:
            try:
                fn(*args, **kwargs)
            except KeyboardInterrupt:
                break
    return loop


def once(fn):
    '''
    Creates a function that can only be called once after the function
    has been imported. Basically you'll need to restart the interpreter
    to call it again.
    @sig once :: (* -> a) -> (* -> a)
    '''
    called = False
    result = None

    @functools.wraps(fn)
    def called_once(*args, **kwargs):
        nonlocal called, result
        if not called:
            called = True
            result = fn(*args, **kwargs)
        return result
    return called_once
