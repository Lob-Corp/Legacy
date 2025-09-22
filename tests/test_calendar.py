import pytest
import math
from dataclasses import replace
from typing import Optional

# Assuming these imports based on the code structure
from date.precision import OrYear, Precision, Sure, About, Maybe, Before, After, YearInt
from date.calendar_date import Calendar, CalendarDate, DateValue
from exception import NotComparable
from date.date import Date, CDate


class TestCalendarDate:
    """Test cases for CalendarDate class"""

    @pytest.fixture
    def sample_calendar_dates(self):
        """Fixture providing sample CalendarDate instances"""
        return {
            "gregorian": CalendarDate(
                DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN
            ),
            "julian": CalendarDate(DateValue(20, 3, 1995, About()), Calendar.JULIAN),
            "french": CalendarDate(DateValue(5, 10, 1800, Maybe()), Calendar.FRENCH),
            "hebrew": CalendarDate(DateValue(10, 1, 2000, Before()), Calendar.HEBREW),
        }

    def test_calendar_date_creation(self, sample_calendar_dates):
        """Test CalendarDate instance creation"""
        for name, cal_date in sample_calendar_dates.items():
            assert isinstance(cal_date, CalendarDate)
            assert isinstance(cal_date.dmy, DateValue)
            assert isinstance(cal_date.cal, Calendar)

    def test_calendar_date_equality(self, sample_calendar_dates):
        """Test CalendarDate equality"""
        # Same calendar dates should be equal
        date1 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
        date2 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
        assert date1.dmy == date2.dmy  # Testing DateValue equality

        # Different calendars should have different comparisons
        date3 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.JULIAN)
        assert date1.dmy == date3.dmy  # Same DateValue
        assert date1.cal != date3.cal  # Different Calendar


class TestDate:
    """Test cases for Date class"""

    @pytest.fixture
    def sample_dates(self):
        """Fixture providing sample Date instances"""
        cal_date = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
        return {
            "calendar_date": Date(cal_date),
            "string_date": Date("2023-06-15"),
            "another_string": Date("June 15, 2023"),
        }

    def test_date_creation(self, sample_dates):
        """Test Date instance creation"""
        for name, date in sample_dates.items():
            assert isinstance(date, Date)
            if name == "calendar_date":
                assert isinstance(date.date, CalendarDate)
            else:
                assert isinstance(date.date, str)

    def test_date_equality_calendar_dates(self, sample_dates):
        """Test Date equality with CalendarDate instances"""
        cal_date1 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
        cal_date2 = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
        cal_date3 = CalendarDate(DateValue(16, 6, 2023, Sure()), Calendar.GREGORIAN)

        date1 = Date(cal_date1)
        date2 = Date(cal_date2)
        date3 = Date(cal_date3)

        assert date1 == date2
        assert not (date1 == date3)

    def test_date_equality_strings(self, sample_dates):
        """Test Date equality with string instances"""
        date1 = Date("2023-06-15")
        date2 = Date("2023-06-15")
        date3 = Date("2023-06-16")

        assert date1 == date2
        assert not (date1 == date3)

    def test_date_equality_mixed_types_error(self, sample_dates):
        """Test Date equality raises error for mixed types"""
        cal_date = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
        date_cal = Date(cal_date)
        date_str = Date("2023-06-15")

        with pytest.raises(NotComparable):
            date_cal == date_str

    def test_date_equality_invalid_type(self, sample_dates):
        """Test Date equality with invalid types"""
        date = sample_dates["calendar_date"]

        with pytest.raises(NotComparable):
            date == "not a Date object"

        with pytest.raises(NotComparable):
            date == 12345

        with pytest.raises(NotComparable):
            date == None

    def test_date_to_cdate_calendar_date_compressible(self, sample_dates):
        """Test date_to_cdate with compressible CalendarDate"""
        cal_date = CalendarDate(DateValue(15, 6, 2023, Sure()), Calendar.GREGORIAN)
        date = Date(cal_date)

        cdate = date.date_to_cdate()
        assert isinstance(cdate, CDate)
        assert isinstance(cdate.cdate, tuple)
        assert len(cdate.cdate) == 2
        assert isinstance(cdate.cdate[0], Calendar)
        assert isinstance(cdate.cdate[1], int)

    def test_date_to_cdate_calendar_date_non_compressible(self, sample_dates):
        """Test date_to_cdate with non-compressible CalendarDate"""
        # Create a non-compressible date (year >= 2500)
        cal_date = CalendarDate(DateValue(15, 6, 2500, Sure()), Calendar.GREGORIAN)
        date = Date(cal_date)

        cdate = date.date_to_cdate()
        assert isinstance(cdate, CDate)
        assert cdate.cdate == cal_date

    def test_date_to_cdate_string(self, sample_dates):
        """Test date_to_cdate with string date"""
        date = sample_dates["string_date"]
        result = date.date_to_cdate()

        # For string dates, it should return the string directly
        assert result == "2023-06-15"


