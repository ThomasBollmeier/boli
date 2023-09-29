from boli.interpreter.interpreter import Interpreter
from boli.interpreter.error import InterpreterError
from boli.frontend.parser import ParseError
from os.path import abspath, dirname, sep


def repl():
    interpreter = Interpreter()
    code = ""
    print("boli REPL 1.0.0")
    _print_help()

    core_dir = abspath(dirname(__file__) + sep + ".." + sep + "core")
    _load_file(interpreter, core_dir + sep + "list.boli")

    while True:
        code += input("boli> ")
        if code[-1] == "\\":
            code = code[:-1]
            continue
        stop, code = _handle_command(interpreter, code)
        if stop:
            break
        if code:
            try:
                value = interpreter.eval_program(code)
                print(value)
            except (ParseError, InterpreterError) as error:
                print(error)
        code = ""


def _handle_command(interpreter, code):
    if code in [":q", ":quit"]:
        return True, ""
    elif code.startswith(":l") or code.startswith(":load"):
        parts = code.split()
        if len(parts) != 2:
            print("Usage: ':l(oad) <file>'")
        else:
            _load_file(interpreter, parts[1].strip())
        return True, ""

    elif code in [":h", ":help"]:
        _print_help()
        return False, ""
    return False, code


def _load_file(interpreter, file_name):
    with open(file_name, "r") as f:
        code = f.read()
        interpreter.eval_program(code)


def _print_help():
    print("Use ':l(oad) <filename>' to load file, ':q(uit)' to exit, ':h(elp)' for help.")


if __name__ == "__main__":
    repl()