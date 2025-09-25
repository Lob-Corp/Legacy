from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from libraries.date import DateValue

class PrecisionBase:
    def __init__(self):
        raise NotImplementedError(
            "PrecisionBase is a base class and cannot be instantiated directly. Use one of its subclasses instead."
        )

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class Sure(PrecisionBase):
    def __init__(self):
        pass


class About(PrecisionBase):
    def __init__(self):
        pass


class Maybe(PrecisionBase):
    def __init__(self):
        pass


class Before(PrecisionBase):
    def __init__(self):
        pass


class After(PrecisionBase):
    def __init__(self):
        pass


@dataclass(frozen=True)
class OrYear(PrecisionBase):
    date_value: "DateValue"

    def __eq__(self, other):
        return isinstance(other, YearInt) and self.date_value == other.date_value

    def __post_init__(self):
        if self.date_value.prec is not None:
            raise ValueError("OrYear precision must have None as its precision.")


@dataclass(frozen=True)
class YearInt(PrecisionBase):
    date_value: "DateValue"

    def __eq__(self, other):
        return isinstance(other, YearInt) and self.date_value == other.date_value

    def __post_init__(self):
        if self.date_value.prec is not None:
            raise ValueError("YearInt precision must have None as its precision.")
