from typing import Optional
from date.precision import After, Before, OrYear, Sure, About, Maybe, YearInt
from dataclasses import replace
from date.calendar_date import DateValue

def eval_strict(strict: bool, d1: DateValue, d2: DateValue, x: int) -> Optional[int]:
    if strict:
        if x == -1 and (isinstance(d1.prec, After) or isinstance(d2.prec, Before)):
            return None
        if x == 1 and (isinstance(d1.prec, Before) or isinstance(d2.prec, After)):
            return None
    print(isinstance(d1.prec, Before))
    return x

# def compare date(strict: bool=false, d1: DateValue, d2: DateValue) -> int:

def compare_date_value_opt(strict: bool, d1: DateValue, d2: DateValue) -> Optional[int]:
    if d1.year == d2.year:
        return compare_month_or_day(False, strict, d1, d2)
    return eval_strict(strict, d1, d2, (d1.year > d2.year) - (d1.year < d2.year))

def compare_prec(strict: bool, d1: DateValue, d2: DateValue) -> Optional[int]:
    if isinstance(d1.prec, (Sure, About, Maybe)) and isinstance(
        d2.prec, (Sure, About, Maybe)
    ):
        return 0
    if d1.prec == d2.prec and isinstance(d1.prec, (After, Before)):
        return 0
    if d1.prec == d2.prec and isinstance(d1.prec, (OrYear, YearInt)):
        return compare_date_value_opt(strict, replace(d1, prec=Sure), replace(d2, prec=Sure))
    if isinstance(d1.prec, Before) or isinstance(d2.prec, After):
        return -1
    if isinstance(d1.prec, After) or isinstance(d2.prec, Before):
        return 1
    return 0



def compare_month_or_day(is_day: bool, strict: bool, d1: DateValue, d2: DateValue) -> Optional[int]:

    def compare_with_unknown(unknown: DateValue, known: DateValue) -> Optional[int]:
        if isinstance(unknown.prec, After):
            return 1
        if isinstance(unknown.prec, Before):
            return -1
        return compare_prec(False, unknown, known) if not strict else None

    # select value to compare and next step
    if is_day:
        x, y, next_cmp = d1.day, d2.day, compare_prec
    else:
        x, y, next_cmp = d1.month, d2.month, lambda s, a, b: compare_month_or_day(True, s, a, b)

    # comparison logic
    if x == 0 and y == 0:
        return compare_prec(strict, d1, d2)
    elif x == 0:
        return compare_with_unknown(d1, d2)
    elif y == 0:
        res = compare_with_unknown(d2, d1)
        return -res if res is not None else None
    else:
        if x == y:
            return next_cmp(strict, d1, d2)
        else:
            return eval_strict(strict, d1, d2, (x > y) - (x < y))

# def compare_dmy_opt(d1: DateValue, d2: DateValue, strict: bool = False) -> Optional[int]:
#     if d1.year == d2.year:
#         return compare_month_or_day(False, strict, d1, d2)
#     else:
#         return eval_strict(strict, d1, d2, (d1.year > d2.year) - (d1.year < d2.year))

# def compare_dmy(d1: DateValue, d2: DateValue, strict: bool = False) -> int:
#     res = compare_dmy_opt(d1, d2, strict)
#     if res is None:
#         raise NotComparable()
#     return res