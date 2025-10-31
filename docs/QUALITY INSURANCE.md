# Quality insurance

This document covers the actions taken to ensure that quality is maintained in the project.

## Merging rules

The `main` branch is **protected** and **requires** a Pull Request from either a `milestone/*` or `hotfix/*` branch to be updated. Likewise `milestone/*` branches are also protected and **requires** a Pull request  to be updated.

### Branch naming convention

- Hotfixes branches should be named `hotfix/*` with `*` being replaced by a short description of the hotfix consisting of 6 words or less. They describe a quick fix on an important bug that is already present in the main branch.
- Milestones branches should be named `milestone/*` with `*` being replaced by a short description of the milestone consisting of 3 words or less. They describe a group of thematically linked features/fixes/refactors.
- Others branches besides main and those two pattern should be attached to a milestone. As such, their naming pattern is as follows: `<branch type>/<milestone-name>/*`.
    - `branch-type` indicates whether the branch corresponds to a new feature (`feature/*`), a bug fix (`fix/*`) a refactor (`refactor/*`) or something else.
    - `milestone-name` correspond to the milestone the branch is attached to.
    - `*` should be a short description of the branch consisting of 6 words or less.

**Note**: an exception can be made in the case of documentation that **doesn't** involve modifying the code base **and** isn't linked to particular milestone, those branches should be named `docs/global/*`with `*` being replaced by a short description of the hotfix consisting of 4 words or less.

**Naming exemples**:
If we create a milestone named *web-server*.
- Milestone branch:
  - `milestone/web-server`

- Feature branches for this milestone:
  - `feature/web-server/add-request-logging`
  - `feature/web-server/support-https`

- Bug fix branches for this milestone:
  - `fix/web-server/fix-500-error-on-timeout`

- Refactor branches for this milestone:
  - `refactor/web-server/improve-routing-logic`

- Chore branches for this milestone:
  - `chore/web-server/update-readme`

- Hotfix branches (can bypass milestones and go directly into `main`):
  - `hotfix/rollback-broken-migration`

### Status checks

In order to merge a branch to main or a milestone, status checks must pass. Those are:
- **Allowed to merge**: only milestone, hotfixes and global documentation branches should be able to merge into main. This pass by default if the target branch is a milestone.
- **Lint check**: Python code should be PEP8 compliant. This is ignored if the branch to be merged is a milestone as milestone code should already be PEP8 compliant.
- **Static type check**: Python code should be MyPy compliant. This is ignored if the branch to be merged is a milestone as milestone code should already be well typed.
- **Unit and integration wide tests**: ran everywhere
- **Project wide tests**: those concerns E2E, Golden Master and tests that compare/test the whole program. As those are heavy, they are ran only on milestones and hotfixes branches.
- **Coverage threshold**: A miminum of 80% of coverage should be attained through tests to pass, ran everywhere

### Merge flow summary

