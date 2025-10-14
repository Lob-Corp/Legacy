# GeneWeb Parser Test Coverage Report

**Date**: October 14, 2025  
**Total Tests**: 54  
**Overall Coverage**: 86%

## Coverage by Module

| Module | Statements | Missing | Coverage | Status |
|--------|-----------|---------|----------|--------|
| `__init__.py` | 3 | 0 | **100%** | ✅ Complete |
| `data_types.py` | 63 | 0 | **100%** | ✅ Complete |
| `parser.py` | 41 | 1 | **98%** | ✅ Excellent |
| `event_parser.py` | 112 | 10 | **91%** | ✅ Excellent |
| `person_parser.py` | 220 | 23 | **90%** | ✅ Excellent |
| `block_parser.py` | 297 | 38 | **87%** | ✅ Good |
| `stream.py` | 36 | 6 | **83%** | ⚠️ Good |
| `utils.py` | 41 | 9 | **78%** | ⚠️ Fair |
| `date_parser.py` | 148 | 49 | **67%** | ⚠️ Needs Work |
| **TOTAL** | **961** | **136** | **86%** | ✅ Good |

## Detailed Analysis

### ✅ Excellent Coverage (90%+)

#### 1. **__init__.py** - 100%
- All exports tested
- Module interface fully validated

#### 2. **data_types.py** - 100%
- All data type variants covered
- Key, Somebody, and GwSyntax classes fully tested

#### 3. **parser.py** - 98%
- Main entry point `parse_gw_file()` well tested
- Only 1 line missing: error handling edge case (line 68)

#### 4. **event_parser.py** - 91%
- Family and personal event parsing well covered
- **Missing coverage**:
  - Line 110: Unknown event tag error path
  - Line 174: Personal event note parsing edge case
  - Line 205: Event witness parsing edge case
  - Line 227: Witness type parsing
  - Lines 247, 252: Witness reference parsing
  - Line 261: Unparsed tokens error (tested with family events)
  - Lines 285, 290: Personal event edge cases
  - Line 301: Personal event completion

#### 5. **person_parser.py** - 90%
- Person parsing, titles, aliases well covered
- **Missing coverage**:
  - Line 68: Public name parsing edge case
  - Lines 136-137, 139: Image parsing variations
  - Line 147: Access right parsing
  - Line 152: Occupation edge case
  - Lines 160-161, 164-165, 168-169: Baptism date variations
  - Line 188: Death date format variations
  - Line 200: Burial parsing variations
  - Lines 292, 294, 296: Death reason parsing
  - Lines 308-311: Execution death variations
  - Lines 335-336: Parse person reference edge case
  - Line 340: First name parsing error

### ⚠️ Good Coverage (80-89%)

#### 6. **block_parser.py** - 87%
- Family, notes, relations blocks well covered
- **Missing coverage**:
  - Lines 122-123: Comment parsing edge case
  - Lines 134-136, 139-140: Event parsing variations
  - Lines 180-182: Child sex parsing edge cases
  - Lines 193-200: Child special cases (sex prefix, surname variations)
  - Line 237: Common child birth place
  - Line 243: Comment line variation
  - Lines 298, 303: Witness parsing edge cases
  - Line 313: Family source parsing
  - Lines 386, 391: Notes block variations
  - Lines 396, 399: Relations block edge cases
  - Lines 410, 419, 425, 430: Relation parsing variations
  - Lines 436, 441-444: Relation mother parsing
  - Line 469: Block type detection edge case
  - Lines 481, 492: Personal events block variations
  - Line 507: Base notes/wizard notes edge cases

#### 7. **stream.py** - 83%
- Line stream functionality mostly covered
- **Missing coverage**:
  - Line 47: Peek without data
  - Line 50: Push back edge case
  - Lines 53-56: Stream reset/empty cases

### ⚠️ Fair Coverage (70-79%)

#### 8. **utils.py** - 78%
- Basic utilities covered
- **Missing coverage**:
  - Lines 23-25: Escape sequence decoding edge cases
  - Line 43: Token parsing edge case
  - Lines 73-78: `get_field()` and `cut_space()` edge cases

### ⚠️ Needs Improvement (<70%)

#### 9. **date_parser.py** - 67%
- Basic date parsing covered, but many edge cases untested
- **Missing coverage**:
  - Lines 40-41: Date text parsing
  - Line 54: Date precision markers
  - Line 76: Month name parsing
  - Lines 85-101: Various date format variations (OrYear, YearInt, Before, After, etc.)
  - Lines 117, 119: Date precision flags
  - Line 129: Date month validation
  - Lines 133-139: Calendar type parsing (Gregorian, Julian, French, Hebrew)
  - Lines 142-149: Date component parsing edge cases
  - Lines 162, 168: Date range parsing
  - Lines 177, 180, 183: Date precision parsing
  - Lines 186-187, 190, 193: Date validation edge cases
  - Lines 208, 211: Optional date parsing
  - Lines 218-223: Date with calendar suffix parsing

