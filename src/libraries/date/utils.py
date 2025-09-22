# from dataclasses import replace
# from typing import Optional

# from exception import NotComparable
# from date.calendar_date import DateValue
# from date.precision import About, After, Before, Maybe, OrYear, Sure, YearInt


# def eval_strict(strict: bool, from_date: DateValue, to_date: DateValue, x: int) -> Optional[int]:
#     if strict:
#         if x == -1 and (isinstance(from_date.prec, After) or isinstance(to_date.prec, Before)):
#             return None
#         if x == 1 and (isinstance(from_date.prec, Before) or isinstance(to_date.prec, After)):
#             return None
#     return x

# def compare(d: DateValue, other: DateValue, strict: bool=False) -> Optional[int]:
#     if not isinstance(other, DateValue):
#         raise NotComparable(f"Cannot compare DateValue with {type(other)}")
#     if d.year == other.year:
#         return compare_month_or_day(False, strict, d, other)
#     return eval_strict(strict, d, other, (d.year > other.year) - (d.year < other.year))


# def compare_date_value_opt(strict: bool, from_date: DateValue, to_date: DateValue) -> Optional[int]:
#     if from_date.year == to_date.year:
#         return compare_month_or_day(False, strict, from_date, to_date)
#     return eval_strict(strict, from_date, to_date, (from_date.year > to_date.year) - (from_date.year < to_date.year))

# def compare_prec(strict: bool, from_date: DateValue, to_date: DateValue) -> Optional[int]:
#     if isinstance(from_date.prec, (Sure, About, Maybe)) and isinstance(
#         to_date.prec, (Sure, About, Maybe)
#     ):
#         return 0
#     if from_date.prec == to_date.prec and isinstance(from_date.prec, (After, Before)):
#         return 0
#     if from_date.prec == to_date.prec and isinstance(from_date.prec, (OrYear, YearInt)):
#         return compare_date_value_opt(strict, replace(from_date, prec=Sure), replace(to_date, prec=Sure))
#     if isinstance(from_date.prec, Before) or isinstance(to_date.prec, After):
#         return -1
#     if isinstance(from_date.prec, After) or isinstance(to_date.prec, Before):
#         return 1
#     return 0


# def compare_month_or_day(is_day: bool, strict: bool, from_date: DateValue, to_date: DateValue) -> Optional[int]:

#     def compare_with_unknown(unknown: DateValue, known: DateValue) -> Optional[int]:
#         if isinstance(unknown.prec, After):
#             return 1
#         if isinstance(unknown.prec, Before):
#             return -1
#         return compare_prec(False, unknown, known) if not strict else None

#     # select value to compare and next step
#     if is_day:
#         x, y, next_cmp = from_date.day, to_date.day, compare_prec
#     else:
#         x, y, next_cmp = from_date.month, to_date.month, lambda s, a, b: compare_month_or_day(True, s, a, b)

#     # comparison logic
#     if x == 0 and y == 0:
#         return compare_prec(strict, from_date, to_date)
#     elif x == 0:
#         return compare_with_unknown(from_date, to_date)
#     elif y == 0:
#         res = compare_with_unknown(to_date, from_date)
#         return -res if res is not None else None
#     else:
#         if x == y:
#             return next_cmp(strict, from_date, to_date)
#         else:
#             return eval_strict(strict, from_date, to_date, (x > y) - (x < y))
