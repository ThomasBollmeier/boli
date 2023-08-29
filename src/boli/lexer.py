from boli.tokens import *
from boli.buffered_stream import BufferedStream
import os

class Lexer:

    def __init__(self, source):
        self._column = 1
        self._line = 1
        self._source = BufferedStream(source)
        self._whitespace = [" ", "\t", "\r", "\n"]

    def advance(self):
        while True:
            ch, line, column = self._skip_whitespace()
            if ch is None:
                return None
            elif ch in TOKENS_1:
                return Token(TOKENS_1[ch], line, column)
            elif ch == '"':
                return self._scan_string(line, column)
            elif ch.isdigit():
                return self._scan_number(ch, line, column)
            elif ch == "'":  # quotation
                next_ch = self._source.peek()
                if next_ch is None:
                    return UnknownToken(line, column, ch)
                if next_ch == "(":
                    return self._scan_quote(line, column)
                self._advance_char()
                return self._scan_identifier(next_ch, line, column, is_part_of_symbol=True)
            elif ch == ";":  # comment
                self._skip_line_comment()
            else:
                return self._scan_identifier(ch, line, column)

    def fetch_all_tokens(self):
        tokens = []
        while True:
            token = self.advance()
            if token is None:
                break
            tokens.append(token)
        return tokens

    def _scan_quote(self, line, column):
        next_ch = self._source.peek()
        if next_ch is None or next_ch not in {"(", "{", "["}:
            return UnknownToken(line, column, "'")
        self._advance_char()
        return Quote(line, column, "'" + next_ch)

    def _scan_identifier(self, start_ch, line, column,is_part_of_symbol=False):
        forbidden_start = {"!", "?", ".", ","}
        if start_ch in forbidden_start:
            return UnknownToken(line, column, start_ch)

        name = start_ch + self._scan_while(self._is_valid_ident_char)

        if name in KEYWORDS:
            return Token(KEYWORDS[name], line, column)

        if name in ["#t", "#true", "#f", "#false"]:
            return BoolToken(line, column, name.startswith("#t"))

        if not is_part_of_symbol:
            return IdentifierToken(line, column, name)
        else:
            return Symbol(line, column, name)

    def _scan_while(self, predicate_fn):
        ret = ""
        while True:
            ch = self._source.peek()
            if ch is None or not predicate_fn(ch):
                break
            ret += ch
            self._advance_char()
        return ret

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
            ch = self._advance_char()[0]
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
        num_str = first_digit_ch + self._scan_while(lambda ch: ch.isdigit() or ch == ".")  # grouping by . is supported
        num_str = num_str.replace(".", "")

        next_two = self._source.peek_many(2)
        if len(next_two) < 2:
            return IntNumToken(line, column, int(num_str))
        fst, snd = next_two
        if fst != "," or not snd.isdigit():
            return IntNumToken(line, column, int(num_str))

        self._advance_char()
        num_str += fst + self._scan_while(lambda ch: ch.isdigit() or ch == ".")
        num_str = num_str.replace(".", "")
        num_str = num_str.replace(",", ".")
        return RealNumToken(line, column, float(num_str))

    def _skip_whitespace(self) -> tuple:
        while True:
            ch, line, column = self._advance_char()
            if ch is None or ch not in self._whitespace:
                break
        return ch, line, column

    def _skip_line_comment(self):
        ch, _, _ = self._advance_char()
        while ch != os.linesep:
            ch, _, _ = self._advance_char()

    def _advance_char(self):
        ch = self._source.advance()
        line = self._line
        column = self._column
        if ch is not None:
            if ch != "\n":
                self._column += 1
            else:
                self._line += 1
                self._column = 1
        return ch, line, column
