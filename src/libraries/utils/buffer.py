class Buffer:
    def __init__(self, capacity: int=80):
        self._buff = bytearray(capacity)
        self._len = 0
    
    @property
    def buff(self):
        return self._buff

    def _ensure_capacity(self, target_len):
        if target_len > len(self._buff):
            grow = max(len(self._buff), target_len - len(self._buff))
            self._buff.extend(b'\x00' * grow)

    def store(self, pos, c):
        if pos >= len(self._buff):
            self._ensure_capacity(pos + 1)
        self._buff[pos] = ord(c)
        self._len = max(self._len, pos + 1)
        return pos + 1

    def mstore(self, pos: int, s: str) -> int:
        return self.gstore(pos, s, 0, len(s))

    def gstore(self, pos, s, si, slen) -> int:
        slice_bytes = s[si:si+slen].encode()
        end = pos + len(slice_bytes)
        self._ensure_capacity(end)
        self._buff[pos:end] = slice_bytes
        self._len = max(self._len, end)
        return end

    def get(self) -> str:
        return self.buff[:self._len].decode()
