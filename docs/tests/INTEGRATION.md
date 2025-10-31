# Integration Tests Inventory

**Last Updated:** October 31, 2025  
**Total Integration Test Files:** 13

## Overview

This document catalogs all integration tests in the GenewebPy project. Integration tests verify that multiple components work together correctly, including database operations, repository patterns, data conversions, and web server routes.

---

## Repository Layer Tests

### repositories/test_converter_to_db.py
**Path:** `tests/repositories/test_converter_to_db.py`  
**Purpose:** Test conversion from application types to database models

**Test Functions (70+ tests):**

#### Precision Conversion (7 tests)
- `test_convert_precision_sure_to_db` - Sure precision → DB
- `test_convert_precision_about_to_db` - About precision → DB
- `test_convert_precision_maybe_to_db` - Maybe precision → DB
- `test_convert_precision_before_to_db` - Before precision → DB
- `test_convert_precision_after_to_db` - After precision → DB
- `test_convert_precision_oryear_to_db` - OrYear precision → DB
- `test_convert_precision_yearint_to_db` - YearInt precision → DB

#### Date Conversion (6 tests)
- `test_convert_date_to_db` - Standard date conversion
- `test_convert_date_none_to_db` - None date handling
- `test_convert_date_string_raises_error` - Invalid type error
- `test_convert_date_tuple_raises_error` - Invalid tuple error
- `test_convert_date_with_year_zero_returns_none` - Year 0 handling
- `test_convert_date_without_precision` - Date without precision

#### Divorce Status (3 tests)
- `test_convert_divorce_not_divorced_to_db` - Not divorced status
- `test_convert_divorce_separated_to_db` - Separated status
- `test_convert_divorce_divorced_to_db` - Divorced status

#### Family Event Names (5 tests)
- `test_convert_fam_event_name_marriage_to_db` - Marriage event
- `test_convert_fam_event_name_divorce_to_db` - Divorce event
- `test_convert_fam_event_name_named_event_to_db` - Custom event
- `test_convert_fam_event_name_pacs_to_db` - PACS event
- `test_convert_all_fam_event_names_to_db` - All event types

#### Family Event & Family (7 tests)
- `test_convert_fam_event_to_db` - Complete family event
- `test_convert_family_minimal_to_db` - Minimal family
- `test_convert_family_with_divorce_to_db` - Family with divorce
- `test_convert_family_with_witnesses_to_db` - Family with witnesses
- `test_convert_family_with_events_to_db` - Family with events
- `test_convert_family_with_children_to_db` - Family with children
- `test_convert_family_complete_to_db` - Complete family (all fields)

#### Death & Burial (10 tests)
- `test_convert_death_not_dead_to_db` - NotDead status
- `test_convert_death_dead_to_db` - Dead status
- `test_convert_death_dead_young_to_db` - DeadYoung status
- `test_convert_death_dead_dont_know_when_to_db` - DeadDontKnowWhen
- `test_convert_death_dont_know_if_dead_to_db` - DontKnowIfDead
- `test_convert_death_of_course_dead_to_db` - OfCourseDead
- `test_convert_burial_unknown_to_db` - UnknownBurial
- `test_convert_burial_buried_to_db` - Buried status
- `test_convert_burial_cremated_to_db` - Cremated status

#### Titles (4 tests)
- `test_convert_title_name_no_title_to_db` - NoTitle
- `test_convert_title_name_use_main_title_to_db` - UseMainTitle
- `test_convert_title_name_title_name_to_db` - TitleName
- `test_convert_title_to_db` - Complete title

#### Relations (2 tests)
- `test_convert_relation_to_db` - Standard relation
- `test_convert_relation_no_father_to_db` - Relation without father

#### Personal Event Names (4 tests)
- `test_convert_pers_event_name_baptism_to_db` - Baptism event
- `test_convert_pers_event_name_bar_mitzvah_to_db` - Bar Mitzvah
- `test_convert_pers_event_name_named_event_to_db` - Custom personal event
- `test_convert_all_pers_event_names_to_db` - All personal event types

#### Personal Events (2 tests)
- `test_convert_personal_event_to_db` - Complete personal event
- `test_convert_personal_event_no_witnesses_to_db` - Event without witnesses

