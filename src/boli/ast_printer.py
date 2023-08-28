from boli.ast_visitor import AstVisitor
from boli.tokens import OPERATORS, TOKENS_1


class AstPrinter(AstVisitor):

    def __init__(self):
        AstVisitor.__init__(self)
        self._indent = 0

    def visit_int(self, integer):
        self._write(f"Int({integer.int_tok.value})")

    def visit_real(self, real):
        self._write(f"Real({real.real_tok.value})")

    def visit_string(self, string):
        self._write(f"String({string.str_tok.str_val})")

    def visit_bool(self, boolean):
        self._write(f"Bool({boolean.bool_tok.bool_val})")

    def visit_ident(self, ident):
        self._write(f"Identifier({ident.ident_tok.name})")

    def visit_list(self, lst):
        self._write("List:")
        self._indent += 1
        for el in lst.elements:
            el.accept(self)
        self._indent -= 1

    def visit_def(self, definition):
        self._write("Definition:")
        self._indent += 1
        definition.ident.accept(self)
        definition.expr.accept(self)
        self._indent -= 1

    def visit_if(self, if_):
        raise NotImplementedError()

    def visit_call(self, call):
        self._write("Call:")
        self._indent += 1
        call.callee.accept(self)
        self._indent += 1
        for arg in call.args:
            arg.accept(self)
        self._indent -= 1
        self._indent -= 1

    def visit_builtin_op(self, builtin_op):
        operator = ""
        for op, token_type in TOKENS_1.items():
            if token_type == builtin_op.op_tok.token_type:
                operator = op
                break
        self._write(f"BuiltinOp({operator})")

    def visit_program(self, program):
        self._write("Program:")
        self._indent += 1
        for child in program.children:
            child.accept(self)
        self._indent-=1

    def _write(self, text):
        print(self._indent * "  " + text)
