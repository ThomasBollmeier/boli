from boli.frontend.ast_visitor import AstVisitor
from boli.frontend.tokens import TokenType, TOKENS_1


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

    def visit_nil(self, nil):
        self._write("nil")

    def visit_ident(self, ident):
        self._write(f"Identifier({ident.ident_tok.name})")

    def visit_symbol(self, symbol):
        self._write(f"Symbol({symbol.symbol_tok.name})")

    def visit_keyword(self, keyword):
        token_type = keyword.keyword_tok.token_type
        if token_type == TokenType.DEF:
            self._write("Def-Keyword")
        elif token_type == TokenType.IF:
            self._write("If-Keyword")
        elif token_type == TokenType.LAMBDA:
            self._write("Lambda-Keyword")
        elif token_type == TokenType.DEF_STRUCT:
            self._write("Def-Struct-Keyword")

    def visit_struct(self, struct):
        self._write(f"StructDefinition({struct.name_tok.name}):")
        self._indent += 1
        for field in struct.fields:
            field.accept(self)
        self._indent -= 1

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

    def visit_block(self, block):
        self._write("Block:")
        self._indent += 1
        for expr in block.expressions:
            expr.accept(self)
        self._indent -= 1

    def visit_if(self, if_):
        self._write("IfExpression:")
        self._indent += 1
        if_.condition.accept(self)
        if_.consequent.accept(self)
        if_.alternate.accept(self)
        self._indent -= 1

    def visit_cond(self, cond):
        self._write("CondExpression:")
        self._indent += 1
        for branch in cond.branches:
            branch.accept(self)
        self._indent -= 1

    def visit_cond_branch(self, cond_branch):
        self._write("CondBranch:")
        self._indent += 1
        cond_branch.condition.accept(self)
        cond_branch.expression.accept(self)
        self._indent -= 1

    def visit_lambda(self, lambda_):
        self._write("Lambda:")
        self._indent += 1
        self._write("Parameters:")
        self._indent += 1
        for param in lambda_.params:
            self._write(param.ident_tok.name)
        if lambda_.var_param:
            self._write(f"{lambda_.var_param.ident_tok.name} (VarParam)")
        self._indent -= 1
        self._write("Body:")
        self._indent += 1
        for expr in lambda_.body:
            expr.accept(self)
        self._indent -= 1
        self._indent -= 1

    def visit_call(self, call):
        if not call.is_tail_call:
            self._write("Call:")
        else:
            self._write("TailCall:")
        self._indent += 1
        call.callee.accept(self)
        self._indent += 1
        for arg in call.args:
            arg.accept(self)
        self._indent -= 1
        self._indent -= 1

    def visit_vararg(self, vararg):
        self._write(f"VarArg({vararg.ident_tok.name})")

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
