class BufferedSource:

    def __init__(self, source):
        self._source = source
        self._buffer = []

    def next_char(self):
        if self._buffer:
            return self._buffer.pop(0)
        else:
            return self._source.next_char()

    def peek(self, n=1):
        idx = n - 1
        if idx >= len(self._buffer):
            size = len(self._buffer)
            while size <= idx:
                ch = self._source.next_char()
                if ch is None:
                    break
                self._buffer.append(ch)
                size += 1
        if idx < len(self._buffer):
            return self._buffer[idx]
        else:
            return None


if __name__ == "__main__":

    from source import Source

    buf_source = BufferedSource(Source("1234567890"))

    print(buf_source.peek())
    print(buf_source.next_char())
    print(buf_source.peek(), buf_source.peek(2))
    while True:
        ch = buf_source.next_char()
        if ch is None:
            break
        print(ch)