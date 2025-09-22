import pytest
from date.precision import Sure, About, Maybe, Before, After, OrYear, YearInt

# from date.date_value import DateValue, CalendarDate, Calendar
from exception import NotComparable
from date.date import Date
from date.calendar_date import DateValue


# ---- Helper function to create dates quickly ----
# ---- Test compare method ----
def test_compare_equal_dates():
    d1 = DateValue(15, 6, 2023, Sure())
    d2 = DateValue(15, 6, 2023, Sure())
    assert d1.compare(d2) == 0
    assert d1 == d2


def test_compare_different_years():
    d1 = DateValue(1, 1, 2020, Sure())
    d2 = DateValue(1, 1, 2023, Sure())
    assert d1.compare(d2) == -1
    assert d2.compare(d1) == 1


def test_compare_zero_day_strict_mode():
    d1 = DateValue(0, 6, 2023, Sure())
    d2 = DateValue(15, 6, 2023, Sure())
    assert d1.compare(d2, strict=True) is None
    assert d2.compare(d1, strict=True) is None


def test_compare_different_year_with_precision():
    d1 = DateValue(15, 6, 2022, Before())
    d2 = DateValue(15, 6, 2023, Before())
    assert d1.compare(d2, strict=True) is None
    assert d2.compare(d1, strict=True) is None


def test_compare_both_zero_days():
    d1 = DateValue(0, 6, 2023, Sure())
    d2 = DateValue(0, 6, 2023, About())
    assert d1.compare(d2, strict=False) == 0


def test_compare_both_zero_days_with_strict():
    d1 = DateValue(0, 6, 2023, Sure())
    d2 = DateValue(0, 6, 2023, About())
    assert d1.compare(d2, strict=True) == 0


def test_compare_precision_fallback():
    d1 = DateValue(15, 6, 2023, Before())
    d2 = DateValue(15, 6, 2023, After())
    assert d1.compare(d2, strict=False) == -1
    assert d2.compare(d1, strict=False) == 1


def test_compare_zero_month_scenarios():
    d1 = DateValue(15, 0, 2023, Sure())
    d2 = DateValue(15, 6, 2023, Sure())
    assert d1.compare(d2, strict=False) == 0
    assert d1.compare(d2, strict=True) is None


def test_compare_both_zero_month_and_day():
    d1 = DateValue(0, 0, 2023, Sure())
    d2 = DateValue(0, 0, 2023, Maybe())
    assert d1.compare(d2, strict=False) == 0


def test_compare_mixed_zero_scenarios():
    d1 = DateValue(15, 0, 2023, Sure())  # zero month, normal day
    d2 = DateValue(0, 6, 2023, Sure())  # normal month, zero day
    assert d1.compare(d2, strict=False) == 0
    assert d2.compare(d1, strict=False) == 0


def test_compare_with_or_year():
    d_or_year = DateValue(day=1, month=5, year=2003, prec=None, delta=0)

    oy = OrYear(d_or_year)

    d1 = DateValue(1, 5, 2001, oy)
    d2 = DateValue(1, 5, 2001, oy)
    assert d1.compare(d2, strict=False) == 0


def test_compare_with_or_year_and_different_years():
    d1 = DateValue(
        day=0, month=0, year=2023, prec=OrYear(date_value=DateValue(0, 0, 2021, None))
    )
    d2 = DateValue(
        day=12, month=0, year=2023, prec=OrYear(date_value=DateValue(0, 0, 2021, None))
    )

    assert d1.compare(d2, strict=True) == 0


def test_compare_with_year_int():
    d_year_int = DateValue(day=1, month=5, year=2003, prec=None, delta=0)
    yi = YearInt(d_year_int)

    d1 = DateValue(1, 5, 2003, yi)
    d2 = DateValue(1, 5, 2003, yi)
    assert d1.compare(d2, strict=False) == 0

