class Ast:

    def __init__(self):
        pass


class Integer(Ast):

    def __init__(self, int_tok):
        Ast.__init__(self)
        self.int_tok = int_tok


class Real(Ast):

    def __init__(self, real_tok):
        Ast.__init__(self)
        self.real_tok = real_tok


class String(Ast):

    def __init__(self, str_tok):
        Ast.__init__(self)
        self.str_tok = str_tok


class Identifier(Ast):

    def __init__(self, ident_tok):
        Ast.__init__(self)
        self.ident_tok = ident_tok


class List(Ast):

    def __init__(self, elements):
        Ast.__init__(self)
        self.elements = elements


class Definition(Ast):

    def __init__(self, ident_tok, expr):
        Ast.__init__(self)
        self.ident_tok = ident_tok
        self.expr = expr


class If(Ast):

    def __init__(self, condition, consequent, alternate):
        Ast.__init__(self)
        self.condition = condition
        self.consequent = consequent
        self.alternate = alternate


class Call(Ast):

    def __init__(self, callee, args):
        Ast.__init__(self)
        self.callee = callee
        self.args = args


class Program(Ast):

    def __init__(self, children):
        Ast.__init__(self)
        self.children = children
