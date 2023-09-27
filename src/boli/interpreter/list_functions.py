from boli.interpreter.values import BuiltInFunc, List, Bool, Nil
from boli.interpreter.error import InterpreterError


@BuiltInFunc
def head(args):
    return args[0].items[0]


@BuiltInFunc
def tail(args):
    return List(args[0].items[1:])


@BuiltInFunc
def take(args):
    return List(args[1].items[:args[0].value])


@BuiltInFunc
def drop(args):
    return List(args[1].items[args[0].value:])


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
    lst_a, lst_b = args
    return List(lst_a.items + lst_b.items)


@BuiltInFunc
def cons(args):
    item, lst = args
    return List([item] + lst.items)


@BuiltInFunc
def map_(args):
    lambda_, lst = args
    new_items = []
    for item in lst.items:
        new_items.append(lambda_([item]))
    return List(new_items)


@BuiltInFunc
def filter_(args):
    lambda_, lst = args
    new_items = []
    for item in lst.items:
        result = lambda_([item])
        if not isinstance(result, Bool):
            raise InterpreterError("Boolean result expected")
        if result.value:
            new_items.append(item)
    return List(new_items)
