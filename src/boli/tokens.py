class TokenType:

    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    LEFT_BRACKET = 5
    RIGHT_BRACKET = 6
    IDENT = 7
    INT_NUM = 8
    REAL_NUM = 9
    STRING = 10
    DEF = 11
    IF = 12
    PLUS = 13
    MINUS = 14
    ASTERISK = 15
    SLASH = 16
    CARET = 17
    PERCENT = 18
    QUOTE = 19
    UNKNOWN = -1


TOKENS_1 = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    "[": TokenType.LEFT_BRACKET,
    "]": TokenType.RIGHT_BRACKET,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.ASTERISK,
    "/": TokenType.SLASH,
    "^": TokenType.CARET,
    "%": TokenType.PERCENT
}

KEYWORDS = {
    "def": TokenType.DEF,
    "if": TokenType.IF,
}

OPERATORS = [
    TokenType.PLUS,
    TokenType.MINUS,
    TokenType.ASTERISK,
    TokenType.SLASH,
    TokenType.CARET,
    TokenType.PERCENT
]

LEFT_TOKENS = [
    TokenType.LEFT_PAREN,
    TokenType.LEFT_BRACE,
    TokenType.LEFT_BRACKET
]

LEFT_TO_RIGHT_MAP = {
    TokenType.LEFT_PAREN: TokenType.RIGHT_PAREN,
    TokenType.LEFT_BRACE: TokenType.RIGHT_BRACE,
    TokenType.LEFT_BRACKET: TokenType.RIGHT_BRACKET
}


class Token:
    def __init__(self, token_type, line, column):
        self.token_type = token_type
        self.line = line
        self.col = column


class StringToken(Token):

    def __init__(self, line, column, str_val):
        Token.__init__(self, TokenType.STRING, line, column)
        self.str_val = str_val


class IntNumToken(Token):

    def __init__(self, line, column, int_val):
        Token.__init__(self, TokenType.INT_NUM, line, column)
        self.value = int_val


class RealNumToken(Token):

    def __init__(self, line, column, real_val):
        Token.__init__(self, TokenType.REAL_NUM, line, column)
        self.value = real_val


class IdentifierToken(Token):

    def __init__(self, line, column, name):
        Token.__init__(self, TokenType.IDENT, line, column)
        self.name = name


class UnknownToken(Token):

    def __init__(self, line, column, lexeme):
        Token.__init__(self, TokenType.UNKNOWN, line, column)
        self.lexeme = lexeme


class Quote(Token):

    def __init__(self, line, column, lexeme):
        Token.__init__(self, TokenType.QUOTE, line, column)
        self.lexeme = lexeme
