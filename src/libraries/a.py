from date.precision import After, About, OrYear, Sure, Maybe, Before
from date.calendar_date import DateValue

d_or_year = DateValue(
    day=1,
    month=2,
    year=2023,
    prec=None,
    delta=0
)
oy = OrYear(d_or_year)

d1 = DateValue(
    day=        1,
    month=      2,
    year=       2024,
    prec=       oy)
d2 = DateValue(
    day=        1,
    month=      2,
    year=       2023,
    prec=       oy)
print("---------------")
print(f"Value d1->d2 (False) : {d1.compare(d2, False)}")
print(f"Value d2->d1 (False) : {d2.compare(d1, False)}")
print(f"Value d1->d2 (True) : {d1.compare(d2, True)}")
print(f"Value d2->d1 (True) : {d2.compare(d1, True)}")