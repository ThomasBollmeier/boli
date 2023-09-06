from boli.interpreter.interpreter import Interpreter
from boli.interpreter.values import *


class TestInterpreter:

    def test_eval_expr(self):

        value = self._eval_code("42", Integer)
        assert str(value) == "42"

        value = self._eval_code("(+ 41 1)", Integer)
        assert str(value) == "42"

        value = self._eval_code("(+ (* 5 8) (+ 1 1))", Integer)
        assert str(value) == "42"

    @staticmethod
    def _eval_code(code, expected_type):
        interpreter = Interpreter()
        value = interpreter.eval_expr(code)
        assert isinstance(value, expected_type)
        return value
