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

        value = self._eval_code("(^ 2 2 3)", Integer)
        assert str(value) == "256"

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

        value = self._eval_code("(and (= 2 (+ 1 1)) 42)", Integer)
        assert str(value) == "42"

        value = self._eval_code("(and (= 1 2) i-will-not-be-evaluated)", Bool)
        assert str(value) == "#f"

        value = self._eval_code("(or 42 i-will-not-be-evaluated)", Integer)
        assert str(value) == "42"

        value = self._eval_code("(not 42)", Bool)
        assert str(value) == "#f"

        value = self._eval_code("(not nil)", Bool)
        assert str(value) == "#t"

        code = """
        (if 42
            "the answer to everything"
            i-will-not-be-evaluated)
        """
        value = self._eval_code(code, String)
        assert str(value) == "the answer to everything"

        code = """
        (if (not 42)
            i-will-not-be-evaluated
            "the answer to everything")
        """
        value = self._eval_code(code, String)
        assert str(value) == "the answer to everything"

    def test_function_call(self):

        code = """
        (def (my-add fst snd further-numbers...)
            (+ fst snd ...further-numbers))
        (def numbers '(1 2 3 4))
        (my-add ...numbers)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, Integer)
        assert str(value) == "10"

    def test_function_call_w_varargs(self):

        code = """
        (def (my-add numbers)
            (+ ...numbers))
        (def numbers '(1 2 3 4))
        (my-add numbers)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, Integer)
        assert str(value) == "10"

    def test_recursive_call(self):

        code = """
        (def (fac n)
            (if (= n 0)
                1
                (* n (fac (- n 1)))))
        (fac 5)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, Integer)
        assert str(value) == "120"

    def test_tail_call(self):

        code = """
        (def (fac n)
            (def (fac-helper n acc)
                (if (= n 0)
                    acc
                    (fac-helper (- n 1) (* n acc))))
            (fac-helper n 1))
            
        (fac 5)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, Integer)
        assert str(value) == "120"

    @staticmethod
    def _eval_code(code, expected_type):
        interpreter = Interpreter()
        value = interpreter.eval_expr(code)
        assert isinstance(value, expected_type)
        return value
