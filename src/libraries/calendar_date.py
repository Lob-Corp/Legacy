from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from libraries.date import DateValue


class Calendar(Enum):
    GREGORIAN = "GREGORIAN"
    JULIAN = "JULIAN"
    FRENCH = "FRENCH"
    HEBREW = "HEBREW"


@dataclass(frozen=True)
class CalendarDate:
    dmy: "DateValue"
    cal: Calendar
