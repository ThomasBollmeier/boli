from boli.frontend.parser import Parser
from boli.frontend.source import Source
from boli.frontend.ast_printer import AstPrinter


class TestParser:

    def test_program(self):

        code = """
        (def nothing nil)
        (def answer-to-everything (+ 41 1))
        (def ego "Thomas") ; <- that is me
        (def my-nested-list '(1 2 3 (4 5)))
        (def sex (if (male? ego) 
                     'male
                     'female))
        (def my-add1 (lambda (x) (+ x 1)))
        (def (my-sum numbers...)
            (+ ...numbers))
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

    def test_vararg(self):

        code = """
        (def (sum args...)
            (+ ...args))
        """

        ast = Parser(Source(code)).program()

        assert ast is not None

        ast.accept(AstPrinter())

    def test_block(self):

        code = """
        (if (= 42 (+ 41 1))
            (block
                (do-first-thing "Foo")
                (do-something-else "Bar"))
            nil)
        """

        ast = Parser(Source(code)).expression()

        assert ast is not None

        ast.accept(AstPrinter())

    def test_tail_call(self):

        code = """
        (def (fac n)
            (def (fac-helper n acc)
                (if (= n 0)
                    acc
                    (block
                        (writeln acc)
                        (fac-helper (- n 1) (* n acc)))))
            (fac-helper n 1))
        """

        ast = Parser(Source(code)).program()

        assert ast is not None

        ast.accept(AstPrinter())
