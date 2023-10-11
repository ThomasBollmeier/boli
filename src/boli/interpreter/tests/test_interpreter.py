from boli.interpreter.interpreter import Interpreter
from boli.interpreter.values import *
import pytest

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
        assert str(value) == '"the answer to everything"'

        code = """
        (if (not 42)
            i-will-not-be-evaluated
            "the answer to everything")
        """
        value = self._eval_code(code, String)
        assert str(value) == '"the answer to everything"'

    def test_cond_expr(self):

        code = """
        (block
            (def answer 42)
            (cond
                [(= answer 42) "the answer to everything"]
                [#t i-will-not-be-evaluated]))
        """
        value = self._eval_code(code, String)
        assert str(value) == '"the answer to everything"'

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

    def test_tail_call_2(self):
        code = """
        (def (reverse lst)
            (def (reverse-helper lst acc)
                (if (empty? lst)
                    acc
                    (reverse-helper (tail lst) (cons (head lst) acc))))
            (reverse-helper lst '()))

        (def (fibo n) ; calculate the first n Fibonacci numbers
            (def (fibo-helper a b n acc)
                (cond
                    [(= n 0) (reverse acc)] 
                    [#t (fibo-helper b (+ a b) (- n 1) (cons a acc))]))
            (fibo-helper 1 1 n '()))
        (fibo 10)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, List)
        assert str(value) == "'(1 1 2 3 5 8 13 21 34 55)"

    def test_closure(self):

        code = """
        (def (make-counter)
            (def cnt 1)
            (lambda ()
                (def ret cnt)
                (set! cnt (+ cnt 1))
                ret))
        (def count (make-counter))
        (def count2 (make-counter))
        (count)
        (count)
        (= (- (count) 2) (count2))
        """
        value = Interpreter().eval_program(code)
        assert isinstance(value, Bool)
        assert str(value) == "#t"

        code = """
        (def (make-adder n)
            (lambda (m)
                (+ m n)))
        ((make-adder 3) 39)    
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, Integer)
        assert str(value) == "42"

    def test_scope(self):

        code = """
        (def (main)
            (def answer 42)
            (def (my-func)
                (def answer 43)
                (writeln answer))
            (writeln)
            (my-func)
            (block
                (def answer 44)
                (writeln answer))
            (writeln answer)
            answer)
        (main)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, Integer)
        assert str(value) == "42"

    def test_cond_expression(self):
        code = """
        (def (main)
            (block
                (def answer 42)
                (cond
                    [(= answer 42) "the answer to everything"]
                    [#t i-will-not-be-evaluated])))
        (main)
        """
        value = Interpreter().eval_program(code)
        assert isinstance(value, String)
        assert str(value) == '"the answer to everything"'

    def test_let_expression(self):
        code = """
        (def (main)
            (let [(answer 42)]
                (cond
                    [(= answer 42) "the answer to everything"]
                    [#t i-will-not-be-evaluated])))
        (main)
        """
        value = Interpreter().eval_program(code)
        assert isinstance(value, String)
        assert str(value) == '"the answer to everything"'

    def test_struct_type(self):
        code = """
        (def-struct person (name first-name sex))
        (def (main)
            person)
        (main)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, StructType)
        assert str(value) == """(def-struct person (name first-name sex))"""

    def test_struct(self):
        code = """
        (def-struct person (name first-name sex))
        (def (main)
            (def ego (create-person "Ballermeier" "Thomas" 'male))
            (writeln)
            (writeln (person-name ego))
            (writeln (person-first-name ego))
            (writeln (person-sex ego))
            (person-set-name! ego "Bollmeier")
            ego)
        (main)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, Struct)
        assert str(value) == """(person "Bollmeier" "Thomas" 'male)"""

    def test_require(self):
        code = """
        (require misc::util ut)
        (def (main)
            (ut::guten-tag "Thomas"))
        (main)
        """

        value = Interpreter().eval_program(code)
        assert isinstance(value, String)
        assert str(value) == '"Guten Tag, Thomas!"'

    def test_require_w_error(self):
        code = """
        (require misc::util ut)
        (def (main)
            (def hello (ut::make-greeter "Hello " "!"))
            (hello "Thomas"))
        (main)
        """
        with pytest.raises(InterpreterError) as error:
            Interpreter().eval_program(code)

    @staticmethod
    def _eval_code(code, expected_type):
        interpreter = Interpreter()
        value = interpreter.eval_expr(code)
        assert isinstance(value, expected_type)
        return value
