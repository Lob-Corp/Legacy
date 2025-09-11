# from __future__ import annotations
# from dataclasses import dataclass
# from typing import Optional

# from calendar.utils import nb_days_in_month
# from date.precision import Precision, Sure, About, Maybe, Before, After

# @dataclass(frozen=True)
# class DateValue:
#     day: int
#     month: int
#     year: int
#     prec: Precision | None
#     delta: int = 0

#     def compress(self) -> Optional[int]:
#         """Compress a concrete date if possible into an integer."""
#         simple = (
#             isinstance(self.prec, (Sure, About, Maybe, Before, After))
#             and self.day >= 0
#             and self.month >= 0
#             and 0 < self.year < 2500
#             and self.delta == 0
#         )
#         # print(simple)
#         if simple:
#             p = {About: 1, Maybe: 2, Before: 3, After: 4}.get(type(self.prec), 0)
#             print("PPPPP: ", p)
#             return (((((p * 32) + self.day) * 13) + self.month) * 2500) + self.year
#         return None

#     @staticmethod
#     def uncompress(x: int) -> DateValue:
#         """Decompress integer back to DateValue."""
#         print("Uncompressing", x)
#         year, x = x % 2500.0, x // 2500.0
#         print(year, float(x))
#         month, x = x % 13.0, x // 13.0
#         print(month, float(x))
#         day, x = x % 32.0, x // 32.0
#         print(day, float(x))
#         print("-------------------")
#         prec = {1: About, 2: Maybe, 3: Before, 4: After}.get(x, Sure)()
#         return DateValue(day, month, year, prec)

#     def time_elapsed(self, d1: DateValue, d2: DateValue) -> DateValue:
#         prec = Maybe()
#         if d1.prec == Sure and d2.prec == Sure:
#             prec = Sure

#         if d1.day == 0 and d1.month == 0:
#             return DateValue(0, 0, d2.year - d1.year, prec)

#         if d1.day == 0:
#             month, r = (
#                 (d2.month - d1.month, 0)
#                 if d1.month <= d2.month
#                 else (d2.month - d1.month + 12, 1)
#             )
#             year = d2.year - d1.year - r
#             return DateValue(0, month, year, prec)

#         day, r = (
#             (d2.day - d1.day, 0)
#             if d1.day <= d2.day
#             else (
#                 d2.day - d1.day + nb_days_in_month(d1.month, d1.year),
#                 1,
#             )
#         )
#         month, r = (
#             (d2.month - d1.month - r, 0)
#             if d1.month + r <= d2.month
#             else (d2.month - d1.month - r + 12, 1)
#         )
#         year = d2.year - d1.year - r
#         return DateValue(day, month, year, prec)

#     def time_elapsed_opt(self, d1: DateValue, d2: DateValue) -> Optional[DateValue]:
#         if d1.prec in [After] and d2.prec in [After]:
#             return None
#         if d1.prec in [Before] and d2.prec in [Before]:
#             return None
#         return self.time_elapsed(d1, d2)
