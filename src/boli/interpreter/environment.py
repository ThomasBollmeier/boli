from boli.interpreter.builtin import *
from boli.interpreter.list_functions import *
from boli.interpreter.module_loader import require, provide
from boli.interpreter.string_functions import *


class Environment:

    def __init__(self, parent=None):
        self._parent = parent
        self._values = {}

    def is_toplevel(self):
        return self._parent is None

    def lookup(self, name):
        if name in self._values:
            return self._values[name][0]
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

    def insert(self, name, value, owned=True):
        self._values[name] = (value, owned)

    def get_exported_values(self):
        ret = {}
        for key, entry in self._values.items():
            value, owned = entry
            if owned:
                ret[key] = value
        return ret


class ModuleEnvironment(Environment):

    def __init__(self):
        Environment.__init__(self, parent=None)
        self._exports = []

    def add_export(self, name, export_alias=None):
        self._exports.append((name, export_alias))

    def get_exported_values(self):
        if self._exports:
            ret = {}
            for name, alias in self._exports:
                exported_name = alias if alias else name
                ret[exported_name] = self._values[name][0]
            return ret
        else:
            return Environment.get_exported_values(self)


def create_global_environment() -> Environment:
    
    ret = ModuleEnvironment()
    ret.insert("+", add, owned=False)
    ret.insert("-", sub, owned=False)
    ret.insert("*", mult, owned=False)
    ret.insert("/", div, owned=False)
    ret.insert("^", exp, owned=False)
    ret.insert("%", mod, owned=False)
    ret.insert("=", eq, owned=False)
    ret.insert(">", gt, owned=False)
    ret.insert(">=", ge, owned=False)
    ret.insert("<", lt, owned=False)
    ret.insert("<=", le, owned=False)
    ret.insert("and", and_, owned=False)
    ret.insert("or", or_, owned=False)
    ret.insert("not", not_, owned=False)
    ret.insert("if", if_, owned=False)
    ret.insert("write", write, owned=False)
    ret.insert("writeln", writeln, owned=False)
    ret.insert("set!", set_bang, owned=False)
    ret.insert("head", head, owned=False)
    ret.insert("tail", tail, owned=False)
    ret.insert("list-ref", list_ref, owned=False)
    ret.insert("list-set!", list_set_bang, owned=False)
    ret.insert("take", take, owned=False)
    ret.insert("take-while", take_while, owned=False)
    ret.insert("drop", drop, owned=False)
    ret.insert("drop-while", drop_while, owned=False)
    ret.insert("filter", filter_, owned=False)
    ret.insert("map", map_, owned=False)
    ret.insert("concat", concat, owned=False)
    ret.insert("count", count, owned=False)
    ret.insert("empty?", is_empty, owned=False)
    ret.insert("cons", cons, owned=False)
    ret.insert("lazy-list", lazy_list, owned=False)
    ret.insert("create-hash-table", create_hash_table, owned=False)
    ret.insert("hash-set!", hash_set_bang, owned=False)
    ret.insert("hash-remove!", hash_remove_bang, owned=False)
    ret.insert("hash-exists?", hash_exists, owned=False)
    ret.insert("hash-ref", hash_ref, owned=False)
    ret.insert("str-sub", str_sub, owned=False)
    ret.insert("str-replace", str_replace, owned=False)
    ret.insert("str-concat", str_concat, owned=False)
    ret.insert("str-upper", str_upper, owned=False)
    ret.insert("str-lower", str_lower, owned=False)
    ret.insert("require", require, owned=False)
    ret.insert("provide", provide, owned=False)

    return ret
