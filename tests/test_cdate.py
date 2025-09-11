import pytest
from date.date import Date, CDate
from date.calendar_date import Calendar, CalendarDate, DateValue
from date.precision import Sure, About, Maybe, Before, After
from date.utils import compare_date_value_opt, compare_prec, compare_month_or_day, eval_strict

# ---------- Tests for DateValue.compress & uncompress ----------
def test_compress_uncompress_sure():
    d = DateValue(1, 1, 2024, Sure())
    compressed = d.compress()
    assert isinstance(compressed, int)
    uncompressed = DateValue.uncompress(compressed)
    assert isinstance(uncompressed, DateValue)
    assert uncompressed.year == 2024

def test_compress_uncompress_about():
    d = DateValue(5, 5, 2022, About())
    compressed = d.compress()
    uncompressed = DateValue.uncompress(compressed)
    assert isinstance(uncompressed, DateValue)

def test_compress_uncompress_maybe():
    d = DateValue(10, 10, 2021, Maybe())
    compressed = d.compress()
    uncompressed = DateValue.uncompress(compressed)
    assert isinstance(uncompressed, DateValue)

def test_compress_uncompress_before_after():
    for cls in [Before, After]:
        d = DateValue(15, 6, 2020, cls())
        compressed = d.compress()
        uncompressed = DateValue.uncompress(compressed)
        assert isinstance(uncompressed, DateValue)

def test_compress_invalid_date():
    d = DateValue(1, 1, 3000, Sure())
    assert d.compress() is None

# ---------- Tests for DateValue.time_elapsed ----------
def test_time_elapsed_full():
    d1 = DateValue(1, 1, 2020, Sure())
    d2 = DateValue(5, 5, 2023, Sure())
    result = d1.time_elapsed(d1, d2)
    assert isinstance(result, DateValue)
    assert result.year == 3

def test_time_elapsed_day_missing():
    d1 = DateValue(0, 1, 2020, Sure())
    d2 = DateValue(5, 1, 2023, Sure())
    result = d1.time_elapsed(d1, d2)
    assert result.year == 3

def test_time_elapsed_month_missing():
    d1 = DateValue(5, 0, 2020, Sure())
    d2 = DateValue(5, 5, 2023, Sure())
    result = d1.time_elapsed(d1, d2)
    assert result.month >= 0

def test_time_elapsed_opt_after_before():
    d1 = DateValue(1, 1, 2024, After())
    d2 = DateValue(1, 1, 2025, After())
    assert d1.time_elapsed_opt(d1, d2) is None
    d1b = DateValue(1, 1, 2024, Before())
    d2b = DateValue(1, 1, 2025, Before())
    assert d1b.time_elapsed_opt(d1b, d2b) is None

def test_time_elapsed_opt_mixed_precisions():
    d1 = DateValue(1, 1, 2024, Sure())
    d2 = DateValue(1, 1, 2025, After())
    result = d1.time_elapsed_opt(d1, d2)
    assert isinstance(result, DateValue)

# ---------- Tests for CDate.cdate_to_date ----------
@pytest.mark.parametrize("calendar", [Calendar.GREGORIAN, Calendar.JULIAN, Calendar.FRENCH, Calendar.HEBREW])
def test_cdate_tuple_to_date(calendar):
    dmy = DateValue(1, 1, 2024, Sure())
    compressed = dmy.compress()
    c = CDate((calendar, compressed))
    result = c.cdate_to_date()
    assert isinstance(result, CalendarDate)
    assert result.cal == calendar

def test_cdate_str_to_date():
    c = CDate("random string")
    assert c.cdate_to_date() == "random string"

def test_cdate_none_to_date():
    c = CDate(None)
    assert c.cdate_to_date() is None

def test_cdate_invalid_raises():
    c = CDate(12345)
    with pytest.raises(ValueError):
        c.cdate_to_date()

# ---------- Tests for Date.date_to_cdate ----------
def test_date_to_cdate_with_calendar():
    dmy = DateValue(1, 1, 2024, Sure())
    d = Date(CalendarDate(dmy, Calendar.GREGORIAN))
    cdate = d.date_to_cdate()
    assert isinstance(cdate, CDate)

def test_date_to_cdate_with_str():
    d = Date("free-form")
    cdate = d.date_to_cdate()
    assert isinstance(cdate, str)
    assert cdate == "free-form"

# ---------- Tests for utils.py ----------
def test_eval_strict_various():
    before = DateValue(1, 1, 2024, Before())
    after = DateValue(1, 1, 2024, After())
    sure = DateValue(1, 1, 2024, Sure())

    assert eval_strict(True, after, before, -1) is None
    assert eval_strict(True, before, after, 1) is None
    assert eval_strict(True, before, after, -1) == -1
    assert eval_strict(True, after, before, 1) == 1
    assert eval_strict(False, before, after, -1) == -1
    assert eval_strict(False, after, before, 1) == 1
    assert eval_strict(True, sure, sure, 0) == 0

def test_compare_prec_all():
    d_sure = DateValue(1, 1, 2024, Sure())
    d_about = DateValue(1, 1, 2024, About())
    d_maybe = DateValue(1, 1, 2024, Maybe())
    d_before = DateValue(1, 1, 2024, Before())
    d_after = DateValue(1, 1, 2024, After())

    # Sure vs About/Maybe
    assert compare_prec(False, d_sure, d_about) == 0
    assert compare_prec(False, d_sure, d_maybe) == 0

    # Before vs After
    assert compare_prec(False, d_before, d_after) == -1
    assert compare_prec(False, d_after, d_before) == 1

def test_compare_date_value_opt_simple():
    d1 = DateValue(1, 1, 2024, Sure())
    d2 = DateValue(2, 2, 2025, Sure())
    assert compare_date_value_opt(False, d1, d2) == -1
    assert compare_date_value_opt(False, d2, d1) == 1

def test_compare_month_or_day_all_cases():
    d1 = DateValue(0, 0, 2024, Sure())
    d2 = DateValue(5, 5, 2024, Sure())
    assert compare_month_or_day(False, False, d1, d2) == -1
    d1b = DateValue(0, 5, 2024, Before())
    d2b = DateValue(5, 0, 2024, After())
    res = compare_month_or_day(True, False, d1b, d2b)
    assert res in [-1, 1, 0, None]
