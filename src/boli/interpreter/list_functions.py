from boli.interpreter.values import BuiltInFunc, List, Bool


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
            raise Exception("Boolean result expected")
        if result.value:
            new_items.append(item)
    return List(new_items)
