from boli.interpreter.values import *


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
    return _apply(args, _exp)


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


def _apply(args, bin_fn):
    ret = Nil()
    for arg in args:
        if not isinstance(arg, Number):
            raise Exception("Invalid argument type")
        if isinstance(ret, Nil):
            ret = arg
        else:
            ret = bin_fn(ret, arg)

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
