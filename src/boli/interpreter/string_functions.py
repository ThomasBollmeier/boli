from boli.interpreter.values import BuiltInFunc, String
from boli.interpreter.error import InterpreterError


@BuiltInFunc
def str_sub(args):
    num_args = len(args)
    if num_args == 2:
        s, idx = args
        return String(s.value[idx.value:])
    elif num_args == 3:
        s, idx, length = args
        return String(s.value[idx.value:idx.value+length.value])
    else:
        raise InterpreterError("str-sub expects two or three arguments")


@BuiltInFunc
def str_replace(args):
    s, old_string, new_string = args
    return String(s.value.replace(old_string.value, new_string.value))


@BuiltInFunc
def str_concat(args):
    new_str = ""
    for s in args:
        new_str += s.value
    return String(new_str)


@BuiltInFunc
def str_upper(args):
    return String(args[0].value.upper())


@BuiltInFunc
def str_lower(args):
    return String(args[0].value.lower())