#### Person Conversion (9 tests)
- `test_convert_person_minimal_to_db` - Minimal person
- `test_convert_person_with_birth_date_to_db` - Person with birth date
- `test_convert_person_with_baptism_date_to_db` - Person with baptism
- `test_convert_person_with_titles_to_db` - Person with titles
- `test_convert_person_with_relations_to_db` - Person with relations
- `test_convert_person_with_events_to_db` - Person with events
- `test_convert_person_with_qualifiers_and_aliases_to_db` - Qualifiers/aliases
- `test_convert_person_with_related_persons_to_db` - Related persons
- `test_convert_person_complete_to_db` - Complete person (all fields)

**Coverage:** Application types → Database models (write path)

---

### repositories/test_converter_from_db.py
**Path:** `tests/repositories/test_converter_from_db.py`  
**Purpose:** Test conversion from database models to application types

**Test Functions (70+ tests):**

#### Precision Conversion (8 tests)
- `test_convert_precision_sure` - DB → Sure precision
- `test_convert_precision_about` - DB → About precision
- `test_convert_precision_maybe` - DB → Maybe precision
- `test_convert_precision_before` - DB → Before precision
- `test_convert_precision_after` - DB → After precision
- `test_convert_precision_oryear` - DB → OrYear precision
- `test_convert_precision_yearint` - DB → YearInt precision
- `test_convert_precision_invalid` - Invalid precision handling

#### Date Conversion (5 tests)
- `test_convert_date_gregorian` - Gregorian calendar
- `test_convert_date_julian` - Julian calendar
- `test_convert_date_with_delta` - Date with delta
- `test_convert_date_french_calendar` - French Republican calendar
- `test_convert_date_hebrew_calendar` - Hebrew calendar

#### Divorce Status (4 tests)
- `test_convert_divorce_status_not_divorced` - NotDivorced
- `test_convert_divorce_status_separated` - Separated
- `test_convert_divorce_status_divorced` - Divorced with date
- `test_convert_divorce_status_divorced_no_date` - Divorced without date

#### Family Events (5 tests)
- `test_convert_fam_event_marriage` - Marriage event
- `test_convert_fam_event_divorce` - Divorce event
- `test_convert_fam_event_all_types` - All family event types
- `test_convert_fam_event_named_event` - Custom family event

#### Family Conversion (8 tests)
- `test_convert_family_basic` - Basic family
- `test_convert_family_with_witnesses` - Family with witnesses
- `test_convert_family_with_children` - Family with children
- `test_convert_family_with_events` - Family with events
- `test_convert_family_divorced` - Divorced family
- `test_convert_family_separated` - Separated family
- `test_convert_family_complete` - Complete family (all fields)

#### Death & Burial (11 tests)
- `test_convert_death_status_not_dead` - NotDead
- `test_convert_death_status_dead` - Dead with date
- `test_convert_death_status_dead_no_date_raises_error` - Dead without date error
- `test_convert_death_status_dead_no_reason_raises_error` - Dead without reason
- `test_convert_death_status_dead_young` - DeadYoung
- `test_convert_death_status_dead_dont_know_when` - DeadDontKnowWhen
- `test_convert_death_status_dont_know_if_dead` - DontKnowIfDead
- `test_convert_death_status_of_course_dead` - OfCourseDead
- `test_convert_burial_status_unknown_burial` - UnknownBurial
- `test_convert_burial_status_burial` - Buried
- `test_convert_burial_status_burial_no_date_raises_error` - Burial date required
- `test_convert_burial_status_cremated` - Cremated
- `test_convert_burial_status_cremated_no_date_raises_error` - Cremated date required

#### Titles (4 tests)
- `test_convert_title_name_no_title` - NoTitle
- `test_convert_title_name_use_main_title` - UseMainTitle
- `test_convert_title_name_title_name` - TitleName
- `test_convert_title_complete` - Complete title

#### Relations (1 test)
- `test_convert_relation_basic` - Basic relation

#### Personal Event Names (4 tests)
- `test_convert_pers_event_name_baptism` - Baptism
- `test_convert_pers_event_name_bar_mitzvah` - Bar Mitzvah
- `test_convert_pers_event_name_named_event` - Custom event
- `test_convert_all_pers_event_names_from_db` - All personal events

#### Personal Events (2 tests)
- `test_convert_personal_event_basic` - Basic personal event
- `test_convert_personal_event_with_witnesses` - Event with witnesses

