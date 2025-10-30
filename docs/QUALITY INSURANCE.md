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
- For more information see [Golden Master](GOLDEN_MASTER.md)

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
