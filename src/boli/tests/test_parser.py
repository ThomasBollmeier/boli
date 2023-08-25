from boli.parser import Parser
from boli.source import Source
#import pytest


class TestParser:

    def test_program(self):

        code = """
        (def answer-to-everything 42)
        (def ego "Thomas")
        """

        parser = Parser(Source(code))
        ast = parser.program()

        assert ast is not None
