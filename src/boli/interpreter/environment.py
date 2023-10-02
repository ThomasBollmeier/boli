from boli.interpreter.builtin import *
from boli.interpreter.list_functions import *
from boli.interpreter.string_functions import *


class Environment:

    def __init__(self, parent=None):
        self._parent = parent
        self._values = {}

    def lookup(self, name):
        if name in self._values:
            return self._values[name]
        elif self._parent:
            return self._parent.lookup(name)
        return None

    def lookup_defining_env(self, name):
        if name in self._values:
            return self
        elif self._parent:
            return self._parent.lookup_defining_env(name)
        else:
            return None

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
    ret.insert("write", write)
    ret.insert("writeln", writeln)
    ret.insert("set!", set_bang)
    ret.insert("head", head)
    ret.insert("tail", tail)
    ret.insert("list-ref", list_ref)
    ret.insert("list-set!", list_set_bang)
    ret.insert("concat", concat)
    ret.insert("count", count)
    ret.insert("empty?", is_empty)
    ret.insert("cons", cons)
    ret.insert("create-hash-table", create_hash_table)
    ret.insert("hash-set!", hash_set_bang)
    ret.insert("hash-remove!", hash_remove_bang)
    ret.insert("hash-exists?", hash_exists)
    ret.insert("hash-ref", hash_ref)
    ret.insert("str-sub", str_sub)
    ret.insert("str-replace", str_replace)
    ret.insert("str-concat", str_concat)
    ret.insert("str-upper", str_upper)
    ret.insert("str-lower", str_lower)

    return ret
