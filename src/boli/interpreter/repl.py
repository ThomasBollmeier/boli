from boli.interpreter.interpreter import Interpreter
from boli.interpreter.error import InterpreterError
from boli.frontend.parser import ParseError


def repl():
    interpreter = Interpreter()
    code = ""

    while True:
        code += input("boli> ")
        if code[-1] == "\\":
            code = code[:-1]
            continue
        try:
            value = interpreter.eval_program(code)
            print(value)
        except (ParseError, InterpreterError) as error:
            print(error)
        code = ""


if __name__ == "__main__":
    repl()
