# Unit Tests Inventory

**Last Updated:** October 31, 2025
**Total Unit Test Files:** 22

## Overview

This document catalogs all unit tests in the GenewebPy project. Unit tests focus on testing individual functions, classes, and methods in isolation with minimal dependencies. This includes parser component tests that test individual parsing functions without requiring database or full system integration.

---

## Core Data Types

### test_calendar.py
**Path:** `tests/test_calendar.py`  
**Purpose:** Test calendar calculations and date operations

**Test Functions:**
- `test_calendar_date_creation` - Calendar date object creation
- `test_calendar_date_equality` - Calendar date equality comparisons
- `test_date_creation` - Date object instantiation
- `test_date_equality_calendar_dates` - Date equality with calendar dates
- `test_date_equality_strings` - Date equality with string representations
- `test_compare_date_value_opt_same_year_path` - Date comparison same year
- `test_compare_date_value_opt_different_years_path` - Date comparison different years
- `test_compare_month_or_day_is_day_true_path` - Month/day comparison logic
- `test_compare_zero_day_scenarios_via_compare` - Zero day handling
- `test_compare_zero_day_strict_mode_via_compare` - Strict mode zero day
- `test_compare_both_zero_days_via_compare` - Both dates with zero days
- `test_compare_precision_fallback_equal_days` - Precision fallback logic
- `test_compare_zero_month_scenarios` - Zero month handling
- `test_compare_both_zero_month_and_day` - Zero month and day
- `test_strict_mode_edge_cases_via_compare` - Strict mode edge cases
- `test_time_elapsed_partial_year` - Time calculation partial year
- `test_time_elapsed_with_days_remainder` - Time calculation with remainder
- `test_time_elapsed_negative_time_difference` - Negative time differences
- `test_time_elapsed_large_date_ranges` - Large date range calculations
- `test_sdn_calculation_consistency` - SDN (Serial Day Number) consistency
- `test_sdn_february_leap_year_handling` - Leap year handling in SDN

**Coverage:** Calendar and date arithmetic operations

---

### test_date.py
**Path:** `tests/test_date.py`  
**Purpose:** Test date data structures and precision handling

**Test Functions:**
- `test_precision_instantiation` - Precision enum creation
- `test_sure_instantiation` - Sure precision
- `test_about_instantiation` - About precision (~)
- `test_maybe_instantiation` - Maybe precision (?)
- `test_before_instantiation` - Before precision (<)
- `test_after_instantiation` - After precision (>)
- `test_oryear_valid` - OrYear precision valid cases
- `test_oryear_invalid_precision_raises` - OrYear invalid precision
- `test_yearint_valid` - YearInt precision valid cases
- `test_yearint_invalid_precision_raises` - YearInt invalid precision
- `test_datevalue_creation` - DateValue dataclass creation
- `test_calendar_date_gregorian` - Gregorian calendar dates
- `test_calendar_date_julian` - Julian calendar dates
- `test_calendar_date_french` - French Republican calendar
- `test_calendar_date_hebrew` - Hebrew calendar dates
- `test_date_as_calendar_date` - Date to CalendarDate conversion
- `test_date_as_text` - Date to text representation

**Coverage:** Date precision, calendar systems, date representations

---

### test_date_value.py
**Path:** `tests/test_date_value.py`  
**Purpose:** Test date value structures and operations

**Test Functions:**
- Tests for DateValue dataclass
- Date precision handling
- Date comparison operations
- Date serialization/deserialization

**Coverage:** DateValue class operations

---

### test_death.py
**Path:** `tests/test_death.py`  
**Purpose:** Test death status and burial types

**Test Functions:**
- Death status enumeration tests
- Burial type tests
- Death reason handling
- Death date validation

**Coverage:** Death and burial data types

---

### test_events.py
**Path:** `tests/test_events.py`  
**Purpose:** Test personal and family event types

**Test Functions:**
- `test_personal_singleton_event_instantiation` - Personal event creation
- `test_personal_named_event` - Named personal events
- `test_personal_event_dataclass` - PersonalEvent dataclass
- `test_personal_event_match` - Event pattern matching
- `test_family_singleton_event_instantiation` - Family event creation
- `test_family_named_event` - Named family events
- `test_family_event_dataclass` - FamilyEvent dataclass
- `test_family_event_match` - Family event pattern matching

**Coverage:** Event data structures (baptism, marriage, custom events)

---

### test_family.py
**Path:** `tests/test_family.py`  
**Purpose:** Test family data structures

**Test Functions:**
- `test_init_with_list_of_ints` - Family initialization with IDs
- `test_init_empty_list` - Empty family
- `test_init_type_check_allows_mixed_types` - Mixed type handling
- `test_from_couple_with_ints` - Couple creation
- `test_is_couple_true` - Couple detection positive
- `test_is_couple_false` - Couple detection negative

