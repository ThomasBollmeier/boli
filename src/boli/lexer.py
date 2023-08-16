from boli.tokens import Token, TokenType
from boli.buffered_source import BufferedSource


class Lexer:

    def __init__(self, source):
        self._column = 1
        self._line = 1
        self._source = BufferedSource(source)
        self._whitespace = [" ", "\t", "\r", "\n"]

    def next_token(self):
        ch, line, column = self._skip_whitespace()
        if ch is None:
            return Token(TokenType.END_OF_INPUT, "", line, column)
        elif ch == "(":
            return Token(TokenType.LEFT_PAREN, ch, line, column)
        elif ch == ")":
            return Token(TokenType.RIGHT_PAREN, ch, line, column)
        elif ch == "{":
            return Token(TokenType.LEFT_BRACE, ch, line, column)
        elif ch == "}":
            return Token(TokenType.RIGHT_BRACE, ch, line, column)
        elif ch == "[":
            return Token(TokenType.LEFT_BRACKET, ch, line, column)
        elif ch == "]":
            return Token(TokenType.RIGHT_BRACKET, ch, line, column)
        elif ch == '"':
            return self._scan_string(line, column)
        elif ch.isdigit():
            return self._scan_number(ch, line, column)
        else:
            return Token(TokenType.UNKNOWN, ch, line, column)

    def _scan_string(self, line, column):
        s = '"'
        prev_ch = None
        while True:
            ch = self._next_char()[0]
            if ch is None:
                return Token(TokenType.UNKNOWN, s, line, column)
            elif ch == '"':
                if prev_ch != "\\":
                    return Token(TokenType.STRING, s + ch, line, column)
            s += ch
            prev_ch = ch

    def _scan_number(self, first_digit_ch, line, column):
        num_str = first_digit_ch
        while True:
            ch = self._source.peek()
            if ch is None or not ch.isdigit():
                break
            num_str += ch
            self._next_char()
        return Token(TokenType.NUMBER, num_str, line, column)

    def _skip_whitespace(self) -> tuple:
        while True:
            ch, line, column = self._next_char()
            if ch is None or ch not in self._whitespace:
                break
        return ch, line, column

    def _next_char(self):
        ch = self._source.next_char()
        line = self._line
        column = self._column
        if ch is not None:
            if ch != "\n":
                self._column += 1
            else:
                self._line += 1
                self._column = 1
        return ch, line, column
