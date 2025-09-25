class Buffer:
    """
    Buffer provides a mutable byte storage with dynamic resizing.
    It allows storing single characters or strings at arbitrary positions,
    and retrieving the stored content as a string.
    """

    def __init__(self, capacity: int = 80):
        """
        Initialize the buffer with a given capacity.

        Args:
            capacity (int): Initial size of the buffer in bytes. Default is 80.
        """
        self._buff = bytearray(capacity)
        self._len = 0

    @property
    def buff(self) -> bytearray:
        """
        Get the underlying bytearray buffer.

        Returns:
            bytearray: The internal buffer.
        """
        return self._buff

    def _ensure_capacity(self, target_len: int):
        """
        Ensure the buffer has at least target_len capacity.

        Args:
            target_len (int): Required minimum length of the buffer.
        """
        if target_len > len(self._buff):
            grow = max(len(self._buff), target_len - len(self._buff))
            self._buff.extend(b'\x00' * grow)

    def store(self, pos: int, c: str) -> int:
        """
        Store a single character at the specified position.

        Args:
            pos (int): Position to store the character.
            c (str): Character to store.

        Returns:
            int: Next position after the stored character.
        """
        if pos >= len(self._buff):
            self._ensure_capacity(pos + 1)
        self._buff[pos] = ord(c)
        self._len = max(self._len, pos + 1)
        return pos + 1

    def mstore(self, pos: int, s: str) -> int:
        """
        Store an entire string starting at the specified position.

        Args:
            pos (int): Position to start storing the string.
            s (str): String to store.

        Returns:
            int: Next position after the stored string.
        """
        return self.gstore(pos, s, 0, len(s))

    def gstore(self, pos: int, s: str, si: int, slen: int) -> int:
        """
        Store a slice of a string at the specified position.

        Args:
            pos (int): Position to start storing.
            s (str): Source string.
            si (int): Start index in the source string.
            slen (int): Length of the slice to store.

        Returns:
            int: Next position after the stored slice.
        """
        slice_bytes = s[si:si+slen].encode()
        end = pos + len(slice_bytes)
        self._ensure_capacity(end)
        self._buff[pos:end] = slice_bytes
        self._len = max(self._len, end)
        return end

    def get(self) -> str:
        """
        Retrieve the current contents of the buffer as a string.

        Returns:
            str: Decoded string from the buffer.
        """
        return self.buff[:self._len].decode()