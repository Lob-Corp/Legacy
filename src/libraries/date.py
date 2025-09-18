from dataclasses import dataclass
from enum import Enum
from typing import Tuple, TypeAlias


class Calendar(Enum):
    GREGORIAN = "gregorian"
    JULIAN = "julian"
    FRENCH = "french"
    HEBREW = "hebrew"


class PrecisionBase:
    def __init__(self):
        raise NotImplementedError(
            "PrecisionBase is a base class and cannot be instantiated"
            "directly. Use one of its subclasses instead.")


@dataclass(frozen=True)
class DateValue:
    day: int
    month: int
    year: int
    prec: PrecisionBase | None
    delta: int

# Precision variants without extra data


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

# Variants that carry extra data


@dataclass(frozen=True)
class OrYear(PrecisionBase):
    date_value: DateValue

    def __post_init__(self):
        if self.date_value.prec is not None:
            raise ValueError(
                "OrYear precision must have None as its precision.")


@dataclass(frozen=True)
class YearInt(PrecisionBase):
    date_value: DateValue

    def __post_init__(self):
        if self.date_value.prec is not None:
            raise ValueError(
                "YearInt precision must have None as its precision.")


@dataclass(frozen=True)
class CalendarDate:
    dmy: DateValue
    cal: Calendar


Date: TypeAlias = CalendarDate | str
"""Type representing a date, which can be either a structured CalendarDate
or a free-form string."""

CompressedDate: TypeAlias = Tuple[Calendar, int] | Date | str | None
"""Type representing a compressed date, which can be a Tuple of Calendar
and year, a structured Date, a free-form string, or None."""
