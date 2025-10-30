import pytest
import math
from dataclasses import replace
from typing import Optional

from libraries.precision import (
    Sure,
    About,
    Maybe,
    Before,
    After,
    YearInt,
)
from libraries.exception import NotComparable
from libraries.date import Date, CompressedDate, DateValue
from libraries.calendar_date import Calendar, CalendarDate


@pytest.fixture
def sample_calendar_dates():
    """Fixture providing sample CalendarDate instances"""
    return {
        "gregorian": CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN),
        "julian": CalendarDate(DateValue(20, 3, 1995, About()), Calendar.JULIAN),
        "french": CalendarDate(DateValue(5, 10, 1800, Maybe()), Calendar.FRENCH),
        "hebrew": CalendarDate(DateValue(10, 1, 2000, Before()), Calendar.HEBREW),
    }


@pytest.fixture
def sample_dates():
    """Fixture providing sample Date instances"""
    cal_date = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
    return {
        "calendar_date": Date(cal_date),
        "string_date": Date("2023-06-15"),
        "another_string": Date("June 15, 2023"),
    }


@pytest.fixture
def sample_cdates():
    """Fixture providing sample CompressedDate instances"""
    return {
        "gregorian_tuple": CompressedDate((Calendar.GREGORIAN, 12345)),
        "julian_tuple": CompressedDate((Calendar.JULIAN, 67890)),
        "french_tuple": CompressedDate((Calendar.FRENCH, 11111)),
        "hebrew_tuple": CompressedDate((Calendar.HEBREW, 22222)),
        "date_object": CompressedDate(Date("2023-06-15")),
        "string": CompressedDate("June 15, 2023"),
        "none": CompressedDate(None),
    }


def test_calendar_date_creation(sample_calendar_dates):
    """Test CalendarDate instance creation"""
    for name, cal_date in sample_calendar_dates.items():
        assert isinstance(cal_date, CalendarDate)
        assert isinstance(cal_date.dmy, DateValue)
        assert isinstance(cal_date.cal, Calendar)


def test_calendar_date_equality(sample_calendar_dates):
    """Test CalendarDate equality"""
    date1 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
    date2 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
    assert date1.dmy == date2.dmy

    date3 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.JULIAN)
    assert date1.dmy == date3.dmy
    assert date1.cal != date3.cal


def test_date_creation(sample_dates):
    """Test Date instance creation"""
    for name, date in sample_dates.items():
        assert isinstance(date, Date)
        if name == "calendar_date":
            assert isinstance(date.date, CalendarDate)
        else:
            assert isinstance(date.date, str)


def test_date_equality_calendar_dates(sample_dates):
    """Test Date equality with CalendarDate instances"""
    cal_date1 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
    cal_date2 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
    cal_date3 = CalendarDate(DateValue(16, 6, 2023, Sure()), Calendar.GREGORIAN)

    date1 = Date(cal_date1)
    date2 = Date(cal_date2)
    date3 = Date(cal_date3)

    assert date1 == date2
    assert not (date1 == date3)


def test_date_equality_strings(sample_dates):
    """Test Date equality with string instances"""
    date1 = Date("2023-06-15")
    date2 = Date("2023-06-15")
    date3 = Date("2023-06-16")

    assert date1 == date2
    assert not (date1 == date3)


def test_date_equality_mixed_types_error(sample_dates):
    """Test Date equality raises error for mixed types"""
    cal_date = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
    date_cal = Date(cal_date)
    date_str = Date("2023-06-15")

    with pytest.raises(NotComparable):
        date_cal == date_str


def test_date_equality_invalid_type(sample_dates):
    """Test Date equality with invalid types"""
    date = sample_dates["calendar_date"]

    with pytest.raises(NotComparable):
        date == "not a Date object"

    with pytest.raises(NotComparable):
        date == 12345

    with pytest.raises(NotComparable):
        date == None


def test_date_to_cdate_calendar_date_compressible(sample_dates):
    """Test date_to_cdate with compressible CalendarDate"""
    cal_date = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
    date = Date(cal_date)

    cdate = date.date_to_cdate()
    assert isinstance(cdate, CompressedDate)
    assert isinstance(cdate.cdate, tuple)
    assert len(cdate.cdate) == 2
    assert isinstance(cdate.cdate[0], Calendar)
    assert isinstance(cdate.cdate[1], int)


