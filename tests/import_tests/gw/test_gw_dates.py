"""Tests for date parsing functionality in GeneWeb parser.

Focus on improving coverage for date_parser.py module.
"""

import pytest
from script.gw_parser.date_parser import date_of_string_py, get_optional_date
from libraries.date import (
    CalendarDate,
    Calendar,
    OrYear,
    YearInt,
    About,
    Maybe,
    Before,
    After,
    Sure,
)


class TestDatePrecisionMarkers:
    """Test date precision markers: ~, ?, <, >"""

    def test_date_with_about_marker(self):
        """Test ~ (about) precision marker."""
        result = date_of_string_py("~1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1950
        assert isinstance(result.dmy.prec, About)

    def test_date_with_maybe_marker(self):
        """Test ? (maybe) precision marker."""
        result = date_of_string_py("?1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1950
        assert isinstance(result.dmy.prec, Maybe)

    def test_date_with_before_marker(self):
        """Test < (before) precision marker."""
        result = date_of_string_py("<1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1950
        assert isinstance(result.dmy.prec, Before)

    def test_date_with_after_marker(self):
        """Test > (after) precision marker."""
        result = date_of_string_py(">1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1950
        assert isinstance(result.dmy.prec, After)

    # @pytest.mark.skip(reason="Multiple precision markers not supported")
    # def test_date_with_multiple_precision_markers(self):
    #     """Test multiple precision markers."""
    #     result = date_of_string_py("~?1950", 0)
    #     assert result is not None


class TestDateRanges:
    """Test date range formats."""

    def test_or_year_format(self):
        """Test OrYear format: 1900|1901"""
        result = date_of_string_py("1900|1901", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1900
        assert isinstance(result.dmy.prec, OrYear)
        assert result.dmy.prec.date_value.year == 1901

    def test_year_range_format(self):
        """Test YearInt range format: 1900..1905"""
        result = date_of_string_py("1900..1905", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1900
        assert isinstance(result.dmy.prec, YearInt)
        assert result.dmy.prec.date_value.year == 1905

    def test_between_format(self):
        """Test 'between' date format (same as YearInt)."""
        result = date_of_string_py("1900..1905", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1900
        assert isinstance(result.dmy.prec, YearInt)
        assert result.dmy.prec.date_value.year == 1905


class TestCalendarSuffixes:
    """Test calendar suffix parsing: G, J, F, H"""

    def test_gregorian_calendar_suffix(self):
        """Test Gregorian calendar suffix (G)."""
        result = date_of_string_py("15/03/1950G", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.cal == Calendar.GREGORIAN
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 1950

    def test_julian_calendar_suffix(self):
        """Test Julian calendar suffix (J)."""
        result = date_of_string_py("15/03/1950J", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.cal == Calendar.JULIAN
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 1950

    def test_french_calendar_suffix(self):
        """Test French Republican calendar suffix (F)."""
        result = date_of_string_py("15/03/1950F", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.cal == Calendar.FRENCH
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 1950

    def test_hebrew_calendar_suffix(self):
        """Test Hebrew calendar suffix (H)."""
        result = date_of_string_py("15/03/1950H", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.cal == Calendar.HEBREW
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 1950


class TestComplexDateFormats:
    """Test complex and edge case date formats."""

    # @pytest.mark.skip(reason="Month names not implemented")
    # def test_date_with_month_name(self):
    #     """Test date with month name."""
    #     result = date_of_string_py("15 March 1950", 0)
    #     # Should handle month names if implemented

    def test_text_date(self):
        """Test text date format."""
        result = date_of_string_py("0(some text date)", 0)
        assert result is not None
        assert isinstance(result, str)
        assert result == "some text date"

    def test_year_only(self):
        """Test year-only date."""
        result = date_of_string_py("1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1950
        assert result.dmy.month == 0
        assert result.dmy.day == 0
        assert isinstance(result.dmy.prec, Sure)

    def test_month_year_format(self):
        """Test month/year format."""
        result = date_of_string_py("03/1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == 1950
        assert result.dmy.month == 3
        assert result.dmy.day == 0

    def test_full_date_format(self):
        """Test full date format dd/mm/yyyy."""
        result = date_of_string_py("15/03/1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 1950

    def test_date_with_precision_and_calendar(self):
        """Test date with both precision marker and calendar suffix."""
        result = date_of_string_py("~15/03/1950G", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.cal == Calendar.GREGORIAN
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 1950
        assert isinstance(result.dmy.prec, About)


class TestOptionalDateParsing:
    """Test get_optional_date function."""

    def test_optional_date_with_date(self):
        """Test optional date parsing with valid date."""
        result, remaining = get_optional_date(["1950", "other", "tokens"])
        assert result is not None
        assert "other" in remaining

    def test_optional_date_without_date(self):
        """Test optional date parsing without date."""
        result, remaining = get_optional_date(["#tag", "value"])
        assert result is None
        assert "#tag" in remaining

    def test_optional_date_empty_tokens(self):
        """Test optional date parsing with empty tokens."""
        result, remaining = get_optional_date([])
        assert result is None
        assert remaining == []

    def test_optional_date_with_precision(self):
        """Test optional date with precision markers."""
        result, remaining = get_optional_date(["~1950", "next"])
        assert result is not None

    def test_optional_date_with_full_date(self):
        """Test optional date with full date format."""
        result, remaining = get_optional_date(["15/03/1950", "next"])
        assert result is not None


class TestDateEdgeCases:
    """Test edge cases and error handling."""

    def test_invalid_date_format(self):
        """Test invalid date format."""
        with pytest.raises(Exception):
            date_of_string_py("invalid", 0)

    def test_empty_date_string(self):
        """Test empty date string."""
        # Empty string returns None, doesn't raise
        result = date_of_string_py("", 0)
        assert result is None

    def test_malformed_date(self):
        """Test malformed date."""
        with pytest.raises(Exception):
            date_of_string_py("99/99/9999", 0)

    def test_date_with_only_slashes(self):
        """Test date with only slashes."""
        with pytest.raises(Exception):
            date_of_string_py("//", 0)


# class TestMonthParsing:
#     """Test month name parsing."""

#     @pytest.mark.skip(reason="Month names not implemented")
#     def test_english_month_names(self):
#         """Test English month names."""
#         months = ["January", "February", "March", "April", "May", "June",
#                   "July", "August", "September", "October", "November",
#                   "December"]
#         for i, month in enumerate(months, 1):
#             result = date_of_string_py(f"15 {month} 1950", 0)
#             # Should parse month names if supported

#     @pytest.mark.skip(reason="Month names not implemented")
#     def test_abbreviated_month_names(self):
#         """Test abbreviated month names."""
#         months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
#                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#         for month in months:
#             result = date_of_string_py(f"15 {month} 1950", 0)
#             # Should parse abbreviated months if supported


class TestDateComponentParsing:
    """Test parsing of individual date components."""

    def test_single_digit_day(self):
        """Test single digit day."""
        result = date_of_string_py("5/03/1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.day == 5
        assert result.dmy.month == 3
        assert result.dmy.year == 1950

    def test_single_digit_month(self):
        """Test single digit month."""
        result = date_of_string_py("15/3/1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 1950

    def test_two_digit_year(self):
        """Test two digit year."""
        result = date_of_string_py("15/03/50", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 50

    def test_three_digit_year(self):
        """Test three digit year."""
        result = date_of_string_py("15/03/950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 950

    def test_four_digit_year(self):
        """Test four digit year."""
        result = date_of_string_py("15/03/1950", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.day == 15
        assert result.dmy.month == 3
        assert result.dmy.year == 1950


class TestDateValidation:
    """Test date validation and bounds checking."""

    def test_valid_leap_year_date(self):
        """Test valid leap year date."""
        result = date_of_string_py("29/02/2000", 0)
        assert result is not None

    def test_invalid_leap_year_date(self):
        """Test invalid leap year date."""
        # February 29 in non-leap year - parser is lenient
        result = date_of_string_py("29/02/1900", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.day == 29
        assert result.dmy.month == 2
        assert result.dmy.year == 1900

    def test_day_out_of_range(self):
        """Test day out of valid range."""
        with pytest.raises(Exception):
            date_of_string_py("32/01/1950", 0)

    def test_month_out_of_range(self):
        """Test month out of valid range."""
        # Month 13 should raise exception (only 12 months in a year)
        with pytest.raises(Exception):
            date_of_string_py("15/13/1950", 0)

    def test_negative_year(self):
        """Test negative year (BCE dates)."""
        result = date_of_string_py("-100", 0)
        assert result is not None
        assert isinstance(result, CalendarDate)
        assert result.dmy.year == -100
