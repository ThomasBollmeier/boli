from boli.frontend.source import Source
from boli.frontend.buffered_stream import BufferedStream


def test_peek():
    source = create_buf_source()
    ch = source.peek()
    assert ch == "1"


def create_buf_source():
    content = "123456789"
    return BufferedStream(Source(content))
