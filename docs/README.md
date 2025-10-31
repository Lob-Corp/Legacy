# Documentation Index

This directory contains comprehensive documentation for the Legacy/GeneWeb project.

## Main Documentation

### 📘 [GWC_IMPLEMENTATION.md](./GWC_IMPLEMENTATION.md) - **START HERE**

**The complete guide to the Python GWC implementation.** This is the main reference document covering:

- Architecture and processing pipeline
- Command-line options (implemented, partial, and planned)
- Parser implementation and fixes
- Dummy person system (OCaml-compatible)
- Converter API reference with code examples
- Usage examples and best practices
- Differences from OCaml version
- Implementation status and roadmap
- Troubleshooting and known issues

**Topics covered**:
- How to use `gwc.py` from command line
- How to use `GwConverter` API programmatically
- Understanding person resolution and dummy handling
- Parser fixes for inline parent definitions
- Type mapping and data enrichment
- Statistics and error handling


## Other Documentation

### �️ [DATABASE.md](./DATABASE.md)
Complete database architecture documentation covering models, relationships, and usage.

**Topics**:
- Database overview and technology stack (SQLAlchemy + SQLite)
- SQLiteDatabaseService API reference
- All 23 data models explained (Person, Family, Events, Titles, etc.)
- Relationship types and cascade behaviors
- All enumerations (Sex, Calendar, EventTypes, etc.)
- Usage examples and best practices
- Complete SQL schema reference
- Troubleshooting and common issues

### 🚀 [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)
**User-friendly guide for migrating your family tree from OCaml Geneweb to GenewebPy.**

**Topics**:
- Understanding what GenewebPy is and why migrate
- Before you start (checking your data, making backups)
- Step-by-step migration (Docker and manual options)
- Verifying your data migrated correctly
- What's different in GenewebPy
- Common issues and troubleshooting
- FAQ for genealogy users

### �🔄 [OCAML_TO_PYTHON.md](./OCAML_TO_PYTHON.md)
Complete reference for OCaml-to-Python translation differences across the entire codebase.

**Topics**:
- Language-level differences (memory, immutability, pattern matching)
- Type system differences (ADTs, variants, records, generics)
- Module-by-module comparison
- Data structure differences (hash tables, arrays, file I/O)
- Algorithm differences (name matching, consanguinity, indexing)
- File format differences (.gw, .gwo, .gwb vs SQLite)
- Questions and clarifications needed for port
- Implementation checklist

### 🧪 [TESTING_POLICY.md](./TESTING_POLICY.md)
**Comprehensive testing guidelines, requirements, and best practices.**

**Topics**:
- Testing philosophy and principles
- Test types: Unit, Integration, Roundtrip, Golden Master, E2E
- Coverage requirements (80% minimum)
- Testing standards and conventions
- Test organization and structure
- Writing effective tests (DO's and DON'Ts)
- Running tests locally and in CI/CD
- Test review process
- Troubleshooting and maintenance

### 📝 [Test Documentation](./tests/)
**Detailed inventory of all tests in the project, organized by category.**

**Files**:
- **[Unit Tests](./tests/UNIT.md)** - tests for individual components
- **[Integration Tests](./tests/INTEGRATION.md)** - tests for component interactions
- **[E2E Tests](./tests/E2E.md)** - tests for complete workflows
- **[Test README](./tests/README.md)** - Overview, statistics, and quick reference

**Coverage**:
- Complete test inventory by file and function
- Test organization and naming conventions
- Running instructions for each category
- Guidelines for adding new tests

### 🧪 [tests/GOLDEN_MASTER.md](./tests/GOLDEN_MASTER.md)
Testing approach and scenarios for ensuring behavioral compatibility with the legacy application.

**Topics**:
- Golden master testing methodology
- Test scenarios for web interface
- Recording and comparison process
- How to run golden master tests

### 🔒 [QUALITY_INSURANCE.md](./QUALITY_INSURANCE.md)
Quality assurance processes and standards for the project.

**Topics**:
- Branch naming conventions
- Merging rules and PR requirements
- Protected branches and status checks
- Code review process
- Issue organization on GitHub Project
- Testing policy summary (see TESTING_POLICY.md for details)

### ⚙️ [TECHNOLOGIES.md](./TECHNOLOGIES.md)
**Comprehensive guide to technologies used in GenewebPy and rationale for each choice.**

**Topics**:
- Core technologies (Python, Flask, SQLite, SQLAlchemy)
- Development tools (MyPy, Pytest)
- Infrastructure & deployment (Docker, Ansible, Systemd)
- Testing framework and organization
- Architecture decisions (Repository pattern, Dataclasses, Parser design)
- Alternatives considered for each technology
- Future considerations and potential improvements

