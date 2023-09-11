from boli.frontend.buffered_stream import BufferedStream
from boli.frontend.lexer import Lexer
from boli.frontend.ast import *
from boli.frontend.tokens import TokenType, Token, OPERATORS, LEFT_TOKENS, LEFT_TO_RIGHT_MAP, KEYWORDS


class ParseError(Exception):
    ...


class Parser:

    def __init__(self, source):
        self._lexer = BufferedStream(Lexer(source))
        self._quotation_level = 0
        self._funcdef_stack = []

    def program(self) -> Program:
        children = []

        while True:
            token = self._lexer.advance()
            if token is None:
                break
            if token.token_type in LEFT_TOKENS:
                next_token = self._lexer.peek()
                if next_token is None:
                    raise ParseError("Expected token but got none")
                if next_token.token_type == TokenType.DEF:
                    self._advance()
                    child = self._definition(LEFT_TO_RIGHT_MAP[token.token_type])
                elif next_token.token_type == TokenType.DEF_STRUCT:
                    self._advance()
                    child = self._struct(LEFT_TO_RIGHT_MAP[token.token_type])
                else:
                    child = self._call(LEFT_TO_RIGHT_MAP[token.token_type])
            else:
                raise ParseError(f"Token type {token.token_type} cannot be used on top level")
            if child is not None:
                children.append(child)

        return Program(children)

    def _definition(self, right_token_type) -> Ast:

        token = self._advance([TokenType.IDENT] + LEFT_TOKENS)
        if token.token_type == TokenType.IDENT:
            identifier = Identifier(token)
            expr = self.expression()
            self._advance([right_token_type])
        else:
            right_type_func = LEFT_TO_RIGHT_MAP[token.token_type]
            id_token = self._advance([TokenType.IDENT])
            identifier = Identifier(id_token)
            params, var_param, body = self._params_and_body(right_token_type, right_type_func)
            expr = Lambda(body, params, var_param)

            self._funcdef_stack.append(id_token.name)
            self._find_tail_calls(body[-1])
            self._funcdef_stack.pop()

        return Definition(identifier, expr)

    def _find_tail_calls(self, ast):
        if isinstance(ast, Call) and isinstance(ast.callee, Identifier):
            name = ast.callee.ident_tok.name
            if name == self._funcdef_stack[-1]:
                ast.is_tail_call = True
                return

        if isinstance(ast, If):
            self._find_tail_calls(ast.consequent)
            self._find_tail_calls(ast.alternate)
            return

        if isinstance(ast, Block) and ast.expressions:
            self._find_tail_calls(ast.expressions[-1])

    def _struct(self, right_token_type) -> Ast:
        name_tok = self._advance([TokenType.IDENT])
        left_token = self._advance(LEFT_TOKENS)
        right_fields_token_type = LEFT_TO_RIGHT_MAP[left_token.token_type]
        fields = []
        while True:
            next_token = self._advance([TokenType.IDENT, right_fields_token_type])
            if next_token is None:
                raise ParseError("Expected token but found none")
            if next_token.token_type == right_fields_token_type:
                break
            fields.append(Identifier(next_token))

        self._advance([right_token_type])

        return Struct(name_tok, fields)

    def expression(self) -> Ast:
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
        elif token.token_type == TokenType.NIL:
            return Nil(token)
        elif token.token_type == TokenType.IDENT:
            return Identifier(token)
        elif token.token_type == TokenType.SYMBOL:
            return Symbol(token)
        elif token.token_type in LEFT_TOKENS:
            expected_end = LEFT_TO_RIGHT_MAP[token.token_type]
            if self._quotation_level == 0:
                next_token = self._lexer.peek()
                if next_token is None:
                    raise ParseError("Expected token but found none")
                if next_token.token_type == TokenType.IF:
                    return self._if(expected_end)
                if next_token.token_type == TokenType.LAMBDA:
                    return self._lambda(expected_end)
                if next_token.token_type == TokenType.BLOCK:
                    return self._block(expected_end)
                return self._call(expected_end)
            return self._quote(expected_end)
        elif token.token_type == TokenType.QUOTE:
            return self._quote(self._expected_end(token.lexeme[1]))
        elif token.token_type in OPERATORS:
            return BuiltInOperator(token)
        elif token.token_type in KEYWORDS.values():
            return Keyword(token)

        raise ParseError("Could not parse expression!")

    def _block(self, end_token_type) -> Ast:
        self._advance([TokenType.BLOCK])
        expressions = []
        while True:
            next_token = self._lexer.peek()
            if next_token and next_token.token_type == end_token_type:
                self._advance()
                break
            expressions.append(self.expression())

        return Block(expressions)

    def _lambda(self, end_lambda_token_type) -> Ast:
        self._advance()
        token = self._advance()
        if token is None or token.token_type not in LEFT_TOKENS:
            raise ParseError("Excepted left paren not found")

        params, var_param, body = self._params_and_body(
            end_lambda_token_type, LEFT_TO_RIGHT_MAP[token.token_type])

        return Lambda(body, params, var_param)

    def _params_and_body(self, end_lambda_token_type, end_params_token_type):
        params = []
        var_param = None

        while True:
            next_token = self._lexer.peek()
            if next_token is None:
                raise ParseError("Expected token but found none")
            if next_token.token_type == end_params_token_type:
                self._advance()
                break
            if var_param is not None:  # the var_param must be the last in the parameter list
                raise ParseError("Expected end of parameters")
            ident_tok = self._lexer.peek()
            if ident_tok is None or ident_tok.token_type != TokenType.IDENT:
                raise ParseError("Excepted identifier not found")
            ident = self.expression()
            dots_tok = self._lexer.peek()
            if dots_tok and dots_tok.token_type == TokenType.DOT_3:
                self._advance()
                var_param = ident
            else:
                params.append(ident)

        body = [self._body_element()]
        while True:
            next_token = self._lexer.peek()
            if next_token is None:
                raise ParseError("Expected token but found none")
            if next_token.token_type == end_lambda_token_type:
                self._advance()
                break
            body.append(self._body_element())

        return params, var_param, body

    def _body_element(self):
        next_tokens = self._lexer.peek_many(2)
        if len(next_tokens) == 2:
            if next_tokens[0].token_type in LEFT_TOKENS and next_tokens[1].token_type == TokenType.DEF:
                left_token_type = next_tokens[0].token_type
                self._advance()
                self._advance()
                right_token_type = LEFT_TO_RIGHT_MAP[left_token_type]
                return self._definition(right_token_type)
            else:
                return self.expression()
        else:
            return self.expression()

    def _if(self, end_token_type) -> Ast:
        self._advance()
        condition = self.expression()
        consequent = self.expression()
        alternate = self.expression()
        self._advance([end_token_type])

        return If(condition, consequent, alternate)

    def _call(self, end_token_type) -> Ast:
        callee = self.expression()

        args = []
        while True:
            next_token = self._lexer.peek()
            if next_token is None:
                raise ParseError("Unexpected end of quote expression")
            if next_token.token_type == end_token_type:
                self._advance()
                break
            if next_token.token_type == TokenType.DOT_3:  # <-- vararg encountered
                self._advance()
                ident_tok = self._advance([TokenType.IDENT])
                args.append(VarArg(ident_tok))
                self._advance([end_token_type])
                break
            args.append(self.expression())

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
            elements.append(self.expression())

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
