# Testing Policy

**Version:** 1.0  
**Last Updated:** October 30, 2025  
**Status:** Active

## Table of Contents

1. [Overview](#overview)
2. [Testing Philosophy](#testing-philosophy)
3. [Test Types and Categories](#test-types-and-categories)
4. [Coverage Requirements](#coverage-requirements)
5. [Testing Standards](#testing-standards)
6. [Test Organization](#test-organization)
7. [Writing Tests](#writing-tests)
8. [Running Tests](#running-tests)
9. [CI/CD Integration](#cicd-integration)
10. [Test Review Process](#test-review-process)
11. [Maintenance and Updates](#maintenance-and-updates)
12. [Troubleshooting](#troubleshooting)

---

## Overview

This document establishes the comprehensive testing policy for the GenewebPy project, a Python reimplementation of the OCaml-based Geneweb genealogy software. Given the critical nature of genealogical data preservation and the complexity of migrating from OCaml to Python, rigorous testing is essential to ensure correctness, reliability, and feature parity with the original implementation.

### Purpose

The testing policy serves to:
- **Ensure Quality**: Maintain high code quality and prevent regressions
- **Facilitate Refactoring**: Enable confident refactoring with comprehensive test coverage
- **Document Behavior**: Tests serve as living documentation of expected behavior
- **Enable Migration**: Verify OCaml-to-Python translation accuracy
- **Support Collaboration**: Provide clear guidelines for contributors

### Scope

This policy applies to:
- All Python code in the `src/` directory
- All test code in the `tests/` directory
- CI/CD pipelines and automated testing workflows
- Pre-merge validation and code review processes

---

## Testing Philosophy

### Core Principles

1. **Test-Driven Quality**: Testing is not optional; it's a fundamental part of development
2. **Fail Fast**: Tests should catch issues early in the development cycle
3. **Maintainability**: Tests should be clear, concise, and easy to maintain
4. **Comprehensive Coverage**: All critical paths and edge cases must be tested
5. **Speed Matters**: Fast test execution enables rapid iteration
6. **Isolation**: Tests should be independent and not rely on external state
7. **Behavioral Compatibility**: Python implementation must match OCaml behavior exactly

### Testing Pyramid

We follow the testing pyramid principle with the following distribution:

```
       /\
      /  \     E2E & Golden Master (5-10%)
     /----\    
    /      \   Integration Tests (20-30%)
   /--------\  
  /          \ Unit Tests (60-75%)
 /____________\
```

- **Unit Tests** (60-75%): Fast, isolated tests of individual functions/classes
- **Integration Tests** (20-30%): Tests of component interactions and workflows
- **E2E/Golden Master** (5-10%): Full application behavior verification

---

## Test Types and Categories

### 1. Unit Tests

**Purpose**: Test individual functions, methods, or classes in isolation.

**Location**: `tests/test_*.py` (at root level)

**Characteristics**:
- Fast execution (< 1ms per test)
- No external dependencies (databases, files, network)
- High coverage of logic branches
- Mock external dependencies

**Examples**:
- `test_date.py` - Date parsing and validation
- `test_person.py` - Person data model
- `test_events.py` - Event handling
- `test_calendar.py` - Calendar conversions
- `test_sosa.py` - Sosa numbering system

**Requirements**:
- All public functions must have unit tests
- Test both happy paths and error conditions
- Cover all logic branches (if/else, switch cases)
- Test boundary conditions
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`

### 2. Integration Tests

**Purpose**: Test interactions between components and data flow through multiple layers.

**Location**: `tests/<component>/` subdirectories

**Characteristics**:
- Test component interactions
- May use real database (SQLite in-memory)
- Test data flow across layers
- Verify repository patterns

**Examples**:
- `tests/repositories/test_repositories_functional.py` - Repository operations
- `tests/repositories/test_converter_to_db.py` - Data conversion layer
- `tests/database/` - Database layer integration

**Requirements**:
- Test realistic workflows (create, read, update, delete)
- Verify bidirectional relationships
- Test transaction boundaries
- Use fixtures for test data setup
- Clean up resources after tests

### 3. Parser Tests

**Purpose**: Verify accurate parsing of GeneWeb (.gw) file format.

**Location**: `tests/import_tests/` and parser-specific test files

**Characteristics**:
- Test OCaml-to-Python translation accuracy
- Verify GeneWeb format compliance
- Test error handling and recovery

**Examples**:
- Tokenization and lexical analysis
- Syntax parsing
- Semantic validation
- Error reporting

**Requirements**:
- Test valid and invalid input formats
- Verify all GeneWeb format constructs
- Test edge cases (empty files, malformed data)
- Compare with OCaml reference implementation

### 4. Roundtrip Tests

**Purpose**: Verify that data can be parsed from .gw files, stored in database, and retrieved without loss or corruption.

**Location**: `tests/gwc_database_roundtrip/`

**Characteristics**:
- End-to-end data integrity tests
- Field-by-field verification
- Compare input with database output

**Test Files**:
- `test_minimal_gw_roundtrip.py` - Minimal test case (2 persons)
- `test_medium_gw_roundtrip.py` - Medium complexity (12 persons, 5 families)
- `test_big_gw_roundtrip.py` - Large dataset (34 persons, 16 families)

**Requirements**:
- **Test EVERY field** for EVERY person and family
- Verify all data types (dates, places, events, relations)
- Check occurrence numbers (occ field)
- Validate event witnesses and sources
- Test special cases (death, burial, divorce)
- Ensure no data loss in conversion

**Test Structure**:
```python
class TestPersonFields:
    def test_person_count(self, db_with_data):
        """Verify correct number of persons parsed"""
        
    def test_person_first_name(self, db_with_data):
        """Verify first name field accuracy"""
        
    def test_person_occ(self, db_with_data):
        """Verify occurrence number field"""

class TestFamilyFields:
    def test_family_count(self, db_with_data):
        """Verify correct number of families parsed"""
        
    def test_marriage_date(self, db_with_data):
        """Verify marriage event date accuracy"""

class TestFieldCompleteness:
    def test_all_person_fields_present(self, db_with_data):
        """Ensure no fields are missing from Person table"""
        
    def test_all_family_fields_present(self, db_with_data):
        """Ensure no fields are missing from Family table"""
```

### 5. Golden Master Tests

**Purpose**: Ensure behavioral compatibility with the original OCaml Geneweb implementation.

**Location**: `tests/golden_master/`

**Characteristics**:
- Record reference behavior from OCaml version
- Compare Python output against recorded reference
- Detect unintended behavioral changes
- HTML snapshot comparison for web interface

**Test Scenarios** (See [tests/GOLDEN_MASTER.md](tests/GOLDEN_MASTER.md) for details):
- Add family workflows
- Edit person/family operations
- Search and navigation
- Event management
- Witness handling

**Requirements**:
- Mark with `@pytest.mark.golden_master` decorator
- Store reference outputs in version control
- Update references only after careful review
- Document any intentional deviations from OCaml behavior

### 6. End-to-End Tests

**Purpose**: Test complete user workflows through the entire application stack.

**Location**: `tests/e2e/` (when implemented)

**Characteristics**:
- Full application testing (HTTP to database)
- Real user scenarios
- Browser automation (if web UI)
- Complete request/response cycle

**Requirements**:
- Test critical user journeys
- Verify error handling and user feedback
- Validate data persistence across sessions

### 7. Performance Tests

**Purpose**: Ensure acceptable performance for large genealogical databases.

**Location**: `tests/performance/` (when implemented)

**Requirements**:
- Test parsing large .gw files (10,000+ persons)
- Benchmark database query performance
- Memory usage profiling
- Identify performance regressions

---

## Coverage Requirements

### Minimum Coverage Thresholds

| Scope | Minimum Coverage | Target Coverage | Enforcement |
|-------|------------------|-----------------|-------------|
| **Overall Project** | 80% | 90% | CI/CD Required |
| **Core Libraries** (`libraries/`) | 90% | 95% | CI/CD Required |
| **Parsers** (`libraries/parser/`) | 85% | 95% | CI/CD Required |
| **Repositories** (`repositories/`) | 85% | 95% | CI/CD Required |
| **Database Layer** (`database/`) | 80% | 90% | CI/CD Required |
| **Web Server** (`wserver/`) | 70% | 85% | Development |
| **Scripts** (`script/`) | 60% | 80% | Development |

### Coverage Enforcement

- **Branch Protection**: PRs to `main` or `milestone/*` must meet 80% minimum coverage
- **Coverage Reports**: Generated on every CI run and visible in PR comments
- **Trend Monitoring**: Coverage should never decrease without explicit justification
- **Exemptions**: Require team lead approval with documented reasoning

### Coverage Tools

```bash
# Generate coverage report
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html

# Check coverage threshold
pytest --cov=src --cov-fail-under=80
```

---

## Testing Standards

### Test Naming Conventions

#### Test Files
- Pattern: `test_<module_name>.py`
- Examples: `test_person.py`, `test_date_parser.py`
- Location: Mirror source structure in `tests/` directory

#### Test Classes
- Pattern: `Test<FeatureOrComponent>`
- Examples: `TestPersonCreation`, `TestDateParsing`
- Group related tests together

#### Test Functions
- Pattern: `test_<function>_<scenario>_<expected_result>`
- Examples:
  - `test_parse_date_valid_format_returns_date_object`
  - `test_create_person_missing_name_raises_validation_error`
  - `test_calculate_age_before_birth_returns_negative`

### Test Structure

Follow the **Arrange-Act-Assert (AAA)** pattern:

```python
def test_create_person_with_valid_data_succeeds():
    # Arrange: Set up test data and dependencies
    person_data = {
        "first_name": "John",
        "surname": "Doe",
        "sex": Sex.MALE
    }
    
    # Act: Execute the function under test
    person = Person.create(person_data)
    
    # Assert: Verify expected outcomes
    assert person.first_name == "John"
    assert person.surname == "Doe"
    assert person.sex == Sex.MALE
    assert person.index is not None
```

### Fixture Usage

Use pytest fixtures for common setup:

```python
@pytest.fixture
def db_service():
    """Provide a clean database service for each test"""
    service = SQLiteDatabaseService(":memory:")
    service.connect()
    service.initialize_schema()
    yield service
    service.close()

@pytest.fixture
def sample_person():
    """Provide a sample person for testing"""
    return Person(
        first_name="Jane",
        surname="Smith",
        sex=Sex.FEMALE,
        occ=0
    )
```

### Assertions

**Use specific assertions**:
```python
# Good
assert len(persons) == 5
assert person.age > 0
assert "error" in response.lower()

# Avoid
assert persons  # Too vague
assert response  # Not descriptive
```

**Use assertion messages**:
```python
assert len(persons) == expected_count, \
    f"Expected {expected_count} persons but got {len(persons)}"
```

### Parametrization

Use `pytest.mark.parametrize` for testing multiple scenarios:

```python
@pytest.mark.parametrize("date_string,expected_year,expected_month", [
    ("1985/05/15", 1985, 5),
    ("2000/12/31", 2000, 12),
    ("1900/01/01", 1900, 1),
])
def test_date_parsing(date_string, expected_year, expected_month):
    date = parse_date(date_string)
    assert date.year == expected_year
    assert date.month == expected_month
```

### Mocking

Use mocking for external dependencies:

```python
from unittest.mock import Mock, patch

def test_fetch_external_data_handles_timeout():
    # Mock the HTTP client
    with patch('requests.get') as mock_get:
        mock_get.side_effect = TimeoutError("Connection timed out")
        
        # Test that timeout is handled gracefully
        result = fetch_data("http://example.com")
        assert result is None
```

### Error Testing

Test error conditions explicitly:

```python
def test_parse_invalid_date_raises_error():
    with pytest.raises(ValueError) as exc_info:
        parse_date("not-a-date")
    
    assert "invalid date format" in str(exc_info.value).lower()
```

---

## Test Organization

### Directory Structure

```
tests/
├── __pycache__/              # Python cache (gitignored)
├── test_*.py                 # Root-level unit tests
│
├── database/                 # Database layer tests
│   ├── test_sqlite_service.py
│   └── test_models.py
│
├── repositories/             # Repository pattern tests
│   ├── test_person_repository.py
│   ├── test_family_repository.py
│   ├── test_converter_to_db.py
│   └── test_repositories_functional.py
│
├── import_tests/             # Import/parser tests
│   └── test_parser_*.py
│
├── gwc_database_roundtrip/   # End-to-end roundtrip tests
│   ├── test_minimal_gw_roundtrip.py
│   ├── test_medium_gw_roundtrip.py
│   └── test_big_gw_roundtrip.py
│
├── golden_master/            # Golden master tests
│   ├── record.py
│   ├── test_golden_master.py
│   └── snapshots/
│
├── tests_wserver/            # Web server tests
│   ├── test_wserver_*.py
│   └── test_template_loader.py
│
└── utils/                    # Testing utilities
    ├── test_buffer.py
    └── fixtures.py
```

### Test Data

**Location**: `test_assets/`

```
test_assets/
├── minimal.gw          # 2 persons, 0 families - basic syntax
├── medium.gw           # 12 persons, 5 families - moderate complexity
└── big.gw              # 34 persons, 16 families - comprehensive features
```

**Guidelines**:
- Keep test data small and focused
- Use meaningful names (minimal, medium, big)
- Document test file contents in header comments
- Version control all test assets
- Include both valid and invalid test cases

---

## Writing Tests

### Test Development Workflow

1. **Write Test First** (TDD approach):
   ```python
   def test_new_feature_does_something():
       # This test will fail initially
       result = new_feature(input_data)
       assert result == expected_output
   ```

2. **Implement Feature**: Write minimal code to make test pass

3. **Refactor**: Improve code while keeping tests green

4. **Add Edge Cases**: Extend tests to cover edge cases

### Guidelines for Effective Tests

#### DO

✅ **Test Behavior, Not Implementation**
```python
# Good - tests behavior
def test_user_can_create_family():
    family = create_family(parent1, parent2)
    assert family.parents == [parent1, parent2]

# Avoid - tests implementation details
def test_family_uses_list_internally():
    family = create_family(parent1, parent2)
    assert isinstance(family._parents, list)  # Implementation detail
```

✅ **Use Descriptive Test Names**
```python
# Good
def test_parse_date_with_year_zero_returns_none()

# Poor
def test_date()
```

✅ **Keep Tests Independent**
```python
# Each test should set up its own data
@pytest.fixture
def person():
    return Person(first_name="John", surname="Doe")

def test_person_age(person):
    # Test uses fixture, doesn't depend on other tests
    assert calculate_age(person, current_year=2025) > 0
```

✅ **Test One Thing Per Test**
```python
# Good - focused test
def test_person_full_name_format():
    person = Person(first_name="John", surname="Doe")
    assert person.full_name == "John Doe"

# Poor - tests multiple things
def test_person_properties():
    person = Person(first_name="John", surname="Doe", age=30)
    assert person.full_name == "John Doe"
    assert person.age == 30
    assert person.is_adult == True
```

✅ **Test Edge Cases**
- Null/None values
- Empty strings/lists
- Zero values
- Negative numbers
- Very large numbers
- Boundary conditions
- Special characters
- Unicode handling

#### DON'T

❌ **Don't Test Framework Code**
```python
# Don't test SQLAlchemy's internals
def test_sqlalchemy_saves_to_database():
    # This tests SQLAlchemy, not your code
    pass
```

❌ **Don't Use Sleep in Tests**
```python
# Bad
def test_async_operation():
    start_operation()
    time.sleep(5)  # Flaky and slow
    assert operation_complete()

# Good - use proper async testing
@pytest.mark.asyncio
async def test_async_operation():
    await start_operation()
    assert await is_operation_complete()
```

❌ **Don't Share State Between Tests**
```python
# Bad - tests depend on execution order
class_variable = None

def test_first():
    class_variable = "value"

def test_second():
    assert class_variable == "value"  # Flaky!
```

❌ **Don't Ignore Test Failures**
```python
# Bad
@pytest.mark.skip("TODO: Fix this later")
def test_important_feature():
    pass

# Good - fix immediately or create issue
def test_important_feature():
    # Test implementation
    pass
```

### Testing Checklist

Before submitting a PR, ensure:

- [ ] All new functions have unit tests
- [ ] Edge cases are covered
- [ ] Error conditions are tested
- [ ] Tests follow naming conventions
- [ ] Tests are independent and isolated
- [ ] Fixtures are used appropriately
- [ ] No hardcoded paths or environment-specific values
- [ ] Tests pass locally
- [ ] Coverage meets threshold (80%+)
- [ ] Test names clearly describe what they test
- [ ] No commented-out tests
- [ ] No print statements (use logging if needed)

---

## Running Tests

### Local Development

**Run all tests**:
```bash
pytest
```

**Run specific test file**:
```bash
pytest tests/test_person.py
```

**Run specific test**:
```bash
pytest tests/test_person.py::test_person_creation
```

**Run tests matching pattern**:
```bash
pytest -k "date_parsing"
```

**Run tests by marker**:
```bash
pytest -m golden_master
```

**Verbose output**:
```bash
pytest -v
```

**Show print statements**:
```bash
pytest -s
```

**Stop on first failure**:
```bash
pytest -x
```

**Run last failed tests**:
```bash
pytest --lf
```

### Coverage Analysis

**Generate coverage report**:
```bash
pytest --cov=src --cov-report=html --cov-report=term
```

**View HTML coverage report**:
```bash
open htmlcov/index.html
```

**Coverage by module**:
```bash
pytest --cov=src --cov-report=term-missing
```

**Fail if coverage below threshold**:
```bash
pytest --cov=src --cov-fail-under=80
```

### Docker Testing

**Run tests in Docker**:
```bash
./docker-manage.sh test
```

**Interactive testing in container**:
```bash
./docker-manage.sh shell
pytest -v
```

### Test Performance

**Show test durations**:
```bash
pytest --durations=10
```

**Run tests in parallel** (requires pytest-xdist):
```bash
pytest -n auto
```

---

## CI/CD Integration

### Status Checks

Tests run automatically as part of CI/CD pipeline. The following checks must pass before merging:

| Check | Description | When Run | Required For |
|-------|-------------|----------|--------------|
| **Unit Tests** | All unit tests in `tests/test_*.py` | Every commit | All branches |
| **Integration Tests** | Repository and database tests | Every commit | All branches |
| **Roundtrip Tests** | GWC database roundtrip verification | Every commit | All branches |
| **Coverage Check** | Overall coverage ≥ 80% | Every commit | All branches |
| **Golden Master** | Behavioral compatibility tests | Milestone/Hotfix | milestone/*, hotfix/* |
| **Lint Check** | PEP8 compliance | Every commit | feature/*, fix/*, refactor/* |
| **Type Check** | MyPy static type checking | Every commit | feature/*, fix/*, refactor/* |

### GitHub Actions Workflow

Example `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests with coverage
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term
    
    - name: Check coverage threshold
      run: |
        pytest --cov=src --cov-fail-under=80
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## Test Review Process

### Code Review Requirements

When reviewing tests in PRs:

✅ **Check for**:
- Test coverage of new/changed code
- Clear test names and structure
- Appropriate use of fixtures
- Edge cases covered
- No flaky or intermittent tests
- No hardcoded values that should be configurable
- Proper error testing

❌ **Red flags**:
- Skipped tests without justification
- Tests that always pass (no assertions)
- Tests with sleep/time delays
- Copy-pasted test code
- Missing edge case coverage
- Tests depending on execution order

### Approval Criteria

Tests must:
1. Pass all CI/CD checks
2. Meet coverage threshold (80%+)
3. Follow naming conventions
4. Be reviewed by at least one team member
5. Have no outstanding questions or comments

---

## Maintenance and Updates

### Updating Tests

**When to update tests**:
- Bug fixes: Add test that reproduces the bug
- New features: Add comprehensive test coverage
- Refactoring: Ensure existing tests still pass
- API changes: Update affected tests
- Dependency updates: Verify compatibility

### Test Debt

Track technical debt in tests:

```python
# TODO: Add edge case for negative dates
# FIXME: This test is flaky, needs investigation
# XXX: Temporary workaround for parser bug #123
```

### Deprecation

When deprecating features:
1. Mark tests with `@pytest.mark.deprecated`
2. Add deprecation timeline in comments
3. Remove tests when feature is removed

### Test Metrics

Monitor test health:
- **Test Count**: Track growth over time
- **Coverage**: Maintain or improve coverage
- **Flakiness**: Identify and fix flaky tests
- **Duration**: Keep test suite fast (< 5 min)
- **Failure Rate**: Investigate frequent failures

---

## Troubleshooting

### Common Issues

#### Tests Pass Locally But Fail in CI

**Possible causes**:
- Environment differences (paths, Python version)
- Missing dependencies in CI environment
- Timezone or locale differences
- Non-deterministic behavior (random, time-dependent)

**Solutions**:
- Use Docker to reproduce CI environment
- Check CI logs for specific errors
- Ensure all dependencies in requirements.txt
- Use fixed seeds for random tests

#### Slow Test Execution

**Possible causes**:
- Too many database operations
- Network calls not mocked
- Large test data files
- Inefficient queries

**Solutions**:
```bash
# Identify slow tests
pytest --durations=10

# Run tests in parallel
pytest -n auto

# Use in-memory database
# Use smaller test datasets
```

#### Flaky Tests

**Symptoms**: Tests that sometimes pass, sometimes fail

**Common causes**:
- Race conditions in async code
- Time-dependent assertions
- External dependencies
- Shared state between tests

**Solutions**:
- Use proper async testing patterns
- Mock time-dependent functions
- Ensure test isolation
- Run flaky test multiple times to reproduce

#### Coverage Not Increasing

**Check**:
- Are new files included in coverage report?
- Are tests actually running?
- Check `.coveragerc` configuration

```bash
# See what's covered
pytest --cov=src --cov-report=term-missing
```

### Getting Help

1. **Check documentation**: Review this policy and test examples
2. **Ask the team**: Post in team chat or discussions
3. **Review existing tests**: Look at similar test cases
4. **Create an issue**: Document the problem with reproduction steps

---

## References

### Related Documentation

- [Quality Insurance](QUALITY_INSURANCE.md) - Branch management and merge flow
- [Golden Master Testing](tests/GOLDEN_MASTER.md) - Golden master test scenarios
- [GWC Implementation Guide](GWC_IMPLEMENTATION.md) - GWC compiler testing
- [Database Architecture](DATABASE.md) - Database testing patterns

### External Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Testing Strategies](https://testing.googleblog.com/)

### Tools

- **pytest**: Primary testing framework
- **pytest-cov**: Coverage reporting
- **pytest-xdist**: Parallel test execution
- **pytest-mock**: Mocking utilities
- **coverage**: Coverage measurement

---

## Approval

This policy has been reviewed and approved by the development team.
