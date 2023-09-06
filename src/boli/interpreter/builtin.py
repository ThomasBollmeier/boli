from boli.interpreter.values import *


@Func
def add(args):
    return _apply(args, lambda a, b: a + b)


@Func
def sub(args):
    return _apply(args, lambda a, b: a - b)


@Func
def mult(args):
    return _apply(args, lambda a, b: a * b)


@Func
def div(args):
    return _apply(args, lambda a, b: a / b)


def _apply(args, bin_fn):
    ret = Nil()
    for arg in args:
        if not isinstance(arg, Integer):
            raise Exception("Invalid argument type")
        if isinstance(ret, Nil):
            ret = arg
        else:
            ret = Integer(bin_fn(ret.int_val, arg.int_val))

    return ret

