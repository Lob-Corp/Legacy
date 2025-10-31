# End-to-End Tests Inventory

**Last Updated:** October 31, 2025  
**Total E2E Test Files:** 2

## Overview

This document catalogs all end-to-end (E2E) tests in the GenewebPy project. E2E tests verify complete roundtrip workflows: data is read from .gw files, stored in the database, and retrieved without data loss. These tests validate **EVERY field for EVERY person and family**.

**Note:** Golden Master tests are documented separately in [GOLDEN_MASTER.md](../GOLDEN_MASTER.md). Import pipeline tests are integration tests documented in [INTEGRATION.md](./INTEGRATION.md).

---

## Roundtrip Tests

Roundtrip tests verify that data can be read from .gw files, stored in the database, and retrieved without data loss. These tests validate **EVERY field for EVERY person and family**.

### gwc_database_roundtrip/test_minimal_gw_roundtrip.py
**Path:** `tests/gwc_database_roundtrip/test_minimal_gw_roundtrip.py`  
**Purpose:** Test minimal.gw roundtrip (small dataset)

**Test Classes:**

#### TestMinimalGwPersons
**Coverage:** Person data roundtrip validation

**Test Methods:**
- Person count verification
- First name accuracy
- Surname accuracy
- Sex/gender field
- Occurrence numbers
- Birth dates and places
- Baptism dates and places
- Death dates and places
- Burial information
- Occupation fields
- Public/private name fields
- Qualifiers and aliases
- Images and notes
- Person sources

**Persons Tested:** ~12 persons from minimal.gw

---

#### TestMinimalGwPersonalEvents
**Coverage:** Personal event data roundtrip

**Test Methods:**
- Event type verification
- Event dates
- Event places
- Event witnesses
- Event notes
- Event sources
- Baptism events
- Bar Mitzvah events
- Confirmation events
- Death events
- Burial events
- Cremation events
- Custom named events

**Events Tested:** All personal events in minimal.gw

---

#### TestMinimalGwFamilies
**Coverage:** Family data roundtrip

**Test Methods:**
- Family count verification
- Parent relationships (father, mother)
- Children lists
- Marriage dates and places
- Marriage witnesses
- Divorce status and dates
- Family events
- Family notes
- Family sources

**Families Tested:** ~5 families from minimal.gw

---

#### TestMinimalGwFieldCompleteness
**Coverage:** Ensure no fields are missed

**Test Methods:**
- All person fields present
- All family fields present
- All event fields present
- No null where data exists
- No data loss in conversion

---

### gwc_database_roundtrip/test_medium_gw_roundtrip.py
**Path:** `tests/gwc_database_roundtrip/test_medium_gw_roundtrip.py`  
**Purpose:** Test medium.gw roundtrip (medium dataset)

**Test Classes:**

#### TestMediumGwCounts
**Coverage:** Verify overall counts match

**Test Methods:**
- `test_person_count` - Total persons match
- `test_family_count` - Total families match
- `test_event_count` - Total events match

---

#### TestMediumGwFamily1
**Coverage:** Specific family #1 roundtrip

**Test Methods:**
- Father identification
- Mother identification
- Children list completeness
- Marriage date accuracy
- Marriage place accuracy
- Marriage witnesses
- Divorce status
- Family events
- Notes and sources

---

#### TestMediumGwFamily2
**Coverage:** Specific family #2 roundtrip

**Test Methods:**
- Same coverage as Family1
- Different data patterns
- Edge cases specific to this family

---

#### TestMediumGwFamily3
**Coverage:** Specific family #3 roundtrip

**Test Methods:**
- Childless family
- Marriage without children
- Event-heavy family

---

#### TestMediumGwFamily4
**Coverage:** Specific family #4 roundtrip

**Test Methods:**
- Complex divorce scenario
- Multiple marriages
- Remarriage handling

---

#### TestMediumGwFamily5
**Coverage:** Specific family #5 roundtrip

**Test Methods:**
- Large family (many children)
- Birth order preservation
- Sibling relationships

---

#### TestMediumGwPersonA1
**Coverage:** Person A.1 (complex person)

**Test Methods:**
- All person fields
- Multiple titles
- Multiple relations
- Multiple events
- Complex dates (ranges, approximate)
- Multiple aliases
- Image links
- Extensive notes

---

#### TestMediumGwPersonC
**Coverage:** Person C (edge cases)

**Test Methods:**
- Minimal data person
- Missing optional fields
- Default value handling

---

#### TestMediumGwPersonYoyo
**Coverage:** Person "Yoyo" (custom name)

**Test Methods:**
- Unusual name handling
- Name with special characters
- Nickname preservation

---

#### TestMediumGwPersonNeuter
**Coverage:** Person with neuter sex

**Test Methods:**
- Non-binary sex handling
- Sex field edge cases
- Unknown sex representation

---

**Total Families Tested:** 5 complete families  
**Total Persons Tested:** 4+ detailed persons  
**Coverage:** ~50+ persons, 5+ families from medium.gw

---

## Summary Statistics