#### Person Conversion (9 tests)
- `test_convert_person_minimal` - Minimal person
- `test_convert_person_with_birth_date` - Person with birth
- `test_convert_person_with_baptism_date` - Person with baptism
- `test_convert_person_with_titles` - Person with titles
- `test_convert_person_with_relations` - Person with relations
- `test_convert_person_with_personal_events` - Person with events
- `test_convert_person_with_qualifiers` - Person with qualifiers
- `test_convert_person_with_aliases` - Person with aliases
- `test_convert_person_complete` - Complete person (all fields)

**Coverage:** Database models → Application types (read path)

---

### repositories/test_repositories_functional.py
**Path:** `tests/repositories/test_repositories_functional.py`  
**Purpose:** Test repository CRUD operations and data integrity

**Test Functions (10+ tests):**
- `test_create_couple_and_family` - Create couple and link to family
- `test_create_family_with_children` - Create family with child persons
- `test_edit_person_and_family` - Update person and family records
- `test_person_family_bidirectional_links` - Verify bidirectional relationships
- `test_multiple_marriages` - Person with multiple marriages
- `test_edge_case_empty_fields` - Handle empty/null fields
- `test_edge_case_large_family` - Family with many children
- `test_edge_case_nonexistent_ids` - Handle missing IDs
- `test_edge_case_orphan_child` - Child without parents
- `test_edge_case_childless_family` - Family without children

**Coverage:** Repository layer, CRUD operations, relationship integrity

---

## Database Layer Tests

### database/test_sqlite_database_service.py
**Path:** `tests/database/test_sqlite_database_service.py`  
**Purpose:** Test SQLite database service operations

**Test Functions:**
- Database connection management
- Schema initialization
- Transaction handling
- Session management
- Database file operations
- Error handling

**Coverage:** SQLiteDatabaseService class

---

### database/test_database_models.py
**Path:** `tests/database/test_database_models.py`  
**Purpose:** Test SQLAlchemy database models

**Test Functions:**
- Model instantiation
- Field validation
- Default values
- Constraints
- Model serialization

**Coverage:** All SQLAlchemy ORM models

---

### database/test_relationships.py
**Path:** `tests/database/test_relationships.py`  
**Purpose:** Test database model relationships

**Test Functions:**
- One-to-many relationships
- Many-to-many relationships
- Bidirectional relationships
- Cascade behaviors
- Orphan deletion
- Back-population

**Coverage:** SQLAlchemy relationships and cascades

---

## Web Server Integration Tests

### tests_wserver/test_wserver_create_app.py
**Path:** `tests/tests_wserver/test_wserver_create_app.py`  
**Purpose:** Test Flask application creation and configuration

**Test Functions:**
- App factory creation
- Configuration loading
- Blueprint registration
- Error handler setup
- Extension initialization

**Coverage:** Flask application factory

---

### tests_wserver/test_translations.py
**Path:** `tests/tests_wserver/test_translations.py`  
**Purpose:** Test translation system integration

**Test Functions:**
- Translation loading
- Locale switching
- Missing translation fallback
- Template translation

**Coverage:** i18n integration with Flask

---

### tests_wserver/test_template_loader.py
**Path:** `tests/tests_wserver/test_template_loader.py`  
**Purpose:** Test custom template loader

**Test Functions:**
- Template loading from filesystem
- Template inheritance
- Template caching
- Custom loader behavior

**Coverage:** Flask template system integration

---

### tests_wserver/test_gwsetup_routes.py
**Path:** `tests/tests_wserver/test_gwsetup_routes.py`  
**Purpose:** Test gwsetup web routes

**Test Functions:**
- Database list route
- Database create route
- Database delete route
- Route authentication
- Error handling

**Coverage:** gwsetup web interface

---

### tests_wserver/test_add_family.py
**Path:** `tests/tests_wserver/test_add_family.py`  
**Purpose:** Test family addition web interface

**Test Classes:**
- `TestAddFamilyRoute` - Route handling tests
- `TestAddFamilyWithDatabase` - Database integration tests
- `TestAddFamilyHelperFunctions` - Helper function tests
- `TestAddFamilyEdgeCases` - Edge case handling

**Coverage:** Add family feature end-to-end

---

## Parser Integration Tests

### import_tests/gw/test_database_verification.py
**Path:** `tests/import_tests/gw/test_database_verification.py`  
**Purpose:** Test database integrity after GW import

