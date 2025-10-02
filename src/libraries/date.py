from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Callable, Optional

from libraries.calendar_date import Calendar, CalendarDate
from libraries.exception import NotComparable
from libraries.precision import (
    OrYear,
    PrecisionBase,
    Sure,
    About,
    Maybe,
    Before,
    After,
    YearInt,
)


@dataclass(frozen=True)
class CompressedDate:
    """Compressed date representation optimized for storage and processing.

    Can represent dates in multiple formats:
    - Tuple of (Calendar, int): Compressed calendar-specific date
    - Date object: Full structured date
    - String: Free-form date text
    - None: Unknown/missing date
    """

    cdate: tuple[Calendar, int] | Date | str | None

    def __eq__(self, other) -> bool:
        if not isinstance(other, CompressedDate):
            return False
        return self.cdate == other.cdate

    def map_cdate(
        self, date_mapper: Optional[Callable[[Date], Date]] = None
    ) -> CompressedDate:
        """Transform the date using provided mapper function.

        Args:
            date_mapper: Function to transform Date objects.
            If None, returns self unchanged.

        Returns:
            New CompressedDate with transformed date,or original
            if no mapper provided
        """
        if date_mapper is None:
            return self
        date = self.cdate_to_date()
        if date is None:
            return date
        return date_mapper(date).date_to_cdate()

    def cdate_to_date(self) -> Date:
        """Convert compressed date to full Date representation.

        Decompresses calendar-specific integer codes back to DateValue objects
        and wraps them in appropriate CalendarDate structures.

        Returns:
            Date object represented with the same compressed date information

        Raises:
            ValueError: If the compressed date format is invalid
        """
        match self.cdate:
            case (Calendar.GREGORIAN, code) if isinstance(code, int):
                return Date(
                    CalendarDate(
                        DateValue.uncompress(code), Calendar.GREGORIAN
                    )
                )
            case (Calendar.JULIAN, code) if isinstance(code, int):
                return Date(
                    CalendarDate(DateValue.uncompress(code), Calendar.JULIAN)
                )
            case (Calendar.FRENCH, code) if isinstance(code, int):
                return Date(
                    CalendarDate(DateValue.uncompress(code), Calendar.FRENCH)
                )
            case (Calendar.HEBREW, code) if isinstance(code, int):
                return Date(
                    CalendarDate(DateValue.uncompress(code), Calendar.HEBREW)
                )
            case Date():
                return self.cdate
            case str():
                return Date(self.cdate)
            case _:
                raise ValueError("Invalid CompressedDate: None")


@dataclass(frozen=True)
class Date:
    """Type representing a date, which can be either a structured CalendarDate
    or a free-form string."""

    date: CalendarDate | str

    def __eq__(self, other) -> bool:
        if not isinstance(other, Date):
            print(f"AAA - {type(self)} vs {type(other)}")
            raise NotComparable(f"Cannot compare Date with {type(other)}")
        if isinstance(self.date, CalendarDate) and isinstance(
            other.date, CalendarDate
        ):
            return self.date == other.date
        if isinstance(self.date, str) and isinstance(other.date, str):
            return self.date == other.date
        raise NotComparable("Cannot compare CalendarDate with str")

    def date_to_cdate(self) -> CompressedDate:
        """Convert Date back to compressed representation for storage.

        Attempts to compress structured CalendarDate to integer format
        if possible, otherwise stores as-is.

        Returns:
            CompressedDate with the same date information in compressed form
        """
        if isinstance(self.date, CalendarDate):
            compressed = self.date.dmy.compress()
            if compressed is not None:
                return CompressedDate((self.date.cal, compressed))
            return CompressedDate(self)
        return CompressedDate(self.date)


