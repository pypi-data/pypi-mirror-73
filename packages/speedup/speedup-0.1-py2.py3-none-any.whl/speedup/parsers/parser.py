import ast
from astor import code_gen

class Parser(code_gen.SourceGenerator):
    """
    Inspired by astor's code_gen module, iterates over an AST to generate new Cython source code
    NOTE: astor uses single quotes rather than double quotes
    """

    def visit_ClassDef(self, node):
        """
        classes should have a cdef in front of their declaration if possible
        """
        # import epdb; epdb.set_trace()
        self.decorators(node, 2)
        # write out only the first line of the class
        self.write("cdef " + code_gen.to_source(node).partition('\n')[0])
        self.body(node.body)
        if not self.indentation:
            self.newline(extra=2)

    def visit_FunctionDef(self, node):
        # import epdb; epdb.set_trace()
        # self.statement(node, '%sdef %s' % (prefix, node.name), '(')
        # TODO: handle function args
        # self.visit_arguments(node.args)
        # self.write(')')
        # self.conditional_write(' -> ', self.get_returns(node))
        # self.write(':')
        # self.body(node.body)
        self.decorators(node, 1 if self.indentation else 2)
        self.statement(node, "cdef" + code_gen.to_source(node)[3:].partition('\n')[0])
        self.body(node.body)
        if not self.indentation:
            self.newline(extra=2)