```
main (protected)
  🡑
  ├── hotfix/* (all status checks required)
  └── milestone/*: (protected, status checks required*)
        🡑
        ├── feature/<milestone-name>/*      │
        ├── refactor/<milestone-name>/*     ├── (status checks required*)
        ├── fix/<milestone-name>/*          │
        └── etc.                            │
```
*: [See Status checks](#status-checks)

### Manual testing

When creating a pull request, when the changes may affect the user flow, the developper assigned to the task should perform manual testing of the workflow, to ensure the user flow remains as wanted.

## Issue Organization

### GitHub Project Board

All issues must be tracked and organized using the GitHub Project board with the following status categories:

| Status | Description | When to Use |
|--------|-------------|-------------|
| **Todo** | Issues ready to be worked on | New issues that have been triaged and approved |
| **Paused** | Work temporarily suspended | Blocked by dependencies, awaiting decisions, or deprioritized |
| **In Progress** | Actively being worked on | Developer has started implementation |
| **In Review** | Pull request submitted | Code is complete and awaiting review |
| **Completed** | Work finished and merged | PR merged to target branch |

### Issue Lifecycle

1. **Creation**: New issue created and added to **Todo**
2. **Assignment**: Developer picks up issue and moves to **In Progress**
3. **Development**: Work continues in **In Progress**
4. **Pull Request**: PR created, issue moves to **In Review**
5. **Merge**: PR merged, issue moves to **Completed**

Issues can be moved to **Paused** at any stage if work is blocked or suspended.

### Pull Request Requirements

**Every Pull Request must be linked to an issue**, except in the following cases:

**Exceptions** (PRs allowed without linked issue):
- **Minimal additions**: Typo fixes, documentation updates, comment improvements
- **Milestone branch updates from main**: PRs to update milestone branches from main
- **Hotfixes**: Critical bug fixes that require immediate attention (though an issue should be created retroactively for tracking)

**Linking a PR to an Issue**:
- Use GitHub keywords in PR description: `Closes #123`, `Fixes #456`, `Resolves #789`
- This automatically moves the issue to **Completed** when PR is merged
- Multiple issues can be linked: `Closes #123, Fixes #456`

### Issue Best Practices

- **Clear Titles**: Use descriptive titles that explain the issue at a glance
- **Detailed Descriptions**: Include context, steps to reproduce (for bugs), or requirements (for features)
- **Labels**: Use appropriate labels (bug, feature, documentation, enhancement, etc.)
- **Milestones**: Assign issues to milestones when applicable
- **Assignees**: Assign the person responsible for the work
- **References**: Link related issues or PRs using `#issue-number`

**Example Issue-PR Workflow**:
```
1. Issue #42 created: "Add support for HTTPS in web server"
   → Status: Todo

2. Developer assigned, starts work
   → Status: In Progress
   → Branch: feature/web-server/support-https

3. PR #45 opened with description: "Closes #42"
   → Status: In Review

4. PR merged to milestone/web-server
   → Status: Completed (automatic)
   → Issue #42 closed automatically
```

## Testing Policy

GenewebPy follows a comprehensive testing policy to ensure code quality, reliability, and behavioral compatibility with the original OCaml implementation.

**For complete testing guidelines, requirements, and best practices, see [Testing Policy](TESTING_POLICY.md).**

### Summary

- **Minimum Coverage**: 80% overall, enforced by CI/CD
- **Test Types**: Unit, Integration, Parser, Roundtrip, Golden Master, E2E
- **Test Organization**: Mirrored directory structure under `tests/`
- **Standards**: Pytest framework, AAA pattern, descriptive naming
- **CI/CD Integration**: Automated testing on all branches with status checks

### Quick Reference

**Unit Testing**:
- Each function tested for valid cases and edge cases
- Fast execution (< 1ms per test)
- No external dependencies
- Located in `tests/test_*.py`

**Integration Testing**:
- Component interaction and data flow
- Repository and database operations
- Located in `tests/<component>/`

**Roundtrip Testing**:
- End-to-end data integrity verification
- Parse .gw files → store in database → verify all fields
- Located in `tests/gwc_database_roundtrip/`
- Test files: `minimal.gw`, `medium.gw`, `big.gw`

**Golden Master Testing**:
- Behavioral compatibility with OCaml Geneweb
- HTML snapshot comparison
- For more information see [Golden Master](tests/GOLDEN_MASTER.md)

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test type
pytest tests/gwc_database_roundtrip/

# In Docker
./docker-manage.sh test
```

See [Testing Policy](TESTING_POLICY.md) for detailed guidelines, standards, and best practices.

---

## Code Quality Principles

To maintain high code quality and ensure maintainability, all contributors should follow these core software engineering principles:

### DRY (Don't Repeat Yourself)

**Principle**: Avoid code duplication by extracting common logic into reusable functions, classes, or modules.

**Benefits**:
- Easier maintenance (fix bugs once, not multiple times)
- Reduced risk of inconsistencies
- Smaller codebase

**Example**:
```python
# ❌ Bad: Duplicated logic
def save_person_to_db(person):
    if not person.name:
        raise ValueError("Name required")
    db.save(person)

def save_family_to_db(family):
    if not family.id:
        raise ValueError("ID required")
    db.save(family)

# ✅ Good: Extracted common logic
def validate_and_save(entity, required_field):
    if not getattr(entity, required_field):
        raise ValueError(f"{required_field} required")
    db.save(entity)
```

---

### SOLID Principles

#### S - Single Responsibility Principle
Each class or function should have one, and only one, reason to change.

#### O - Open/Closed Principle
Software entities should be open for extension but closed for modification.

#### L - Liskov Substitution Principle
Subtypes must be substitutable for their base types.

#### I - Interface Segregation Principle
Clients should not be forced to depend on interfaces they don't use.

#### D - Dependency Inversion Principle
Depend on abstractions, not concretions. Use dependency injection.

---

### DAMP (Descriptive And Meaningful Phrases)

**Principle**: In tests, prioritize readability over strict DRY. Tests should be clear and self-documenting.

**Guidelines**:
- Use descriptive test names that explain what is being tested
- Prefer explicit setup over shared fixtures when it improves clarity
- Duplicate setup code in tests if it makes them easier to understand
- Follow AAA pattern (Arrange, Act, Assert)

**Example**:
```python
# ✅ Good: Clear, self-documenting test
def test_person_with_birth_date_calculates_age_correctly():
    # Arrange
    birth_date = Date(year=1990, month=1, day=1)
    person = Person(name="John", birth_date=birth_date)
    
    # Act
    age = person.calculate_age(reference_date=Date(2025, 1, 1))
    
    # Assert
    assert age == 35
```

---

### TDD (Test-Driven Development)

**Principle**: Write tests before implementing functionality.

**TDD Cycle (Red-Green-Refactor)**:
1. **Red**: Write a failing test for the desired functionality
2. **Green**: Write the minimum code to make the test pass
3. **Refactor**: Improve the code while keeping tests passing

**Benefits**:
- Better test coverage by design
- Clearer requirements and interface design
- Reduced debugging time
- More modular, testable code

**When to use TDD**:
- ✅ New features with clear requirements
- ✅ Bug fixes (write test that reproduces bug, then fix)
- ✅ Refactoring (tests ensure behavior preserved)
- ⚠️ Exploratory/prototype code (can add tests after direction is clear)

**Example workflow**:
```bash
# 1. Write failing test
def test_parse_date_with_about_precision():
    result = parse_date("~1950")
    assert result.precision == About()  # ❌ FAILS

# 2. Implement minimal code
def parse_date(date_str: str):
    if date_str.startswith("~"):
        return Date(year=int(date_str[1:]), precision=About())
    # ... ✅ PASSES

# 3. Refactor and add more cases
# Add edge cases, improve implementation
```

---

### Applying These Principles in GenewebPy

- **Parser modules**: Each parser (date, person, family) has a single responsibility (SRP)
- **Repository pattern**: Database operations abstracted behind interfaces (DIP)
- **Converter modules**: Separate concerns of parsing vs. database operations (SRP)
- **Test organization**: Unit, integration, and E2E tests follow DAMP with descriptive names
- **Type hints**: Enforced via MyPy for better maintainability and catching errors early