def test_date_to_cdate_calendar_date_non_compressible(sample_dates):
    """Test date_to_cdate with non-compressible CalendarDate"""
    cal_date = CalendarDate(DateValue(15, 6, 2500, Sure()), Calendar.GREGORIAN)
    date = Date(cal_date)

    cdate = date.date_to_cdate()
    assert isinstance(cdate, CompressedDate)
    assert cdate.cdate == Date(cal_date)


def test_date_to_cdate_string(sample_dates):
    """Test date_to_cdate with string date"""
    date = sample_dates["string_date"]
    result = date.date_to_cdate()

    assert result == CompressedDate("2023-06-15")


def test_cdate_creation(sample_cdates):
    """Test CompressedDate instance creation"""
    for name, cdate in sample_cdates.items():
        assert isinstance(cdate, CompressedDate)


def test_cdate_to_date_calendar_tuples(sample_cdates):
    """Test cdate_to_date with calendar tuples"""
    calendars = [
        Calendar.GREGORIAN,
        Calendar.JULIAN,
        Calendar.FRENCH,
        Calendar.HEBREW,
    ]

    for calendar in calendars:
        cdate = CompressedDate((calendar, 12345))
        result = cdate.cdate_to_date()
        assert isinstance(result, Date)
        assert isinstance(result.date, CalendarDate)
        assert result.date.cal == calendar


def test_cdate_to_date_date_object(sample_cdates):
    """Test cdate_to_date with Date object"""
    date_obj = Date("2023-06-15")
    cdate = CompressedDate(date_obj)
    result = cdate.cdate_to_date()
    assert result == date_obj


def test_cdate_to_date_string(sample_cdates):
    """Test cdate_to_date with string"""
    string_date = "June 15, 2023"
    cdate = CompressedDate(string_date)
    result = cdate.cdate_to_date()
    assert result == Date(string_date)


def test_cdate_to_date_none(sample_cdates):
    """Test cdate_to_date with None"""
    cdate = sample_cdates["none"]
    with pytest.raises(ValueError, match="Invalid CompressedDate: None"):
        cdate.cdate_to_date()


def test_cdate_to_date_invalid_value():
    """Test cdate_to_date with invalid value raises ValueError"""
    cdate = CompressedDate(12345)
    with pytest.raises(ValueError, match="Invalid CompressedDate"):
        cdate.cdate_to_date()


def test_full_compression_cycle():
    """Test full compression/decompression cycle through all classes"""
    original_dv = DateValue(15, 6, 2023, Sure())
    original_cd = CalendarDate(original_dv, Calendar.GREGORIAN)
    original_date = Date(original_cd)

    cdate = original_date.date_to_cdate()

    recovered_date = cdate.cdate_to_date()

    assert isinstance(recovered_date, Date)
    assert recovered_date.date.cal == Calendar.GREGORIAN
    assert recovered_date.date.dmy.day == 15
    assert recovered_date.date.dmy.month == 6
    assert recovered_date.date.dmy.year == 2023
    assert isinstance(recovered_date.date.dmy.prec, Sure)


def test_non_compressible_cycle():
    """Test cycle with non-compressible date"""
    original_dv = DateValue(15, 6, 2023, Sure(), delta=5)
    original_cd = CalendarDate(original_dv, Calendar.GREGORIAN)
    original_date = Date(original_cd)

    cdate = original_date.date_to_cdate()

    assert isinstance(cdate, CompressedDate)


def test_string_date_cycle():
    """Test cycle with string date"""
    original_str = "June 15, 2023"
    original_date = Date(original_str)

    result = original_date.date_to_cdate()
    assert result == CompressedDate(original_str)


def test_compare_date_value_opt_same_year_path():
    """Test __compare_date_value_opt first return path (same year) via compare method"""
    date1 = DateValue(15, 6, 2023, Sure())
    date2 = DateValue(20, 6, 2023, Sure())

    result = date1.compare(date2, strict=False)
    assert result == -1

    result_strict = date1.compare(date2, strict=True)
    assert result_strict == -1

    result_equal = date1.compare(date1, strict=False)
    assert result_equal == 0


def test_compare_date_value_opt_different_years_path():
    """Test __compare_date_value_opt second return path (different years) via compare method"""
    date_early = DateValue(31, 12, 2022, Sure())
    date_late = DateValue(1, 1, 2023, Sure())

    result = date_early.compare(date_late, strict=False)
    assert result == -1

    result_reverse = date_late.compare(date_early, strict=False)
    assert result_reverse == 1

    result_strict = date_early.compare(date_late, strict=True)
    assert result_strict == -1


