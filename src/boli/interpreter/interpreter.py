from boli.frontend.source import Source
from boli.frontend.parser import Parser
from boli.frontend.ast import *
from boli.frontend.ast_visitor import AstVisitor
from boli.frontend.tokens import *
from boli.interpreter.builtin import *
from boli.interpreter.environment import create_global_environment


class Interpreter(AstVisitor):

    def __init__(self):
        self._cur_env = create_global_environment()

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
        return String(string.str_tok.str_val)

    def visit_bool(self, boolean):
        return Bool(boolean.bool_tok.bool_val)

    def visit_nil(self, nil):
        return Nil()

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

    def visit_if(self, if_expr):
        callable_ = self._cur_env.lookup("if")
        if not isinstance(callable_, Callable):
            raise Exception("if is not callable")
        return callable_(self, [if_expr.condition,
                                if_expr.consequent,
                                if_expr.alternate])

    def visit_lambda(self, lambda_):
        pass

    def visit_call(self, call):
        callee = call.callee
        callable_ = self._get_callable(callee)
        if not callable_.with_lazy_arg_eval:
            arg_vals = [arg.accept(self) for arg in call.args]
            return callable_(arg_vals)
        else:
            return callable_(self, call.args)

    def visit_builtin_op(self, builtin_op):
        pass

    def visit_program(self, program):
        ret = Nil()
        for child in program.children:
            value = child.accept(self)
            if isinstance(value, Value):
                ret = value

        return ret

    def _get_callable(self, callee) -> Callable:
        if isinstance(callee, BuiltInOperator):
            key = OP_TYPE_TO_STR[callee.op_tok.token_type]
        elif isinstance(callee, Identifier):
            key = callee.ident_tok.name
        else:
            raise NotImplementedError()

        ret = self._cur_env.lookup(key)
        if not isinstance(ret, Callable):
            raise Exception("Expected callable function")

        return ret
