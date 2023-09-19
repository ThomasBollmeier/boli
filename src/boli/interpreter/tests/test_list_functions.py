from boli.interpreter.interpreter import Interpreter
from boli.interpreter.values import List, Integer, Bool


class TestListFunctions:

    def test_head(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (head lst))
        (main)
        """, "1", Integer)

    def test_tail(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (tail lst))
        (main)
        """, "'(2 3 4)")

    def test_list_ref(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (list-ref lst 1))
        (main)
        """, "2", Integer)

    def test_list_set_bang(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (list-set! lst 1 42)
            lst)
        (main)
        """, "'(1 42 3 4)")

    def test_concat(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (def other-lst '(5 6))
            (concat lst other-lst))
        (main)
        """, "'(1 2 3 4 5 6)")

    def test_cons(self):

        self._assert_code("""
        (def (main) 
            (def lst '(2 3 4))
            (cons 1 lst))
        (main)
        """, "'(1 2 3 4)")

    def test_count(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (count lst))
        (main)
        """, "4", Integer)

    def test_empty(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (empty? lst))
        (main)
        """, "#f", Bool)

        self._assert_code("""
        (def (main) 
            (empty? '()))
        (main)
        """, "#t", Bool)

    def test_map(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (def (add1 n) (+ n 1))
            (map add1 lst))
        (main)
        """, "'(2 3 4 5)")

    def test_filter(self):

        self._assert_code("""
        (def (main) 
            (def lst '(1 2 3 4))
            (def (even? n) (= 0 (% n 2)))
            (filter even? lst))
        (main)
        """, "'(2 4)")

    def test_fold_left(self):

        code = """
        (def (foldl fn init-val lst)
            (def (foldl-helper lst acc)
                (if (empty? lst)
                    acc
                    (foldl-helper (tail lst) (fn acc (head lst)))))
            (foldl-helper lst init-val))
        (def (main)
            (foldl * 1 '(1 2 3 4)))
        (main)
        """

        self._assert_code(code, "24", Integer)

    def test_reverse(self):
        code = """
         (def (reverse lst)
             (def (reverse-helper lst acc)
                 (if (empty? lst)
                     acc
                     (reverse-helper (tail lst) (cons (head lst) acc))))
             (reverse-helper lst '()))
         (def (main)
             (reverse '(1 2 3 4)))
         (main)
         """

        self._assert_code(code, "'(4 3 2 1)")

    @staticmethod
    def _assert_code(code, expected_value, expected_type=None):
        expected_type = expected_type or List
        value = Interpreter().eval_program(code)
        assert isinstance(value, expected_type)
        assert str(value) == expected_value