def test_compare_with_unknown_date_after():
    d1 = DateValue(1, 0, 2003, After())
    d2 = DateValue(1, 5, 2003, Sure())
    assert d1.compare(d2, strict=False) == 1




def test_compare_invalid_type():
    d1 = DateValue(1, 1, 2020, Sure())
    with pytest.raises(NotComparable):
        d1.compare("not a date")


# ---- Test compress & uncompress ----
def test_compress_and_uncompress():
    d1 = DateValue(15, 6, 2023, Sure())
    compressed = d1.compress()
    assert compressed is not None
    d2 = DateValue.uncompress(compressed)
    assert isinstance(d2, DateValue)


def test_compress_invalid_date():
    d1 = DateValue(-1, 6, 2023, Sure())  # invalid day
    assert d1.compress() is None

# ---- Test time elapsed ----
def test_date_difference_basic():
    d1 = DateValue(1, 1, 2020, Sure())
    d2 = DateValue(1, 1, 2023, Sure())
    elapsed = DateValue.date_difference(d1, d2)
    assert isinstance(elapsed, DateValue)
    assert elapsed.year >= 3


# def test_date_difference_with_before_after():
#     d1 = DateValue(1, 1, 2020, Before())
#     d2 = DateValue(1, 1, 2023, After())
#     assert DateValue.date_difference(d1, d2) is not None


def test_date_difference_with_same_prec():
    d1 = DateValue(1, 1, 2020, Before())
    d2 = DateValue(1, 1, 2023, Before())
    assert DateValue.date_difference(d1, d2) is None

def test_date_difference_with_before_after():
    d1 = DateValue(1, 1, 2020, After())
    d2 = DateValue(1, 1, 2023, Before())
    assert DateValue.date_difference(d1, d2) == DateValue(1, 0, 3, Before())



# ---- Test _combine_precision ----
def test_combine_precision_cases():
    assert isinstance(DateValue._combine_precision(Sure(), Sure()), Sure)
    assert isinstance(DateValue._combine_precision(Sure(), Maybe()), Maybe)
    assert isinstance(DateValue._combine_precision(Sure(), After()), After)
    assert isinstance(DateValue._combine_precision(Sure(), Before()), Before)


# ---- All precision pairs test using compare() ----
precisions = [Sure(), About(), Maybe(), Before(), After()]


@pytest.mark.parametrize("p1", precisions)
@pytest.mark.parametrize("p2", precisions)
def test_compare_all_precisions(p1, p2):
    d1 = DateValue(15, 6, 2023, p1)
    d2 = DateValue(15, 6, 2023, p2)
    result = d1.compare(d2, strict=False)

    # Expected behavior based on __compare_prec logic:
    if isinstance(p1, Before) and isinstance(p2, After):
        assert result == -1  # Before < After
    elif isinstance(p1, After) and isinstance(p2, Before):
        assert result == 1  # After > Before
    elif type(p1) == type(p2) and not isinstance(p1, (Before, After)):
        assert result == 0  # Equal precision = equal dates
    else:
        # For other combos, result could be 0 or ±1 depending on strict rules
        assert result in [0, 1, -1, None]


# # ---- Compress & uncompress tests ----
# def test_compress_and_uncompress():
#     d1 = DateValue(15, 6, 2023, Sure())
#     compressed = d1.compress()
#     assert compressed is not None
#     d2 = DateValue.uncompress(compressed)
#     assert isinstance(d2, DateValue)


# def test_compress_invalid_date():
#     d1 = DateValue(-1, 6, 2023, Sure())  # invalid day
#     assert d1.compress() is None


# # ---- Combine precision tests ----
# def test_combine_precision_cases():
#     assert isinstance(DateValue._combine_precision(Sure(), Sure()), Sure)
#     assert isinstance(DateValue._combine_precision(Sure(), Maybe()), Maybe)
#     assert isinstance(DateValue._combine_precision(Sure(), After()), After)
#     assert isinstance(DateValue._combine_precision(Sure(), Before()), Before)
