from boli.interpreter.error import InterpreterError


class Value:
    def __init__(self):
        pass


class Nil(Value):

    def __init__(self):
        Value.__init__(self)

    def __str__(self):
        return "nil"


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
        return '"' + self.value + '"'


class Symbol(Value):

    def __init__(self, symbol_name):
        Value.__init__(self)
        self.value = symbol_name

    def __str__(self):
        return f"'{self.value}"


class List(Value):

    def __init__(self, items):
        Value.__init__(self)
        self.items = items

    def __str__(self):
        return "'(" + " ".join([str(item) for item in self.items]) + ")"


class HashTable(Value):

    def __init__(self):
        Value.__init__(self)
        self.key_values = {}

    def set_bang(self, key, value):
        self.key_values[str(key)] = value
        return self

    def remove_bang(self, key):
        key_str = str(key)
        if key_str in self.key_values:
            del self.key_values[key_str]
        return self

    def exists(self, key):
        return Bool(str(key) in self.key_values)

    def ref(self, key):
        key_str = str(key)
        if key_str in self.key_values:
            return self.key_values[key_str]
        return Nil()

    def __str__(self):
        key_values_str = " ".join([f"{key} {value}" for key, value in self.key_values.items()])
        return f"(hash-table {key_values_str})"


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

    def __str__(self):
        return "<BuiltInFunction>"


class BuiltInFuncLazy(Value, Callable):

    def __init__(self, func):
        Value.__init__(self)
        Callable.__init__(self, with_lazy_arg_eval=True)
        self._func = func

    def __call__(self, interpreter, args):
        return self._func(interpreter, args)

    def __str__(self):
        return "<BuiltInFunction>"


class Lambda(Value, Callable):

    def __init__(self, lambda_, interpreter):
        Value.__init__(self)
        Callable.__init__(self)
        self._lambda = lambda_
        self._interpreter = interpreter

    def __call__(self, args):
        arguments = args
        while True:
            func_interpreter = self._init_func_interpreter(arguments)
            ret = Nil()
            try:
                for elem in self._lambda.body:
                    ret = elem.accept(func_interpreter)
                break
            except TailCall as tail_call:
                arguments = tail_call.args

        return ret

    def _init_func_interpreter(self, args):
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

        return func_interpreter

    def __str__(self):
        return "<LambdaFunction>"


class StructType(Value):

    def __init__(self, name, fields):
        Value.__init__(self)
        self.name = name
        self.fields = fields
        self.field_indices = dict(zip(fields, range(len(fields))))

    def __str__(self):
        return f"""(def-struct {self.name} ({" ".join(self.fields) }))"""

    def make_create(self):
        @BuiltInFunc
        def create(field_values):
            return Struct(self, field_values)
        return create

    def make_getter(self, field):
        @BuiltInFunc
        def getter(args):
            instance = args[0]
            field_idx = self.field_indices[field]
            return instance.field_values[field_idx]
        return getter

    def make_setter(self, field):
        @BuiltInFunc
        def setter(args):
            instance, field_value = args
            field_idx = self.field_indices[field]
            instance.field_values[field_idx] = field_value
            return Nil()
        return setter


class Struct(Value):

    def __init__(self, struct_type, field_values):
        Value.__init__(self)
        self.struct_type = struct_type
        if len(field_values) != len(self.struct_type.fields):
            raise InterpreterError("Numbers of values and fields do not match")
        self.field_values = field_values

    def __str__(self):
        values_str = " ".join([str(field_val) for field_val in self.field_values])
        return f"({self.struct_type.name} {values_str})"


class TailCall(InterpreterError):

    def __init__(self, args):
        self.args = args
