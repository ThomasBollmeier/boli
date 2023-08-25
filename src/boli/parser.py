from boli.buffered_stream import BufferedStream
from boli.lexer import Lexer
from boli.ast import *
from boli.tokens import TokenType, Token, OPERATORS


class ParseError(Exception):
    ...


class Parser:

    def __init__(self, source):
        self._lexer = BufferedStream(Lexer(source))

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
        identifier = Identifier(id_token.name)
        expr = self._expression()
        right_token_type = {
            TokenType.LEFT_PAREN: TokenType.RIGHT_PAREN,
            TokenType.LEFT_BRACE: TokenType.RIGHT_BRACE,
            TokenType.LEFT_BRACKET: TokenType.RIGHT_BRACKET
        }[left_token_type]
        self._advance([right_token_type])

        return Definition(identifier, expr)

    def _expression(self) -> Ast:
        token = self._advance()

        if token.token_type == TokenType.INT_NUM:
            return Integer(token)
        elif token.token_type == TokenType.REAL_NUM:
            return Real(token)
        elif token.token_type == TokenType.STRING:
            return String(token)

        raise NotImplementedError()

    def _advance(self, expected_token_types = None) -> Token | None:
        token = self._lexer.advance()
        if token is None:
            if expected_token_types is None:
                return None
            else:
                raise ParseError(f"Expected token type but got none")
        if expected_token_types is not None and token.token_type not in expected_token_types:
            raise ParseError(f"Unexpected token type {token.token_type}")
        return token
