class AstVisitor:

    def visit_int(self, integer):
        pass

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

    def visit_abs_name(self, abs_name):
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

    def visit_block(self, block):
        pass

    def visit_if(self, if_):
        pass

    def visit_lambda(self, lambda_):
        pass

    def visit_call(self, call):
        pass

    def visit_vararg(self, vararg):
        pass

    def visit_builtin_op(self, builtin_op):
        pass

    def visit_program(self, program):
        pass
