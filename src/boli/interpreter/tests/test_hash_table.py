from boli.interpreter.interpreter import Interpreter
from boli.interpreter.values import HashTable, String, Bool


class TestHashTable:

    def test_creation(self):

        self._assert_code("""
        (def (main) 
            (def ego (create-hash-table 'name "Bollmeier" 'first-name "Thomas"))
            ego)
        (main)
        """, """(hash-table 'name "Bollmeier" 'first-name "Thomas")""")

    def test_set(self):

        self._assert_code("""
        (def (main) 
            (def ego (create-hash-table 'name "Bollmeier" 'first-name "Thomas"))
            (hash-set! ego 'sex 'male))
        (main)
        """, """(hash-table 'name "Bollmeier" 'first-name "Thomas" 'sex 'male)""")

    def test_remove(self):

        self._assert_code("""
        (def (main) 
            (def ego (create-hash-table 'name "Bollmeier" 'first-name "Thomas"))
            (hash-remove! ego 'first-name)
            (hash-exists? ego 'first-name))
        (main)
        """, "#f", Bool)

    def test_ref(self):

        self._assert_code("""
        (def (main) 
            (def ego (create-hash-table 'name "Bollmeier" 'first-name "Thomas"))
            (hash-ref ego 'name))
        (main)
        """, '"Bollmeier"', String)

    def test_exists(self):

        self._assert_code("""
        (def (main) 
            (def ego (create-hash-table 'name "Bollmeier" 'first-name "Thomas"))
            (hash-exists? ego 'name))
        (main)
        """, "#t", Bool)

    @staticmethod
    def _assert_code(code, expected_value, expected_type=None):
        expected_type = expected_type or HashTable
        value = Interpreter().eval_program(code)
        assert isinstance(value, expected_type)
        assert str(value) == expected_value
