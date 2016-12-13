import importlib
import inspect
import pkgutil
from pyfunk import combinators as cm, collections as cl
from pyfunk.monads import Maybe, fmap


def submodules(module):
    '''
    Lists all submodules of the given module as a "." seperated
    paths starting from the given module.
    @sig submodules :: Module -> [Str]
    '''
    if hasattr(module, '__path__'):
        return [x[1] for x in pkgutil.walk_packages(module.__path__, module.__name__ + '.')]
    else:
        return [module.__name__]


@cm.curry
def members(predicate, module):
    '''
    Returns a list of all the members as a tuple of the name with
    the module path appended and the member's value of the
    given module filtered according to the given predicate
    @sig members :: (Module -> Bool) -> Module -> [(Str, (* -> a))]
    '''
    if predicate(module):
        return [(module.__name__, module)]
    else:
        return [('%s.%s' % (module.__name__, x), y)
                for x, y in inspect.getmembers(module, predicate)]


def import_module(path):
    '''
    Import the module specified by the path.
    @sig import_module :: Str -> Maybe Module
    '''
    try:
        return Maybe.of(importlib.import_module(path))
    except ImportError:
        return Maybe.of(None)


def unwrap(mpath):
    '''
    Correctly unwraps the path tuple from the maybe.
    @sig normalize :: Maybe [(Str, Module)] -> [(Str, Module)]
    '''
    return mpath.or_else([])

__import_submodules = cm.compose(fmap(import_module), submodules)
__get_functions = cm.compose(fmap(fmap(members(inspect.isfunction))), __import_submodules)
__list_functions = cm.compose(cl.flatten, fmap(unwrap), __get_functions)


def list_functions(module):
    '''
    Generates a tuple of all functions in a given module and it's
    submodules with their module paths.
    @sig list_function :: Moduel -> [(Str, (* -> a))]
    '''
    return __list_functions(module)


__map_functions = cm.compose(cl.fzip, __list_functions)


def map_functions(module):
    '''
    Behaves like list_functions except that it returns a map
    of the function t0 their paths rather than a list of tuples
    '''
    return __map_functions(module)
