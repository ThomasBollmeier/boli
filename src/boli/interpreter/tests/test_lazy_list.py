from boli.interpreter.interpreter import Interpreter
from boli.interpreter.values import ListIter, LazyList, Integer


class TestLazyList:

    def test_head(self):
        interpreter = Interpreter()
        code = """
        (require list l)
        (def lst (lazy-list ...(l::range 1 11)))
        (head (drop 3 lst))
        """
        actual = interpreter.eval_program(code)
        assert (str(actual) == "4")


    def test_filter(self):
        interpreter = Interpreter()
        code = """
        (require list l)
        (def even? (λ (x) (= 0 (% x 2))))
        (def lst (lazy-list ...(l::range 1 11)))
        (take 3 (filter even? lst))
        """
        actual = interpreter.eval_program(code)
        assert (str(actual) == "'(2 4 6)")


    def test_map(self):
        interpreter = Interpreter()
        code = """
        (require list l)
        (def (square x) (* x x))
        (def lst (lazy-list ...(l::range 1 11)))
        (take 3 (map square lst))
        """
        actual = interpreter.eval_program(code)
        assert (str(actual) == "'(1 4 9)")

    def test_drop(self):
        interpreter = Interpreter()
        code = """
        (require list l)
        (def lst (lazy-list ...(l::range 1 11)))
        (take 3 (drop 5 lst))
        """
        actual = interpreter.eval_program(code)
        assert (str(actual) == "'(6 7 8)")

    def test_drop_while(self):
        interpreter = Interpreter()
        code = """
        (require list l)
        (def lst (lazy-list ...(l::range 1 11)))
        (take 3 (drop-while (λ (x) (> 40 (* x x))) lst))
        """
        actual = interpreter.eval_program(code)
        assert (str(actual) == "'(7 8 9)")

    def test_take_while(self):
        interpreter = Interpreter()
        code = """
        (require list l)
        (def lst (lazy-list ...(l::range 1 11)))
        (take-while (λ (x) (> 40 (* x x))) lst)
        """
        actual = interpreter.eval_program(code)
        assert (str(actual) == "'(1 2 3 4 5 6)")
