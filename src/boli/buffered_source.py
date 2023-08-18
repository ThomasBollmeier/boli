class BufferedSource:

    def __init__(self, source):
        self._source = source
        self._buffer = []

    def advance(self):
        if self._buffer:
            return self._buffer.pop(0)
        else:
            return self._source.advance()

    def peek(self, n=1):
        idx = n - 1
        if idx >= len(self._buffer):
            self._fill_buffer(idx)
        if idx < len(self._buffer):
            return self._buffer[idx]
        else:
            return None

    def peek_many(self, n=1):
        idx = n - 1
        if idx >= len(self._buffer):
            self._fill_buffer(idx)
        if idx < len(self._buffer):
            return self._buffer[:n]
        else:
            return self._buffer[:]

    def _fill_buffer(self, new_size):
        size = len(self._buffer)
        while size <= new_size:
            ch = self._source.advance()
            if ch is None:
                break
            self._buffer.append(ch)
            size += 1
