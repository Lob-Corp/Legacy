# Database Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [Populating the Database](#populating-the-database)
3. [Technology Stack](#technology-stack)
4. [Database Service](#database-service)
5. [Data Models](#data-models)
6. [Relationships](#relationships)
7. [Enumerations](#enumerations)
8. [Usage Examples](#usage-examples)
9. [Schema Reference](#schema-reference)
10. [Visual Diagrams](#visual-diagrams)
11. [Quick Reference](#quick-reference)

---

## Overview

The GenewebPy database is a genealogical data management system built with SQLAlchemy ORM. It provides a comprehensive structure to store and manage family trees, including persons, families, relationships, events, titles, and more.

### Key Features
- **Person Management**: Store detailed biographical information
- **Family Structures**: Track marriages, divorces, and family relationships
- **Event Recording**: Personal and family events with witnesses
- **Relationship Tracking**: Native and non-native parent relationships
- **Title Management**: Noble titles and their date ranges
- **Date Precision**: Multiple calendar systems and precision levels
- **Data Integrity**: Foreign key constraints and enum validations

### Database Schema
The complete SQL schema is available here: [database_schema.sql](assets/database_schema.sql)

---

## Populating the Database

### Using gwc (GeneWeb Compiler)

The primary way to populate the database is using the `gwc` tool, which parses GeneWeb `.gw` files and creates a SQLite database.

**See**: [GWC_IMPLEMENTATION.md](GWC_IMPLEMENTATION.md) for complete gwc documentation.

#### Quick Start

```bash
# Create database from .gw file
python -m script.gwc -v -f -o family.db family.gw

# Multiple files
python -m script.gwc -v -f -o database.db file1.gw file2.gw
```

#### Options

- `-v`: Verbose output with progress information
- `-f`: Force overwrite if database exists
- `-o <file>`: Output database file (default: a.sql)
- `-stats`: Show compilation statistics
- `-nofail`: Continue on errors
- `-bnotes <mode>`: Control base notes merging (merge/erase/first/drop)

### Using Repositories (Programmatic)

For programmatic access, use the repository pattern:

```python
from database.sqlite_database_service import SQLiteDatabaseService
from repositories.person_repository import PersonRepository
from repositories.family_repository import FamilyRepository

# Initialize
db_service = SQLiteDatabaseService("family.db")
db_service.connect()

person_repo = PersonRepository(db_service)
family_repo = FamilyRepository(db_service)

# Add a person
person = Person(...)  # See Usage Examples below
person_repo.add_person(person)

# Retrieve persons
all_persons = person_repo.get_all_persons()
person = person_repo.get_person_by_id(1)
```

#### Repository Methods

**PersonRepository**:
- `add_person(person)`: Add a new person
- `edit_person(person)`: Update existing person
- `get_person_by_id(id)`: Retrieve by ID
- `get_all_persons()`: Get all persons

**FamilyRepository**:
- `add_family(family)`: Add a new family
- `edit_family(family)`: Update existing family
- `get_family_by_id(id)`: Retrieve by ID
- `get_all_families()`: Get all families

#### Converters

The repositories use converters to transform between application types and database models:

- **`converter_to_db.py`**: Converts application types (Person, Family) to database models
- **`converter_from_db.py`**: Converts database models back to application types

These handle all the complexity of:
- Converting dates with precision and calendars
- Managing relationship tables (Couple, Ascends, Unions, Descends)
- Handling events and witnesses
- Managing titles and relations

---

## Technology Stack

### Core Technologies
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapping (ORM) library
- **SQLite**: Lightweight, file-based relational database
- **Python 3.12+**: Programming language

### SQLAlchemy Features Used
- Declarative Base for model definitions
- Session management for database transactions
- Relationship definitions with cascade operations
- Enum support for type-safe enumeration columns
- Foreign key constraints for referential integrity

---

## Database Service

### SQLiteDatabaseService

The `SQLiteDatabaseService` class provides a high-level interface for database operations.

**Location**: `src/database/sqlite_database_service.py`

#### Key Features

```python
from database.sqlite_database_service import SQLiteDatabaseService

# Initialize service
db_service = SQLiteDatabaseService(database_path="my_database.db")

# Connect to database (creates tables if needed)
db_service.connect()

# Get a session
session = db_service.get_session()

# Perform operations...

# Disconnect when done
db_service.disconnect()
```

#### Main Methods

| Method                                          | Description                                            |
| ----------------------------------------------- | ------------------------------------------------------ |
| `connect()`                                     | Establishes database connection and creates all tables |
| `disconnect()`                                  | Closes database connection and disposes engine         |
| `get_session()`                                 | Returns a new SQLAlchemy Session object                |
| `add(session, obj)`                             | Adds a single object to the session                    |
| `add_all(session, objs)`                        | Adds multiple objects to the session                   |
| `delete(session, obj)`                          | Marks a single object for deletion                     |
| `delete_all(session, objs)`                     | Marks multiple objects for deletion                    |
| `get(session, model, query)`                    | Retrieves a single record matching query               |
| `get_all(session, model, query, offset, limit)` | Retrieves multiple records with pagination             |
| `refresh(session, obj)`                         | Reloads object state from database                     |
| `apply(session)`                                | Commits the current transaction                        |

#### Connection Management

The service uses lazy initialization:
- Database connection is established only when `connect()` is called
- Tables are automatically created if they don't exist
- The engine is properly disposed on `disconnect()`

#### Session Pattern

```python
db_service = SQLiteDatabaseService("base.db")
db_service.connect()

# Get session
session = db_service.get_session()

try:
    # Create objects
    person = Person(first_name="John", surname="Doe", ...)
    db_service.add(session, person)
    
    # Commit changes
    db_service.apply(session)
finally:
    session.close()

db_service.disconnect()
```

---

## Data Models

### Core Models

#### 1. Person
**Table**: `Person`  
**Purpose**: Stores individual biographical information

**Key Fields**:
- `first_name`, `surname`: Name information
- `sex`: Gender (MALE, FEMALE, NEUTER)
- `birth_date`, `baptism_date`: Birth-related dates
- `death_status`, `death_date`, `death_reason`: Death information
- `burial_status`, `burial_date`: Burial information
- `occupation`: Professional information
- `access_right`: Privacy level (PUBLIC, PRIVATE, IFTITLES)

**Relationships**:
- `birth_date_obj`, `baptism_date_obj`, `death_date_obj`, `burial_date_obj`: Links to Date objects
- `ascend`: One-to-one with Ascends (parents)
- `families`: One-to-one with Unions (marriages/families)

#### 2. Family
**Table**: `Family`  
**Purpose**: Represents a marriage or union between two persons

**Key Fields**:
- `marriage_date`: Date of marriage/union
- `marriage_place`, `marriage_note`, `marriage_src`: Marriage details
- `relation_kind`: Type of union (MARRIED, NOT_MARRIED, ENGAGED, etc.)
- `divorce_status`: Divorce state (NOT_DIVORCED, DIVORCED, SEPARATED)
- `divorce_date`: Date of divorce if applicable

**Relationships**:
- `parents`: One-to-one with Couple (the two partners)
- `children`: One-to-one with Descends (list of children)
- `marriage_date_obj`, `divorce_date_obj`: Links to Date objects

#### 3. Couple
**Table**: `Couple`  
**Purpose**: Links two persons as partners in a family

**Relationships**:
- `father_obj`: Link to Person (first partner)
- `mother_obj`: Link to Person (second partner)

#### 4. Ascends
**Table**: `Ascends`  
**Purpose**: Represents a person's parentage

**Key Fields**:
- `parents`: Foreign key to Family (the parents' family)
- `consang`: Consanguinity coefficient

**Relationships**:
- `parents_obj`: Link to Family object

#### 5. Descends
**Table**: `Descends`  
**Purpose**: Container for a family's children

**Relationships**:
- `children`: Many-to-many with Person through DescendChildren

#### 6. Unions
**Table**: `Unions`  
**Purpose**: Container for a person's families/marriages

**Relationships**:
- `families`: Many-to-many with Family through UnionFamilies

---

### Date and Time Models

#### 7. Date
**Table**: `Date`  
**Purpose**: Stores date information with calendar and precision

**Key Fields**:
- `iso_date`: Date in ISO format (TEXT)
- `calendar`: Calendar system (GREGORIAN, JULIAN, FRENCH, HEBREW)
- `precision_id`: Link to Precision object
- `delta`: Days offset

**Relationships**:
- `precision_obj`: One-to-one with Precision (owns the precision exclusively)

**Important**: Due to `single_parent=True` cascade, each Date must have its own unique Precision instance.

#### 8. Precision
**Table**: `Precision`  
**Purpose**: Defines date precision and uncertainty

**Key Fields**:
- `precision_level`: Precision type (SURE, ABOUT, MAYBE, BEFORE, AFTER, ORYEAR, YEARINT)
- `iso_date`: Reference date
- `calendar`: Calendar system
- `delta`: Days range

---

### Event Models

#### 9. PersonalEvent
**Table**: `PersonalEvent`  
**Purpose**: Records events in a person's life

**Key Fields**:
- `person_id`: Link to Person
- `name`: Event type (BIRTH, BAPTISM, DEATH, BURIAL, GRADUATION, etc.)
- `date`: Event date
- `place`, `reason`, `note`, `src`: Event details

**Supported Event Types**: 50+ event types including:
- Life events: BIRTH, BAPTISM, DEATH, BURIAL, CREMATION
- Religious: CONFIRMATION, FIRST_COMMUNION, BAR_MITZVAH, BAT_MITZVAH
- Education: GRADUATE, DIPLOMA, EDUCATION
- Military: MILITARY_SERVICE, MILITARY_PROMOTION, MILITARY_DISTINCTION
- Civil: NATURALISATION, IMMIGRATION, EMIGRATION, MARRIAGE
- Professional: OCCUPATION, RETIRED
- And many more...

#### 10. FamilyEvent
**Table**: `FamilyEvent`  
**Purpose**: Records events related to a family/marriage

**Key Fields**:
- `family_id`: Link to Family
- `name`: Event type (MARRIAGE, DIVORCE, ENGAGE, etc.)
- `date`: Event date
- `place`, `reason`, `note`, `src`: Event details

**Supported Event Types**:
- MARRIAGE, NO_MARRIAGE, NO_MENTION
- ENGAGE, DIVORCE, SEPARATED, ANNULATION
- MARRIAGE_BANN, MARRIAGE_CONTRACT, MARRIAGE_LICENSE
- PACS, RESIDENCE
- NAMED_EVENT (custom events)

---

### Witness Models

#### 11. PersonEventWitness
**Table**: `PersonEventWitness`  
**Purpose**: Links persons as witnesses to personal events

**Key Fields**:
- `person_id`: The witness
- `event_id`: The personal event
- `kind`: Witness type (WITNESS, WITNESS_GODPARENT, WITNESS_CIVILOFFICER, etc.)

#### 12. FamilyEventWitness
**Table**: `FamilyEventWitness`  
**Purpose**: Links persons as witnesses to family events

**Key Fields**:
- `person_id`: The witness
- `event_id`: The family event
- `kind`: Witness type

#### 13. FamilyWitness
**Table**: `FamilyWitness`  
**Purpose**: Links persons as general witnesses to a family

**Key Fields**:
- `family_id`: The family
- `person_id`: The witness

---

### Relationship Models

#### 14. Relation
**Table**: `Relation`  
**Purpose**: Defines non-native parent relationships

**Key Fields**:
- `type`: Relationship type (Adoption, Recognition, CandidateParent, GodParent, FosterParent)
- `father_id`, `mother_id`: The non-biological parents
- `sources`: Documentation sources

#### 15. PersonRelations
**Table**: `PersonRelations`  
**Purpose**: Links related persons (siblings, etc.)

**Key Fields**:
- `person_id`: First person
- `related_person_id`: Related person

#### 16. PersonNonNativeRelations
**Table**: `PersonNonNativeRelations`  
**Purpose**: Links persons to their non-native parent relationships

**Key Fields**:
- `person_id`: The child
- `relation_id`: The Relation defining the non-native parents

---

### Title Models

#### 17. Titles
**Table**: `Titles`  
**Purpose**: Stores noble titles and their validity periods

**Key Fields**:
- `name`: Title name (Duke, Count, Baron, etc.)
- `ident`: Unique identifier
- `place`: Geographic location
- `date_start`, `date_end`: Validity period
- `nth`: Ordinal number (1st, 2nd, etc.)

**Relationships**:
- `date_start_obj`, `date_end_obj`: Links to Date objects

#### 18. PersonTitles
**Table**: `PersonTitles`  
**Purpose**: Links persons to their titles

**Key Fields**:
- `person_id`: The person
- `title_id`: The title

---

### Location Models

#### 19. Place
**Table**: `Place`  
**Purpose**: Stores hierarchical geographic information

**Key Fields**:
- `town`: Town/city name
- `township`: Township
- `canton`: Canton
- `district`: District
- `county`: County
- `region`: Region/state
- `country`: Country
- `other`: Additional location details

---

### Junction Tables

#### 20. PersonEvents
Links Person ↔ PersonalEvent

#### 21. FamilyEvents
Links Family ↔ FamilyEvent

#### 22. UnionFamilies
Links Unions ↔ Family

#### 23. DescendChildren
Links Descends ↔ Person

---

## Relationships

### Relationship Types

#### One-to-One Relationships
Defined with `uselist=False` and `single_parent=True`:

```python
# Person → Ascends (one person has one ascends container)
ascend = relationship("Ascends", uselist=False, 
                     foreign_keys=[ascend_id],
                     cascade="all, delete-orphan",
                     single_parent=True)

# Family → Couple (one family has one couple)
parents = relationship("Couple", uselist=False,
                      foreign_keys=[parents_id],
                      cascade="all, delete-orphan",
                      single_parent=True)
```

#### One-to-Many Relationships
Default SQLAlchemy behavior:

```python
# Person → PersonalEvent (one person, many events)
# Defined on PersonalEvent side:
person_obj = relationship("Person", foreign_keys=[person_id])
```

#### Many-to-Many Relationships
Through junction tables:

```python
# Descends ↔ Person through DescendChildren
children = relationship("Person", 
                       secondary="DescendChildren",
                       back_populates="parent_families")
```

### Cascade Behaviors

**"all, delete-orphan"**: Used for owned relationships
- Deleting parent deletes children
- Removing child from parent deletes child
- Used for: Family→Couple, Person→Ascends, Date→Precision

**single_parent=True**: Ensures exclusive ownership
- Each child can have only one parent
- Prevents sharing of child objects
- Critical for Date→Precision (each Date must own its Precision)

### Important Constraint: Date and Precision

Each `Date` object **must** have its own unique `Precision` instance due to `single_parent=True`:

```python
# ❌ WRONG - Sharing precision between dates
precision = Precision(precision_level=DatePrecision.SURE, ...)
date1 = Date(precision_obj=precision, ...)
date2 = Date(precision_obj=precision, ...)  # ERROR!

# ✅ CORRECT - Each date has its own precision
precision1 = Precision(precision_level=DatePrecision.SURE, ...)
date1 = Date(precision_obj=precision1, ...)

precision2 = Precision(precision_level=DatePrecision.SURE, ...)
date2 = Date(precision_obj=precision2, ...)
```

---

## Enumerations

### Person Enums

#### Sex
```python
class Sex(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTER = "NEUTER"
```

#### AccessRight
```python
class AccessRight(enum.Enum):
    IFTITLES = "IFTITLES"  # Public if person has titles
    PUBLIC = "PUBLIC"       # Always public
    PRIVATE = "PRIVATE"     # Always private
```

#### DeathStatus
```python
class DeathStatus(enum.Enum):
    NOT_DEAD = "NOT_DEAD"
    DEAD = "DEAD"
    DEAD_YOUNG = "DEAD_YOUNG"
    DEAD_DONT_KNOW_WHEN = "DEAD_DONT_KNOW_WHEN"
    DONT_KNOW_IF_DEAD = "DONT_KNOW_IF_DEAD"
    OF_COURSE_DEAD = "OF_COURSE_DEAD"
```

#### DeathReason
```python
class DeathReason(enum.Enum):
    KILLED = "KILLED"
    MURDERED = "MURDERED"
    EXECUTED = "EXECUTED"
    DISAPPEARED = "DISAPPEARED"
    UNSPECIFIED = "UNSPECIFIED"
```

#### BurialStatus
```python
class BurialStatus(enum.Enum):
    UNKNOWN_BURIAL = "UNKNOWN_BURIAL"
    BURIAL = "BURIAL"
    CREMATED = "CREMATED"
```

### Family Enums

#### MaritalStatus
```python
class MaritalStatus(enum.Enum):
    MARRIED = "MARRIED"
    NOT_MARRIED = "NOT_MARRIED"
    ENGAGED = "ENGAGED"
    NO_SEXES_CHECK_NOT_MARRIED = "NO_SEXES_CHECK_NOT_MARRIED"
    NO_MENTION = "NO_MENTION"
    NO_SEXES_CHECK_MARRIED = "NO_SEXES_CHECK_MARRIED"
    MARRIAGE_BANN = "MARRIAGE_BANN"
    MARRIAGE_CONTRACT = "MARRIAGE_CONTRACT"
    MARRIAGE_LICENSE = "MARRIAGE_LICENSE"
    PACS = "PACS"
    RESIDENCE = "RESIDENCE"
```

#### DivorceStatus
```python
class DivorceStatus(enum.Enum):
    NOT_DIVORCED = "NOT_DIVORCED"
    DIVORCED = "DIVORCED"
    SEPARATED = "SEPARATED"
```

### Date Enums

#### DatePrecision
```python
class DatePrecision(enum.Enum):
    SURE = "SURE"        # Exact date
    ABOUT = "ABOUT"      # Approximate date
    MAYBE = "MAYBE"      # Uncertain date
    BEFORE = "BEFORE"    # Before this date
    AFTER = "AFTER"      # After this date
    ORYEAR = "ORYEAR"    # One of two years
    YEARINT = "YEARINT"  # Year interval
```

#### Calendar
```python
class Calendar(enum.Enum):
    GREGORIAN = "GREGORIAN"  # Standard calendar
    JULIAN = "JULIAN"        # Old-style calendar
    FRENCH = "FRENCH"        # French Revolutionary calendar
    HEBREW = "HEBREW"        # Hebrew calendar
```

### Event Enums

#### PersonalEventName
50+ event types including:
- BIRTH, BAPTISM, DEATH, BURIAL, CREMATION
- GRADUATE, DIPLOMA, EDUCATION
- CONFIRMATION, FIRST_COMMUNION, BAR_MITZVAH
- MILITARY_SERVICE, OCCUPATION, RETIRED
- And many more...

#### FamilyEventName
```python
class FamilyEventName(enum.Enum):
    MARRIAGE = "MARRIAGE"
    NO_MARRIAGE = "NO_MARRIAGE"
    NO_MENTION = "NO_MENTION"
    ENGAGE = "ENGAGE"
    DIVORCE = "DIVORCE"
    SEPARATED = "SEPARATED"
    ANNULATION = "ANNULATION"
    MARRIAGE_BANN = "MARRIAGE_BANN"
    MARRIAGE_CONTRACT = "MARRIAGE_CONTRACT"
    MARRIAGE_LICENSE = "MARRIAGE_LICENSE"
    PACS = "PACS"
    RESIDENCE = "RESIDENCE"
    NAMED_EVENT = "NAMED_EVENT"
```

### Witness Enum

#### EventWitnessKind
```python
class EventWitnessKind(enum.Enum):
    WITNESS = "WITNESS"
    WITNESS_GODPARENT = "WITNESS_GODPARENT"
    WITNESS_CIVILOFFICER = "WITNESS_CIVILOFFICER"
    WITNESS_RELIGIOUSOFFICER = "WITNESS_RELIGIOUSOFFICER"
    WITNESS_INFORMANT = "WITNESS_INFORMANT"
    WITNESS_ATTENDING = "WITNESS_ATTENDING"
    WITNESS_MENTIONED = "WITNESS_MENTIONED"
    WITNESS_OTHER = "WITNESS_OTHER"
```

### Relation Enum

#### RelationToParentType
```python
class RelationToParentType(enum.Enum):
    Adoption = "Adoption"
    Recognition = "Recognition"
    CandidateParent = "CandidateParent"
    GodParent = "GodParent"
    FosterParent = "FosterParent"
```

---

## Usage Examples

### Example 1: Creating a Person

```python
from database.sqlite_database_service import SQLiteDatabaseService
from database.person import Person, Sex, DeathStatus, BurialStatus
from database.date import Date, Precision, DatePrecision, Calendar
from libraries.title import AccessRight

# Initialize database
db_service = SQLiteDatabaseService("genealogy.db")
db_service.connect()
session = db_service.get_session()

try:
    # Create birth date with precision
    birth_precision = Precision(
        precision_level=DatePrecision.SURE,
        iso_date="1850-06-15",
        calendar=Calendar.GREGORIAN,
        delta=0
    )
    birth_date = Date(
        iso_date="1850-06-15",
        calendar=Calendar.GREGORIAN,
        precision_obj=birth_precision,
        delta=0
    )
    
    # Create person
    person = Person(
        first_name="John",
        surname="Doe",
        occ=0,
        image="",
        public_name="John Doe",
        qualifiers="",
        aliases="",
        first_names_aliases="",
        surname_aliases="",
        occupation="Farmer",
        sex=Sex.MALE,
        access_right=AccessRight.PUBLIC,
        birth_date_obj=birth_date,
        birth_place="London",
        birth_note="Born at home",
        birth_src="Birth certificate",
        baptism_place="",
        baptism_note="",
        baptism_src="",
        death_status=DeathStatus.DEAD,
        death_reason=None,
        death_place="London",
        death_note="",
        death_src="",
        burial_status=BurialStatus.BURIAL,
        burial_place="London Cemetery",
        burial_note="",
        burial_src="",
        notes="",
        src=""
    )
    
    # Save to database
    db_service.add(session, person)
    db_service.apply(session)
    
    print(f"Person created with ID: {person.id}")
    
finally:
    session.close()
    db_service.disconnect()
```

### Example 2: Creating a Family

```python
from database.family import Family, MaritalStatus, DivorceStatus
from database.couple import Couple
from database.descends import Descends

# Assuming father and mother Person objects already exist
session = db_service.get_session()

try:
    # Create couple
    couple = Couple(
        father_obj=father,
        mother_obj=mother
    )
    
    # Create marriage date
    marriage_precision = Precision(
        precision_level=DatePrecision.SURE,
        iso_date="1875-08-20",
        calendar=Calendar.GREGORIAN,
        delta=0
    )
    marriage_date = Date(
        iso_date="1875-08-20",
        calendar=Calendar.GREGORIAN,
        precision_obj=marriage_precision,
        delta=0
    )
    
    # Create children container
    descends = Descends()
    
    # Create family
    family = Family(
        parents=couple,
        children=descends,
        marriage_date_obj=marriage_date,
        marriage_place="London Church",
        marriage_note="Large ceremony",
        marriage_src="Church records",
        relation_kind=MaritalStatus.MARRIED,
        divorce_status=DivorceStatus.NOT_DIVORCED,
        divorce_date=None,
        comment="",
        origin_file="family.ged",
        src=""
    )
    
    db_service.add(session, family)
    db_service.apply(session)
    
    print(f"Family created with ID: {family.id}")
    
finally:
    session.close()
```

### Example 3: Adding a Personal Event

```python
from database.personal_event import PersonalEvent, PersonalEventName

session = db_service.get_session()

try:
    # Create graduation event
    event_precision = Precision(
        precision_level=DatePrecision.SURE,
        iso_date="1870-06-01",
        calendar=Calendar.GREGORIAN,
        delta=0
    )
    event_date = Date(
        iso_date="1870-06-01",
        calendar=Calendar.GREGORIAN,
        precision_obj=event_precision,
        delta=0
    )
    
    graduation = PersonalEvent(
        person_obj=person,
        name=PersonalEventName.GRADUATE,
        date_obj=event_date,
        place="Oxford University",
        reason="Bachelor of Arts",
        note="With honors",
        src="University records"
    )
    
    db_service.add(session, graduation)
    db_service.apply(session)
    
    print(f"Event created with ID: {graduation.id}")
    
finally:
    session.close()
```

### Example 4: Querying Data

```python
from database.person import Person, Sex

session = db_service.get_session()

try:
    # Get single person by ID
    person = db_service.get(session, Person, {"id": 1})
    if person:
        print(f"Found: {person.first_name} {person.surname}")
    
    # Get all males
    males = db_service.get_all(
        session, 
        Person, 
        {"sex": Sex.MALE},
        offset=0,
        limit=100
    )
    print(f"Found {len(males)} male persons")
    
    # Custom query using session
    farmers = session.query(Person).filter(
        Person.occupation.like("%Farmer%")
    ).all()
    print(f"Found {len(farmers)} farmers")
    
finally:
    session.close()
```

### Example 5: Cascade Delete Behavior

```python
session = db_service.get_session()

try:
    # Create person with dates
    person = Person(...)
    person.birth_date_obj = Date(...)  # Has precision
    
    db_service.add(session, person)
    db_service.apply(session)
    
    # Deleting person will cascade delete:
    # - birth_date Date object
    # - birth_date's Precision object
    # - All related PersonalEvent objects
    # - All related PersonEventWitness objects
    db_service.delete(session, person)
    db_service.apply(session)
    
    print("Person and all related data deleted")
    
finally:
    session.close()
```

---

## Schema Reference

### Complete SQL Schema
The full database schema with all tables, columns, constraints, and CHECK constraints is available in:

📄 **[assets/database_schema.sql](assets/database_schema.sql)**

### Quick Reference
For a quick lookup table of all models and common operations:

⚡ **[DATABASE_QUICK_REF.md](DATABASE_QUICK_REF.md)**

### Schema Statistics
- **Total Tables**: 23
- **Core Entity Tables**: 5 (Person, Family, Couple, Ascends, Descends)
- **Event Tables**: 2 (PersonalEvent, FamilyEvent)
- **Junction Tables**: 8
- **Support Tables**: 8 (Date, Precision, Place, Titles, Relation, etc.)

### Generating Updated Schema

To regenerate the schema file after model changes:

```bash
python src/script/export_database_schema.py -o docs/assets/database_schema.sql
```

Options:
- `-d sqlite|postgresql|mysql` - Choose SQL dialect
- `-l` - List all tables
- `-t` - Include INSERT statement templates

---

## Best Practices

### 1. Always Use Unique Precision Objects

```python
# Each Date needs its own Precision
precision1 = Precision(...)
date1 = Date(precision_obj=precision1, ...)

precision2 = Precision(...)
date2 = Date(precision_obj=precision2, ...)
```

### 2. Use Context Managers for Sessions

```python
session = db_service.get_session()
try:
    # Your database operations
    db_service.apply(session)
finally:
    session.close()
```

### 3. Commit Transactions Explicitly

```python
# Add objects
db_service.add(session, obj)

# Commit when ready
db_service.apply(session)
```

### 4. Handle Cascade Deletes Carefully

Be aware that deleting a parent object will cascade delete children:
- Deleting Person deletes their dates, events, etc.
- Deleting Family deletes the Couple
- Deleting Date deletes its Precision

### 5. Use Enums for Type Safety

```python
# Use enum values, not strings
person.sex = Sex.MALE  # ✅ Correct
person.sex = "MALE"    # ❌ May cause issues
```

### 6. Validate Date Calendar Consistency

Ensure date and precision use the same calendar:

```python
precision = Precision(calendar=Calendar.GREGORIAN, ...)
date = Date(calendar=Calendar.GREGORIAN, precision_obj=precision, ...)
```

---

## Testing

Comprehensive tests are available in:
- `tests/database/test_database_models.py`
- `tests/database/test_relationships_comprehensive.py`

Run tests with:
```bash
pytest tests/database/ -v
```

---

## Maintenance

### Database Migrations

For schema changes:
1. Modify model definitions in `src/database/`
2. Create migration script if needed
3. Regenerate schema: `python src/script/export_database_schema.py`
4. Update documentation
5. Run tests to verify changes

### Backup and Recovery

SQLite database files can be backed up by simply copying the `.db` file:

```bash
cp base.db base_backup.db
```

For production use, consider using SQLite's backup API or regular file system backups.

---

## Troubleshooting

### Common Issues

**Issue**: `InvalidRequestError: Instance <Precision> is already associated`  
**Solution**: Each Date must have its own Precision object. Don't reuse Precision instances.

**Issue**: `IntegrityError: FOREIGN KEY constraint failed`  
**Solution**: Ensure referenced objects are saved before creating relationships.

**Issue**: `AttributeError: 'NoneType' object has no attribute`  
**Solution**: Check that relationships are properly loaded. Use `session.refresh()` if needed.

---

## Visual Diagrams

### Entity Relationship Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Core Entity Structure                          │
└─────────────────────────────────────────────────────────────────────────┘

                            ┌──────────────┐
                            │    Person    │
                            │──────────────│
                            │ id           │
                            │ first_name   │
                            │ surname      │
                            │ sex          │
                            │ birth_date ◆─┼────┐
                            │ death_date ◆─┼──┐ │
                            │ ascend_id  ──┼┐ │ │
                            │ families_id ─┼┼┐│ │
                            └──────────────┘││││ │
                                            ││││ │
                    ┌───────────────────────┘│││ │
                    │                        │││ │
                    ▼                        │││ │
            ┌──────────────┐                │││ │
            │   Ascends    │                │││ │
            │──────────────│                │││ │
            │ id           │                │││ │
            │ parents    ──┼─┐              │││ │
            │ consang      │ │              │││ │
            └──────────────┘ │              │││ │
                             │              │││ │
                             ▼              │││ │
                    ┌──────────────┐        │││ │
                    │    Family    │        │││ │
                    │──────────────│        │││ │
                    │ id           │        │││ │
                    │ marriage_date◆─┼──┐   │││ │
                    │ divorce_date ◆─┼┐ │   │││ │
                    │ parents_id  ──┼┼┐│   │││ │
                    │ children_id ──┼┼┼┼┐  │││ │
                    └──────────────┘│││││  │││ │
                                    │││││  │││ │
                ┌───────────────────┘││││  │││ │
                │                    ││││  │││ │
                ▼                    ││││  │││ │
        ┌──────────────┐             ││││  │││ │
        │    Couple    │             ││││  │││ │
        │──────────────│             ││││  │││ │
        │ id           │             ││││  │││ │
        │ father_id  ──┼──┐          ││││  │││ │
        │ mother_id  ──┼─┐│          ││││  │││ │
        └──────────────┘ ││          ││││  │││ │
                         ││          ││││  │││ │
        ┌────────────────┼┼──────────┘│││  │││ │
        │                ││           │││  │││ │
        │         ┌──────┼┘           │││  │││ │
        │         │      │            │││  │││ │
        │         │      │            │││  │││ │
        │         │  ┌───┼────────────┘││  │││ │
        │         │  │   │             ││  │││ │
        │         │  │   └─────────────┼┘  │││ │
        │         │  │                 │   │││ │
        │         │  │ ┌───────────────┘   │││ │
        │         │  │ │                   │││ │
        ▼         ▼  ▼ ▼                   │││ │
     [Person] [Person]                     │││ │
     Father    Mother                      │││ │
                                           │││ │
                    ┌──────────────────────┘││ │
                    │                       ││ │
                    ▼                       ││ │
            ┌──────────────┐                ││ │
            │   Descends   │                ││ │
            │──────────────│                ││ │
            │ id           │                ││ │
            │ children   ──┼─────┐          ││ │
            └──────────────┘     │          ││ │
                                 │          ││ │
                                 ▼          ││ │
                       [Person, Person, ...]││ │
                          Children          ││ │
                                            ││ │
            ┌───────────────────────────────┼┘ │
            │                               │  │
            ▼                               │  │
     ┌──────────────┐                      │  │
     │    Unions    │                      │  │
     │──────────────│                      │  │
     │ id           │                      │  │
     │ families   ──┼──────┐               │  │
     └──────────────┘      │               │  │
                           │               │  │
                           ▼               │  │
                  [Family, Family, ...]    │  │
                                           │  │
                                           │  │
  ┌────────────────────────────────────────┼──┼───────┐
  │                     Date Module        │  │       │
  └────────────────────────────────────────┼──┼───────┘
                                           │  │
                    ┌──────────────┐       │  │
                    │     Date     │◄──────┘  │
                    │──────────────│          │
                    │ id           │          │
                    │ iso_date     │          │
                    │ calendar     │          │
                    │ precision_id─┼──┐       │
                    │ delta        │  │       │
                    └──────────────┘  │       │
                                      │       │
                                      ▼       │
                            ┌──────────────┐  │
                            │  Precision   │  │
                            │──────────────│  │
                            │ id           │  │
                            │ precision_lvl│  │
                            │ calendar     │  │
                            │ delta        │  │
                            └──────────────┘  │
                                              │
                                              │
                      ┌───────────────────────┘
                      │
                      ▼
           [birth_date, death_date, baptism_date, ...]


┌─────────────────────────────────────────────────────────────────────────┐
│                           Event Structure                               │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐                      ┌──────────────┐
    │    Person    │                      │    Family    │
    │──────────────│                      │──────────────│
    │ id           │                      │ id           │
    └──────────────┘                      └──────────────┘
            │                                     │
            │ person_id                           │ family_id
            │                                     │
            ▼                                     ▼
    ┌──────────────────┐              ┌──────────────────┐
    │ PersonalEvent    │              │  FamilyEvent     │
    │──────────────────│              │──────────────────│
    │ id               │              │ id               │
    │ person_id        │              │ family_id        │
    │ name (enum)      │              │ name (enum)      │
    │ date           ◆─┼──┐           │ date           ◆─┼──┐
    │ place            │  │           │ place            │  │
    │ note             │  │           │ note             │  │
    └──────────────────┘  │           └──────────────────┘  │
            │             │                   │             │
            │             └─────────┐         │             └────────┐
            │ event_id              │         │ event_id            │
            │                       │         │                     │
            ▼                       │         ▼                     │
    ┌───────────────────┐          │ ┌───────────────────┐         │
    │PersonEventWitness │          │ │FamilyEventWitness │         │
    │───────────────────│          │ │───────────────────│         │
    │ person_id       ──┼──┐       │ │ person_id       ──┼──┐      │
    │ event_id          │  │       │ │ event_id          │  │      │
    │ kind (enum)       │  │       │ │ kind (enum)       │  │      │
    └───────────────────┘  │       │ └───────────────────┘  │      │
                           │       │                        │      │
                           ▼       │                        ▼      │
                      [Person]     │                   [Person]    │
                      Witness      │                   Witness     │
                                   ▼                               ▼
                               [Date obj]                      [Date obj]


┌─────────────────────────────────────────────────────────────────────────┐
│                      Relationship Structure                             │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │    Person    │
    └──────────────┘
            │
            │ person_id
            │
            ▼
    ┌────────────────────────┐
    │PersonNonNativeRelations│
    │────────────────────────│
    │ person_id              │
    │ relation_id          ──┼──┐
    └────────────────────────┘  │
                                │
                                ▼
                        ┌──────────────┐
                        │   Relation   │
                        │──────────────│
                        │ id           │
                        │ type (enum)  │◄─── Adoption, Recognition,
                        │ father_id  ──┼──┐  CandidateParent,
                        │ mother_id  ──┼─┐│  GodParent, FosterParent
                        │ sources      │ ││
                        └──────────────┘ ││
                                         ││
                                         ▼▼
                                    [Persons]
                                 Non-bio parents


┌─────────────────────────────────────────────────────────────────────────┐
│                          Title Structure                                │
└─────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │    Person    │
    └──────────────┘
            │
            │ person_id
            │
            ▼
    ┌──────────────┐
    │PersonTitles  │
    │──────────────│
    │ person_id    │
    │ title_id   ──┼──┐
    └──────────────┘  │
                      │
                      ▼
              ┌──────────────┐
              │    Titles    │
              │──────────────│
              │ id           │
              │ name         │◄─── Duke, Count, Baron, etc.
              │ place        │
              │ date_start ◆─┼──┐
              │ date_end   ◆─┼─┐│
              │ nth          │ ││
              └──────────────┘ ││
                               ││
                               ▼▼
                          [Date objects]
                        Start and End dates
```

### Diagram Legend

```
┌──────┐
│Table │   = Database table/entity
└──────┘

  ──┐      = Foreign key relationship
    │
    ▼

  ──◆──    = Owned relationship (with cascade delete)

 [Items]   = Collection/List of related items

 (enum)    = Enumeration column with CHECK constraint
```

### Relationship Type Summary

**One-to-One** (uselist=False):
- Person → Ascends, Person → Unions
- Family → Couple, Family → Descends
- Date → Precision (MUST BE UNIQUE)

**One-to-Many**:
- Person → PersonalEvent, Family → FamilyEvent
- Person → Witness entries

**Many-to-Many** (via junction tables):
- Person ↔ Person (PersonRelations)
- Person ↔ Titles (PersonTitles)
- Descends ↔ Person (DescendChildren)
- Unions ↔ Family (UnionFamilies)

### Cascade Delete Summary

| Delete     | Cascades To                                                          |
| ---------- | -------------------------------------------------------------------- |
| **Person** | All Date objects, PersonalEvent, PersonEventWitness, Ascends, Unions |
| **Family** | Couple, Descends, FamilyEvent, marriage/divorce Dates                |
| **Date**   | Precision (exclusive ownership)                                      |
| **Couple** | Nothing (just removes link)                                          |

### Enumeration Summary

| Table          | Column          | Values Count                          |
| -------------- | --------------- | ------------------------------------- |
| Person         | sex             | 3 (MALE, FEMALE, NEUTER)              |
| Person         | access_right    | 3 (PUBLIC, PRIVATE, IFTITLES)         |
| Person         | death_status    | 6                                     |
| Person         | death_reason    | 5                                     |
| Person         | burial_status   | 3                                     |
| Family         | relation_kind   | 11 (marriage types)                   |
| Family         | divorce_status  | 3                                     |
| Date/Precision | calendar        | 4 (GREGORIAN, JULIAN, FRENCH, HEBREW) |
| Precision      | precision_level | 7                                     |
| PersonalEvent  | name            | 50+ event types                       |
| FamilyEvent    | name            | 13 event types                        |
| Relation       | type            | 5 relationship types                  |
| *EventWitness  | kind            | 8 witness types                       |

---

## Quick Reference

### All Models at a Glance

#### Core Entities

| Model      | Table    | Primary Use                    | Key Relationships                  |
| ---------- | -------- | ------------------------------ | ---------------------------------- |
| `Person`   | Person   | Individual biographical data   | → Ascends, Unions, Date objects    |
| `Family`   | Family   | Marriage/union between persons | → Couple, Descends, Date objects   |
| `Couple`   | Couple   | Partner relationship           | → 2 Person objects (father/mother) |
| `Ascends`  | Ascends  | Person's parentage             | → Family                           |
| `Descends` | Descends | Family's children              | ↔ Person (many-to-many)            |
| `Unions`   | Unions   | Person's families              | ↔ Family (many-to-many)            |

#### Date & Time

| Model       | Table     | Primary Use                | Key Relationships                   |
| ----------- | --------- | -------------------------- | ----------------------------------- |
| `Date`      | Date      | Date with calendar system  | → Precision (one-to-one, EXCLUSIVE) |
| `Precision` | Precision | Date precision/uncertainty | Owned by one Date only              |

#### Events

| Model                | Table              | Primary Use                  | Key Relationships       |
| -------------------- | ------------------ | ---------------------------- | ----------------------- |
| `PersonalEvent`      | PersonalEvent      | Life events                  | → Person, Date          |
| `FamilyEvent`        | FamilyEvent        | Marriage/family events       | → Family, Date          |
| `PersonEventWitness` | PersonEventWitness | Witnesses to personal events | → Person, PersonalEvent |
| `FamilyEventWitness` | FamilyEventWitness | Witnesses to family events   | → Person, FamilyEvent   |
| `FamilyWitness`      | FamilyWitness      | General family witnesses     | → Family, Person        |

#### Relationships

| Model                      | Table                    | Primary Use                     | Key Relationships               |
| -------------------------- | ------------------------ | ------------------------------- | ------------------------------- |
| `Relation`                 | Relation                 | Non-native parent relationships | → 2 Person objects, source docs |
| `PersonRelations`          | PersonRelations          | Person-to-person links          | → 2 Person objects              |
| `PersonNonNativeRelations` | PersonNonNativeRelations | Link to non-native parents      | → Person, Relation              |

#### Titles & Places

| Model          | Table        | Primary Use                   | Key Relationships            |
| -------------- | ------------ | ----------------------------- | ---------------------------- |
| `Titles`       | Titles       | Noble titles with date ranges | → 2 Date objects (start/end) |
| `PersonTitles` | PersonTitles | Person's titles               | → Person, Titles             |
| `Place`        | Place        | Geographic locations          | Standalone                   |

#### Junction Tables

| Model             | Table           | Links Between          |
| ----------------- | --------------- | ---------------------- |
| `PersonEvents`    | PersonEvents    | Person ↔ PersonalEvent |
| `FamilyEvents`    | FamilyEvents    | Family ↔ FamilyEvent   |
| `UnionFamilies`   | UnionFamilies   | Unions ↔ Family        |
| `DescendChildren` | DescendChildren | Descends ↔ Person      |

### Import Paths Cheat Sheet

```python
# Core entities
from database.person import Person, Sex, DeathStatus, BurialStatus
from database.family import Family, MaritalStatus, DivorceStatus
from database.couple import Couple
from database.ascends import Ascends
from database.descends import Descends
from database.unions import Unions

# Date & time
from database.date import Date, DatePrecision, Calendar
from database.precision import Precision

# Events
from database.personal_event import PersonalEvent, PersonalEventName
from database.family_event import FamilyEvent, FamilyEventName
from database.person_event_witness import PersonEventWitness, EventWitnessKind
from database.family_event_witness import FamilyEventWitness
from database.family_witness import FamilyWitness

# Relationships
from database.relation import Relation, RelationToParentType
from database.person_relations import PersonRelations
from database.person_non_native_relations import PersonNonNativeRelations

# Titles & places
from database.titles import Titles
from database.person_titles import PersonTitles
from database.place import Place

# Junction tables
from database.person_events import PersonEvents
from database.family_events import FamilyEvents
from database.union_families import UnionFamilies
from database.descend_children import DescendChildren

# Service
from database.sqlite_database_service import SQLiteDatabaseService

# Other imports
from libraries.title import AccessRight
from libraries.death_info import DeathReason
```

### Common Enums Quick Reference

**Person**:
- `Sex`: MALE, FEMALE, NEUTER
- `AccessRight`: PUBLIC, PRIVATE, IFTITLES
- `DeathStatus`: NOT_DEAD, DEAD, DEAD_YOUNG, DEAD_DONT_KNOW_WHEN, DONT_KNOW_IF_DEAD, OF_COURSE_DEAD
- `DeathReason`: KILLED, MURDERED, EXECUTED, DISAPPEARED, UNSPECIFIED
- `BurialStatus`: UNKNOWN_BURIAL, BURIAL, CREMATED

**Family**:
- `MaritalStatus`: MARRIED, NOT_MARRIED, ENGAGED, PACS, RESIDENCE, etc. (11 total)
- `DivorceStatus`: NOT_DIVORCED, DIVORCED, SEPARATED

**Date**:
- `DatePrecision`: SURE, ABOUT, MAYBE, BEFORE, AFTER, ORYEAR, YEARINT
- `Calendar`: GREGORIAN, JULIAN, FRENCH, HEBREW

**Events**:
- `PersonalEventName`: 50+ types (BIRTH, DEATH, GRADUATE, MILITARY_SERVICE, etc.)
- `FamilyEventName`: 13 types (MARRIAGE, DIVORCE, ENGAGE, PACS, etc.)
- `EventWitnessKind`: 8 types (WITNESS, WITNESS_GODPARENT, WITNESS_CIVILOFFICER, etc.)

**Relationships**:
- `RelationToParentType`: Adoption, Recognition, CandidateParent, GodParent, FosterParent

### Field Counts by Model

| Model         | Total Columns | Foreign Keys | Enums |
| ------------- | ------------- | ------------ | ----- |
| Person        | 36            | 6            | 5     |
| Family        | 13            | 4            | 2     |
| Date          | 5             | 1            | 1     |
| Precision     | 5             | 0            | 2     |
| PersonalEvent | 8             | 2            | 1     |
| FamilyEvent   | 8             | 2            | 1     |
| Titles        | 7             | 2            | 0     |
| Relation      | 5             | 2            | 1     |
| Place         | 9             | 0            | 0     |
| Couple        | 3             | 2            | 0     |

---

## Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Database Schema SQL](assets/database_schema.sql)

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**Maintainer**: GenewebPy Development Team
