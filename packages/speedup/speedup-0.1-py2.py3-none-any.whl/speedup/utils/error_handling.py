import sys
from termcolor import colored


def throw_error(error, color=None):
    """simple wrapper to universally throw errors"""
    if color is not None:
        error = colored(error, color)
    print(error)
    sys.exit(1)
