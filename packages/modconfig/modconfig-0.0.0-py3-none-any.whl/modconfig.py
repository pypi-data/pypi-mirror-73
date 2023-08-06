import json
import logging
import os
from importlib import import_module


__version__ = "0.0.0"
__license__ = "MIT"


logger = logging.getLogger('scfg')


class Config:

    def __init__(self, mod, **scope):
        if mod:

            if isinstance(mod, str):
                try:
                    mod = import_module(mod)

                except ImportError:
                    logger.error('Invalid configuration module given: %s', mod)

            for name in dir(mod):
                scope.setdefault(name, getattr(mod, name))

        self.__dict__.update({
            name: scope[name] for name in scope
            if not name.startswith('_')
        })

        for name in os.environ:
            if not hasattr(self, name):
                continue

            value = os.environ[name]
            value_type = type(getattr(self, name))
            try:
                value = json.loads(value)
            except ValueError:
                pass

            try:
                value = value_type(value)
            except (ValueError, TypeError):
                continue

            setattr(self, name, value)
