from enum import Enum, auto


def leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def nb_days_in_month(month: int, year: int) -> int:
    if month == 2 and leap_year(year):
        return 29
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return days[month - 1] if 1 <= month <= 12 else 0


# def to_calendars(d: DateValue) -> CalendarDate:
#     """Convert Dmy to CalendarDate"""
#     return CalendarDate(day=d.day, month=d.month, year=d.year, delta=d.delta)


# def of_calendars(cd: CalendarDate, prec: Optional[Precision] = None) -> Dmy:
#     """Convert CalendarDate back to Dmy with optional precision"""
#     return Dmy(
#         day=cd.day,
#         month=cd.month,
#         year=cd.year,
#         delta=cd.delta,
#         prec=prec if prec else Sure()
#     )


# # --- Conversion stubs for calendar systems ---
# def sdn_of_gregorian(d: Dmy) -> int:
#     return sdn_of_gregorian_cal(to_calendars(d))


# def gregorian_of_sdn(prec: Precision, sdn: int) -> Dmy:
#     return of_calendars(gregorian_of_sdn_cal(sdn), prec)


# # Similarly for Julian, French, Hebrew
# def sdn_of_julian(d: Dmy) -> int:
#     return sdn_of_julian_cal(to_calendars(d))

# def julian_of_sdn(prec: Precision, sdn: int) -> Dmy:
#     return of_calendars(julian_of_sdn_cal(sdn), prec)


# # # --- Dmy2 conversion ---
# # def dmy_of_dmy2(to_date: Dmy2) -> Dmy:
# #     return Dmy(day=to_date.day2, month=to_date.month2, year=to_date.year2, delta=to_date.delta2, prec=Sure())


# # --- Aux function for precision handling ---
# def aux(fn, d: DateValue) -> DateValue:
#     def aux2(to_date: DateValue):
#         d = of_calendars(fn(to_calendars(dmy_of_dmy2(to_date))))
#         return DateValue(day2=d.day, month2=d.month, year2=d.year, delta2=d.delta)

#     prec = d.prec
#     if isinstance(d.prec, OrYear):
#         prec = OrYear(aux2(d.prec.d))
#     elif isinstance(d.prec, YearInt):
#         prec = YearInt(aux2(d.prec.d))

#     return of_calendars(fn(to_calendars(d)), prec)


class MoonPhase(Enum):
    NEWMOON = auto(),
    FIRSTQUARTER = auto(),
    FULLMOON = auto(),
    LASTQUARTER = auto()
    
