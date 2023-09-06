class Value:
    def __init__(self):
        pass


class Nil(Value):

    def __init__(self):
        Value.__init__(self)


class Integer(Value):

    def __init__(self, int_val):
        Value.__init__(self)
        self.int_val = int_val

    def __str__(self):
        return f"{self.int_val}"


class Func(Value):

    def __init__(self, func):
        Value.__init__(self)
        self._func = func

    def __call__(self, args):
        return self._func(args)