**Coverage:** Family dataclass creation and methods

---

### test_person.py
**Path:** `tests/test_person.py`  
**Purpose:** Test person data structures

**Test Functions:**
- `test_place_full_creation` - Place object creation
- `test_person_minimal_stubs` - Minimal person creation
- `test_person_with_empty_lists` - Person with empty collections

**Coverage:** Person and Place dataclasses

---

### test_title.py
**Path:** `tests/test_title.py`  
**Purpose:** Test title data structures

**Test Functions:**
- `test_title_name_base_instantiation` - TitleName base creation
- `test_use_main_title` - UseMainTitle variant
- `test_no_title` - NoTitle variant
- `test_title_name` - TitleName variant
- `test_title_dataclass` - Title dataclass
- `test_title_match` - Title pattern matching
- `test_titlename_equality` - TitleName equality
- `test_title_namebase_equality` - TitleNameBase equality
- `test_title_equality` - Title equality
- `test_title_without_date_mapper` - Title without dates
- `test_title_with_date_mapper` - Title with date ranges
- `test_no_title_date_mapper` - NoTitle mapping

**Coverage:** Title and nobility name handling

---

## Utility Functions

### test_name_utils_2.py
**Path:** `tests/test_name_utils_2.py`  
**Purpose:** Test name processing and matching utilities

**Test Functions:**
- `test_unaccent_utf_8` - Unicode accent removal
- `test_next_chars_if_equiv` - Character equivalence
- `test_lower` - Lowercase conversion
- `test_title` - Title case conversion
- `test_abbrev` - Name abbreviation
- `test_roman_number` - Roman numeral detection
- `test_abbreviate_name` - Full name abbreviation
- `test_strip_lower` - Strip and lowercase
- `test_abbreviate_lower` - Abbreviate and lowercase pipeline
- `test_concat` - String concatenation
- `test_contains_forbidden_char` - Forbidden character detection
- `test_integration_genealogy_workflow` - End-to-end name processing
- `test_name_matching_scenarios` - Name matching edge cases
- `test_unicode_international_names` - International name support
- `test_constants_accessibility` - Constant definitions
- `test_title_numbers_and_special_chars` - Title with special chars
- `test_title_edge_cases` - Title edge cases
- `test_title_mixed_separators` - Mixed separator handling
- `test_abbrev_saint_abbreviations` - Saint name abbreviation
- `test_abbrev_particle_removal` - Particle removal (de, von, etc.)
- `test_abbrev_mixed_case_particles` - Mixed case particles
- `test_abbrev_multiple_particles` - Multiple particles
- `test_abbrev_no_changes_needed` - No abbreviation needed
- `test_abbrev_edge_cases` - Abbreviation edge cases
- `test_abbrev_ier_replacement` - -ier suffix replacement
- `test_roman_number_valid_at_start` - Roman numeral at start
- `test_roman_number_valid_after_space` - Roman numeral after space
- `test_roman_number_mixed_case` - Mixed case Roman numerals
- `test_roman_number_partial_match` - Partial Roman numeral match
- `test_roman_number_edge_cases` - Roman numeral edge cases
- `test_abbreviate_name_vowel_removal` - Vowel removal in abbreviation
- `test_abbreviate_name_character_replacements` - Character substitution
- `test_abbreviate_name_ph_replacement` - PH replacement
- `test_abbreviate_name_h_removal` - H removal
- `test_abbreviate_name_s_removal_at_end` - Trailing S removal
- `test_abbreviate_name_double_consonant_removal` - Double consonant reduction
- `test_abbreviate_name_roman_numerals_preserved` - Preserve Roman numerals
- `test_abbreviate_name_case_preservation` - Case preservation
- `test_abbreviate_name_edge_cases` - Abbreviation edge cases
- `test_abbreviate_name_multiple_words` - Multi-word abbreviation
- `test_strip_lower_basic_functionality` - Basic strip/lower
- `test_strip_lower_accented_characters` - Accented character handling
- `test_strip_lower_multiple_spaces` - Multiple space handling
- `test_strip_lower_special_characters` - Special character handling
- `test_strip_lower_edge_cases` - Strip/lower edge cases
- `test_abbreviate_lower_full_pipeline` - Full pipeline test
- `test_abbreviate_lower_case_normalization` - Case normalization
- `test_abbreviate_lower_particles_and_phonetic` - Particles + phonetic
- `test_abbreviate_lower_edge_cases` - Pipeline edge cases
- `test_concat_basic_functionality` - Basic concatenation
- `test_concat_empty_strings` - Empty string concatenation
- `test_concat_whitespace_handling` - Whitespace handling
- `test_concat_special_characters` - Special character concatenation
- `test_contains_forbidden_char_found_single` - Single forbidden char
- `test_contains_forbidden_char_found_multiple` - Multiple forbidden chars
- `test_contains_forbidden_char_not_found` - No forbidden chars
- `test_contains_forbidden_char_edge_cases` - Forbidden char edge cases
- `test_genealogy_name_processing_workflow` - Genealogy workflow
- `test_data_validation_and_cleaning` - Data validation
- `test_unicode_and_international_names` - Unicode name handling

