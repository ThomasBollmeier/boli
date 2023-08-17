from boli.lexer import Lexer
from boli.source import Source
from boli.tokens import TokenType


class TestLexer:

    def test_lexer(self):
        code = """
        ( ( ) {} [] "\\"Test\\" 1\\2" 42 is-this-an-identifier? + - * / 
        def if)
        """
        lexer = Lexer(Source(code))
        tokens = []

        while True:
            token = lexer.next_token()
            tokens.append(token)
            if token.token_type == TokenType.END_OF_INPUT:
                break

        assert len(tokens) == 18
        self.assert_token_type(tokens, 0, TokenType.LEFT_PAREN)
        self.assert_token_type(tokens, 1, TokenType.LEFT_PAREN)
        self.assert_token_type(tokens, 2, TokenType.RIGHT_PAREN)
        self.assert_token_type(tokens, 3, TokenType.LEFT_BRACE)
        self.assert_token_type(tokens, 4, TokenType.RIGHT_BRACE)
        self.assert_token_type(tokens, 5, TokenType.LEFT_BRACKET)
        self.assert_token_type(tokens, 6, TokenType.RIGHT_BRACKET)
        self.assert_token_type(tokens, 7, TokenType.STRING)
        assert tokens[7].str_val == r'"Test" 1\2'
        self.assert_token_type(tokens, 8, TokenType.NUMBER)
        assert tokens[8].num_val == 42
        self.assert_token_type(tokens, 9, TokenType.IDENT)
        assert tokens[9].name == 'is-this-an-identifier?'
        self.assert_token_type(tokens, 10, TokenType.PLUS)
        self.assert_token_type(tokens, 11, TokenType.MINUS)
        self.assert_token_type(tokens, 12, TokenType.ASTERISK)
        self.assert_token_type(tokens, 13, TokenType.SLASH)
        self.assert_token_type(tokens, 14, TokenType.DEF)
        self.assert_token_type(tokens, 15, TokenType.IF)
        self.assert_token_type(tokens, 16, TokenType.RIGHT_PAREN)
        self.assert_token_type(tokens, 17, TokenType.END_OF_INPUT)

    @staticmethod
    def assert_token_type(tokens, idx, expected):
        assert tokens[idx].token_type == expected

