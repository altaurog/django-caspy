from .version import __version__    # noqa

try:
    str = unicode  # python 2.7
except NameError:
    str = str