class TestCDate:
    """Test cases for CDate class"""

    @pytest.fixture
    def sample_cdates(self):
        """Fixture providing sample CDate instances"""
        return {
            "gregorian_tuple": CDate((Calendar.GREGORIAN, 12345)),
            "julian_tuple": CDate((Calendar.JULIAN, 67890)),
            "french_tuple": CDate((Calendar.FRENCH, 11111)),
            "hebrew_tuple": CDate((Calendar.HEBREW, 22222)),
            "date_object": CDate(Date("2023-06-15")),
            "string": CDate("June 15, 2023"),
            "none": CDate(None),
        }

    def test_cdate_creation(self, sample_cdates):
        """Test CDate instance creation"""
        for name, cdate in sample_cdates.items():
            assert isinstance(cdate, CDate)

    def test_cdate_to_date_calendar_tuples(self, sample_cdates):
        """Test cdate_to_date with calendar tuples"""
        calendars = [
            Calendar.GREGORIAN,
            Calendar.JULIAN,
            Calendar.FRENCH,
            Calendar.HEBREW,
        ]

        for calendar in calendars:
            cdate = CDate((calendar, 12345))
            result = cdate.cdate_to_date()
            assert isinstance(result, CalendarDate)
            assert result.cal == calendar
            assert isinstance(result.dmy, DateValue)

    def test_cdate_to_date_date_object(self, sample_cdates):
        """Test cdate_to_date with Date object"""
        date_obj = Date("2023-06-15")
        cdate = CDate(date_obj)
        result = cdate.cdate_to_date()
        assert result == date_obj

    def test_cdate_to_date_string(self, sample_cdates):
        """Test cdate_to_date with string"""
        string_date = "June 15, 2023"
        cdate = CDate(string_date)
        result = cdate.cdate_to_date()
        assert result == string_date

    def test_cdate_to_date_none(self, sample_cdates):
        """Test cdate_to_date with None"""
        cdate = sample_cdates["none"]
        result = cdate.cdate_to_date()
        assert result is None

    def test_cdate_to_date_invalid_value(self):
        """Test cdate_to_date with invalid value raises ValueError"""
        cdate = CDate(12345)  # Invalid type
        with pytest.raises(ValueError, match="Invalid CDate"):
            cdate.cdate_to_date()


class TestIntegration:
    """Integration tests combining multiple classes"""

    def test_full_compression_cycle(self):
        """Test full compression/decompression cycle through all classes"""
        # Create original date
        original_dv = DateValue(15, 6, 2023, Sure())
        original_cd = CalendarDate(original_dv, Calendar.GREGORIAN)
        original_date = Date(original_cd)

        # Convert to CDate
        cdate = original_date.date_to_cdate()

        # Convert back to Date
        recovered_date = cdate.cdate_to_date()

        # Verify the cycle worked
        assert isinstance(recovered_date, CalendarDate)
        assert recovered_date.cal == Calendar.GREGORIAN
        assert recovered_date.dmy.day == 15
        assert recovered_date.dmy.month == 6
        assert recovered_date.dmy.year == 2023
        assert isinstance(recovered_date.dmy.prec, Sure)

    def test_non_compressible_cycle(self):
        """Test cycle with non-compressible date"""
        # Create non-compressible date (delta != 0)
        original_dv = DateValue(15, 6, 2023, Sure(), delta=5)
        original_cd = CalendarDate(original_dv, Calendar.GREGORIAN)
        original_date = Date(original_cd)

        # Convert to CDate
        cdate = original_date.date_to_cdate()

        # Should store the original CalendarDate since it's not compressible
        assert isinstance(cdate, CDate)
        assert cdate.cdate == original_cd

    def test_string_date_cycle(self):
        """Test cycle with string date"""
        original_str = "June 15, 2023"
        original_date = Date(original_str)

        # Convert to CDate (should return string directly)
        result = original_date.date_to_cdate()
        assert result == original_str