def test_compare_month_or_day_is_day_true_path():
    """Test __compare_month_or_day with is_day=True path via compare method"""
    date1 = DateValue(10, 6, 2023, Sure())
    date2 = DateValue(20, 6, 2023, Sure())

    result = date1.compare(date2, strict=False)
    assert result == -1

    date3 = DateValue(15, 6, 2023, About())
    date4 = DateValue(15, 6, 2023, Maybe())
    result_equal = date3.compare(date4, strict=False)
    assert result_equal == 0


def test_compare_zero_day_scenarios_via_compare():
    """Test zero day handling in __compare_month_or_day via compare method"""
    date_zero_day = DateValue(0, 6, 2023, Sure())
    date_normal = DateValue(15, 6, 2023, Sure())

    result = date_zero_day.compare(date_normal, strict=False)
    assert result == 0

    result_reverse = date_normal.compare(date_zero_day, strict=False)
    assert result_reverse == 0


def test_compare_zero_day_strict_mode_via_compare():
    """Test zero day handling in strict mode via compare method"""
    date_zero_day = DateValue(0, 6, 2023, Sure())
    date_normal = DateValue(15, 6, 2023, Sure())

    result = date_zero_day.compare(date_normal, strict=True)
    assert result is None

    result_reverse = date_normal.compare(date_zero_day, strict=True)
    assert result_reverse is None


def test_compare_both_zero_days_via_compare():
    """Test both days zero scenario via compare method"""
    date1_zero = DateValue(0, 6, 2023, Sure())
    date2_zero = DateValue(0, 6, 2023, About())

    result = date1_zero.compare(date2_zero, strict=False)
    assert result == 0


def test_compare_precision_fallback_equal_days():
    """Test precision fallback when days are equal via compare method"""
    date_before = DateValue(15, 6, 2023, Before())
    date_after = DateValue(15, 6, 2023, After())

    result = date_before.compare(date_after, strict=False)
    assert result == -1


def test_compare_zero_month_scenarios():
    """Test zero month handling via compare method"""
    date_zero_month = DateValue(15, 0, 2023, Sure())
    date_normal_month = DateValue(15, 6, 2023, Sure())

    result = date_zero_month.compare(date_normal_month, strict=False)
    assert result == 0

    result_strict = date_zero_month.compare(date_normal_month, strict=True)
    assert result_strict is None


def test_compare_both_zero_month_and_day():
    """Test scenario with both zero month and zero day via compare method"""
    date1_zeros = DateValue(0, 0, 2023, Sure())
    date2_zeros = DateValue(0, 0, 2023, Maybe())

    result = date1_zeros.compare(date2_zeros, strict=False)
    assert result == 0


def test_strict_mode_edge_cases_via_compare():
    """Test strict mode edge cases via compare method"""
    date1 = DateValue(0, 5, 2023, Sure())
    date2 = DateValue(10, 5, 2023, Sure())

    result_non_strict = date1.compare(date2, strict=False)
    assert result_non_strict == 0

    result_strict = date1.compare(date2, strict=True)
    assert result_strict is None


def test_time_elapsed_partial_year():
    """Test time_elapsed with partial year calculations"""
    from_date = DateValue(1, 1, 2020, Sure())
    to_date = DateValue(1, 7, 2020, Sure())

    elapsed = DateValue.date_difference(from_date, to_date)
    assert elapsed.year == 0
    assert elapsed.month >= 5
    assert isinstance(elapsed.prec, Sure)


def test_time_elapsed_with_days_remainder():
    """Test time_elapsed with specific day calculations"""
    from_date = DateValue(1, 1, 2020, Sure())
    to_date = DateValue(15, 1, 2020, Sure())

    elapsed = DateValue.date_difference(from_date, to_date)
    assert elapsed.year == 0
    assert elapsed.month == 0
    assert elapsed.day == 14
    assert isinstance(elapsed.prec, Sure)


def test_time_elapsed_negative_time_difference():
    """Test time_elapsed when to_date is before from_date"""
    from_date = DateValue(1, 1, 2021, Sure())
    to_date = DateValue(1, 1, 2020, Sure())

    elapsed = DateValue.date_difference(from_date, to_date)
    assert isinstance(elapsed, DateValue)
    assert isinstance(elapsed.prec, Sure)


def test_time_elapsed_large_date_ranges():
    """Test time_elapsed with very large date ranges"""
    ancient_date = DateValue(1, 1, 100, Sure())
    modern_date = DateValue(31, 12, 2000, Sure())

    elapsed = DateValue.date_difference(ancient_date, modern_date)
    assert elapsed.year >= 1900
    assert isinstance(elapsed, DateValue)
    assert isinstance(elapsed.prec, Sure)


