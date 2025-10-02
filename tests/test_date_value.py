import pytest
import math
from dataclasses import replace
from typing import Optional

# Assuming these imports based on the code structure
from libraries.precision import OrYear, PrecisionBase, Sure, About, Maybe, Before, After, YearInt
from libraries.calendar_date import Calendar, CalendarDate
# NotComparable intentionally not imported here; tests use compare return values
from libraries.date import Date, CompressedDate, DateValue



# Helper fixture for common DateValue samples
@pytest.fixture
def sample_dates():
    return {
        "basic": DateValue(15, 6, 2023, Sure()),
        "about": DateValue(10, 3, 2020, About()),
        "before": DateValue(5, 1, 2000, Before()),
        "after": DateValue(25, 8, 1995, After()),
        "zero_day": DateValue(0, 6, 2023, Sure()),
        "zero_month": DateValue(15, 0, 2023, Sure()),
        "with_delta": DateValue(15, 6, 2023, Sure(), delta=5),
        "edge_year_low": DateValue(1, 1, 1, Sure()),
        "edge_year_high": DateValue(31, 12, 2499, Sure()),
        "year_too_high": DateValue(15, 6, 2500, Sure()),
    }


def test_compress_and_uncompress_roundtrip(sample_dates):
    original = sample_dates["basic"]
    compressed = original.compress()
    assert compressed is not None and isinstance(compressed, int)
    uncompressed = DateValue.uncompress(compressed)
    assert uncompressed.day == original.day
    assert uncompressed.month == original.month
    assert uncompressed.year == original.year
    assert uncompressed.delta == 0


def test_compress_invalid_cases(sample_dates):
    assert sample_dates["with_delta"].compress() is None
    assert sample_dates["year_too_high"].compress() is None
    assert DateValue(-1, 6, 2023, Sure()).compress() is None
    assert DateValue(15, -1, 2023, Sure()).compress() is None
    assert DateValue(15, 6, 0, Sure()).compress() is None


def test_sdn_of_date_increasing():
    d1 = DateValue(1, 1, 2000, Sure())
    d2 = DateValue(2, 1, 2000, Sure())
    assert isinstance(DateValue._sdn_of_date(d1), int)
    assert DateValue._sdn_of_date(d2) > DateValue._sdn_of_date(d1)


def test_combine_precision_rules():
    assert isinstance(DateValue._combine_precision(Sure(), Sure()), Sure)
    assert isinstance(DateValue._combine_precision(Sure(), About()), Maybe)
    assert isinstance(DateValue._combine_precision(About(), After()), After)
    assert isinstance(DateValue._combine_precision(After(), Before()), Before)


def test_basic_compare_and_eq():
    a = DateValue(1, 1, 2000, Sure())
    b = DateValue(2, 1, 2000, Sure())
    assert a.compare(b) == -1
    assert not (a == b)


def test_unknown_day_with_after_behaviour():
    a = DateValue(0, 5, 2000, After())
    b = DateValue(10, 5, 2000, Sure())
    assert a.compare(b) == 1


def test_oryear_branch_compares_as_sure():
    inner = DateValue(1, 1, 2000, None)
    p_or = OrYear(inner)
    a = DateValue(1, 1, 2000, p_or)
    b = DateValue(1, 1, 2000, p_or)
    assert a.compare(b) == 0


def test_strict_compare_non_comparable_returns_none():
    from_date = DateValue(1, 1, 2000, After())
    to_date = DateValue(1, 1, 2001, Sure())
    assert from_date.compare(to_date, strict=True) is None


def test_date_difference_basic():
    a = DateValue(1, 1, 2000, Sure())
    b = DateValue(1, 1, 2001, Sure())
    diff = DateValue.date_difference(a, b)
    assert isinstance(diff, DateValue)
    assert diff.year == 1

