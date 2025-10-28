"""Line stream for parsing GeneWeb files.

Provides lookahead and pushback capabilities for line-based parsing.
"""

from typing import Iterator, Optional, Iterable
from collections import deque


def iter_strip_lines(lines: Iterable[str]) -> Iterator[str]:
    """Strip and filter empty lines from input."""
    for raw in lines:
        line = raw.rstrip('\r\n')
        if not line:
            continue
        yield line


class LineStream:
    """Lookahead + pushback capable line stream over pre-filtered lines."""

    def __init__(self, source: Iterator[str]):
        self._src = source
        self._buf: deque[str] = deque()

    def peek(self) -> Optional[str]:
        """Look at next line without consuming it."""
        if not self._buf:
            try:
                nxt = next(self._src)
            except StopIteration:
                return None
            self._buf.appendleft(nxt)
        return self._buf[0]

    def pop(self) -> Optional[str]:
        """Consume and return next line."""
        if self._buf:
            return self._buf.popleft()
        try:
            return next(self._src)
        except StopIteration:
            return None

    def push_back(self, line: str) -> None:
        """Push a line back onto the stream."""
        self._buf.appendleft(line)

    def __iter__(self) -> 'LineStream':
        return self

    def __next__(self) -> str:
        nxt = self.pop()
        if nxt is None:
            raise StopIteration
        return nxt
