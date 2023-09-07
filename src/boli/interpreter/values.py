class Value:
    def __init__(self):
        pass


class Nil(Value):

    def __init__(self):
        Value.__init__(self)


class Number:
    pass


class Integer(Value, Number):

    def __init__(self, int_val):
        Value.__init__(self)
        Number.__init__(self)
        self.value = int_val

    def __str__(self):
        return f"{self.value}"


class Real(Value, Number):

    def __init__(self, real_val):
        Value.__init__(self)
        Number.__init__(self)
        self.value = real_val

    def __str__(self):
        return f"{self.value}".replace(".", ",")


class Bool(Value):

    def __init__(self, bool_val):
        Value.__init__(self)
        self.value = bool_val

    def __str__(self):
        return "#t" if self.value else "#f"


class BuiltInFunc(Value):

    def __init__(self, func):
        Value.__init__(self)
        self._func = func

    def __call__(self, args):
        return self._func(args)