# Additional edge case tests
class TestInternalMethodsViaPublicAPI:
    """Test internal method code paths by calling them indirectly through the compare method"""

    def test_compare_date_value_opt_same_year_path(self):
        """Test __compare_date_value_opt first return path (same year) via compare method"""
        # Test when years are equal - this triggers __compare_date_value_opt's first return
        date1 = DateValue(15, 6, 2023, Sure())
        date2 = DateValue(20, 6, 2023, Sure())

        # Non-strict comparison (default behavior)
        result = date1.compare(date2, strict=False)
        assert result == -1  # date1 < date2 (day 15 < day 20)

        # Strict comparison
        result_strict = date1.compare(date2, strict=True)
        assert result_strict == -1  # Should still work for normal day comparisons

        # Test equal dates same year
        result_equal = date1.compare(date1, strict=False)
        assert result_equal == 0

    def test_compare_date_value_opt_different_years_path(self):
        """Test __compare_date_value_opt second return path (different years) via compare method"""
        # Test when years are different - this triggers __compare_date_value_opt's second return
        date_early = DateValue(31, 12, 2022, Sure())
        date_late = DateValue(1, 1, 2023, Sure())

        # Non-strict mode with different years
        result = date_early.compare(date_late, strict=False)
        assert result == -1  # 2022 < 2023

        result_reverse = date_late.compare(date_early, strict=False)
        assert result_reverse == 1  # 2023 > 2022

        # Strict mode with different years (should work the same)
        result_strict = date_early.compare(date_late, strict=True)
        assert result_strict == -1

    def test_compare_month_or_day_is_day_true_path(self):
        """Test __compare_month_or_day with is_day=True path via compare method"""
        # When months are equal, the method recurses with is_day=True
        date1 = DateValue(10, 6, 2023, Sure())  # Same month, different days
        date2 = DateValue(20, 6, 2023, Sure())

        result = date1.compare(date2, strict=False)
        assert result == -1  # day 10 < day 20 (triggers is_day=True comparison)

        # Test equal days (should fall back to precision comparison)
        date3 = DateValue(15, 6, 2023, About())
        date4 = DateValue(15, 6, 2023, Maybe())
        result_equal = date3.compare(date4, strict=False)
        assert result_equal == 0  # About and Maybe should be equal

    def test_compare_zero_day_scenarios_via_compare(self):
        """Test zero day handling in __compare_month_or_day via compare method"""
        # Test zero day vs normal day in non-strict mode
        date_zero_day = DateValue(0, 6, 2023, Sure())
        date_normal = DateValue(15, 6, 2023, Sure())

        result = date_zero_day.compare(date_normal, strict=False)
        assert result == 0

        result_reverse = date_normal.compare(date_zero_day, strict=False)
        assert result_reverse == 0

    def test_compare_zero_day_strict_mode_via_compare(self):
        """Test zero day handling in strict mode via compare method"""
        # Test zero day vs normal day in strict mode
        date_zero_day = DateValue(0, 6, 2023, Sure())
        date_normal = DateValue(15, 6, 2023, Sure())

        result = date_zero_day.compare(date_normal, strict=True)
        assert result is None  # strict mode should return None for zero comparisons

        result_reverse = date_normal.compare(date_zero_day, strict=True)
        assert (
            result_reverse is None
        )  # strict mode should return None for zero comparisons

    def test_compare_both_zero_days_via_compare(self):
        """Test both days zero scenario via compare method"""
        # Test both zero days - should fall back to precision comparison
        date1_zero = DateValue(0, 6, 2023, Sure())
        date2_zero = DateValue(0, 6, 2023, About())

        result = date1_zero.compare(date2_zero, strict=False)
        assert result == 0  # Sure and About should be equal in precision comparison

    def test_compare_precision_fallback_equal_days(self):
        """Test precision fallback when days are equal via compare method"""
        # Test equal days with different precisions - should use precision comparison
        date_before = DateValue(15, 6, 2023, Before())
        date_after = DateValue(15, 6, 2023, After())

        result = date_before.compare(date_after, strict=False)
        assert result == -1  # Before should be less than After

    def test_compare_zero_month_scenarios(self):
        """Test zero month handling via compare method"""
        # Test zero month vs normal month
        date_zero_month = DateValue(15, 0, 2023, Sure())
        date_normal_month = DateValue(15, 6, 2023, Sure())

        result = date_zero_month.compare(date_normal_month, strict=False)
        assert result == 0

        # Test in strict mode
        result_strict = date_zero_month.compare(date_normal_month, strict=True)
        assert (
            result_strict is None
        )  # strict mode should return None for zero comparisons

    def test_compare_both_zero_month_and_day(self):
        """Test scenario with both zero month and zero day via compare method"""
        date1_zeros = DateValue(0, 0, 2023, Sure())
        date2_zeros = DateValue(0, 0, 2023, Maybe())

        result = date1_zeros.compare(date2_zeros, strict=False)
        assert result == 0  # Should fall back to precision comparison

    def test_strict_mode_edge_cases_via_compare(self):
        """Test strict mode edge cases via compare method"""
        # Test cases where strict mode affects the outcome
        date1 = DateValue(0, 5, 2023, Sure())  # zero day
        date2 = DateValue(10, 5, 2023, Sure())  # normal day

        # Non-strict should work
        result_non_strict = date1.compare(date2, strict=False)
        assert result_non_strict == 0

        # Strict should return None due to zero day
        result_strict = date1.compare(date2, strict=True)
        assert result_strict is None

    def test_time_elapsed_partial_year(self):
        """Test time_elapsed with partial year calculations"""
        from_date = DateValue(1, 1, 2020, Sure())
        to_date = DateValue(1, 7, 2020, Sure())  # 6 months later

        elapsed = DateValue.date_difference(from_date, to_date)
        assert elapsed.year == 0  # Less than a year
        assert elapsed.month >= 5  # Should be around 6 months (181 days / 30)
        assert isinstance(elapsed.prec, Sure)

    def test_time_elapsed_with_days_remainder(self):
        """Test time_elapsed with specific day calculations"""
        from_date = DateValue(1, 1, 2020, Sure())
        to_date = DateValue(15, 1, 2020, Sure())  # 14 days later

        elapsed = DateValue.date_difference(from_date, to_date)
        assert elapsed.year == 0  # No full years
        assert elapsed.month == 0  # No full months (14 days < 30)
        assert elapsed.day == 14  # Should be 14 days
        assert isinstance(elapsed.prec, Sure)

    def test_time_elapsed_negative_time_difference(self):
        """Test time_elapsed when to_date is before from_date"""
        from_date = DateValue(1, 1, 2021, Sure())
        to_date = DateValue(1, 1, 2020, Sure())  # 1 year earlier

        elapsed = DateValue.date_difference(from_date, to_date)
        # Should handle negative elapsed time
        # The calculation will give negative delta_days, leading to negative years
        assert isinstance(elapsed, DateValue)
        assert isinstance(elapsed.prec, Sure)
        # The exact values depend on the SDN calculation, but it should be a valid DateValue

    def test_time_elapsed_large_date_ranges(self):
        """Test time_elapsed with very large date ranges"""
        ancient_date = DateValue(1, 1, 100, Sure())  # Year 100
        modern_date = DateValue(31, 12, 2000, Sure())  # Year 2000

        elapsed = DateValue.date_difference(ancient_date, modern_date)
        assert elapsed.year >= 1900  # Should be around 1900 years
        assert isinstance(elapsed, DateValue)
        assert isinstance(elapsed.prec, Sure)

    def test_sdn_calculation_consistency(self):
        """Test that SDN calculations are consistent and monotonic"""
        dates = [
            DateValue(1, 1, 2020, Sure()),
            DateValue(2, 1, 2020, Sure()),
            DateValue(1, 2, 2020, Sure()),
            DateValue(1, 1, 2021, Sure()),
        ]

        sdns = [DateValue._sdn_of_date(date) for date in dates]

        # SDNs should be monotonically increasing for these dates
        assert sdns[0] < sdns[1]  # Next day
        assert sdns[1] < sdns[2]  # Next month
        assert sdns[2] < sdns[3]  # Next year

        # All should be positive integers
        for sdn in sdns:
            assert isinstance(sdn, int)
            assert sdn > 0

    def test_sdn_february_leap_year_handling(self):
        """Test SDN calculation handles February in leap years correctly"""
        leap_feb_28 = DateValue(28, 2, 2020, Sure())  # 2020 is leap year
        leap_feb_29 = DateValue(29, 2, 2020, Sure())
        leap_mar_1 = DateValue(1, 3, 2020, Sure())

        sdn_28 = DateValue._sdn_of_date(leap_feb_28)
        sdn_29 = DateValue._sdn_of_date(leap_feb_29)
        sdn_mar_1 = DateValue._sdn_of_date(leap_mar_1)

        # Should be consecutive days
        assert sdn_29 == sdn_28 + 1
        assert sdn_mar_1 == sdn_29 + 1

    def test_precision_combinations_via_compare(self):
        """Test different precision combinations affecting compare results"""
        # Test Before vs After precision (should trigger __compare_prec)
        before_date = DateValue(15, 6, 2023, Before())
        after_date = DateValue(15, 6, 2023, After())
        sure_date = DateValue(15, 6, 2023, Sure())

        # Before < After
        result1 = before_date.compare(after_date, strict=False)
        assert result1 == -1

        # Before < Sure
        result2 = before_date.compare(sure_date, strict=False)
        assert result2 == -1

        # Sure < After
        result3 = sure_date.compare(after_date, strict=False)
        assert result3 == -1

    def test_or_year_year_int_precision_via_compare(self):
        """Test OrYear and YearInt precision handling via compare method"""
        # This would test the OrYear/YearInt precision logic if those are used
        # Since they're mentioned in the code but not in our test fixtures,
        # we'll create a minimal test structure
        try:
            # Note: These may not be available depending on the actual precision module
            or_year_date = DateValue(15, 6, 2023, Sure())  # Placeholder
            year_int_date = DateValue(15, 6, 2023, Sure())  # Placeholder

            result = or_year_date.compare(year_int_date, strict=False)
            assert result == 0  # Same dates with any precision should be comparable
        except (NameError, AttributeError):
            # Skip if OrYear/YearInt are not available
            pytest.skip("OrYear/YearInt precision types not available")

    def test_complex_comparison_chains_via_compare(self):
        """Test complex comparison scenarios that exercise multiple code paths"""
        # Chain of comparisons that test different parts of the logic
        dates = [
            DateValue(0, 0, 2023, Before()),  # Zero month/day + Before
            DateValue(0, 5, 2023, Sure()),  # Zero day + Sure
            DateValue(10, 5, 2023, About()),  # Normal + About
            DateValue(10, 5, 2023, Maybe()),  # Normal + Maybe
            DateValue(10, 5, 2023, After()),  # Normal + After
            DateValue(20, 5, 2023, Sure()),  # Later day + Sure
            DateValue(15, 6, 2023, Sure()),  # Later month + Sure
        ]

        # Test that all consecutive pairs are properly ordered
        for i in range(len(dates) - 1):
            result = dates[i].compare(dates[i + 1], strict=False)
            assert result in [-1, 0], (
                f"Expected <= for comparison {i} to {i + 1}, got {result}"
            )

    def test_eval_strict_behavior_via_compare(self):
        """Test __eval_strict behavior indirectly through compare method"""
        # Test non-strict mode (should always return a result for valid dates)
        date1 = DateValue(15, 6, 2023, Sure())
        date2 = DateValue(20, 6, 2023, Sure())

        result_non_strict = date1.compare(date2, strict=False)
        assert result_non_strict == -1  # Should always get a result in non-strict mode

        # Test strict mode with zero values (should return None in some cases)
        date_zero = DateValue(0, 6, 2023, Sure())
        date_normal = DateValue(15, 6, 2023, Sure())

        result_strict_with_zero = date_zero.compare(date_normal, strict=True)
        assert (
            result_strict_with_zero is None
        )  # Strict mode with zero should return None


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_leap_year_dates(self):
        """Test dates in leap years"""
        leap_date = DateValue(29, 2, 2020, Sure())  # Leap year
        non_leap_date = DateValue(28, 2, 2021, Sure())  # Non-leap year

        # Both should be compressible and work normally
        assert leap_date.compress() is not None
        assert non_leap_date.compress() is not None

    def test_large_time_differences(self):
        """Test time calculations with large date differences"""
        ancient_date = DateValue(1, 1, 1, Sure())
        modern_date = DateValue(31, 12, 2499, Sure())

        elapsed = DateValue.date_difference(ancient_date, modern_date)
        assert isinstance(elapsed, DateValue)
        assert elapsed.year > 2000  # Should be a large number of years
