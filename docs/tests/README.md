# Test Documentation

This folder contains comprehensive documentation about all tests in the GenewebPy project.

## Test Categories

### 📋 [Unit Tests](./UNIT.md)
**Complete inventory of unit tests** - Tests for individual functions, classes, and methods in isolation.

- **22 test files**
- **400+ test functions**
- **Coverage:** Data types, utilities, algorithms, business logic, parser components

**Key Files:**
- Data types: calendar, date, events, family, person, title
- Utilities: name_utils, secure_string, translator
- Algorithms: consanguinity, sosa
- Database: database service
- Web: gwsetup, gwd_root
- Parser: gw_import, gw_field_parsing, gw_dates, gw_utils, gw_converter

---

### 🔗 [Integration Tests](./INTEGRATION.md)
**Complete inventory of integration tests** - Tests for component interactions, repository patterns, and database operations.

- **13 test files**
- **300+ test functions**
- **Coverage:** Converters, repositories, database, web routes

**Key Files:**
- Repository: converter_to_db, converter_from_db, repositories_functional
- Database: database_models, sqlite_database_service, relationships
- Web Server: wserver_create_app, translations, template_loader, gwsetup_routes, add_family
- Parser Integration: database_verification, gw_converter

---

### 🌐 [End-to-End Tests](./E2E.md)
**Complete inventory of E2E tests** - Tests for complete roundtrip workflows from input to output with no data loss.

- **2 test files**
- **200+ test functions**
- **3 test databases:** minimal.gw, medium.gw, big.gw
- **Coverage:** Complete roundtrip (.gw → Database → Retrieval)

**Key Files:**
- Roundtrip: test_minimal_gw_roundtrip, test_medium_gw_roundtrip

**Note:** Golden Master tests documented in [GOLDEN_MASTER.md](../GOLDEN_MASTER.md)

---

## Quick Reference

### By Test Type

| Test Type | Location | Purpose | Example |
|-----------|----------|---------|---------|
| **Unit** | `tests/test_*.py`, `tests/import_tests/gw/` | Test individual functions | `test_calendar.py`, `test_gw_dates.py` |
| **Integration** | `tests/repositories/`, `tests/database/` | Test component interactions | `test_converter_to_db.py` |
| **E2E** | `tests/gwc_database_roundtrip/` | Test complete roundtrip workflows | `test_minimal_gw_roundtrip.py` |
| **Golden Master** | `tests/golden_master/` | Compare with OCaml output (see [GOLDEN_MASTER.md](../GOLDEN_MASTER.md)) | HTML comparison tests |

### By Coverage Area

| Area | Unit Tests | Integration Tests | E2E Tests |
|------|-----------|-------------------|-----------|
| **Data Types** | ✅ Extensive | ✅ Converter tests | ✅ Roundtrip tests |
| **Utilities** | ✅ Extensive | ❌ N/A | ❌ N/A |
| **Algorithms** | ✅ Basic | ❌ N/A | ❌ N/A |
| **Database** | ✅ Basic | ✅ Extensive | ✅ Via roundtrip |
| **Repository** | ❌ N/A | ✅ Extensive | ✅ Via roundtrip |
| **Parser** | ❌ N/A | ✅ Import pipeline | ✅ Via roundtrip |
| **Web Server** | ✅ Basic | ✅ Routes | ❌ N/A |

---

## Test Statistics

### Overall Coverage
- **Total test files:** 37
- **Total test functions:** 900+
- **Code coverage target:** 80% minimum
- **Core libraries coverage:** 90% target
- **Parser coverage:** 85% target

### Test Distribution
```
Unit Tests:        ~44% (400+ tests)
Integration Tests: ~33% (300+ tests)
E2E Tests:         ~22% (200+ tests)
```

---

## Running Tests

### Run All Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### Run By Category
```bash
# Unit tests only
pytest tests/test_*.py tests/utils/ tests/import_tests/gw/ -v

# Integration tests only
pytest tests/repositories/ tests/database/ tests/tests_wserver/ -v

# E2E tests only (roundtrip)
pytest tests/gwc_database_roundtrip/ -v

# Golden master tests (see GOLDEN_MASTER.md for details)
pytest tests/golden_master/ -v
```

### Run By Module
```bash
# Calendar tests
pytest tests/test_calendar.py -v

# Repository tests
pytest tests/repositories/ -v

# Roundtrip tests
pytest tests/gwc_database_roundtrip/ -v
```

### Run Specific Tests
```bash
# Specific test function
pytest tests/test_calendar.py::test_calendar_date_creation -v

# Specific test class
pytest tests/gwc_database_roundtrip/test_minimal_gw_roundtrip.py::TestMinimalGwPersons -v

# Tests matching pattern
pytest tests/ -k "test_person" -v
```

---

## Test Organization

