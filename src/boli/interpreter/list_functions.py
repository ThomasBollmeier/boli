from boli.interpreter.values import BuiltInFunc, List, Bool, Nil
from boli.interpreter.error import InterpreterError


@BuiltInFunc
def head(args):
    return args[0].items[0]


@BuiltInFunc
def tail(args):
    return List(args[0].items[1:])


@BuiltInFunc
def list_ref(args):
    lst, idx = args
    return lst.items[idx.value]


@BuiltInFunc
def list_set_bang(args):
    lst, idx, new_item = args
    lst.items[idx.value] = new_item
    return Nil()


@BuiltInFunc
def concat(args):
    total_list = []
    for lst in args:
        total_list.extend(lst.items)
    return List(total_list)


@BuiltInFunc
def cons(args):
    item, lst = args
    return List([item] + lst.items)
