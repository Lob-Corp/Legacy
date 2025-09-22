from __future__ import annotations
from dataclasses import dataclass, replace
from enum import Enum

import math
from typing import Optional
from date.precision import OrYear, Precision, Sure, About, Maybe, Before, After, YearInt
from exception import NotComparable


class Calendar(Enum):
    GREGORIAN = "gregorian"
    JULIAN = "julian"
    FRENCH = "french"
    HEBREW = "hebrew"


@dataclass(frozen=True)
class CalendarDate:
    dmy: DateValue
    cal: Calendar

    # def __eq__(self, other) -> bool:
    #     if not isinstance(other, CalendarDate):
    #         raise NotComparable(f"Cannot compare CalendarDate with {type(other)}")
    #     return self.dmy == other.dmy


@dataclass(frozen=True)
class DateValue:
    day: int
    month: int
    year: int
    prec: Precision | None
    delta: int = 0

    def __eq__(self, other: DateValue) -> bool:
        result = self.compare(other)
        if result is None:
            raise NotComparable("Dates not comparable")
        return result == 0

    def compare(self, other: DateValue, strict: bool = False) -> Optional[int]:
        if not isinstance(other, DateValue):
            raise NotComparable(f"Cannot compare DateValue with {type(other)}")

        if self.year == other.year:
            return self.__compare_month_or_day(False, strict, self, other)

        return self.__eval_strict(
            strict, (self.year > other.year) - (self.year < other.year), self, other
        )

    def __eval_strict(
        self, strict: bool, comparison: int, from_date: DateValue, to_date: DateValue
    ) -> Optional[int]:
        if strict:
            if comparison == -1 and (
                isinstance(from_date.prec, After) or isinstance(to_date.prec, Before)
            ):
                return None
            if comparison == 1 and (
                isinstance(from_date.prec, Before) or isinstance(to_date.prec, After)
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
        if isinstance(from_date.prec, Before) or isinstance(to_date.prec, After):
            return -1
        if isinstance(from_date.prec, After) or isinstance(to_date.prec, Before):
            return 1
        return 0

    def __compare_month_or_day(
        self, is_day: bool, strict: bool, from_date: DateValue, to_date: DateValue
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
        """Compress a concrete date if possible into an integer."""
        simple = (
            isinstance(self.prec, (Sure, About, Maybe, Before, After))
            and self.day >= 0
            and self.month >= 0
            and 0 < self.year < 2500
            and self.delta == 0
        )
        if simple:
            p = {About: 1, Maybe: 2, Before: 3, After: 4}.get(type(self.prec), 0)
            return (((((p * 32) + self.day) * 13) + self.month) * 2500) + self.year
        return None

    @staticmethod
    def uncompress(x: int) -> DateValue:
        """Decompress integer back to DateValue."""
        year, x = x % 2500, x // 2500
        month, x = x % 13, x // 13
        day, x = x % 32, x // 32
        prec = {1: About, 2: Maybe, 3: Before, 4: After}.get(x, Sure)()
        return DateValue(day, month, year, prec)

    @staticmethod
    def _combine_precision(p1: Precision, p2: Precision) -> Precision:
        # if not isinstance(p1, Before) and not isinstance(p2, After):
        #     return Before()
        # if not isinstance(p1, After) and not isinstance(p2, Before):
        #     return After()
        # if isinstance(p1, (Maybe, Sure, About)) and isinstance(p2, (Maybe, Sure, About)):
        #     return Maybe()
        # if p1 == p2 and isinstance(p1, Sure):
        #     return Sure()
        # return Maybe()
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
        # require fully specified positive day/month/year
        if d.day <= 0 or d.month <= 0 or d.year == 0:
            raise ValueError("Cannot compute SDN for unknown day/month/year")

        # integer algorithm for Gregorian calendar JDN
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
        if from_date.prec == to_date.prec and isinstance(
            from_date.prec, (Before, After)
        ):
            return None
        prec = DateValue._combine_precision(from_date.prec, to_date.prec)
        delta_days = DateValue._sdn_of_date(to_date) - DateValue._sdn_of_date(from_date)

        years = delta_days // 365
        months = (delta_days % 365) // 30
        days = (delta_days % 365) % 30

        return DateValue(days, months, years, prec)
