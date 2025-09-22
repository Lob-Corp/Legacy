from __future__ import annotations
from dataclasses import dataclass

from date.calendar_date import Calendar, CalendarDate, DateValue
from exception import NotComparable
# --- Compression & uncompression --- #

@dataclass(frozen=True)
class CDate:
    cdate: tuple[Calendar, int] | Date | str | None

    def cdate_to_date(self) -> Date:
        match self.cdate:
            case (Calendar.GREGORIAN, code):
                return CalendarDate(DateValue.uncompress(code), Calendar.GREGORIAN)
            case (Calendar.JULIAN, code):
                return CalendarDate(DateValue.uncompress(code), Calendar.JULIAN)
            case (Calendar.FRENCH, code):
                return CalendarDate(DateValue.uncompress(code), Calendar.FRENCH)
            case (Calendar.HEBREW, code):
                return CalendarDate(DateValue.uncompress(code), Calendar.HEBREW)
            case Date() | str():
                return self.cdate
            case None:
                return None
            case _:
                raise ValueError("Invalid CDate: Cnone")


@dataclass(frozen=True)
class Date:
    """Type representing a date, which can be either a structured CalendarDate or a free-form string."""

    date: CalendarDate | str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Date):
            raise NotComparable(f"Cannot compare Date with {type(other)}")
        if isinstance(self.date, CalendarDate) and isinstance(other.date, CalendarDate):
            return self.date == other.date
        if isinstance(self.date, str) and isinstance(other.date, str):
            return self.date == other.date
        raise NotComparable("Cannot compare CalendarDate with str")

    def date_to_cdate(self) -> CDate:
        match self.date:
            case CalendarDate(dmy, cal):
                compressed = dmy.compress()
                if compressed is not None:
                    return CDate((cal, compressed))
                return CDate(self.date)
            case str():
                return self.date
