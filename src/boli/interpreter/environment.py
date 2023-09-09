from boli.interpreter.builtin import *


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


def create_global_environment() -> Environment:
    
    ret = Environment()
    ret.insert("+", add)
    ret.insert("-", sub)
    ret.insert("*", mult)
    ret.insert("/", div)
    ret.insert("^", exp)
    ret.insert("%", mod)
    ret.insert("=", eq)
    ret.insert(">", gt)
    ret.insert(">=", ge)
    ret.insert("<", lt)
    ret.insert("<=", le)
    ret.insert("and", and_)
    ret.insert("or", or_)
    ret.insert("not", not_)
    ret.insert("if", if_)

    return ret
