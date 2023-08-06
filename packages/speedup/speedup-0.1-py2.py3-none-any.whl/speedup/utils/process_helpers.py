import os
from contextlib import contextmanager
from subprocess import check_output, CalledProcessError, Popen, PIPE
from speedup.utils import error_handling


def run(command, cwd=None, raise_on_failure=False):
    """wrapper around check_output"""
    try:
        output = check_output(command, cwd=cwd).decode("utf-8")
    except CalledProcessError as e:
        if raise_on_failure:
            raise e
        error_handling.throw_error(e.output, 'red')

    return output


def run_popen(command, shell=False, stdout=PIPE, stderr=PIPE, cwd=None,
              preexec_fn=None):
    """to suppress output, pass False to stdout or stderr
       None is a valid option that we want to allow"""
    with open(os.devnull, 'w') as quiet:
        stdout = quiet if stdout is False else stdout
        stderr = quiet if stderr is False else stderr
        if not (isinstance(command, str) or isinstance(command, list)):
            error_handling.throw_error(
                "The following command is invalid:\n{}".format(command))
        try:
            return Popen(command, stdout=stdout, stderr=stderr, shell=shell,
                         cwd=cwd, preexec_fn=preexec_fn)
        except CalledProcessError as e:
            error_handling.throw_error(e.output, 'red')


@contextmanager
def prevent_deadlock(proc):
    """function designed to read from a process' pipe and prevent deadlock
       Useful for when we can't use `.communicate()` and need a `.wait()` with
       also using PIPEs.
       We won't actually do anything with the output here.
    """
    yield
    for line in iter(proc.stdout.readline, b''):
        pass


# if self.args['--verbose']:
#     self.push_process = process_helpers.run_popen(
#         push_cmd, stdout=True, stderr=True)
#     self.push_process.wait()
#     # add newline to separate push output from container deploy output
#     print('')
# else:
#     self.push_process = process_helpers.run_popen(push_cmd)

def _poll_docker_proc(self):
    """used only in the case of non-verbose deploy mode to dump loading
       bar and any error that happened
    """
    last_push_duration = files.fetch_action_arg(
        'push', 'last_push_duration')
    with process_helpers.prevent_deadlock(self.push_process):
        progress_bar.duration_progress(
            'Pushing {}'.format(self.config["name"]), last_push_duration,
            lambda: self.push_process.poll() is not None)

    # If the push fails, get stdout/stderr messages and display them
    # to the user, with the error message in red.
    if self.push_process.poll() != 0:
        push_stdout, push_error = self.push_process.communicate()
        print(push_stdout.decode("utf-8"))
        error_handling.throw_error(push_error.decode("utf-8"), 'red')
