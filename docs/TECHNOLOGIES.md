# Technologies & Architecture Decisions

**Version:** 1.0  
**Last Updated:** October 31, 2025  
**Status:** Active

## Table of Contents

1. [Overview](#overview)
2. [Core Technologies](#core-technologies)
3. [Development Tools](#development-tools)
4. [Infrastructure & Deployment](#infrastructure--deployment)
5. [Testing Framework](#testing-framework)
6. [Architecture Decisions](#architecture-decisions)
7. [Alternatives Considered](#alternatives-considered)
8. [Future Considerations](#future-considerations)

---

## Overview

GenewebPy is a Python reimplementation of the OCaml-based Geneweb genealogy software. This document explains the technology choices made for the project, the reasoning behind each decision, and alternatives that were considered.

### Design Principles

Our technology choices are guided by:
- **Maintainability**: Code should be easy to understand and modify
- **Performance**: Acceptable speed for genealogical databases (up to 100,000+ persons)
- **Compatibility**: Behavioral parity with original OCaml Geneweb
- **Modern Practices**: Leverage current Python ecosystem and best practices
- **Accessibility**: Lower barrier to entry for contributors vs. OCaml

---

## Core Technologies

### Python 3.12.11

**Choice**: Python 3.12.11 as the primary programming language

**Why 3.12?**
- Latest stable release with performance improvements
- Enhanced type system features
- Better error messages
- Improved dataclass performance
- Pattern matching support (introduced in 3.10, refined in 3.12)

**Alternatives Considered**:
- **Keep OCaml**: Excellent performance but smaller community, harder to maintain
- **Rust**: Great performance but steeper learning curve, smaller ecosystem for web
- **Go**: Good performance but less expressive type system for our domain
- **TypeScript/Node.js**: Good ecosystem but less suitable for data processing

### Flask 3.x

**Choice**: Flask as the web framework

**Why Flask?**

✅ **Advantages**:
- **Simplicity**: Minimal, unopinionated framework - easy to understand
- **Flexibility**: Can structure application as needed
- **Lightweight**: Small footprint, fast startup
- **Well-Documented**: Excellent documentation and community resources
- **Extensions**: Rich ecosystem of extensions (SQLAlchemy, testing, etc.)
- **WSGI Standard**: Compatible with production servers (Gunicorn, uWSGI)

❌ **Trade-offs**:
- Fewer built-in features than Django (but we don't need them)
- Need to make more architectural decisions (vs. Django's conventions)

**Use Cases in GenewebPy**:
```python
# Web server for genealogy interface
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/person/<int:person_id>')
def show_person(person_id):
    person = person_repo.get_person_by_id(person_id)
    return render_template('person.html', person=person)
```

### SQLite 3

**Choice**: SQLite as the database engine

**Why SQLite?**

✅ **Advantages**:
- **Zero Configuration**: No server to set up or manage
- **File-Based**: Single file per database, easy to backup/transfer
- **Reliable**: ACID compliant, battle-tested, rock-solid
- **Fast**: Excellent read performance for our query patterns
- **Embedded**: No network overhead, direct file access
- **Cross-Platform**: Works identically on all platforms
- **Standard Tools**: Can use any SQLite browser/tool

❌ **Trade-offs**:
- Limited concurrent writes (not an issue for genealogy use case)
- No built-in replication (can use file-based replication)
- Size limits (not a concern - supports very large databases)

**Why Not OCaml's .gwb Format?**
- Proprietary binary format, hard to inspect/debug
- Requires custom tools to access
- No standard query language
- Difficult to backup/transfer
- Can't use standard database tools


**Alternatives Considered**:
- **PostgreSQL**: Overkill, requires server setup, too complex for typical use
- **MySQL/MariaDB**: Same issues as PostgreSQL
- **MongoDB**: NoSQL not ideal for genealogical relationships
- **Keep .gwb**: Limits tooling and accessibility

### SQLAlchemy 2.x

**Choice**: SQLAlchemy as the ORM (Object-Relational Mapper)

**Why SQLAlchemy?**

✅ **Advantages**:
- **Powerful ORM**: Maps database tables to Python classes elegantly
- **Relationship Handling**: Excellent support for complex relationships (families, persons)
- **Type Safety**: Integrates well with Python type hints
- **Query Builder**: Expressive API for complex queries
- **Migration Support**: Works with Alembic for schema migrations
- **Mature**: Industry-standard, well-tested, excellent documentation

**Example Usage**:
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

class Person(Base):
    __tablename__ = 'person'
    
    index: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    
    # Bidirectional relationships
    families_as_parent: Mapped[List["FamilyLink"]] = relationship(
        back_populates="person"
    )
```

**Benefits for Our Domain**:
- Handles complex genealogical relationships (persons ↔ families)
- Automatic cascade deletes for integrity
- Lazy loading for performance
- Session management for transactions

**Alternatives Considered**:
- **Raw SQL**: More verbose, error-prone, no type safety
- **Django ORM**: Tied to Django framework
- **Peewee**: Simpler but less powerful for complex relationships
- **Pony ORM**: Interesting but smaller community

---

## Development Tools

### Type Checking: MyPy

**Choice**: MyPy for static type checking

**Why MyPy?**

✅ **Advantages**:
- **Catch Errors Early**: Find type-related bugs before runtime
- **Documentation**: Type hints serve as inline documentation
- **IDE Support**: Better autocomplete and refactoring in editors
- **Gradual Typing**: Can adopt incrementally, doesn't require all-or-nothing
- **Industry Standard**: De facto standard for Python type checking

**Example**:
```python
from typing import Optional, List

def get_person_by_name(
    first_name: str,
    surname: str,
    occ: int = 0
) -> Optional[Person]:
    """Type hints document parameters and return type"""
    ...
```

**Configuration** (`.mypy.ini`):
```ini
[mypy]
python_version = 3.12
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

**Alternatives Considered**:
- **Pyright**: Microsoft's type checker, fast but less mature
- **Pyre**: Facebook's checker, complex setup
- **No type checking**: Would lose safety benefits

### Testing: Pytest

**Choice**: Pytest as the testing framework

**Why Pytest?**

✅ **Advantages**:
- **Simple Syntax**: Clean test code with minimal boilerplate
- **Powerful Fixtures**: Excellent dependency injection for test setup
- **Parametrization**: Easy to test multiple scenarios
- **Rich Ecosystem**: Plugins for coverage, parallel execution, etc.
- **Great Output**: Clear, helpful error messages
- **Industry Standard**: Most popular Python testing framework

**Example**:
```python
@pytest.fixture
def db_with_data():
    """Fixture providing database with test data"""
    db = SQLiteDatabaseService(":memory:")
    db.connect()
    db.initialize_schema()
    # Load test data...
    yield db
    db.close()

def test_person_count(db_with_data):
    """Test using fixture"""
    persons = person_repo.get_all_persons()
    assert len(persons) == 12
```

**Plugins Used**:
- `pytest-cov`: Coverage reporting
- `pytest-xdist`: Parallel test execution
- `pytest-mock`: Mocking utilities

**Alternatives Considered**:
- **unittest**: Built-in but more verbose, less powerful
- **nose2**: Less active development
- **doctest**: Good for documentation but limited testing capabilities

### Version Control: Git + GitHub

**Choice**: Git with GitHub for hosting

**Why Git + GitHub?**

✅ **Git Advantages**:
- **Distributed**: Everyone has full history
- **Branching**: Excellent branch management
- **Industry Standard**: Universal understanding
- **Performance**: Fast operations

✅ **GitHub Advantages**:
- **Pull Requests**: Great code review workflow
- **Issues**: Integrated issue tracking
- **Actions**: CI/CD automation
- **Projects**: Kanban boards for organization
- **Community**: Easy for contributors to participate

**Branch Strategy**:
- `main`: Production-ready code
- `milestone/*`: Feature group branches
- `feature/milestone/*`: Individual features
- `hotfix/*`: Urgent production fixes

See [QUALITY_INSURANCE.md](QUALITY_INSURANCE.md) for details.

---

## Infrastructure & Deployment

### Docker

**Choice**: Docker for containerization

**Why Docker?**

✅ **Advantages**:
- **Consistency**: "Works on my machine" → "Works everywhere"
- **Isolation**: Application and dependencies self-contained
- **Portability**: Run on any Docker-capable host
- **Simplified Deployment**: Single command to start application
- **Development Parity**: Dev environment matches production
- **Easy Updates**: Pull new image, restart container

**Docker Compose Stack**:
```yaml
services:
  geneweb:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data        # Databases
      - ./bases:/app/bases      # Alternative database location
      - ./logs:/app/logs        # Application logs
    environment:
      - DEBUG=false
      - HOST=0.0.0.0
      - PORT=8080
```

**Benefits for Users**:
- No Python installation needed
- No dependency management
- Easy upgrades
- Clean uninstall

**Alternatives Considered**:
- **VM (VirtualBox, VMware)**: Too heavy, slower
- **Native Installation**: Complex dependencies, platform-specific issues
- **Snap/Flatpak**: Linux-only, more complex than Docker

### Ansible

**Choice**: Ansible for deployment automation

**Why Ansible?**

✅ **Advantages**:
- **Agentless**: Uses SSH, no agent on target servers
- **Declarative**: Describe desired state, Ansible handles details
- **Idempotent**: Safe to run multiple times
- **YAML-Based**: Human-readable playbooks
- **Large Community**: Extensive module library

**Use Case**:
```yaml
# Deploy to multiple servers
- name: Deploy GenewebPy
  hosts: production
  tasks:
    - name: Pull latest code
      git:
        repo: https://github.com/Lob-Corp/Legacy.git
        dest: /opt/genewebpy
    
    - name: Build Docker image
      docker_image:
        name: genewebpy
        source: build
    
    - name: Start service
      docker_compose:
        project_src: /opt/genewebpy
        state: present
```

**Alternatives Considered**:
- **Chef/Puppet**: More complex, require agents
- **Terraform**: Better for infrastructure, not application deployment
- **Shell Scripts**: Error-prone, not idempotent

## Testing Framework

### Test Organization

**Choice**: Hierarchical test structure with pytest

**Test Types**:

1. **Unit Tests** (`tests/test_*.py`)
   - Fast, isolated
   - Mock external dependencies
   - Test individual functions/classes

2. **Integration Tests** (`tests/repositories/`, `tests/database/`)
   - Test component interactions
   - Use real SQLite (in-memory)
   - Verify data flow

3. **Roundtrip Tests** (`tests/gwc_database_roundtrip/`)
   - Parse .gw → Database → Verify
   - Field-by-field validation
   - Critical for data integrity

4. **Golden Master Tests** (`tests/golden_master/`)
   - Compare with OCaml behavior
   - HTML snapshot comparison
   - Ensure compatibility

**Why This Structure?**
- Clear separation of concerns
- Easy to run specific test types
- Matches testing pyramid (many unit, fewer integration)
- Fast feedback loop

See [TESTING_POLICY.md](TESTING_POLICY.md) for complete details.

### Coverage: pytest-cov

**Choice**: pytest-cov for code coverage analysis

**Why pytest-cov?**

✅ **Advantages**:
- **Integration**: Works seamlessly with pytest
- **Multiple Formats**: HTML, XML, terminal output
- **Branch Coverage**: Not just lines, but branches
- **CI/CD Ready**: Easy to integrate with GitHub Actions

**Usage**:
```bash
# Generate coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Enforce minimum coverage
pytest --cov=src --cov-fail-under=80
```

**Coverage Requirements**:
- Overall: 80% minimum
- Core libraries: 90% minimum
- Parsers: 85% minimum

---

## Architecture Decisions

### Repository Pattern

**Choice**: Repository pattern for data access

**Why Repository Pattern?**

✅ **Advantages**:
- **Separation of Concerns**: Business logic separate from data access
- **Testability**: Easy to mock repositories
- **Flexibility**: Can swap database implementation
- **Clear API**: Well-defined interface for data operations

**Structure**:
```
repositories/
├── person_repository.py      # Person CRUD operations
├── family_repository.py      # Family CRUD operations
├── converter_to_db.py        # App types → Database models
└── converter_from_db.py      # Database models → App types
```

**Example**:
```python
class PersonRepository:
    """Handles all person-related database operations"""
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """Retrieve person by ID"""
        ...
    
    def save_person(self, person: Person) -> int:
        """Save person to database"""
        ...
```

**Alternatives Considered**:
- **Active Record**: Couples model with database (Django ORM style)
- **Direct ORM Access**: Spreads data access logic throughout code
- **DAO Pattern**: Similar to repositories but more Java-centric

### Dataclasses for Domain Models

**Choice**: Python dataclasses for application types

**Why Dataclasses?**

✅ **Advantages**:
- **Immutability**: Can use `frozen=True` to emulate OCaml records
- **Type Safety**: Full type hint support
- **Automatic Methods**: `__init__`, `__repr__`, `__eq__` generated
- **Pattern Matching**: Works with Python 3.10+ pattern matching
- **Zero Runtime Cost**: Pure Python, no magic

**Example**:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Person:
    """Immutable person representation"""
    first_name: str
    surname: str
    sex: Sex
    occ: int = 0
    birth_date: Optional[Date] = None
    death_date: Optional[Date] = None
```

**OCaml Equivalence**:
```ocaml
(* OCaml record *)
type person = {
  first_name : string;
  surname : string;
  sex : sex;
  occ : int;
  birth_date : date option;
  death_date : date option;
}
```

**Alternatives Considered**:
- **attrs**: More features but external dependency
- **Pydantic**: Focused on validation, runtime overhead
- **namedtuple**: Less flexible, older style
- **Regular classes**: More boilerplate, no immutability

### Parser Design: Lexer + Parser

**Choice**: Two-stage parsing (tokenization → parsing)

**Why Two-Stage?**

✅ **Advantages**:
- **Clear Separation**: Lexical analysis separate from syntax analysis
- **Easier Testing**: Can test tokenizer and parser independently
- **Better Errors**: More precise error reporting
- **Matches OCaml**: Similar structure to original implementation

**Pipeline**:
```
.gw file text
      ↓
Tokenizer (stream.py)
      ↓
Token stream
      ↓
Parser (parser.py, block_parser.py, person_parser.py)
      ↓
Application types (Person, Family)
      ↓
Converter (converter_to_db.py)
      ↓
Database models
      ↓
SQLite database
```

**Alternatives Considered**:
- **Parser Combinator**: More functional but complex
- **Generated Parser** (PLY, ANTLR): Overkill for our simple format
- **Regex-Based**: Too fragile for complex syntax

---

## Future Considerations

### Potential Improvements

#### Database Scaling

For very large installations (> 100,000 persons):
- **PostgreSQL**: Better concurrent access
- **Read Replicas**: Distribute read load
- **Sharding**: Split by family branches
- **Timeline**: Only if needed (most genealogy databases < 10,000 persons)

#### Load Balancing

For high-traffic installations with multiple users:
- **nginx**: Reverse proxy and load balancer
  - Distribute requests across multiple Flask instances
  - SSL/TLS termination
  - Static file serving (offload from Flask)
  - Rate limiting and caching
- **Use Case**: Public genealogy websites with hundreds of concurrent users
- **Setup**: nginx → multiple Gunicorn workers → Flask app

#### Security Enhancements

For multi-user installations:
- **Authentication**: OAuth2, SAML
- **Authorization**: Role-based access control
- **Encryption**: At-rest and in-transit

---

## Technology Decision Template

When considering new technologies:

1. **Does it solve a real problem?** (Not just "cool tech")
2. **Does it fit our architecture?** (Consistent with existing choices)
3. **Is it mature and maintained?** (Active community, regular updates)
4. **Can the team learn it?** (Reasonable learning curve)
5. **What's the complexity cost?** (Simplicity is a feature)
6. **What are alternatives?** (Due diligence on options)
7. **Is it reversible?** (Can we change our mind later?)

---

## Summary

### Core Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Language** | Python 3.12 | Readability, ecosystem, maintainability |
| **Web Framework** | Flask 3.x | Simplicity, flexibility, well-documented |
| **Database** | SQLite 3 | Zero-config, reliable, file-based |
| **ORM** | SQLAlchemy 2.x | Powerful, mature, handles complex relationships |
| **Testing** | Pytest | Simple, powerful, industry standard |
| **Type Checking** | MyPy | Early error detection, documentation |
| **Containerization** | Docker | Portability, consistency, easy deployment |
| **Automation** | Ansible | Agentless, declarative, idempotent |
| **Version Control** | Git + GitHub | Industry standard, great workflow |

### Design Philosophy

- **Simplicity over complexity**
- **Standards over custom solutions**
- **Proven over bleeding-edge**
- **Python over language-specific features**
- **Community over isolation**

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-31 | Team | Initial technology documentation |

---

## Further Reading

### Internal Documentation
- [DATABASE.md](DATABASE.md) - Database architecture details
- [GWC_IMPLEMENTATION.md](GWC_IMPLEMENTATION.md) - Parser implementation
- [TESTING_POLICY.md](TESTING_POLICY.md) - Testing approach
- [OCAML_TO_PYTHON.md](OCAML_TO_PYTHON.md) - Translation patterns

### External Resources
- [Python Documentation](https://docs.python.org/3.12/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)

---

**Questions about technology choices?** Open an issue on GitHub for discussion!
