import math
from functools import total_ordering

@total_ordering
class Sosa:
    """
    Represents a Sosa number in genealogy, used to identify individuals in an ancestry tree.

    Attributes:
        value (int): The Sosa number (must be non-negative).
    """

    value: int

    def __init__(self, value: int):
        """
        Initialize a Sosa number.
        Args:
            value (int): The Sosa number (must be non-negative).
        Raises:
            ValueError: If value is negative.
        """
        if value < 0:
            raise ValueError("Sosa number must be non-negative")
        self.value = value

    @staticmethod
    def zero() -> 'Sosa':
        """Return the root Sosa (0)."""
        return Sosa(0)

    @staticmethod
    def one() -> 'Sosa':
        """Return the first ancestor Sosa (1)."""
        return Sosa(1)

    def __eq__(self, other):
        """Check equality with another Sosa number."""
        if not isinstance(other, Sosa):
            return NotImplemented
        return self.value == other.value

    def __gt__(self, other):
        """Check if this Sosa number is greater than another."""
        if not isinstance(other, Sosa):
            return NotImplemented
        return self.value > other.value

    def __add__(self, other):
        """Add two Sosa numbers."""
        return Sosa(self.value + other.value)

    def __sub__(self, other):
        """Subtract another Sosa number from this one."""
        if self.value < other.value:
            raise ValueError("Result would be negative")
        return Sosa(self.value - other.value)

    def __mul__(self, n: int):
        """Multiply Sosa number by an integer."""
        return Sosa(self.value * n)

    def __floordiv__(self, n: int):
        """Integer division of Sosa number by n."""
        if n == 0:
            raise ZeroDivisionError()
        return Sosa(self.value // n)

    def __mod__(self, n: int):
        """Modulo operation for Sosa number."""
        if n == 0:
            raise ZeroDivisionError()
        return Sosa(self.value % n)

    def __pow__(self, n: int):
        """Raise Sosa number to the power n."""
        return Sosa(pow(self.value, n))

    def __str__(self):
        """Return string representation of Sosa number."""
        return str(self.value)

    def __repr__(self):
        """Return detailed string representation of Sosa object."""
        return f"Sosa({self.value})"

    def gen(self) -> int:
        """
        Return the generation number for this Sosa.
        Returns:
            int: Generation number (0 for root).
        """
        return 0 if self.value == 0 else math.floor(math.log2(self.value)) + 1

    def branches(self) -> list[int]:
        """
        Return the path from root to this Sosa as a list of 0/1.
        Returns:
            list[int]: Path to this Sosa.
        """
        x = self.value
        path = []
        while x > 1:
            path.append(x % 2)
            x //= 2
        return path[::-1]

    @staticmethod
    def of_int(i: int) -> 'Sosa':
        """Create a Sosa from an integer."""
        return Sosa(i)

    @staticmethod
    def of_string(s: str) -> 'Sosa':
        """Create a Sosa from a string."""
        return Sosa(int(s))

    def to_string_sep(self, sep: str) -> str:
        """
        Return the Sosa number as a string with a separator every 3 digits.
        Args:
            sep (str): Separator string.
        Returns:
            str: Formatted Sosa number.
        """
        s = str(self.value)
        parts = []
        while s:
            parts.append(s[-3:])
            s = s[:-3]
        return sep.join(reversed(parts))

    def father(self) -> 'Sosa':
        """
        Return the Sosa number of the father.
        Raises:
            ValueError: If Sosa is zero.
        """
        if (self.value == 0):
            raise ValueError("Zero has no father")
        return Sosa(self.value * 2)

    def mother(self) -> 'Sosa':
        """
        Return the Sosa number of the mother.
        Raises:
            ValueError: If Sosa is zero.
        """
        if (self.value == 0):
            raise ValueError("Zero has no mother")
        return Sosa(self.value * 2 + 1)

    def child(self) -> 'Sosa':
        """
        Return the Sosa number of the child.
        Raises:
            ValueError: If Sosa is 0 or 1.
        """
        if self.value <= 1:
            raise ValueError("Sosa(0) and Sosa(1) have no child")
        return Sosa(self.value // 2)
