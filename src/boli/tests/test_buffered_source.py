from boli.source import Source
from boli.buffered_source import BufferedSource


def test_peek():
    source = create_buf_source()
    ch = source.peek()
    assert ch == "1"


def create_buf_source():
    content = "123456789"
    return BufferedSource(Source(content))
