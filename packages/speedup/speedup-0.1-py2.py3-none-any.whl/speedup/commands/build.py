import ast
import importlib
from pathlib import Path

from speedup.commands import Command
from speedup.parsers import Parser
from speedup.utils import error_handling, process_helpers, progress_bar

# from IPython import embed; embed()
# import epdb; epdb.set_trace()


class BuildCommand(Command):
    def __init__(self, args):
        super(BuildCommand, self).__init__(args)

    def action(self):
        """
        Builds a new Cythonized app for the `--project-path` in the `--output-dir`
        """
        project_path = Path(self.args.project_path)
        if project_path.is_dir():
            for path in project_path.rglob("*.py"):
                self._process_file(path)
        else:
            self._process_file(self.args.project_path)
            

    def _process_file(self, filename):
        """
        Generates an AST of the 'filename' FIX
        """
        with open(filename, 'r') as f:
            node = ast.parse(f.read(), filename=filename)
            result = "".join(self._transpile(node))

        if self.args.stdout:
            print(result)

    def _transpile(self, node):
        """
        Recursive function that calls a parser if available to handle transpilation logic FIX
        """
        parser = Parser(indent_with=' ' * self.args.indent_with)
        parser.visit(node)
        return parser.result
