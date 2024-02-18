from boli.interpreter.values import BuiltInFunc, List, LazyList, ListIter, Nil, NaturalNumberIter
from boli.interpreter.error import InterpreterError


@BuiltInFunc
def list_(args):
    return List(args)


@BuiltInFunc
def head(args):
    lst = args[0]
    if isinstance(lst, List):
        return args[0].items[0]
    elif isinstance(lst, LazyList):
        return lst.take(1).items[0]


@BuiltInFunc
def tail(args):
    lst = args[0]
    if isinstance(lst, List):
        return List(args[0].items[1:])
    elif isinstance(lst, LazyList):
        return lst.drop(1)


@BuiltInFunc
def list_ref(args):
    lst, idx = args
    return lst.items[idx.value] if 0 <= idx.value < len(lst.items) else Nil()


@BuiltInFunc
def list_set_bang(args):
    lst, idx, new_item = args
    if 0 <= idx.value < len(lst.items):
        lst.items[idx.value] = new_item
    return Nil()


@BuiltInFunc
def take(args):
    num, lst = args
    n = num.value
    if isinstance(lst, List):
        return List(lst.items[:n])
    elif isinstance(lst, LazyList):
        return lst.take(n)
    else:
        raise InterpreterError("take can only be used with (Lazy)Lists")


@BuiltInFunc
def take_while(args):
    fn, lst = args
    if isinstance(lst, List):
        items = []
        for it in lst.items:
            if not fn([it]).value:
                break
            items.append(it)
        return List(items)
    elif isinstance(lst, LazyList):
        return lst.take_while(fn)
    else:
        raise InterpreterError("take-while can only be used with (Lazy)Lists")


@BuiltInFunc
def drop(args):
    num, lst = args
    n = num.value
    if isinstance(lst, List):
        return List(lst.items[n:])
    elif isinstance(lst, LazyList):
        return lst.drop(n)
    else:
        raise InterpreterError("drop can only be used with (Lazy)Lists")


@BuiltInFunc
def drop_while(args):
    fn, lst = args
    if isinstance(lst, List):
        idx = 0
        for it in lst.items:
            if not fn([it]).value:
                break
            idx += 1
        return List(lst.items[idx:])
    elif isinstance(lst, LazyList):
        return lst.drop_while(fn)
    else:
        raise InterpreterError("drop-while can only be used with (Lazy)Lists")


@BuiltInFunc
def filter_(args):
    predicate, lst = args
    if isinstance(lst, List):
        filtered = [it for it in lst.items if predicate([it]).value]
        return List(filtered)
    elif isinstance(lst, LazyList):
        return lst.filter(predicate)
    else:
        raise InterpreterError("filter can only be used with (Lazy)Lists")


@BuiltInFunc
def map_(args):
    fn, lst = args
    if isinstance(lst, List):
        return List([fn([it]) for it in lst.items])
    elif isinstance(lst, LazyList):
        return lst.map(fn)
    else:
        raise InterpreterError("map can only be used with (Lazy)Lists")


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


@BuiltInFunc
def lazy_list(args):
    return LazyList(ListIter(args))


@BuiltInFunc
def naturals(args):
    start = 0 if not args else args[0].value
    return LazyList(NaturalNumberIter(start))

