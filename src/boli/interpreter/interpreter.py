from boli.source import Source
from boli.parser import Parser
from boli.ast import *
from boli.ast_visitor import AstVisitor
# from boli.interpreter.values import *
from boli.interpreter.builtin import *
from boli.tokens import *


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
        pass

    def visit_string(self, string):
        pass

    def visit_bool(self, boolean):
        pass

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
            op = TOKEN_TYPE_TO_CHAR_1[callee.op_tok.token_type]
            func = self._cur_env.lookup(op)
            if not isinstance(func, Func):
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
