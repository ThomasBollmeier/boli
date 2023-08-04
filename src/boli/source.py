class Source:

    def __init__(self, content):
        self._content = content
        self._pos = 0
        self._max_pos = len(self._content) - 1

    def next_char(self):
        if self._pos > self._max_pos:
            return None
        ret = self._content[self._pos]
        self._pos += 1
        return ret
