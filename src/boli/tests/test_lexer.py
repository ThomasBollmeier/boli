from boli.lexer import Lexer
from boli.source import Source
from boli.tokens import TokenType, NumberToken
import pytest


class TestLexer:

    def test_lexer(self):
        code = """
        ( ( ) {} [] "\\"Test\\" 1\\2" 42 is-this-an-identifier? + - * / 
        def if)
        """
        tokens = self._create_lexer(code).fetch_all_tokens()

        assert len(tokens) == 18
        self._assert_token_type(tokens, 0, TokenType.LEFT_PAREN)
        self._assert_token_type(tokens, 1, TokenType.LEFT_PAREN)
        self._assert_token_type(tokens, 2, TokenType.RIGHT_PAREN)
        self._assert_token_type(tokens, 3, TokenType.LEFT_BRACE)
        self._assert_token_type(tokens, 4, TokenType.RIGHT_BRACE)
        self._assert_token_type(tokens, 5, TokenType.LEFT_BRACKET)
        self._assert_token_type(tokens, 6, TokenType.RIGHT_BRACKET)
        self._assert_token_type(tokens, 7, TokenType.STRING)
        assert tokens[7].str_val == r'"Test" 1\2'
        self._assert_token_type(tokens, 8, TokenType.NUMBER)
        assert tokens[8].num_val == 42
        self._assert_token_type(tokens, 9, TokenType.IDENT)
        assert tokens[9].name == 'is-this-an-identifier?'
        self._assert_token_type(tokens, 10, TokenType.PLUS)
        self._assert_token_type(tokens, 11, TokenType.MINUS)
        self._assert_token_type(tokens, 12, TokenType.ASTERISK)
        self._assert_token_type(tokens, 13, TokenType.SLASH)
        self._assert_token_type(tokens, 14, TokenType.DEF)
        self._assert_token_type(tokens, 15, TokenType.IF)
        self._assert_token_type(tokens, 16, TokenType.RIGHT_PAREN)
        self._assert_token_type(tokens, 17, TokenType.END_OF_INPUT)

    @pytest.mark.parametrize("num_str, expected_num_val", [
        ("42", 42),
        ("-42", -42),
        ("42.1", 42.1)
    ])
    def test_number(self, num_str, expected_num_val):
        lexer = self._create_lexer(num_str)
        tokens = lexer.fetch_all_tokens(include_end_of_input=False)
        assert len(tokens) == 1
        num_token = tokens[0]
        assert isinstance(num_token, NumberToken)
        assert num_token.num_val == expected_num_val

    @staticmethod
    def _assert_token_type(tokens, idx, expected):
        assert tokens[idx].token_type == expected

    @staticmethod
    def _create_lexer(code):
        return Lexer(Source(code))

