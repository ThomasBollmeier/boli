from boli.parser import Parser
from boli.source import Source
#import pytest


class TestParser:

    def test_program(self):

        code = """
        (def answer-to-everything 42)
        (def ego "Thomas") ; <- that is me
        (def my-list '(1 2 3))
        """

        parser = Parser(Source(code))
        ast = parser.program()

        assert ast is not None
