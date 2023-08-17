class TokenType:

    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    LEFT_BRACKET = 5
    RIGHT_BRACKET = 6
    IDENT = 7
    NUMBER = 8
    STRING = 9
    DEF = 10
    IF = 11
    PLUS = 12
    MINUS = 13
    ASTERISK = 14
    SLASH = 15
    END_OF_INPUT = 999
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
    "/": TokenType.SLASH
}

KEYWORDS = {
    "def": TokenType.DEF,
    "if": TokenType.IF,
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


class NumberToken(Token):

    def __init__(self, line, column, num_val):
        Token.__init__(self, TokenType.NUMBER, line, column)
        self.num_val = num_val


class IdentifierToken(Token):

    def __init__(self, line, column, name):
        Token.__init__(self, TokenType.IDENT, line, column)
        self.name = name


class UnknownToken(Token):

    def __init__(self, line, column, lexeme):
        Token.__init__(self, TokenType.UNKNOWN, line, column)
        self.lexeme = lexeme
