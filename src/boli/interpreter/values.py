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


class String(Value):

    def __init__(self, str_val):
        Value.__init__(self)
        self.value = str_val

    def __str__(self):
        return self.value


class List(Value):

    def __init__(self, items):
        Value.__init__(self)
        self.items = items

    def __str__(self):
        ret = "'(" + " ".join([str(item) for item in self.items]) + ")"


class Callable:

    def __init__(self, with_lazy_arg_eval=False):
        self.with_lazy_arg_eval = with_lazy_arg_eval

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class BuiltInFunc(Value, Callable):

    def __init__(self, func):
        Value.__init__(self)
        Callable.__init__(self)
        self._func = func

    def __call__(self, args):
        return self._func(args)


class BuiltInFuncLazy(Value, Callable):

    def __init__(self, func):
        Value.__init__(self)
        Callable.__init__(self, with_lazy_arg_eval=True)
        self._func = func

    def __call__(self, interpreter, args):
        return self._func(interpreter, args)


class Lambda(Value, Callable):

    def __init__(self, lambda_, interpreter):
        Value.__init__(self)
        Callable.__init__(self)
        self._lambda = lambda_
        self._interpreter = interpreter

    def __call__(self, args):
        func_interpreter = self._interpreter.new_child()
        func_env = func_interpreter.get_environment()
        # map parameters to arguments
        param_idx = 0
        for param in self._lambda.params:
            param_name = param.ident_tok.name
            func_env.insert(param_name, args[param_idx])
            param_idx += 1
        if self._lambda.var_param is not None:
            var_param_name = self._lambda.var_param.ident_tok.name
            func_env.insert(var_param_name, List(args[param_idx:]))

        ret = Nil()
        for elem in self._lambda.body:
            ret = elem.accept(func_interpreter)

        return ret
