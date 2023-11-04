from argparse import ArgumentParser
from boli.interpreter.interpreter import Interpreter
from boli.interpreter.error import InterpreterError
from boli.frontend.parser import ParseError

BOLI_VERSION = "0.4.1"


def run():
    parser = ArgumentParser('Run a boli program')
    parser.add_argument('source_file',
                        nargs='?')
    parser.add_argument('--version',
                        action='version',
                        version=BOLI_VERSION)

    args = parser.parse_args()

    if not args.source_file:
        repl()
    else:
        _load_file(Interpreter(), args.source_file)


def repl():
    interpreter = Interpreter()
    code = ""
    print(f"boli REPL {BOLI_VERSION}")
    _print_help()

    while True:
        code += input("boli> ")
        if code[-1] == "\\":
            code = code[:-1]
            continue
        try:
            stop, code = _handle_command(interpreter, code)
            if stop:
                break
            if code:
                value = interpreter.eval_program(code)
                print(value)
        except (ParseError, InterpreterError, FileNotFoundError) as error:
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
        return False, ""
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
    run()
