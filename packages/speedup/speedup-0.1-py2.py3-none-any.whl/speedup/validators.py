"""
Place for Argparse custom validation
"""
import os
from argparse import ArgumentTypeError

def file_or_dir_exists(string):
    if not os.path.exists(string):
        raise ArgumentTypeError(f"{string} is not a valid path!")
    return string