### Directory Structure
```
tests/
├── test_*.py                    # Unit tests (root level)
├── utils/                       # Utility unit tests
│   └── test_buffer.py
├── repositories/                # Repository integration tests
│   ├── test_converter_to_db.py
│   ├── test_converter_from_db.py
│   └── test_repositories_functional.py
├── database/                    # Database integration tests
│   ├── test_database_models.py
│   ├── test_sqlite_database_service.py
│   └── test_relationships.py
├── tests_wserver/               # Web server integration tests
│   ├── test_wserver_create_app.py
│   ├── test_translations.py
│   ├── test_template_loader.py
│   ├── test_gwsetup_routes.py
│   └── test_add_family.py
├── gwc_database_roundtrip/      # E2E roundtrip tests
│   ├── test_minimal_gw_roundtrip.py
│   └── test_medium_gw_roundtrip.py
├── import_tests/gw/             # E2E import tests
│   ├── test_gw_import.py
│   ├── test_gw_field_parsing.py
│   ├── test_gw_dates.py
│   ├── test_gw_utils.py
│   ├── test_data.py
│   ├── test_gw_converter.py
│   └── test_database_verification.py
└── golden_master/               # Golden master framework
    ├── record.py
    ├── web_action_runner.py
    └── clean_rule.py
```

---

## Test Naming Conventions

### Files
- Unit tests: `test_<module>.py`
- Integration tests: `test_<component>_<interaction>.py`
- E2E tests: `test_<dataset>_<workflow>.py`

### Functions
- Unit: `test_<function>_<scenario>()`
- Integration: `test_<operation>_<scenario>()`
- E2E: `test_<workflow>_<scenario>()`

### Classes
- Roundtrip: `Test<Dataset><Entity>`
- Golden Master: `Test<Feature>GoldenMaster`
- Integration: `Test<Component><Operation>`

---

## Coverage Requirements

### Minimum Coverage
- **Overall:** 80%
- **Core libraries:** 90%
- **Parsers:** 85%
- **Repository:** 85%
- **Database models:** 90%

### Critical Paths
- ✅ **Must be 100%:** Converter to/from DB
- ✅ **Must be 100%:** Roundtrip preservation
- ✅ **Must be >90%:** Data type operations
- ✅ **Must be >85%:** Parser logic

---

## Test Data

### Test Assets
Located in `test_assets/`:
- `minimal.gw` - Small dataset (~12 persons, ~5 families)
- `medium.gw` - Medium dataset (~50 persons, ~20 families)
- `big.gw` - Large dataset (~1000+ persons, ~400+ families)

### Test Databases
Generated during tests:
- `:memory:` - In-memory SQLite (most integration tests)
- `test_*.db` - File-based SQLite (E2E tests)
- Cleaned up automatically after tests

---

## CI/CD Integration

Tests run automatically on:
- Every push to any branch
- Every pull request
- Pre-merge validation
- Nightly builds (full suite with big.gw)

**Status Checks Required:**
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Roundtrip tests pass (minimal + medium)
- [ ] Coverage meets minimum thresholds

---

## Adding New Tests

### 1. Determine Test Type
- **Testing a function?** → Unit test
- **Testing components together?** → Integration test
- **Testing end-to-end workflow?** → E2E test

### 2. Choose Location
- Unit: `tests/test_<module>.py`
- Integration: `tests/<subsystem>/test_*.py`
- E2E: `tests/gwc_database_roundtrip/` or `tests/import_tests/`

### 3. Write Test
- Follow naming conventions
- Use appropriate fixtures
- Write clear assertions
- Add docstrings

### 4. Update Documentation
- Add to appropriate inventory file:
  - [UNIT.md](./UNIT.md)
  - [INTEGRATION.md](./INTEGRATION.md)
  - [E2E.md](./E2E.md)
- Update test counts
- Update coverage areas

---

## Troubleshooting Tests

### Common Issues

**Import Errors:**
```bash
# Make sure PYTHONPATH is set
export PYTHONPATH=/path/to/Legacy:$PYTHONPATH
pytest tests/
```

**Database Errors:**
```bash
# Clean test databases
rm -f test_*.db
pytest tests/
```

**Fixture Errors:**
```bash
# Check conftest.py is present
ls tests/conftest.py
pytest tests/ -v
```

**Coverage Not Generating:**
```bash
# Install coverage plugin
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

---

## See Also

- **[Testing Policy](../TESTING_POLICY.md)** - Complete testing guidelines and best practices
- **[Quality Insurance](../QUALITY_INSURANCE.md)** - Code review and quality standards
- **[GWC Implementation](../GWC_IMPLEMENTATION.md)** - Parser and import documentation
- **[Database Documentation](../DATABASE.md)** - Database schema and models
- **[Main Documentation Index](../README.md)** - Complete documentation navigation

---

**Questions about tests?** Open an issue on GitHub with the `testing` label!
