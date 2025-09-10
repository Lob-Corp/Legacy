import math
from functools import total_ordering

@total_ordering
class Sosa:
    value: int

    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Sosa number must be non-negative")
        self.value = value

    @staticmethod
    def zero() -> 'Sosa':
        return Sosa(0)

    @staticmethod
    def one() -> 'Sosa':
        return Sosa(1)

    def __eq__(self, other):
        if not isinstance(other, Sosa):
            return NotImplemented
        return self.value == other.value

    def __gt__(self, other):
        if not isinstance(other, Sosa):
            return NotImplemented
        return self.value > other.value

    def __add__(self, other):
        return Sosa(self.value + other.value)

    def __sub__(self, other):
        if self.value < other.value:
            raise ValueError("Result would be negative")
        return Sosa(self.value - other.value)

    def __mul__(self, n: int):
        return Sosa(self.value * n)

    def __floordiv__(self, n: int):
        if n == 0:
            raise ZeroDivisionError()
        return Sosa(self.value // n)

    def __mod__(self, n: int):
        if n == 0:
            raise ZeroDivisionError()
        return Sosa(self.value % n)

    def __pow__(self, n: int):
        return Sosa(pow(self.value, n))

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Sosa({self.value})"

    def gen(self) -> int:
        return 0 if self.value == 0 else math.floor(math.log2(self.value)) + 1

    def branches(self) -> list[int]:
        x = self.value
        path = []
        while x > 1:
            path.append(x % 2)
            x //= 2
        return path[::-1]

    @staticmethod
    def of_int(i: int) -> 'Sosa':
        return Sosa(i)

    @staticmethod
    def of_string(s: str) -> 'Sosa':
        return Sosa(int(s))

    def to_string_sep(self, sep: str) -> str:
        s = str(self.value)
        parts = []
        while s:
            parts.append(s[-3:])
            s = s[:-3]
        return sep.join(reversed(parts))

    def father(self) -> 'Sosa':
        if (self.value == 0):
            raise ValueError("Zero has no father")
        return Sosa(self.value * 2)

    def mother(self) -> 'Sosa':
        if (self.value == 0):
            raise ValueError("Zero has no mother")
        return Sosa(self.value * 2 + 1)

    def child(self) -> 'Sosa':
        if self.value <= 1:
            raise ValueError("Sosa(0) and Sosa(1) have no child")
        return Sosa(self.value // 2)

