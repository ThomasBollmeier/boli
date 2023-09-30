from boli.frontend.source import Source
from boli.frontend.parser import Parser
from boli.frontend.ast import BuiltInOperator, Identifier, Call
from boli.frontend.ast_visitor import AstVisitor
from boli.frontend.tokens import OP_TYPE_TO_STR
from boli.interpreter.environment import create_global_environment, Environment
from boli.interpreter.values import Callable, Value, Integer, Real, String, Bool, Nil, Lambda, List, TailCall, Symbol, \
    StructType
from boli.interpreter.builtin import is_truthy
from boli.interpreter.error import InterpreterError
from boli.interpreter.module_loader import ModuleLoader


class Interpreter(AstVisitor):

    def __init__(self, env=None):
        if env is None:
            self._cur_env = create_global_environment()
            ModuleLoader().load_file(self, "list")  # <-- load list functions
        else:
            self._cur_env = env

    def new_child(self):
        return Interpreter(Environment(self._cur_env))

    def get_environment(self):
        return self._cur_env

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
        name = ident.ident_tok.name
        value = self._cur_env.lookup(name)
        if value is None:
            raise InterpreterError(f"Identifier '{name}' is unknown")
        return value

    def visit_symbol(self, symbol):
        return Symbol(symbol.symbol_tok.name)

    def visit_keyword(self, keyword):
        pass

    def visit_struct(self, struct):
        name = struct.name_tok.name
        fields = [field.ident_tok.name for field in struct.fields]

        struct_type = StructType(name, fields)

        self._cur_env.insert(name, struct_type)
        self._cur_env.insert(f"create-{name}", struct_type.make_create())
        for field in fields:
            self._cur_env.insert(f"{name}-{field}", struct_type.make_getter(field))
            self._cur_env.insert(f"{name}-set-{field}!", struct_type.make_setter(field))

        return Nil()

    def visit_list(self, lst):
        return List([elem.accept(self) for elem in lst.elements])

    def visit_def(self, definition):
        name = definition.ident.ident_tok.name
        expr_value = definition.expr.accept(self)
        self._cur_env.insert(name, expr_value)
        return Nil()

    def visit_block(self, block):
        ret = Nil()
        block_interpreter = self.new_child()
        for expr in block.expressions:
            ret = expr.accept(block_interpreter)
        return ret

    def visit_if(self, if_expr):
        callable_ = self._cur_env.lookup("if")
        if not isinstance(callable_, Callable):
            raise InterpreterError("if is not callable")
        return callable_(self, [if_expr.condition,
                                if_expr.consequent,
                                if_expr.alternate])

    def visit_cond(self, cond):
        for branch in cond.branches:
            if is_truthy(branch.condition.accept(self)):
                return branch.expression.accept(self)
        return Nil()

    def visit_cond_branch(self, cond_branch):
        pass

    def visit_lambda(self, lambda_):
        return Lambda(lambda_, self)

    def visit_call(self, call):
        if call.is_tail_call:
            #  Tail call optimization:
            raise TailCall(self._arg_values(call.args))
        callee = call.callee
        callable_ = self._get_callable(callee)
        if not callable_.with_lazy_arg_eval:
            return callable_(self._arg_values(call.args))
        else:
            return callable_(self, call.args)

    def _arg_values(self, args):
        arg_vals = []
        for arg in args:
            arg_val = arg.accept(self)
            if isinstance(arg_val, list):
                arg_vals.extend(arg_val)
            else:
                arg_vals.append(arg_val)
        return arg_vals

    def visit_vararg(self, vararg):
        vararg_name = vararg.ident_tok.name
        vararg_value = self._cur_env.lookup(vararg_name)
        if vararg_value is None:
            raise InterpreterError(f"Identifier '{vararg_name}' is unknown")
        if not isinstance(vararg_value, List):
            raise InterpreterError("Vararg must be of list type")
        return [it for it in vararg_value.items]

    def visit_builtin_op(self, builtin_op):
        op = OP_TYPE_TO_STR[builtin_op.op_tok.token_type]
        return self._cur_env.lookup(op)

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
        elif isinstance(callee, Call):
            return callee.accept(self)
        else:
            raise NotImplementedError()

        ret = self._cur_env.lookup(key)
        if not isinstance(ret, Callable):
            raise InterpreterError("Expected callable function")

        return ret
