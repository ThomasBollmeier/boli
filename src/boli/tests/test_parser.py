from boli.parser import Parser
from boli.source import Source
from boli.ast_printer import AstPrinter


class TestParser:

    def test_program(self):

        code = """
        (def answer-to-everything (+ 41 1))
        (def ego "Thomas") ; <- that is me
        (def my-nested-list '(1 2 3 (4 5)))
        (def sex (if (male? ego) 
                     'male
                     'female))
        (def my-sum (lambda (x*) (apply + x)))
        (def (my-sum-2 x*)
            (def local-fn +)
            (def (my-add1 x) (+ x 1))
            (apply local-fn x))
        """

        parser = Parser(Source(code))
        ast = parser.program()

        assert ast is not None

        ast.accept(AstPrinter())

    def test_struct(self):

        code = """
        (def-struct Person (name first-name sex))
        """

        ast = Parser(Source(code)).program()

        assert ast is not None

        ast.accept(AstPrinter())
