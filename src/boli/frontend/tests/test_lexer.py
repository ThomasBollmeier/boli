from boli.frontend.lexer import Lexer
from boli.frontend.source import Source
from boli.frontend.tokens import TokenType, IntNumToken, RealNumToken
import pytest


class TestLexer:

    def test_lexer(self):
        code = """
        ( ( ) {} [] "\\"Test\\" 1\\2" 42 is-this-an-identifier? + - * / 
        def if) ^ % 'a-symbol nil = > >= < <= ... block
        """
        tokens = self._create_lexer(code).fetch_all_tokens()

        assert len(tokens) == 28
        self._assert_token_type(tokens, 0, TokenType.LEFT_PAREN)
        self._assert_token_type(tokens, 1, TokenType.LEFT_PAREN)
        self._assert_token_type(tokens, 2, TokenType.RIGHT_PAREN)
        self._assert_token_type(tokens, 3, TokenType.LEFT_BRACE)
        self._assert_token_type(tokens, 4, TokenType.RIGHT_BRACE)
        self._assert_token_type(tokens, 5, TokenType.LEFT_BRACKET)
        self._assert_token_type(tokens, 6, TokenType.RIGHT_BRACKET)
        self._assert_token_type(tokens, 7, TokenType.STRING)
        assert tokens[7].str_val == r'"Test" 1\2'
        self._assert_token_type(tokens, 8, TokenType.INT_NUM)
        assert tokens[8].value == 42
        self._assert_token_type(tokens, 9, TokenType.IDENT)
        assert tokens[9].name == 'is-this-an-identifier?'
        self._assert_token_type(tokens, 10, TokenType.PLUS)
        self._assert_token_type(tokens, 11, TokenType.MINUS)
        self._assert_token_type(tokens, 12, TokenType.ASTERISK)
        self._assert_token_type(tokens, 13, TokenType.SLASH)
        self._assert_token_type(tokens, 14, TokenType.DEF)
        self._assert_token_type(tokens, 15, TokenType.IF)
        self._assert_token_type(tokens, 16, TokenType.RIGHT_PAREN)
        self._assert_token_type(tokens,17, TokenType.CARET)
        self._assert_token_type(tokens,18, TokenType.PERCENT)
        self._assert_token_type(tokens, 19, TokenType.SYMBOL)
        assert tokens[19].name == 'a-symbol'
        self._assert_token_type(tokens, 20, TokenType.NIL)
        self._assert_token_type(tokens, 21, TokenType.EQ)
        self._assert_token_type(tokens, 22, TokenType.GT)
        self._assert_token_type(tokens, 23, TokenType.GE)
        self._assert_token_type(tokens, 24, TokenType.LT)
        self._assert_token_type(tokens, 25, TokenType.LE)
        self._assert_token_type(tokens, 26, TokenType.DOT_3)
        self._assert_token_type(tokens, 27, TokenType.BLOCK)

    @pytest.mark.parametrize("num_str, expected_num_val", [
        ("42", 42),
        ("42,1", 42.1),
        ("1.000.000", 1000000)
    ])
    def test_number(self, num_str, expected_num_val):
        lexer = self._create_lexer(num_str)
        tokens = lexer.fetch_all_tokens()
        assert len(tokens) == 1
        num_token = tokens[0]
        assert isinstance(num_token, IntNumToken) or isinstance(num_token, RealNumToken)
        assert num_token.value == expected_num_val

    def test_quote(self):
        code = """
        (def my-list '(1 2 3))
        """
        tokens = self._create_lexer(code).fetch_all_tokens()

        assert len(tokens) == 9
        self._assert_token_type(tokens, 0, TokenType.LEFT_PAREN)
        self._assert_token_type(tokens, 1, TokenType.DEF)
        self._assert_token_type(tokens, 2, TokenType.IDENT)
        assert tokens[2].name == "my-list"
        self._assert_token_type(tokens, 3, TokenType.QUOTE)
        assert tokens[3].lexeme == "'("
        self._assert_token_type(tokens, 4, TokenType.INT_NUM)
        self._assert_token_type(tokens, 5, TokenType.INT_NUM)
        self._assert_token_type(tokens, 6, TokenType.INT_NUM)
        self._assert_token_type(tokens, 7, TokenType.RIGHT_PAREN)
        self._assert_token_type(tokens, 8, TokenType.RIGHT_PAREN)

    def test_varargs(self):
        code = """
        (def my-func (lambda (arg1 args2...)))
        """
        tokens = self._create_lexer(code).fetch_all_tokens()
        assert len(tokens) == 12

    @staticmethod
    def _assert_token_type(tokens, idx, expected):
        assert tokens[idx].token_type == expected

    @staticmethod
    def _create_lexer(code):
        return Lexer(Source(code))

