from boli.frontend.source import Source
from boli.frontend.parser import Parser
from boli.frontend.ast import *
from boli.frontend.ast_visitor import AstVisitor
from boli.interpreter.builtin import *
from boli.frontend.tokens import *


class Environment:

    def __init__(self, parent=None):
        self._parent = parent
        self._values = {}

    def lookup(self, name) -> Value:
        if name in self._values:
            return self._values[name]
        elif self._parent:
            return self._parent.lookup(name)
        return Nil()

    def insert(self, name, value):
        self._values[name] = value


class Interpreter(AstVisitor):

    def __init__(self):
        self._global = Environment()
        self._global.insert("+", add)
        self._global.insert("-", sub)
        self._global.insert("*", mult)
        self._global.insert("/", div)
        self._global.insert("^", exp)
        self._global.insert("%", mod)
        self._global.insert("=", eq)
        self._global.insert(">", gt)
        self._global.insert(">=", ge)
        self._global.insert("<", lt)
        self._global.insert("<=", le)

        self._cur_env = self._global

    def eval_program(self, code) -> Value:
        parser = Parser(Source(code))
        ast = parser.program()
        return ast.accept(self)

    def eval_expr(self, code) -> Value:
        parser = Parser(Source(code))
        ast = parser.expression()
        return ast.accept(self)

    def visit_int(self, integer) -> Value:
        return Integer(integer.int_tok.value)

    def visit_real(self, real):
        return Real(real.real_tok.value)

    def visit_string(self, string):
        pass

    def visit_bool(self, boolean):
        return Bool(boolean.bool_tok.bool_val)

    def visit_nil(self, nil):
        pass

    def visit_ident(self, ident):
        pass

    def visit_symbol(self, symbol):
        pass

    def visit_keyword(self, keyword):
        pass

    def visit_struct(self, struct):
        pass

    def visit_list(self, lst):
        pass

    def visit_def(self, definition):
        pass

    def visit_if(self, if_):
        pass

    def visit_lambda(self, lambda_):
        pass

    def visit_call(self, call):
        callee = call.callee

        if isinstance(callee, BuiltInOperator):
            op = OP_TYPE_TO_STR[callee.op_tok.token_type]
            func = self._cur_env.lookup(op)
            if not isinstance(func, BuiltInFunc):
                raise Exception("Expected function")
            arg_vals = [arg.accept(self) for arg in call.args]
            return func(arg_vals)
        else:
            return Nil()

    def visit_builtin_op(self, builtin_op):
        pass

    def visit_program(self, program):
        ret = Nil()
        for child in program.children:
            value = child.accept(self)
            if isinstance(value, Value):
                ret = value

        return ret
