from ctypes import Union
from dataclasses import dataclass
from enum import Enum


class Calendar(Enum):
    GREGORIAN = "gregorian"
    JULIAN = "julian"
    FRENCH = "french"
    HEBREW = "hebrew"


class Precision:
    def __init__(self):
        raise NotImplementedError(
            "Precision is a base class and cannot be instantiated directly. Use one of its subclasses instead.")


@dataclass(frozen=True)
class DateValue:
    day: int
    month: int
    year: int
    prec: Precision | None
    delta: int

# Precision variants without extra data


class Sure(Precision):
    def __init__(self):
        pass


class About(Precision):
    def __init__(self):
        pass


class Maybe(Precision):
    def __init__(self):
        pass


class Before(Precision):
    def __init__(self):
        pass


class After(Precision):
    def __init__(self):
        pass

# Variants that carry extra data
@dataclass(frozen=True)
class OrYear(Precision):
    date_value: DateValue
    def __post_init__(self):
        if self.date_value.prec is not None:
            raise ValueError(
                "OrYear precision must have None as its precision.")


@dataclass(frozen=True)
class YearInt(Precision):
    date_value: DateValue
    def __post_init__(self):
        if self.date_value.prec is not None:
            raise ValueError(
                "YearInt precision must have None as its precision.")


@dataclass(frozen=True)
class CalendarDate:
    dmy: DateValue
    cal: Calendar


Date = CalendarDate | str
