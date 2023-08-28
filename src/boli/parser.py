from boli.buffered_stream import BufferedStream
from boli.lexer import Lexer
from boli.ast import *
from boli.tokens import TokenType, Token, OPERATORS, LEFT_TOKENS, LEFT_TO_RIGHT_MAP


class ParseError(Exception):
    ...


class Parser:

    def __init__(self, source):
        self._lexer = BufferedStream(Lexer(source))
        self._quotation_level = 0

    def program(self) -> Program:
        children = []

        while True:
            token = self._lexer.advance()
            if token is None:
                break
            if token.token_type in [TokenType.LEFT_PAREN, TokenType.LEFT_BRACE, TokenType.LEFT_BRACKET]:
                allowed = [TokenType.DEF, TokenType.IDENT] + OPERATORS
                next_token = self._advance(allowed)
                if next_token.token_type == TokenType.DEF:
                    child = self._definition(token.token_type)
                else:
                    raise NotImplementedError()
            else:
                raise ParseError(f"Token type {token.token_type} cannot be used on top level")
            if child is not None:
                children.append(child)

        return Program(children)

    def _definition(self, left_token_type) -> Ast:
        id_token = self._advance([TokenType.IDENT])
        identifier = Identifier(id_token)
        expr = self._expression()
        right_token_type = LEFT_TO_RIGHT_MAP[left_token_type]
        self._advance([right_token_type])

        return Definition(identifier, expr)

    def _expression(self) -> Ast:
        token = self._advance()
        if token is None:
            raise ParseError("Expected token type but got none")

        if token.token_type == TokenType.INT_NUM:
            return Integer(token)
        elif token.token_type == TokenType.REAL_NUM:
            return Real(token)
        elif token.token_type == TokenType.STRING:
            return String(token)
        elif token.token_type == TokenType.BOOL:
            return Bool(token)
        elif token.token_type == TokenType.IDENT:
            return Identifier(token)
        elif token.token_type in LEFT_TOKENS:
            expected_end = LEFT_TO_RIGHT_MAP[token.token_type]
            if self._quotation_level == 0:
                return self._call(expected_end)
            return self._quote(expected_end)
        elif token.token_type == TokenType.QUOTE:
            return self._quote(self._expected_end(token.lexeme[1]))
        elif token.token_type in OPERATORS:
            return BuiltInOperator(token)

        raise ParseError("Could not parse expression!")

    def _call(self, end_token_type) -> Ast:
        callee = self._expression()

        args = []
        while True:
            next_token = self._lexer.peek()
            if next_token is None:
                raise ParseError("Unexpected end of quote expression")
            if next_token.token_type == end_token_type:
                self._advance()
                break
            args.append(self._expression())

        return Call(callee, args)

    def _quote(self, expected_end) -> Ast:
        self._quotation_level += 1
        elements = []

        while True:
            next_token = self._lexer.peek()
            if next_token is None:
                raise ParseError("Unexpected end of quote expression")
            if next_token.token_type == expected_end:
                self._advance()
                break
            elements.append(self._expression())

        self._quotation_level -= 1
        return List(elements)

    @staticmethod
    def _expected_end(lexeme):
        return {
            "(": TokenType.RIGHT_PAREN,
            "{": TokenType.RIGHT_BRACE,
            "[": TokenType.RIGHT_BRACKET,
        }[lexeme]

    def _advance(self, expected_token_types = None) -> Token | None:
        token = self._lexer.advance()
        if token is None:
            if expected_token_types is None:
                return None
            else:
                raise ParseError("Expected token type but got none")
        if expected_token_types is not None and token.token_type not in expected_token_types:
            raise ParseError(f"Unexpected token type {token.token_type}")
        return token