**Coverage:** 60+ tests for name processing, matching, and validation

---

### test_secure_string.py
**Path:** `tests/test_secure_string.py`  
**Purpose:** Test secure string utilities

**Test Functions:**
- Secure string encoding/decoding
- String sanitization
- Security-related string operations

**Coverage:** String security utilities

---

### test_translator.py
**Path:** `tests/test_translator.py`  
**Purpose:** Test translation utilities

**Test Functions:**
- Translation key lookup
- Locale handling
- Translation fallback logic

**Coverage:** i18n translation system

---

## Algorithm Tests

### test_consanguinity_rate.py
**Path:** `tests/test_consanguinity_rate.py`  
**Purpose:** Test consanguinity (blood relationship) calculations

**Test Functions:**
- Consanguinity rate calculations
- Relationship degree determination
- Family tree traversal for consanguinity

**Coverage:** Genetic relationship calculations

---

### test_sosa.py
**Path:** `tests/test_sosa.py`  
**Purpose:** Test Sosa-Stradonitz numbering system

**Test Functions:**
- Sosa number calculation
- Ancestral numbering
- Generation detection

**Coverage:** Genealogical numbering system

---

## Database Tests

### test_database.py
**Path:** `tests/test_database.py`  
**Purpose:** Test database service and operations

**Test Functions:**
- Database connection handling
- Schema initialization
- Basic CRUD operations

**Coverage:** Database service layer

---

## Web Server Tests

### test_gwsetup.py
**Path:** `tests/test_gwsetup.py`  
**Purpose:** Test gwsetup CLI commands

**Test Functions:**
- Database create command
- Database gwc command
- Database delete command
- CLI argument parsing

**Coverage:** gwsetup command-line interface

---

### test_gwd_root_impl.py
**Path:** `tests/test_gwd_root_impl.py`  
**Purpose:** Test gwd (GeneWeb Daemon) root implementation

**Test Functions:**
- Route handling
- Request processing
- Response generation

**Coverage:** Web server core functionality

---

## Utilities

### utils/test_buffer.py
**Path:** `tests/utils/test_buffer.py`  
**Purpose:** Test buffer utilities

**Test Functions:**
- Buffer read operations
- Buffer write operations
- Buffer management

**Coverage:** Buffer utility functions

---

## Parser Components

### import_tests/gw/test_gw_import.py
**Path:** `tests/import_tests/gw/test_gw_import.py`  
**Purpose:** Test GeneWeb file parsing - converts .gw files to GwSyntax data structures

**Test Classes:**
- `TestBlockParsing` - 6 tests for parsing person/family blocks
- `TestFamilyParsing` - 7 tests for family structure parsing
- `TestRelationParsing` - 5 tests for relation parsing
- `TestPersonalEventParsing` - 4 tests for personal event parsing
- `TestFamilyEventParsing` - 18 tests for family event parsing (marriage, divorce, separation, etc.)
- `TestDirectiveParsing` - 3 tests for directive parsing
- `TestComplexScenarios` - 20+ tests for complex parsing scenarios

**Total:** 60+ tests for .gw file parsing logic

**Coverage:** Complete .gw file format parsing

---

### import_tests/gw/test_gw_field_parsing.py
**Path:** `tests/import_tests/gw/test_gw_field_parsing.py`  
**Purpose:** Test field-level parsing accuracy across different test files

**Test Classes:**
- `TestMinimalGwParsing` - Tests parsing minimal.gw (12 persons, 5 families)
- `TestMediumGwParsing` - Tests parsing medium.gw (50 persons, 20 families)
- `TestBigGwParsing` - Tests parsing big.gw (1000+ persons, 400+ families)
- `TestFieldCompletenessAllFiles` - Validates field completeness across all test files

**Total:** 40+ tests for field parsing validation

**Coverage:** Field-level parsing accuracy validation

---

### import_tests/gw/test_gw_dates.py
**Path:** `tests/import_tests/gw/test_gw_dates.py`  
**Purpose:** Test date parsing functionality in GeneWeb parser

