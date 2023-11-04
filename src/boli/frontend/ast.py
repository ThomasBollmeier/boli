class Ast:

    def __init__(self):
        pass

    def accept(self, visitor):
        return None


class Integer(Ast):

    def __init__(self, int_tok):
        Ast.__init__(self)
        self.int_tok = int_tok

    def accept(self, visitor):
        return visitor.visit_int(self)


class Real(Ast):

    def __init__(self, real_tok):
        Ast.__init__(self)
        self.real_tok = real_tok

    def accept(self, visitor):
        return visitor.visit_real(self)


class String(Ast):

    def __init__(self, str_tok):
        Ast.__init__(self)
        self.str_tok = str_tok

    def accept(self, visitor):
        return visitor.visit_string(self)


class Bool(Ast):

    def __init__(self, bool_tok):
        Ast.__init__(self)
        self.bool_tok = bool_tok

    def accept(self, visitor):
        return visitor.visit_bool(self)


class Nil(Ast):

    def __init__(self, nil_tok=None):
        Ast.__init__(self)
        self.nil_tok = nil_tok

    def accept(self, visitor):
        return visitor.visit_nil(self)


class Identifier(Ast):

    def __init__(self, ident_tok):
        Ast.__init__(self)
        self.ident_tok = ident_tok

    def accept(self, visitor):
        return visitor.visit_ident(self)

    def __str__(self):
        return self.ident_tok.name


class AbsoluteName(Ast):

    def __init__(self, module_path, ident_tok):
        Ast.__init__(self)
        self.module_path = module_path
        self.ident_tok = ident_tok

    def accept(self, visitor):
        return visitor.visit_abs_name(self)

    def __str__(self):
        segments = [m.name for m in self.module_path]
        segments.append(self.ident_tok.name)
        return "::".join(segments)


class Symbol(Ast):

    def __init__(self, symbol_tok):
        Ast.__init__(self)
        self.symbol_tok = symbol_tok

    def accept(self, visitor):
        return visitor.visit_symbol(self)


class Keyword(Ast):

    def __init__(self, keyword_tok):
        Ast.__init__(self)
        self.keyword_tok = keyword_tok

    def accept(self, visitor):
        return visitor.visit_keyword(self)


class List(Ast):

    def __init__(self, elements):
        Ast.__init__(self)
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_list(self)


class Struct(Ast):

    def __init__(self, name_tok, fields):
        Ast.__init__(self)
        self.name_tok = name_tok
        self.fields = fields

    def accept(self, visitor):
        return visitor.visit_struct(self)


class Definition(Ast):

    def __init__(self, ident, expr):
        Ast.__init__(self)
        self.ident = ident
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_def(self)


class Block(Ast):

    def __init__(self, expressions):
        Ast.__init__(self)
        self.expressions = expressions

    def accept(self, visitor):
        return visitor.visit_block(self)


class If(Ast):

    def __init__(self, condition, consequent, alternate):
        Ast.__init__(self)
        self.condition = condition
        self.consequent = consequent
        self.alternate = alternate

    def accept(self, visitor):
        return visitor.visit_if(self)


class Lambda(Ast):

    def __init__(self, body, params, var_param=None):
        Ast.__init__(self)
        self.body = body
        self.params = params
        self.var_param = var_param

    def accept(self, visitor):
        return visitor.visit_lambda(self)


class Call(Ast):

    def __init__(self, callee, args):
        Ast.__init__(self)
        self.callee = callee
        self.args = args
        self.is_tail_call = False

    def accept(self, visitor):
        return visitor.visit_call(self)


class VarArg(Ast):

    def __init__(self, expr):
        Ast.__init__(self)
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_vararg(self)


class BuiltInOperator(Ast):

    def __init__(self, operator_tok):
        Ast.__init__(self)
        self.op_tok = operator_tok

    def accept(self, visitor):
        return visitor.visit_builtin_op(self)


class Program(Ast):

    def __init__(self, children):
        Ast.__init__(self)
        self.children = children

    def accept(self, visitor):
        return visitor.visit_program(self)