### ♿ [ACCESSIBILITY.md](./ACCESSIBILITY.md)
**Guidelines for making GenewebPy accessible to all users, including those with disabilities.**

**Topics**:
- Accessibility principles (semantic HTML, keyboard navigation, ARIA)
- Color contrast and visual requirements
- Implementation guidelines and templates
- Testing for accessibility (automated and manual)
- Common issues and solutions
- Tools and resources

---

## Quick Navigation

### I want to...

**...understand the database architecture**
→ Read [DATABASE.md](./DATABASE.md)

**...use the database service**
→ Read [DATABASE.md § Database Service](./DATABASE.md#database-service)

**...understand data models and relationships**
→ Read [DATABASE.md § Data Models](./DATABASE.md#data-models) and [§ Relationships](./DATABASE.md#relationships)

**...see database usage examples**
→ Read [DATABASE.md § Usage Examples](./DATABASE.md#usage-examples)

**...understand how gwc works**
→ Read [GWC_IMPLEMENTATION.md § Overview](./GWC_IMPLEMENTATION.md#overview)

**...use gwc from command line**
→ Read [GWC_IMPLEMENTATION.md § Command-Line Options](./GWC_IMPLEMENTATION.md#command-line-options) and [§ Usage Examples](./GWC_IMPLEMENTATION.md#usage-examples)

**...understand testing requirements and best practices**
→ Read [TESTING_POLICY.md](./TESTING_POLICY.md)

**...write tests for my code**
→ Read [TESTING_POLICY.md § Writing Tests](./TESTING_POLICY.md#writing-tests) and [§ Testing Standards](./TESTING_POLICY.md#testing-standards)

**...run tests locally or in CI/CD**
→ Read [TESTING_POLICY.md § Running Tests](./TESTING_POLICY.md#running-tests)

**...understand coverage requirements**
→ Read [TESTING_POLICY.md § Coverage Requirements](./TESTING_POLICY.md#coverage-requirements)

**...see a complete list of all tests**
→ Read [Test Documentation](./tests/) - [Unit](./tests/UNIT.md), [Integration](./tests/INTEGRATION.md), [E2E](./tests/E2E.md)

**...find specific tests for a component**
→ Search in [Unit Tests](./tests/UNIT.md), [Integration Tests](./tests/INTEGRATION.md), or [E2E Tests](./tests/E2E.md)

**...understand test organization**
→ Read [Test README](./tests/README.md)

**...migrate my family tree from OCaml Geneweb to GenewebPy**
→ Read [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)

**...export my Geneweb database**
→ Read [MIGRATION_GUIDE.md § Step-by-Step Migration](./MIGRATION_GUIDE.md#step-by-step-migration)

**...verify my data migrated correctly**
→ Read [MIGRATION_GUIDE.md § Verifying Your Data](./MIGRATION_GUIDE.md#verifying-your-data)

**...understand OCaml-to-Python differences**
→ Read [OCAML_TO_PYTHON.md](./OCAML_TO_PYTHON.md)

**...run tests**
→ Read [tests/GOLDEN_MASTER.md](./tests/GOLDEN_MASTER.md)

**...understand the development workflow**
→ Read [QUALITY_INSURANCE.md](./QUALITY_INSURANCE.md)

**...understand why specific technologies were chosen**
→ Read [TECHNOLOGIES.md](./TECHNOLOGIES.md)

**...know what tools and frameworks are used**
→ Read [TECHNOLOGIES.md § Core Technologies](./TECHNOLOGIES.md#core-technologies)

**...understand architecture decisions**
→ Read [TECHNOLOGIES.md § Architecture Decisions](./TECHNOLOGIES.md#architecture-decisions)

**...make the application accessible to all users**
→ Read [ACCESSIBILITY.md](./ACCESSIBILITY.md)

**...test accessibility compliance**
→ Read [ACCESSIBILITY.md § Testing for Accessibility](./ACCESSIBILITY.md#testing-for-accessibility)

**...fix accessibility issues**
→ Read [ACCESSIBILITY.md § Common Issues and Solutions](./ACCESSIBILITY.md#common-issues-and-solutions)

## Contributing to Documentation

When updating documentation:

1. **Always update GWC_IMPLEMENTATION.md first** - it's the single source of truth
2. **Add changelog entries** at the bottom of GWC_IMPLEMENTATION.md
3. **Keep examples up to date** with actual working code
4. **Test code snippets** before adding them to docs
5. **Update this index** when adding new doc files

### Documentation Style Guide

- Use clear, concise language
- Include working code examples
- Provide both CLI and API examples where applicable
- Link between related sections
- Keep table of contents updated
