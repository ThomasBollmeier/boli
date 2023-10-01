from boli.interpreter.interpreter import Interpreter
from boli.interpreter.values import String, Integer


class TestStringFunctions:

    def test_count(self):
        self._assert_code("""
        (def name "Thomas")
        (count name)
        """, "6", Integer)

    def test_sub(self):
        self._assert_code("""
        (def name "Thomas")
        (str-sub name 2 3)
        """, '"oma"')

    def test_replace(self):
        self._assert_code("""
        (def name "Thomas")
        (str-replace name "o" "e")
        """, '"Themas"')

    def test_concat(self):
        self._assert_code("""
        (str-concat "Thomas" " " "Bollmeier")
        """, '"Thomas Bollmeier"')

    def test_to_upper(self):
        self._assert_code("""
        (str->upper "Thomas")
        """, '"THOMAS"')

    def test_to_lower(self):
        self._assert_code("""
        (str->lower "Thomas")
        """, '"thomas"')

    def test_capitalize(self):
        self._assert_code("""
        (def (capitalize s)
            (str-concat (str->upper (str-sub s 0 1)) 
                        (str-sub s 1)))
        (capitalize "thomas")
        """, '"Thomas"')

    @staticmethod
    def _assert_code(code, expected_value, expected_type=None):
        expected_type = expected_type or String
        value = Interpreter().eval_program(code)
        assert isinstance(value, expected_type)
        assert str(value) == expected_value
