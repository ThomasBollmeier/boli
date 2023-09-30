import os.path
from os.path import abspath, dirname, sep
from boli.interpreter.error import InterpreterError


class ModuleLoader:

    def __init__(self):
        self._module_paths = [
            abspath(dirname(__file__) + sep + ".." + sep + "core")
        ]

    def load_file(self, interpreter, module_name):
        file_path = self._find_file_path(module_name)
        with open(file_path, "r") as f:
            code = f.read()
            interpreter.eval_program(code)

    def _find_file_path(self, module_name):
        for module_path in self._module_paths:
            file_path = module_path + os.sep + module_name + ".boli"
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return file_path
        raise InterpreterError(f"Cannot load module '{module_name}'")
