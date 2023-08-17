from boli.tokens import *
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
            return Token(TokenType.END_OF_INPUT, line, column)
        elif ch in TOKENS_1:
            return Token(TOKENS_1[ch], line, column)
        elif ch == '"':
            return self._scan_string(line, column)
        elif ch.isdigit():
            return self._scan_number(ch, line, column)
        else:
            return self._scan_identifier(ch, line, column)

    def _scan_identifier(self, start_ch, line, column):
        forbidden_start = set(["!", "?"])
        if start_ch in forbidden_start:
            return UnknownToken(line, column, start_ch)
        name = start_ch
        while True:
            ch = self._source.peek()
            if ch is None or not self._is_valid_ident_char(ch):
                break
            name += ch
            self._next_char()
        if name not in KEYWORDS:
            return IdentifierToken(line, column, name)
        else:
            return Token(KEYWORDS[name], line, column)

    def _is_valid_ident_char(self, ch):
        if ch in self._whitespace:
            return False
        if ch in set(list('"(){}[]/')):
            return False
        return True

    def _scan_string(self, line, column):
        s = ''
        prev_ch = None
        while True:
            ch = self._next_char()[0]
            if ch is None:
                return StringToken(line, column, self._convert_str(s))
            elif ch == '"':
                if prev_ch != "\\":
                    return StringToken(line, column, self._convert_str(s))
            s += ch
            prev_ch = ch

    @staticmethod
    def _convert_str(s):
        return s.replace(r'\"', '"')

    def _scan_number(self, first_digit_ch, line, column):
        num_str = first_digit_ch
        while True:
            ch = self._source.peek()
            if ch is None or not ch.isdigit():
                break
            num_str += ch
            self._next_char()
        return NumberToken(line, column, float(num_str))

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
