"""
Lightweight objects
"""
import collections
from caspy import str


class Lightweight(collections.Mapping):
    def __init__(self, *args, **kwargs):
        for f in self._fields:
            setattr(self, f, get(f, *args, **kwargs))

    def copy(self, **kwargs):
        return self.__class__(self, **kwargs)

    def __iter__(self):
        return iter(self._fields)

    def __len__(self):
        return len(self._fields)

    def __str__(self):
        return str(getattr(self, self._fields[0]))

    def __getitem__(self, name):
        return getattr(self, name)

    def __repr__(self):
        kwargs = ['{}={!r}'.format(f, getattr(self, f)) for f in self._fields]
        return '{}({})'.format(self.__class__.__name__, ', '.join(kwargs))


def get(*args, **kwargs):
    return kwargs.get(args[0], _get(args[0], *args[1:]))


def _get(name, *args):
    if args:
        try:
            return args[0].get(name, get(name, *args[1:]))
        except AttributeError:
            return getattr(args[0], name, get(name, *args[1:]))