**Test Functions:**
- `test_database_can_retrieve_all_persons` - All persons retrievable
- `test_database_can_retrieve_all_families` - All families retrievable
- `test_database_family_parents_exist` - Parent existence
- `test_database_family_children_exist` - Child existence
- `test_database_person_families_exist` - Family existence
- `test_database_person_parents_exist` - Parent relationships
- `test_database_bidirectional_parent_child_links` - Bidirectional integrity
- `test_database_bidirectional_family_person_links` - Family links integrity
- `test_database_statistics` - Database statistics accuracy

**Coverage:** Database integrity after import

---

### import_tests/gw/test_gw_converter.py
**Path:** `tests/import_tests/gw/test_gw_converter.py`  
**Purpose:** Test GW file converter integration

**Test Functions:**
- Full file parsing
- Person creation from GW
- Family creation from GW
- Database persistence
- Error handling during conversion

**Coverage:** GW → Database pipeline

---

## Summary Statistics

### By Layer:
- **Repository Layer:** 3 test files (240+ tests)
- **Database Layer:** 3 test files
- **Web Server:** 5 test files
- **Parser Integration:** 2 test files
  - test_database_verification.py: 9 tests
  - test_gw_converter.py: ~10 tests

### Total:
- **13 integration test files**
- **300+ individual test functions**
- **Coverage areas:** Converters, repositories, database, web routes

---

## Running Integration Tests

```bash
# Run all repository tests
pytest tests/repositories/ -v

# Run all database tests
pytest tests/database/ -v

# Run all web server tests
pytest tests/tests_wserver/ -v

# Run with coverage
pytest tests/repositories/ --cov=src.repositories --cov-report=html
```

---

## Test Organization

Integration tests follow these conventions:
- **File naming:** `test_<module>.py`
- **Function naming:** `test_<operation>_<scenario>`
- **Location:** 
  - `tests/repositories/` - Repository layer
  - `tests/database/` - Database layer
  - `tests/tests_wserver/` - Web server
  - `tests/import_tests/gw/` - Import pipeline
- **Dependencies:** Multiple components, database, fixtures
- **Fixtures:** Database sessions, test data, Flask app

---

## Key Integration Points

### 1. Application ↔ Database
- **Converter to DB:** `test_converter_to_db.py`
- **Converter from DB:** `test_converter_from_db.py`
- **Coverage:** All 23 database models

### 2. Repository ↔ Database
- **CRUD Operations:** `test_repositories_functional.py`
- **Relationship Integrity:** Bidirectional links
- **Coverage:** PersonRepository, FamilyRepository

### 3. Parser ↔ Database
- **Import Pipeline:** `test_gw_converter.py`
- **Data Verification:** `test_database_verification.py`
- **Coverage:** .gw files → SQLite

### 4. Web ↔ Database
- **Route Handlers:** `test_add_family.py`, `test_gwsetup_routes.py`
- **Template Integration:** `test_template_loader.py`
- **Coverage:** Flask routes → Repository → Database

---

## Adding New Integration Tests

When adding new integration tests:

1. **Identify integration point:** What components interact?
2. **Choose location:** 
   - Repository layer? → `tests/repositories/`
   - Database models? → `tests/database/`
   - Web routes? → `tests/tests_wserver/`
   - Import pipeline? → `tests/import_tests/gw/`
3. **Use fixtures:** Database session, test data
4. **Test both directions:** Write and read operations
5. **Verify relationships:** Check bidirectional links
6. **Test error cases:** Invalid data, missing references
7. **Update this document:** Add to inventory

**Example:**
```python
import pytest
from src.repositories.person_repository import PersonRepository
from src.libraries.person import Person, Sex

@pytest.fixture
def person_repo(db_session):
    """Provide person repository with database session"""
    return PersonRepository(db_session)

def test_create_and_retrieve_person(person_repo):
    """Test person creation and retrieval"""
    # Create person
    person = Person(
        first_name="John",
        surname="Smith",
        sex=Sex.MALE,
        occ=0
    )
    person_id = person_repo.save_person(person)
    
    # Retrieve person
    retrieved = person_repo.get_person_by_id(person_id)
    
    # Verify
    assert retrieved.first_name == "John"
    assert retrieved.surname == "Smith"
    assert retrieved.sex == Sex.MALE
```

---

## See Also

- [Unit Tests](./UNIT.md) - Isolated component tests
- [E2E Tests](./E2E.md) - End-to-end system tests
- [Testing Policy](../TESTING_POLICY.md) - Complete testing guidelines