## Test Categories

### 1. Basic Block Tests (11 tests)
- ✅ Family blocks (various marriage types)
- ✅ Notes blocks
- ✅ Relations blocks
- ✅ Personal events blocks
- ✅ Base notes blocks
- ✅ Wizard notes blocks
- ✅ Page extension blocks

### 2. Complex Scenario Tests (14 tests)
- ✅ Families with all features
- ✅ Complex dates
- ✅ Persons with all fields
- ✅ Multiple relations
- ✅ Events with witnesses
- ✅ Marriage histories
- ✅ Nested surnames
- ✅ Mixed content files
- ✅ Death variations
- ✅ Calendar dates
- ✅ Sex overrides
- ✅ Complex titles/aliases
- ✅ All witness types
- ✅ Edge cases

### 3. Family Event Tests (10 tests) - NEW
- ✅ All event types (marriage, bann, contract, license, residence, separation, divorce)
- ✅ Events with witnesses
- ✅ No marriage scenarios
- ✅ Engagement only
- ✅ PACS (French civil union)
- ✅ Annulment
- ✅ Multiple residences
- ✅ Complex dates
- ✅ Notes and sources
- ✅ Custom named events

### 4. Directive Tests (2 tests)
- ✅ Encoding directive
- ✅ GWPlus directive

### 5. Error Handling Tests (1 test)
- ✅ No-fail mode

## Recommendations for Improving Coverage

### Priority 1: Date Parser (67% → 85%+)
**Why**: Date parsing is critical and has the lowest coverage

Add tests for:
1. Text dates (e.g., "0(text date)")
2. Date precision markers (~, ?, <, >)
3. OrYear format (1900|1901)
4. YearInt ranges (1900..1905)
5. Calendar suffixes (G, J, F, H)
6. Date component parsing edge cases
7. Invalid date handling

**Suggested test file**: `test_gw_dates.py`

### Priority 2: Utils (78% → 95%+)
**Why**: Utilities are foundational and should be thoroughly tested

Add tests for:
1. Escape sequence handling (backslash sequences)
2. Underscore to space conversion edge cases
3. `get_field()` with various inputs
4. `cut_space()` edge cases

**Suggested addition**: Add unit tests to existing test file

### Priority 3: Stream (83% → 95%+)
**Why**: Simple module, easy to get to high coverage

Add tests for:
1. Peek on empty stream
2. Push back multiple times
3. Stream exhaustion scenarios

**Suggested addition**: Add unit tests to existing test file

### Priority 4: Block Parser Edge Cases (87% → 92%+)
**Why**: Already good coverage, just need edge cases

Add tests for:
1. Children with sex prefixes (m:, f:)
2. Children with complex surname variations
3. Comment line variations
4. Empty blocks
5. Relation parsing with missing parents

**Suggested tests**: Add to existing complex scenario tests

### Priority 5: Person Parser Edge Cases (90% → 95%+)
**Why**: Already excellent, minor gaps

Add tests for:
1. All death reason codes (k, m, e, s variations)
2. Burial variations
3. Image parsing edge cases
4. All access right types

**Suggested tests**: Extend existing person field tests

## Coverage Goals

- **Starting Point**: 86%
- **Current**: 88% ✓ (+2%)
- **Short-term** (Next target): 90%
- **Medium-term** (All priorities): 93%
- **Long-term** (Comprehensive): 95%

## Test Statistics

- **Total Tests**: 142 (54 integration + 88 unit)
- **Passing**: 130 (92%)
- **Skipped**: 12 (tests for unimplemented features or known bugs)
- **Test Files**: 3
  - `test_gw_import.py`: 54 integration tests
  - `test_gw_dates.py`: 39 date parsing unit tests
  - `test_gw_utils.py`: 50 utility/stream unit tests

## Notes

1. The parser handles the core GeneWeb file format very well
2. Most uncovered code is error handling and edge cases
3. Complex date formats need more comprehensive testing
4. Consider adding property-based tests (hypothesis) for date parsing
5. Consider adding integration tests with real GeneWeb database files

## Test Execution

All 54 tests pass successfully:
```bash
PYTHONPATH=/home/axelh/Git-Folders/Legacy/Legacy/src:$PYTHONPATH \
python -m pytest tests/import_tests/gw/test_gw_import.py \
--cov=src/script/gw_parser --cov-report=term-missing -v
```

## Recent Improvements

### Bug Fixes During Testing
1. **Critical**: Fixed `_parse_child_line()` to call `build_person()` for proper attribute parsing
   - Children in family blocks now correctly parse qualifiers, aliases, titles, etc.
   - This was discovered while adding complex scenario tests

### Test Additions
1. Added 14 complex scenario tests
2. Added 10 family event tests
3. Improved test data organization
4. All tests passing with 86% coverage
