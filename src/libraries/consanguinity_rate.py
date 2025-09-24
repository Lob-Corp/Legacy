class ConsanguinityRate():
    def __init__(self, fix_value: int):
        """Class to represent consanguinity rate with a fix value.
        Equivalent to from_int."""
        self.__fix_value = fix_value

    @staticmethod
    def from_rate(rate: float) -> 'ConsanguinityRate':
        """Create a ConsanguinityRate from a float rate."""
        fix_value = int((rate * 1000000.0) + 0.5)
        return ConsanguinityRate(fix_value)

    @staticmethod
    def from_integer(value: int) -> 'ConsanguinityRate':
        """Create a ConsanguinityRate from an integer value.
        It is the rate * 1000000."""
        return ConsanguinityRate(value)

    def rate(self) -> float:
        """Return the consanguinity rate itself as a float."""
        return float(self.__fix_value) / 1000000.0

    def __int__(self) -> int:
        """Return the integer representation of the fix value."""
        return self.__fix_value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConsanguinityRate):
            raise TypeError(
                "Can only compare ConsanguinityRate with ConsanguinityRate")
        return self.__fix_value == other.__fix_value

    def __ne__(self, value: object) -> bool:
        return not self.__eq__(value)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, ConsanguinityRate):
            raise TypeError(
                "Can only compare ConsanguinityRate with ConsanguinityRate")
        return self.__fix_value > other.__fix_value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ConsanguinityRate):
            raise TypeError(
                "Can only compare ConsanguinityRate with ConsanguinityRate")
        return self.__fix_value < other.__fix_value

    def __ge__(self, other: object) -> bool:
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other: object) -> bool:
        return self.__lt__(other) or self.__eq__(other)
