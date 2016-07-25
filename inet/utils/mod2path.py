from importlib import import_module
from inet.errors import MethodNotFound
from inspect import getmembers, isfunction
from pkgutil import walk_packages
from


def get_paths(mod):
    if hasattr(mod, '__path__'):
        return [x[1] for x in walk_packages(mod.__path__, mod.__name__ + '.')]
    else:
        return [x for x, y in getmembers(mod)]


def load_mod(path):
    return import_module(path)



def split_path(path):
    parts = path.split('.')
    return '.'.join(parts[1:-1]), parts[-1:][0]


def call_function(path, data):
    modpath, fnname = split_path(path)
    try:
        mod = load_mod(modpath)
        fn = getattr(mod, fnname)
        return fn(data)
    except (AttributeError, ImportError):
        raise MethodNotFound()