### By Category:
- **Roundtrip Tests:** 2 files (minimal, medium)
  - TestMinimalGwPersons: ~50 tests
  - TestMinimalGwPersonalEvents: ~20 tests
  - TestMinimalGwFamilies: ~20 tests
  - TestMinimalGwFieldCompleteness: ~10 tests
  - TestMediumGw*: ~100 tests

### Total:
- **2 E2E test files**
- **200+ individual test functions**
- **3 test databases:** minimal.gw, medium.gw, big.gw
- **Coverage:** Complete roundtrip: .gw → Database → Retrieval (no data loss)

---

## Running E2E Tests

```bash
# Run all roundtrip tests
pytest tests/gwc_database_roundtrip/ -v

# Run minimal roundtrip
pytest tests/gwc_database_roundtrip/test_minimal_gw_roundtrip.py -v

# Run medium roundtrip
pytest tests/gwc_database_roundtrip/test_medium_gw_roundtrip.py -v

# Run specific test class
pytest tests/gwc_database_roundtrip/test_minimal_gw_roundtrip.py::TestMinimalGwPersons -v

# Run with coverage
pytest tests/gwc_database_roundtrip/ --cov=src --cov-report=html
```

---

## Test Data Files

### minimal.gw
**Location:** `test_assets/minimal.gw`  
**Size:** ~12 persons, ~5 families  
**Purpose:** Basic roundtrip testing  
**Features:**
- Simple family structures
- Basic dates
- Common fields
- No edge cases

### medium.gw
**Location:** `test_assets/medium.gw`  
**Size:** ~50 persons, ~20 families  
**Purpose:** Complex roundtrip testing  
**Features:**
- Complex family structures
- Multiple marriages
- Divorce scenarios
- Complex dates (ranges, calendars)
- Titles and relations
- Custom events
- Edge cases

### big.gw
**Location:** `test_assets/big.gw`  
**Size:** ~1000+ persons, ~400+ families  
**Purpose:** Performance and stress testing  
**Features:**
- Large dataset
- Performance benchmarking
- Memory usage testing
- Import speed testing

---

## Test Organization

E2E tests follow these conventions:
- **File naming:** `test_<dataset>_roundtrip.py`
- **Class naming:** `Test<Dataset><Entity>` (e.g., `TestMinimalGwPersons`)
- **Location:** `tests/gwc_database_roundtrip/`
- **Dependencies:** Test data files (.gw), database, import pipeline
- **Fixtures:** Database with imported data from .gw files

---

## Roundtrip Test Pattern

Roundtrip tests follow this pattern:

```python
class TestMinimalGwPersons:
    """Test person data roundtrip from minimal.gw"""
    
    @pytest.fixture(scope="class")
    def database(self):
        """Import minimal.gw into database"""
        db = create_database()
        gwc_import("test_assets/minimal.gw", db)
        yield db
        db.close()
    
    def test_person_count(self, database):
        """Verify person count matches .gw file"""
        expected = 12  # From manual count of minimal.gw
        actual = database.count_persons()
        assert actual == expected
    
    def test_person_first_name(self, database):
        """Verify first name preserved"""
        person = database.get_person(index=1)
        assert person.first_name == "John"
    
    def test_person_birth_date(self, database):
        """Verify birth date preserved"""
        person = database.get_person(index=1)
        assert person.birth_date.year == 1950
        assert person.birth_date.month == 6
        assert person.birth_date.day == 15
        assert person.birth_date.precision == Precision.SURE
```

**Key Points:**
- Test EVERY field
- Compare with original .gw file
- Verify no data loss
- Check data types
- Validate relationships

---

## Adding New Roundtrip Tests

When adding new roundtrip tests:

1. **Create or select test data:** Use existing .gw files or add new ones to `test_assets/`

2. **Create test file:** `tests/gwc_database_roundtrip/test_<dataset>_roundtrip.py`

3. **Write test classes:** Organize by entity (Persons, Families, Events, etc.)

4. **Test ALL fields:** Don't skip any fields - verify every person and family field

5. **Test relationships:** Verify bidirectional links (parent-child, family-person)

6. **Test edge cases:** Empty fields, null values, unusual data

7. **Compare with source:** Manually verify against original .gw file

8. **Update this document:** Add to inventory with test counts

---

## Critical Roundtrip Tests

These tests must pass for release:

✅ **Data Integrity:**
- [ ] All minimal.gw persons preserved (100% fields)
- [ ] All minimal.gw families preserved (100% fields)
- [ ] All medium.gw data preserved (100% fields)
- [ ] No field data loss in any test file
- [ ] All relationships bidirectional
- [ ] Person count matches source
- [ ] Family count matches source

---

## See Also

- [Unit Tests](./UNIT.md) - Isolated component tests
- [Integration Tests](./INTEGRATION.md) - Component interaction tests (includes import pipeline)
- [Golden Master Tests](../GOLDEN_MASTER.md) - OCaml compatibility testing
- [Testing Policy](../TESTING_POLICY.md) - Complete testing guidelines
- [GWC Implementation](../GWC_IMPLEMENTATION.md) - Import pipeline documentation
