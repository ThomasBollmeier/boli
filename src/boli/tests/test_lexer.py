from boli.lexer import Lexer
from boli.source import Source
from boli.tokens import TokenType


def test_lexer():
    #           12345678901234567890123456
    #           ( ( ) {} [] "\"Test\"" 42)
    code = r'( ( ) {} [] "\"Test\" 1\2" 42)'
    lexer = Lexer(Source(code))
    tokens = []

    while True:
        token = lexer.next_token()
        tokens.append(token)
        if token.token_type == TokenType.END_OF_INPUT:
            break

    assert len(tokens) == 11
    assert_token_type(tokens, 0, TokenType.LEFT_PAREN)
    assert_token_type(tokens, 1, TokenType.LEFT_PAREN)
    assert_token_type(tokens, 2, TokenType.RIGHT_PAREN)
    assert_token_type(tokens, 3, TokenType.LEFT_BRACE)
    assert_token_type(tokens, 4, TokenType.RIGHT_BRACE)
    assert_token_type(tokens, 5, TokenType.LEFT_BRACKET)
    assert_token_type(tokens, 6, TokenType.RIGHT_BRACKET)
    assert_token_type(tokens, 7, TokenType.STRING)
    assert tokens[7].lexeme == r'"\"Test\" 1\2"'
    assert_token_type(tokens, 8, TokenType.NUMBER)
    assert tokens[8].lexeme == "42"
    assert_token_type(tokens, 9, TokenType.RIGHT_PAREN)
    assert_token_type(tokens, 10, TokenType.END_OF_INPUT)


def assert_token_type(tokens, idx, expected):
    assert tokens[idx].token_type == expected

