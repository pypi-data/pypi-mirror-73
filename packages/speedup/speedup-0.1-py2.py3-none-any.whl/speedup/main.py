#!/usr/bin/env python3

# SIDE EFFECTS
"""
A side-effect of cdef is that the function is no longer available from Python-space, as Python wouldn’t
know how to call it. It is also no longer possible to change f() at runtime.

Using the cpdef keyword instead of cdef, a Python wrapper is also created, so that the function is
available both from Cython (fast, passing typed values directly) and from Python (wrapping values in Python
objects). In fact, cpdef does not just provide a Python wrapper, it also installs logic to allow the method
to be overridden by python methods, even when called from within cython. This does add a tiny overhead
compared to cdef methods.

cdef functions cannot take *args and **kwargs type arguments. This is because they cannot easily be translated into a C signature.
"""

# SAMPLE CODE CALLING CYTHONIZE
"""
https://github.com/kivy/python-for-android/blob/e02541fff57960a51f2c8f76f0eafdf23e48d032/pythonforandroid/recipes/kivy/__init__.py
https://github.com/kivy/python-for-android/blob/e02541fff57960a51f2c8f76f0eafdf23e48d032/pythonforandroid/recipe.py#L1040
https://github.com/kivy/python-for-android/blob/e02541fff57960a51f2c8f76f0eafdf23e48d032/pythonforandroid/recipe.py#L1112
https://github.com/kivy/python-for-android/blob/e02541fff57960a51f2c8f76f0eafdf23e48d032/pythonforandroid/logger.py#L144
https://github.com/cjrh/easycython/blob/master/easycython/easycython.py#L10
https://lbolla.info/python-threads-cython-gil
"""

# DEBUG CYTHONIZATION
"""
Cython has a way to visualise where interaction with Python objects and Python’s C-API is taking place.
For this, pass the annotate=True parameter to cythonize(). It produces a HTML file.

https://cython.readthedocs.io/en/stable/src/userguide/debugging.html
"""

# PURE PYTHON
"""
PURE PYTHON MODE == 20-50% speedup only: https://cython.readthedocs.io/en/stable/src/tutorial/pure.html#pure-mode
Cython has support for compiling .py files, and accepting type annotations using decorators and other
valid Python syntax. This allows the same source to be interpreted as straight Python, or compiled for
optimized results.
"""

# TODO: support `with nogil`? O_o
# PARALELLISM
"""
https://cython.readthedocs.io/en/stable/src/userguide/parallelism.html
Cython supports native parallelism through the cython.parallel module. To use this kind of parallelism,
the GIL must be released (see Releasing the GIL). It currently supports OpenMP, but later on more
backends might be supported.

You can release the GIL around a section of code using the with nogil statement:

with nogil:
    <code to be executed with the GIL released>
Code in the body of the with-statement must not raise exceptions or manipulate Python objects in any
way, and must not call anything that manipulates Python objects without first re-acquiring the GIL.
Cython validates these operations at compile time, but cannot look into external C functions, for example.
They must be correctly declared as requiring or not requiring the GIL (see below) in order to make Cython’s
checks effective.

Acquiring the GIL
A C function that is to be used as a callback from C code that is executed without the GIL needs to acquire
the GIL before it can manipulate Python objects. This can be done by specifying with gil in the function
header:

cdef void my_callback(void *data) with gil:
    ...
If the callback may be called from another non-Python thread, care must be taken to initialize the GIL
first, through a call to PyEval_InitThreads(). If you’re already using cython.parallel in your module,
this will already have been taken care of.

The GIL may also be acquired through the with gil statement:

with gil:
    <execute this block with the GIL acquired>
"""
import argparse
import os

from speedup.commands import BuildCommand, RunCommand
from speedup.validators import file_or_dir_exists

# every available command and its corresponding action will go here
COMMAND_MAP = (
    ('build', BuildCommand),
    ('run', RunCommand)
)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "action",
        choices=[x[0] for x in COMMAND_MAP],
        help="Build an app, or run it with pipx")
    parser.add_argument(
        "--project-path",
        help="Path to Python code to be Cythonized. Defaults to SPEEDUP_PROJECT_PATH with a "
             "fallback to the `cwd`.",
        default=os.environ.get('SPEEDUP_PROJECT_PATH', '.'),
        type=file_or_dir_exists)
    parser.add_argument(
        "--indent-with",
        help="Amount of space to indent code with. Defaults to 2.",
        default=2,
        type=int)
    parser.add_argument(
        "--verbose",
        help="Adds verbosity to commands",
        action='store_true',
        default=False)

    # whether or not we'll dump output to stdout or to an output path
    output_type = parser.add_mutually_exclusive_group(required=True)
    output_type.add_argument(
        "--output-path",
        help="Dir where Cythonized `--project-path` code goes. Defaults to SPEEDUP_OUTPUT_PATH with a "
             "fallback to /tmp. Specify the same path as `--project-path` to overwrite existing code with "
             "the faster Cythonized version.",
        default=os.environ.get('SPEEDUP_OUTPUT_PATH', '/tmp/'),
        type=file_or_dir_exists)
    output_type.add_argument(
        "--stdout",
        help="Rather than writing to an output path, dump output to stdout instead",
        action='store_true',
        default=False)
    
    return parser.parse_args()


def run_command(args):
    """maps params into commands"""
    for command, CommandClass in COMMAND_MAP:
        if args.action == command:
            CommandClass(args).action()
            return


def main():
    try:
        run_command(get_args())
    # we want to allow SystemExit as we're intentionally catching those
    # via the error_handling module
    except Exception:
        print("You found a bug! Here's the traceback:")
        raise

