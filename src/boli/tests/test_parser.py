from boli.parser import Parser
from boli.source import Source
from boli.ast_printer import AstPrinter


class TestParser:

    def test_program(self):

        code = """
        (def answer-to-everything (+ 41 1))
        (def ego "Thomas") ; <- that is me
        (def my-nested-list '(1 2 3 (4 5)))
        (def male? #t)
        """

        parser = Parser(Source(code))
        ast = parser.program()

        assert ast is not None

        ast.accept(AstPrinter())