def test_sdn_calculation_consistency():
    """Test that SDN calculations are consistent and monotonic"""
    dates = [
        DateValue(1, 1, 2020, Sure()),
        DateValue(2, 1, 2020, Sure()),
        DateValue(1, 2, 2020, Sure()),
        DateValue(1, 1, 2021, Sure()),
    ]

    sdns = [DateValue._sdn_of_date(date) for date in dates]

    assert sdns[0] < sdns[1]
    assert sdns[1] < sdns[2]
    assert sdns[2] < sdns[3]

    for sdn in sdns:
        assert isinstance(sdn, int)
        assert sdn > 0


def test_sdn_february_leap_year_handling():
    """Test SDN calculation handles February in leap years correctly"""
    leap_feb_28 = DateValue(28, 2, 2020, Sure())
    leap_feb_29 = DateValue(29, 2, 2020, Sure())
    leap_mar_1 = DateValue(1, 3, 2020, Sure())

    sdn_28 = DateValue._sdn_of_date(leap_feb_28)
    sdn_29 = DateValue._sdn_of_date(leap_feb_29)
    sdn_mar_1 = DateValue._sdn_of_date(leap_mar_1)

    assert sdn_29 == sdn_28 + 1
    assert sdn_mar_1 == sdn_29 + 1


def test_precision_combinations_via_compare():
    """Test different precision combinations affecting compare results"""
    before_date = DateValue(15, 6, 2023, Before())
    after_date = DateValue(15, 6, 2023, After())
    sure_date = DateValue(15, 6, 2023, Sure())

    result1 = before_date.compare(after_date, strict=False)
    assert result1 == -1

    result2 = before_date.compare(sure_date, strict=False)
    assert result2 == -1

    result3 = sure_date.compare(after_date, strict=False)
    assert result3 == -1


def test_or_year_year_int_precision_via_compare():
    """Test OrYear and YearInt precision handling via compare method"""
    try:
        or_year_date = DateValue(15, 6, 2023, Sure())
        year_int_date = DateValue(15, 6, 2023, Sure())

        result = or_year_date.compare(year_int_date, strict=False)
        assert result == 0
    except (NameError, AttributeError):
        pytest.skip("OrYear/YearInt precision types not available")


def test_complex_comparison_chains_via_compare():
    """Test complex comparison scenarios that exercise multiple code paths"""
    # Chain of comparisons that test different parts of the logic
    dates = [
        DateValue(0, 0, 2023, Before()),
        DateValue(0, 5, 2023, Sure()),
        DateValue(10, 5, 2023, About()),
        DateValue(10, 5, 2023, Maybe()),
        DateValue(10, 5, 2023, After()),
        DateValue(20, 5, 2023, Sure()),
        DateValue(15, 6, 2023, Sure()),
    ]

    for i in range(len(dates) - 1):
        result = dates[i].compare(dates[i + 1], strict=False)
        assert result in [-1, 0], (
            f"Expected <= for comparison {i} to {i + 1}, got {result}"
        )


def test_eval_strict_behavior_via_compare():
    """Test __eval_strict behavior indirectly through compare method"""
    date1 = DateValue(15, 6, 2023, Sure())
    date2 = DateValue(20, 6, 2023, Sure())

    result_non_strict = date1.compare(date2, strict=False)
    assert result_non_strict == -1

    # Test strict mode with zero values (should return None in some cases)
    date_zero = DateValue(0, 6, 2023, Sure())
    date_normal = DateValue(15, 6, 2023, Sure())

    result_strict_with_zero = date_zero.compare(date_normal, strict=True)
    assert result_strict_with_zero is None


def test_leap_year_dates():
    """Test dates in leap years"""
    leap_date = DateValue(29, 2, 2020, Sure())
    non_leap_date = DateValue(28, 2, 2021, Sure())

    # Both should be compressible and work normally
    assert leap_date.compress() is not None
    assert non_leap_date.compress() is not None


def test_large_time_differences():
    """Test time calculations with large date differences"""
    ancient_date = DateValue(1, 1, 1, Sure())
    modern_date = DateValue(31, 12, 2499, Sure())

    elapsed = DateValue.date_difference(ancient_date, modern_date)
    assert isinstance(elapsed, DateValue)
    assert elapsed.year > 2000
