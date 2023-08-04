class TokenType:

    LEFT_PAREN = 1
    RIGHT_PAREN = 2
    LEFT_BRACE = 3
    RIGHT_BRACE = 4
    LEFT_BRACKET = 5
    RIGHT_BRACKET = 6
    ID = 7
    NUMBER = 8
    STRING = 9
    DEF = 10
    IF = 11
    END_OF_INPUT = 99
    UNKNOWN = -1


class Token:
    def __init__(self, token_type, lexeme, line, column):
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.col = column
