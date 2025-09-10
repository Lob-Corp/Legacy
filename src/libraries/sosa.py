import math

class Sosa:
    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Sosa number must be non-negative")
        self.value = value

    @staticmethod
    def zero():
        return Sosa(0)

    @staticmethod
    def one():
        return Sosa(1)

    def eq(self, other):
        return self.value == other.value

    def gt(self, other):
        return self.value > other.value

    def compare(self, other):
        return (self.value > other.value) - (self.value < other.value)

    def add(self, other):
        return Sosa(self.value + other.value)

    def sub(self, other):
        if self.value < other.value:
            raise ValueError("Result would be negative")
        return Sosa(self.value - other.value)

    def twice(self):
        return Sosa(self.value * 2)

    def half(self):
        return Sosa(self.value // 2)

    def even(self):
        return self.value % 2 == 0

    def inc(self, increment: int):
        return Sosa(self.value + increment)

    def mul(self, n: int):
        return Sosa(self.value * n)

    def exp(self, n: int):
        return Sosa(pow(self.value, n))

    def div(self, n: int):
        if n == 0:
            raise ZeroDivisionError()
        return Sosa(self.value // n)

    def modl(self, n: int):
        if n == 0:
            raise ZeroDivisionError()
        return Sosa(self.value % n)

    def gen(self):
        if self.value == 0:
            return 0
        return math.floor(math.log2(self.value)) + 1

    def branches(self):
        x = self.value
        path = []
        while x > 1:
            path.append(x % 2)
            x //= 2
        return path[::-1]

    @staticmethod
    def of_int(i: int):
        return Sosa(i)

    @staticmethod
    def of_string(s: str):
        return Sosa(int(s))

    def to_string(self):
        return str(self.value)

    def to_string_sep(self, sep: str):
        s = str(self.value)
        parts = []
        while s:
            parts.append(s[-3:])
            s = s[:-3]
        return sep.join(reversed(parts))
