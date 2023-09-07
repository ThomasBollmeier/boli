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

        value = self._eval_code("(+ 41 1,0)", Real)
        assert str(value) == "42,0"

        value = self._eval_code("(^ 7 2)", Integer)
        assert str(value) == "49"

        value = self._eval_code("(^ 7,0 2)", Real)
        assert str(value) == "49,0"

        value = self._eval_code("(% 85 43)", Integer)
        assert str(value) == "42"

        value = self._eval_code("(= 42 (+ 41 1))", Bool)
        assert str(value) == "#t"

        value = self._eval_code("(> 42 41)", Bool)
        assert str(value) == "#t"

        value = self._eval_code("(>= 42 41)", Bool)
        assert str(value) == "#t"

        value = self._eval_code("(< 42 41)", Bool)
        assert str(value) == "#f"

        value = self._eval_code("(<= 42 41)", Bool)
        assert str(value) == "#f"

    @staticmethod
    def _eval_code(code, expected_type):
        interpreter = Interpreter()
        value = interpreter.eval_expr(code)
        assert isinstance(value, expected_type)
        return value
