import json
import time
import uuid

from speedup.commands import Command
from speedup.utils import error_handling, process_helpers, progress_bar


class RunCommand(Command):
    def __init__(self, args):
        super(RunCommand, self).__init__(args)

    def action(self):
        """creates docker images
           if `--watch` is passed, continually will build on change
        """
        print('yay')

    def _build(self):
        if self.args['--verbose']:
            build_process = process_helpers.run_popen(build_cmd,
                                                      shell=True,
                                                      stdout=True,
                                                      stderr=True)
        else:
            build_process = process_helpers.run_popen(build_cmd,
                                                      shell=True)
            with process_helpers.prevent_deadlock(build_process):
                progress_bar.duration_progress(
                    'Building {}'.format(
                        self.config["name"]), last_build_duration,
                    lambda: build_process.poll() is not None)
        if build_process.poll() != 0:
            # When we have an error, get the stdout and error output
            # and display them both with the error output in red.
            output, error_msg = build_process.communicate()
            if output:
                print(output.decode("utf-8"))
            if error_msg:
                error_handling.throw_error(error_msg.decode("utf-8"), 'red')

        built_time = time.time()

        # Write last container to file
        with open('.build.json', 'w') as f:
            f.write(json.dumps({
                "last_container": container_name,
                "last_build_duration": built_time - started_build_time
            }))

        print("Built {}".format(container_name))

    def _watch_and_build(self):
        event_handler = EventHandler(self._build)
        observer = Observer()
        observer.schedule(event_handler, './', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            observer.stop()
        observer.join()