**Test Classes:**
- `TestDatePrecisionMarkers` - Tests ~, ?, <, > precision markers
- `TestDateRanges` - Tests date range parsing (between dates)
- `TestCalendarSuffixes` - Tests calendar system suffixes (G, J, F, H)
- `TestComplexDateFormats` - Tests complex date formats
- `TestOptionalDateParsing` - Tests optional date handling
- `TestDateEdgeCases` - Tests edge cases in date parsing
- `TestDateComponentParsing` - Tests year/month/day component parsing
- `TestDateValidation` - Tests date validation logic

**Total:** 50+ tests for date parsing

**Coverage:** Date parser module (date_parser.py)

---

### import_tests/gw/test_gw_utils.py
**Path:** `tests/import_tests/gw/test_gw_utils.py`  
**Purpose:** Test utility functions for .gw file processing

**Test Classes:**
- `TestFieldsTokenization` - Tests field tokenization logic
- `TestCopyDecode` - Tests string decoding operations
- `TestGetField` - Tests field extraction from records
- `TestCutSpace` - Tests whitespace handling
- `TestLineStream` - Tests line streaming functionality
- `TestFieldsWithSpecialCharacters` - Tests special character handling

**Total:** 40+ tests for parser utilities

**Coverage:** Parser utility functions (utils.py)

---

### import_tests/gw/test_gw_converter.py
**Path:** `tests/import_tests/gw/test_gw_converter.py`  
**Purpose:** Test conversion from GwSyntax to application types

**Test Functions:**
- GwSyntax to Person conversion
- GwSyntax to Family conversion
- Date conversion
- Name conversion
- Event conversion
- Relation conversion

**Total:** ~10 tests for type conversion

**Coverage:** GW format to application type conversion

---

## Summary Statistics

### By Category:
- **Data Types:** 8 test files (calendar, date, death, events, family, person, title, date_value)
- **Utilities:** 3 test files (name_utils, secure_string, translator)
- **Algorithms:** 2 test files (consanguinity, sosa)
- **Database:** 1 test file
- **Web Server:** 2 test files (gwsetup, gwd_root)
- **Utils:** 1 test file (buffer)
- **Parser Components:** 5 test files (gw_import, gw_field_parsing, gw_dates, gw_utils, gw_converter)

### Total:
- **22 unit test files**
- **400+ individual test functions**
- **Coverage areas:** Data structures, business logic, utilities, algorithms, parser components

---

## Running Unit Tests

```bash
# Run all unit tests
pytest tests/ -v --ignore=tests/repositories/ --ignore=tests/gwc_database_roundtrip/ --ignore=tests/golden_master/ --ignore=tests/tests_wserver/ --ignore=tests/database/

# Run specific test file
pytest tests/test_calendar.py -v

# Run parser unit tests
pytest tests/import_tests/gw/ -v

# Run with coverage
pytest tests/test_calendar.py --cov=src.libraries --cov-report=html
pytest tests/import_tests/gw/ --cov=src.script.gw_parser --cov-report=html

# Run tests matching pattern
pytest tests/ -k "test_date" -v
```

---

## Test Organization

Unit tests follow these conventions:
- **File naming:** `test_<module>.py`
- **Function naming:** `test_<function>_<scenario>`
- **Location:** Directly in `tests/`, `tests/utils/`, or `tests/import_tests/gw/`
- **Dependencies:** Minimal, mostly testing pure functions
- **Fixtures:** Defined in conftest.py or inline

---

## Adding New Unit Tests

When adding new unit tests:

1. **Create test file:** `tests/test_<module>.py`
2. **Import module:** `from src.libraries.<module> import ...`
3. **Write test functions:** Use `test_` prefix
4. **Use fixtures:** For common setup
5. **Use parametrize:** For multiple test cases
6. **Add assertions:** Clear, specific assertions
7. **Update this document:** Add new tests to inventory

**Example:**
```python
import pytest
from src.libraries.date import Date, Precision

def test_date_creation():
    """Test Date object creation"""
    date = Date(year=2000, month=1, day=1, precision=Precision.SURE)
    assert date.year == 2000
    assert date.month == 1
    assert date.day == 1
    assert date.precision == Precision.SURE

@pytest.mark.parametrize("year,month,day", [
    (2000, 1, 1),
    (1950, 12, 31),
    (1800, 6, 15),
])
def test_date_valid_dates(year, month, day):
    """Test Date creation with valid dates"""
    date = Date(year=year, month=month, day=day)
    assert date.year == year
```

---

## See Also

- [Integration Tests](./INTEGRATION.md) - Tests for component interactions
- [E2E Tests](./E2E.md) - End-to-end system tests
- [Testing Policy](../TESTING_POLICY.md) - Complete testing guidelines