@dataclass(frozen=True)
class DateValue:
    """
    Represents a specific date with day, month, year and precision information.
    Core date structure that handles uncertain dates, different precision
    levels, and comparison operations. Day/month values of 0 indicate unknown
    components.
    """

    day: int
    month: int
    year: int
    prec: Optional[PrecisionBase]
    delta: int = 0

    def __eq__(self, other) -> bool:
        """Check equality by comparing dates, raising error
        if not comparable."""
        result = self.compare(other)
        if result is None:
            raise NotComparable("Dates not comparable")
        return result == 0

    def compare(self, other: DateValue, strict: bool = False) -> Optional[int]:
        """Compare two DateValue objects with precision awareness.

        Args:
            other: DateValue to compare against
            strict: If True, incompatible precision combinations return None

        Returns:
            -1 if self < other,
            0 if equal,
            1 if self > other,
            None if incomparable

        Raises:
            NotComparable: If comparing with non-DateValue object
        """
        if not isinstance(other, DateValue):
            raise NotComparable(f"Cannot compare DateValue with {type(other)}")

        if self.year == other.year:
            return self.__compare_month_or_day(False, strict, self, other)

        return self.__eval_strict(
            strict,
            (self.year > other.year) - (self.year < other.year),
            self,
            other,
        )

    def __eval_strict(
        self,
        strict: bool,
        comparison: int,
        from_date: DateValue,
        to_date: DateValue,
    ) -> Optional[int]:
        if strict:
            if comparison == -1 and (
                isinstance(from_date.prec, After)
                or isinstance(to_date.prec, Before)
            ):
                return None
            if comparison == 1 and (
                isinstance(from_date.prec, Before)
                or isinstance(to_date.prec, After)
            ):
                return None
            return comparison
        return comparison

    def __compare_prec(
        self, strict: bool, from_date: DateValue, to_date: DateValue
    ) -> Optional[int]:
        if isinstance(from_date.prec, (Sure, About, Maybe)) and isinstance(
            to_date.prec, (Sure, About, Maybe)
        ):
            return 0
        if from_date.prec == to_date.prec and isinstance(
            from_date.prec, (After, Before)
        ):
            return 0
        if type(from_date.prec) is type(to_date.prec) and isinstance(
            from_date.prec, (OrYear, YearInt)
        ):
            a = replace(from_date, prec=Sure())
            b = replace(to_date, prec=Sure())
            return a.compare(b, strict)
        if isinstance(from_date.prec, Before) or isinstance(
            to_date.prec, After
        ):
            return -1
        if isinstance(from_date.prec, After) or isinstance(
            to_date.prec, Before
        ):
            return 1
        return 0

    def __compare_month_or_day(
        self,
        is_day: bool,
        strict: bool,
        from_date: DateValue,
        to_date: DateValue,
    ) -> Optional[int]:
        """Compare months first, then days, using prec if needed."""

        def compare_with_unknown_value(unknown_value, known_value):
            match unknown_value.prec:
                case After():
                    return 1
                case Before():
                    return -1
                case _:
                    return (
                        self.__compare_prec(strict, unknown_value, known_value)
                        if not strict
                        else None
                    )

        if is_day:
            x, y = from_date.day, to_date.day

            def func(strict, fd, td):
                return self.__compare_prec(strict, fd, td)

        else:
            x, y = from_date.month, to_date.month

            def func(strict, fd, td):
                return self.__compare_month_or_day(True, strict, fd, td)

        match (x, y):
            case (0, 0):
                return self.__compare_prec(strict, from_date, to_date)
            case (0, _):
                return compare_with_unknown_value(from_date, to_date)
            case (_, 0):
                res = compare_with_unknown_value(to_date, from_date)
                return -res if res is not None else None
            case _:
                match (x > y) - (x < y):
                    case 0:
                        return func(strict, from_date, to_date)
                    case comparison:
                        return self.__eval_strict(
                            strict, comparison, from_date, to_date
                        )

    def compress(self) -> Optional[int]:
        """Compress a concrete date into an integer for efficient storage.

        Only compresses dates with simple precision types and valid ranges
        (year 1-2499, non-negative day/month, no delta offset).

        Returns:
            Compressed integer representation, or None if not compressible
        """
        simple = (
            isinstance(self.prec, (Sure, About, Maybe, Before, After))
            and self.day >= 0
            and self.month >= 0
            and 0 < self.year < 2500
            and self.delta == 0
        )
        if simple:
            if self.prec is None:
                p = 0
            else:
                p = {About: 1, Maybe: 2, Before: 3, After: 4}.get(
                    type(self.prec), 0
                )
            return (
                ((((p * 32) + self.day) * 13) + self.month) * 2500
            ) + self.year
        return None

    @staticmethod
    def uncompress(x: int) -> DateValue:
        """Decompress integer back to DateValue.

        Reverses the compression algorithm to extract day, month, year,
        and precision information from the packed integer format.

        Args:
            x: Compressed integer representation

        Returns:
            DateValue with extracted date components and precision
        """
        year, x = x % 2500, x // 2500
        month, x = x % 13, x // 13
        day, x = x % 32, x // 32
        prec = {1: About, 2: Maybe, 3: Before, 4: After}.get(x, Sure)()
        return DateValue(day, month, year, prec)

    @staticmethod
    def _combine_precision(
        p1: Optional[PrecisionBase], p2: Optional[PrecisionBase]
    ) -> PrecisionBase:
        """Combine two precision values into a single precision level.

        Used when performing operations on dates with different precision
        levels to determine the appropriate precision for the result.

        Args:
            p1: First precision level
            p2: Second precision level

        Returns:
            Combined precision level based on the uncertainty rules
        """
        if isinstance(p1, Sure) and isinstance(p2, Sure):
            return Sure()
        if isinstance(p1, (Maybe, Sure, About)) and isinstance(
            p2, (Maybe, Sure, About)
        ):
            return Maybe()
        if isinstance(p1, (About, Maybe, Sure, Before)) and isinstance(
            p2, (After, Sure, Maybe, About)
        ):
            return After()
        if isinstance(p1, (About, Maybe, Sure, After)) and isinstance(
            p2, (Before, Sure, Maybe, About)
        ):
            return Before()
        return Maybe()

    @staticmethod
    def _sdn_of_date(d: DateValue) -> int:
        """Calculate Serial Day Number (SDN) for a fully specified date.

        Uses the standard Julian Day Number algorithm for Gregorian calendar.
        Requires complete day/month/year information (no zero values).

        Args:
            d: DateValue with complete date information

        Returns:
            Serial day number for astronomical/chronological calculations

        Raises:
            ValueError: If day, month, or year are zero/unknown
        """
        if d.day <= 0 or d.month <= 0 or d.year == 0:
            raise ValueError("Cannot compute SDN for unknown day/month/year")

        a = (14 - d.month) // 12
        y = d.year + 4800 - a
        m = d.month + 12 * a - 3
        jdn = (
            d.day
            + ((153 * m + 2) // 5)
            + 365 * y
            + y // 4
            - y // 100
            + y // 400
            - 32045
        )
        return jdn

    @staticmethod
    def date_difference(
        from_date: DateValue, to_date: DateValue
    ) -> Optional[DateValue]:
        """Calculate the difference between two dates.

        Computes approximate years, months, and days between dates using
        simple 365-day years and 30-day months. Combines precision levels
        to determine result uncertainty.

        Args:
            from_date: Starting date
            to_date: Ending date

        Returns:
            DateValue representing the time difference, or None if incomparable
        """
        if from_date.prec == to_date.prec and isinstance(
            from_date.prec, (Before, After)
        ):
            return None
        prec = DateValue._combine_precision(from_date.prec, to_date.prec)
        delta_days = DateValue._sdn_of_date(to_date) - DateValue._sdn_of_date(
            from_date
        )

        years = delta_days // 365
        months = (delta_days % 365) // 30
        days = (delta_days % 365) % 30

        return DateValue(days, months, years, prec)
