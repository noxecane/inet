from collections import namedtuple
from inet.error import exceptions, MethodNotFound
from inet.utils import modules
from pyfunk import combinators as cm, collections as cl
from pyfunk.monads import either


safe_map = cm.compose(cl.fmap(either.ftry), modules.extract_functions)
safe_map.__doc__ = '''
Wraps all the functions from modules.extract_functions in a ftry from Either monad.
@sig safe_map :: Either e => Dict (* -> a) -> Dict (* -> e b a)
'''

Server = namedtuple('Server', ['uuid', 'port', 'sock', 'servicemap'])


@cm.curry
def confirm_path(servicemap, path):
    '''
    Ensures the function path is in the given servicemap
    @sig confirm_path :: Dict (* -> a) -> Str -> (Dict (* -> a), Str)
    '''
    if path not in servicemap:
        raise MethodNotFound
    return servicemap, path


def success_report(res):
    '''
    Generates a tuple to represent a successfull response
    @sig success_report :: a -> (Str, a)
    '''
    return 'success', res


def error_report(err):
    '''
    Generates an error tuple to represent failure of the an
    handler
    @sig error_report :: Error -> (Str, Dict Str)
    '''
    return 'error', exceptions.as_dict(err)


@cm.curry
def handle_request(servicemap, path, data):
    return __try_function(__get(*__confirm_path(servicemap, path)), data,
                          __success_report, __error_report)


@cm.curry
def register(servicemap, module):

    fnpaths = safe_map(module)
    servicemap.update(fnpaths)
    return fnpaths
