from boli.interpreter.values import *
from boli.frontend.ast import Identifier


@BuiltInFunc
def add(args):
    def _add(a, b):
        if isinstance(a, Integer) and isinstance(b, Integer):
            return Integer(a.value + b.value)
        else:
            return Real(a.value + b.value)
    return _apply(args, _add)


@BuiltInFunc
def sub(args):
    def _sub(a, b):
        if isinstance(a, Integer) and isinstance(b, Integer):
            return Integer(a.value - b.value)
        else:
            return Real(a.value - b.value)
    return _apply(args, _sub)


@BuiltInFunc
def mult(args):
    def _mult(a, b):
        if isinstance(a, Integer) and isinstance(b, Integer):
            return Integer(a.value * b.value)
        else:
            return Real(a.value * b.value)
    return _apply(args, _mult)


@BuiltInFunc
def div(args):
    def _div(a, b):
        if isinstance(a, Integer) and isinstance(b, Integer):
            return Integer(a.value // b.value)
        else:
            return Real(a.value / b.value)
    return _apply(args, _div)


@BuiltInFunc
def exp(args):
    def _exp(a, b):
        if isinstance(a, Integer) and isinstance(b, Integer):
            return Integer(a.value ** b.value)
        else:
            return Real(a.value ** b.value)
    return _apply(args, _exp, left_associative=False)


@BuiltInFunc
def mod(args):
    def _mod(a, b):
        if isinstance(a, Integer) and isinstance(b, Integer):
            return Integer(a.value % b.value)
        else:
            raise Exception("Modulo operator requires integer operands")
    return _apply(args, _mod)


@BuiltInFunc
def eq(args):
    return _compare(args, lambda a, b: a == b)


@BuiltInFunc
def gt(args):
    return _compare(args, lambda a, b: a > b)


@BuiltInFunc
def ge(args):
    return _compare(args, lambda a, b: a >= b)


@BuiltInFunc
def lt(args):
    return _compare(args, lambda a, b: a < b)


@BuiltInFunc
def le(args):
    return _compare(args, lambda a, b: a <= b)


@BuiltInFuncLazy
def and_(interpreter, args):
    ret = Bool(True)
    for arg in args:
        arg_val = arg.accept(interpreter)
        if is_truthy(arg_val):
            ret = arg_val
        else:
            return Bool(False)
    return ret


@BuiltInFuncLazy
def or_(interpreter, args):
    for arg in args:
        arg_val = arg.accept(interpreter)
        if is_truthy(arg_val):
            return arg_val
    return Bool(False) and args or Bool(True)


@BuiltInFunc
def not_(args):
    if len(args) != 1:
        raise Exception("not expects a single argument")
    return Bool(not is_truthy(args[0]))


@BuiltInFuncLazy
def if_(interpreter, args):
    condition, consequent, alternate = args
    cond_val = condition.accept(interpreter)
    if is_truthy(cond_val):
        return consequent.accept(interpreter)
    else:
        return alternate.accept(interpreter)


@BuiltInFunc
def write(args):
    for arg in args:
        print(str(arg), end=" ")
    return Nil()


@BuiltInFunc
def writeln(args):
    for arg in args:
        print(str(arg), end=" ")
    print()
    return Nil()


@BuiltInFuncLazy
def set_bang(interpreter, args):
    if len(args) != 2:
        raise Exception("function set! expects two arguments")
    if not isinstance(args[0], Identifier):
        raise Exception("set!: first argument must be identifier")
    name = args[0].ident_tok.name
    env = interpreter.get_environment()
    def_env = env.lookup_defining_env(name)
    if def_env is None:
        raise Exception(f"identifier {name} is unknown")
    value = args[1].accept(interpreter)
    def_env.insert(name, value)
    return Nil()


@BuiltInFunc
def count(args):
    container_type = args[0]
    if isinstance(container_type, List):
        return Integer(len(container_type.items))
    elif isinstance(container_type, HashTable):
        return Integer(len(container_type.key_values))
    else:
        raise Exception("Unsupported type for 'count'")


@BuiltInFunc
def is_empty(args):
    container_type = args[0]
    if isinstance(container_type, List):
        return Bool(len(container_type.items) == 0)
    elif isinstance(container_type, HashTable):
        return Bool(len(container_type.key_values) == 0)
    else:
        raise Exception("Unsupported type for 'empty?'")


@BuiltInFunc
def create_hash_table(args):
    ret = HashTable()
    if len(args) % 2 != 0:
        raise Exception("#keys and #values do not match")
    for i, arg in enumerate(args):
        if i % 2 == 0:
            if not isinstance(arg, Symbol) and not isinstance(arg, String):
                raise Exception("Only symbols or strings are supported as hash keys")
            key = arg
        else:
            ret.set_bang(key, arg)
    return ret


@BuiltInFunc
def hash_set_bang(args):
    hash_table, key, value = args
    if not isinstance(key, Symbol) and not isinstance(key, String):
        raise Exception("Only symbols or strings are supported as hash keys")
    return hash_table.set_bang(key, value)


@BuiltInFunc
def hash_remove_bang(args):
    hash_table, key = args
    if not isinstance(key, Symbol) and not isinstance(key, String):
        raise Exception("Only symbols or strings are supported as hash keys")
    return hash_table.remove_bang(key)


@BuiltInFunc
def hash_exists(args):
    hash_table, key = args
    return hash_table.exists(key)


@BuiltInFunc
def hash_ref(args):
    hash_table, key = args
    return hash_table.ref(key)


def is_truthy(value):
    if isinstance(value, Bool):
        return value.value
    if isinstance(value, Nil):
        return False
    return True


def _apply(args, bin_fn, left_associative=True):
    ret = Nil()
    if left_associative:
        for arg in args:
            if not isinstance(arg, Number):
                raise Exception("Invalid argument type")
            if isinstance(ret, Nil):
                ret = arg
            else:
                ret = bin_fn(ret, arg)
    else:
        args_rev = reversed(args)
        for arg in args_rev:
            if not isinstance(arg, Number):
                raise Exception("Invalid argument type")
            if isinstance(ret, Nil):
                ret = arg
            else:
                ret = bin_fn(arg, ret)

    return ret


def _compare(args, fn):
    if len(args) < 2:
        raise Exception("Comparisons require at least two arguments")

    prev = None
    for arg in args:
        if not isinstance(arg, Number):
            raise Exception("Invalid argument type")
        if prev is not None and not fn(prev, arg.value):
            return Bool(False)
        prev = arg.value

    return Bool(True)
