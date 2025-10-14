"""Date parsing functionality for GeneWeb files.

Handles parsing of dates with various precision markers, calendars, and ranges.
"""

from typing import Any, Optional, List, Tuple, Sequence

from libraries.date import (
    CompressedDate,
    Calendar,
    DateValue,
    CalendarDate,
    Sure,
    About,
    Maybe,
    Before,
    After,
    OrYear,
    YearInt,
    PrecisionBase,
)


def date_of_string_py(s: str, start: int = 0) -> Optional[CompressedDate]:
    """Faithful port of OCaml date_of_string.

    Returns CalendarDate or textual date (str) or None.
    Supports:
    - Precision markers: ~, ?, <, >
    - Date formats: year, month/year, day/month/year
    - OrYear (|) and YearInt (..) ranges
    - Calendar suffixes: G (Gregorian), J (Julian), F (French), H (Hebrew)
    - Text dates in format: 0(text here)
    """
    i_ref = start

    def champ(i: int) -> tuple[int, int]:
        neg = False
        if i < len(s) and s[i] == '-':
            neg = True
            i += 1
        n = 0
        while i < len(s) and s[i].isdigit():
            n = 10 * n + (ord(s[i]) - 48)
            i += 1
        return (-n if neg else n, i)

    def skip_slash(i: int) -> Optional[int]:
        if i < len(s) and s[i] == '/':
            return i + 1
        return None

    if i_ref >= len(s):
        return None

    # precision
    c = s[i_ref]
    if c == '~':
        precision: PrecisionBase = About()
        i_ref += 1
    elif c == '?':
        precision = Maybe()
        i_ref += 1
    elif c == '>':
        precision = After()
        i_ref += 1
    elif c == '<':
        precision = Before()
        i_ref += 1
    else:
        precision = Sure()

    undefined = False
    year, i_ref2 = champ(i_ref)
    if i_ref2 == i_ref + 1 and s[i_ref] == '0':
        undefined = True
    i_ref = i_ref2

    def error(n: int) -> None:
        raise ValueError(f'date_of_string{n} {s}')

    def dmy2(year2: int, i: int) -> tuple[tuple[int, int, int], int]:
        maybe = skip_slash(i)
        if maybe is not None:
            i = maybe
            month2 = year2
            year2, i = champ(i)
            maybe2 = skip_slash(i)
            if maybe2 is not None:
                i = maybe2
                day2 = month2
                month2 = year2
                year2, i = champ(i)
                if month2 < 1 or month2 > 12:
                    error(2)
                if day2 < 1 or day2 > 31:
                    error(3)
                return (day2, month2, year2), i
            if month2 < 1 or month2 > 12:
                error(4)
            return (0, month2, year2), i
        return (0, 0, year2), i

    date: Optional[Tuple[Any, int]]
    maybe = skip_slash(i_ref)
    if maybe is not None:
        i_ref = maybe
        month = year
        year, i_ref = champ(i_ref)
        maybe2 = skip_slash(i_ref)
        if maybe2 is not None:
            i_ref = maybe2
            day = month
            month = year
            year, i_ref = champ(i_ref)
            if month < 1 or month > 12:
                error(2)
            if day < 1 or day > 31:
                error(3)
            dv = DateValue(
                day=day,
                month=month,
                year=year,
                prec=precision,
                delta=0)
            date = (CalendarDate(dv, Calendar.GREGORIAN), i_ref)
        else:
            if year == 0:
                date = None
            elif month < 1 or month > 12:
                error(4)
            else:
                dv = DateValue(
                    day=0,
                    month=month,
                    year=year,
                    prec=precision,
                    delta=0)
                date = (CalendarDate(dv, Calendar.GREGORIAN), i_ref)
    else:
        if undefined:
            if i_ref == len(s):
                date = None
            elif s[i_ref] == '(' and s[-1] == ')':
                inner = s[i_ref + 1: len(s) - 1].strip()
                inner = inner.replace('_', ' ')
                date = (inner, len(s))
            else:
                raise ValueError(f'date_of_string {s}')
        else:
            dv = DateValue(day=0, month=0, year=year, prec=precision, delta=0)
            date = (CalendarDate(dv, Calendar.GREGORIAN), i_ref)

    # OrYear / YearInt
    if date is not None and isinstance(date[0], CalendarDate):
        from dataclasses import replace
        caldate, idx = date
        if idx < len(s) and s[idx] == '|':
            year2, j = champ(idx + 1)
            (d2, m2, y2), j = dmy2(year2, j)
            dv2 = DateValue(day=d2, month=m2, year=y2, prec=None, delta=0)
            # Replace frozen dataclass instead of modifying
            new_dmy = replace(caldate.dmy, prec=OrYear(dv2))
            caldate = replace(caldate, dmy=new_dmy)
            date = (caldate, j)
        elif idx + 1 < len(s) and s[idx:idx + 2] == '..':
            year2, j = champ(idx + 2)
            (d2, m2, y2), j = dmy2(year2, j)
            dv2 = DateValue(day=d2, month=m2, year=y2, prec=None, delta=0)
            # Replace frozen dataclass instead of modifying
            new_dmy = replace(caldate.dmy, prec=YearInt(dv2))
            caldate = replace(caldate, dmy=new_dmy)
            date = (caldate, j)

    # Calendar suffix
    if date is not None and isinstance(date[0], CalendarDate):
        from dataclasses import replace
        caldate, idx = date
        if idx < len(s):
            suf = s[idx]
            if suf == 'G':
                caldate = replace(caldate, cal=Calendar.GREGORIAN)
                idx += 1
            elif suf == 'J':
                caldate = replace(caldate, cal=Calendar.JULIAN)
                idx += 1
            elif suf == 'F':
                caldate = replace(caldate, cal=Calendar.FRENCH)
                idx += 1
            elif suf == 'H':
                caldate = replace(caldate, cal=Calendar.HEBREW)
                idx += 1
            date = (caldate, idx)

    if date is None:
        return None
    dt, idx = date
    if idx != len(s):
        raise ValueError(f'date_of_string5 {s}')
    return dt


def get_optional_date(
        tokens: Sequence[str]) -> Tuple[Optional[CompressedDate], List[str]]:
    """Extract an optional date from token list.

    Args:
        tokens: Token sequence

    Returns:
        Tuple of (date, remaining_tokens)
    """
    if not tokens:
        return None, []
    t0 = tokens[0]
    if not t0:
        return None, list(tokens)
    if t0[0] in ('~', '?', '<', '>', '-', '0', '1', '2',
                 '3', '4', '5', '6', '7', '8', '9'):
        try:
            dt = date_of_string_py(t0, 0)
            if dt is not None:
                return dt, list(tokens[1:])
        except Exception:
            pass  # fall through if parsing fails
    if t0.startswith('!'):
        # explicit absence retains token
        return None, list(tokens)
    return None, list(tokens)
