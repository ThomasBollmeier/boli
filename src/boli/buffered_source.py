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
