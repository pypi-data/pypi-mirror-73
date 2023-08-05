
'''so_lazy lazy loading Python package'''

import json
import os

with open(os.path.dirname(__file__) + '/pkg_info.json') as handle:
    _pkg_info = json.load(handle)

__author__ = _pkg_info['author']
__homepage__ = _pkg_info['homepage']
__download__ = _pkg_info['download']
__license__ = _pkg_info['license']
__description__ = _pkg_info['description']
__version__ = _pkg_info['version']

from functools import wraps

def lazy(**dec_kwargs):
    '''Lazy loader decorator'''

    def _decorator(obj):

        @wraps(obj)
        def wrapper(*args, **kwargs):

            # check if class decorator
            if isinstance(obj, type):
                raise ClassDecoratedError('lazy is not designed to decorate classes')

            # set defaults
            loader = None
            loader_name = dec_kwargs.get('loader', '_lazy_loader')

            # check if calling class has loader
            if len(args) > 0:
                loader = getattr(args[0], loader_name, None)

            # check calling scope for loader
            if loader is None:
                loader = obj.__globals__.get(loader_name, None)

            # call lazy loader
            if loader is not None:
                loader()
            else:
                raise NoLoaderError('%s not found in current scope' % loader_name)

            return obj(*args, **kwargs)

        return wrapper

    return _decorator

# ----------
# Exceptions
# -----------

class ClassDecoratedError(TypeError):
    '''Class decorator error'''

class NoLoaderError(AttributeError):
    '''No loader found error'''
