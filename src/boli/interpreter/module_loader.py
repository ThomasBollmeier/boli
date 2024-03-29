import os.path
from os.path import abspath, dirname, sep

from boli.frontend.ast import Identifier, AbsoluteName, Call
from boli.interpreter.error import InterpreterError
from boli.interpreter.values import BuiltInFuncLazy


class ModuleLoader:

    def __init__(self, module_search_paths=None):
        if module_search_paths is None:
            module_search_paths = [os.path.curdir, abspath(dirname(__file__) + sep + ".." + sep + "core")]
        self._module_search_paths = module_search_paths

    def load_module(self, interpreter, module_name):
        module_path = os.sep.join(module_name.split("::"))
        file_path = self._find_file_path(module_path)
        with open(file_path, "r") as f:
            code = f.read()
            interpreter.eval_program(code)

    def load_modules(self, interpreter, module_names):
        for module_name in module_names:
            self.load_module(interpreter, module_name)

    def _find_file_path(self, module_path):
        for module_search_path in self._module_search_paths:
            file_path = module_search_path + os.sep + module_path + ".boli"
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return file_path
        module_name = module_path.replace(os.sep, "::")
        raise InterpreterError(f"Cannot load module '{module_name}'")


@BuiltInFuncLazy
def require(interpreter, args):
    module_env = interpreter.get_environment()
    if not module_env.is_toplevel():
        raise InterpreterError("require can only used on top level")
    num_args = len(args)
    if num_args == 1:
        module_name = str(args[0])
        alias_name = ""
    elif num_args == 2:
        module_name = str(args[0])
        alias_name = str(args[1])
    else:
        raise InterpreterError("require must not be called with more than two arguments")

    module_interpreter = interpreter.new_with_global_env()
    ModuleLoader().load_module(module_interpreter, module_name)
    exported_values = module_interpreter.get_environment().get_exported_values()

    env = interpreter.get_environment()
    for key, value in exported_values.items():
        name = f"{alias_name}::{key}" if alias_name else key
        env.insert(name, value, owned=False)


@BuiltInFuncLazy
def provide(interpreter, args):
    from boli.interpreter.environment import ModuleEnvironment
    module_env = interpreter.get_environment()
    if not isinstance(module_env, ModuleEnvironment):
        raise InterpreterError("provide can only used on top level")
    for arg in args:
        if isinstance(arg, Identifier) or isinstance(arg, AbsoluteName):
            name = str(arg)
            module_env.add_export(name)
        elif isinstance(arg, Call):
            name_ast = arg.callee
            alias_ast = arg.args[0]
            if not isinstance(name_ast, Identifier) and not isinstance(name_ast, AbsoluteName):
                raise InterpreterError("invalid argument for provide")
            if not isinstance(alias_ast, Identifier):
                raise InterpreterError("invalid argument for provide")
            module_env.add_export(str(name_ast), str(alias_ast))
        else:
            raise InterpreterError("invalid argument for provide")
