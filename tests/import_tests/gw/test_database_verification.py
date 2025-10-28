"""Parametric pytest tests to verify database integrity.

This test module validates that a database file contains all expected data
and that all relationships are correctly maintained.
"""

import pytest
from pathlib import Path

from database.sqlite_database_service import SQLiteDatabaseService
from repositories.person_repository import PersonRepository
from repositories.family_repository import FamilyRepository

import database.couple  # noqa: F401
import database.ascends  # noqa: F401
import database.unions  # noqa: F401
import database.union_families  # noqa: F401
import database.descends  # noqa: F401
import database.descend_children  # noqa: F401
import database.family  # noqa: F401
import database.person  # noqa: F401
import database.relation  # noqa: F401
import database.titles  # noqa: F401
import database.family_events  # noqa: F401
import database.person_events  # noqa: F401
import database.person_titles  # noqa: F401
import database.person_non_native_relations  # noqa: F401
import database.date  # noqa: F401
import database.place  # noqa: F401


@pytest.fixture
def database_service(request):
    """Fixture to provide a database service for a given database file.

    Usage:
        @pytest.mark.parametrize("database_service",
        ["test_minimal.db", "test_medium.db", "test_big.db"],
                                 indirect=True)
    """
    db_path = request.param

    if not Path(db_path).exists():
        pytest.skip(f"Database file '{db_path}' not found")

    db_service = SQLiteDatabaseService(db_path)
    db_service.connect()

    yield db_service


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_can_retrieve_all_persons(database_service):
    """Test that all persons can be retrieved from the database."""
    person_repo = PersonRepository(database_service)

    all_persons = person_repo.get_all_persons()

    assert isinstance(all_persons, list)
    assert len(all_persons) >= 0

    for person in all_persons:
        assert hasattr(person, 'index')
        assert hasattr(person, 'first_name')
        assert hasattr(person, 'surname')
        assert hasattr(person, 'sex')
        assert hasattr(person, 'families')
        assert hasattr(person, 'ascend')


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_can_retrieve_all_families(database_service):
    """Test that all families can be retrieved from the database."""
    family_repo = FamilyRepository(database_service)

    all_families = family_repo.get_all_families()

    assert isinstance(all_families, list)
    assert len(all_families) >= 0

    for family in all_families:
        assert hasattr(family, 'index')
        assert hasattr(family, 'parents')
        assert hasattr(family, 'children')
        assert hasattr(family, 'marriage_date')
        assert hasattr(family, 'relation_kind')
        assert hasattr(family, 'divorce_status')


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_family_parents_exist(database_service):
    """Test that all family parents reference existing persons."""
    person_repo = PersonRepository(database_service)
    family_repo = FamilyRepository(database_service)

    all_persons = person_repo.get_all_persons()
    all_families = family_repo.get_all_families()

    person_ids = {p.index for p in all_persons}

    for family in all_families:
        for parent_id in family.parents.parents:
            assert parent_id in person_ids, (
                f"Family #{family.index} references non-existent "
                f"parent #{parent_id}"
            )


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_family_children_exist(database_service):
    """Test that all family children reference existing persons."""
    person_repo = PersonRepository(database_service)
    family_repo = FamilyRepository(database_service)

    all_persons = person_repo.get_all_persons()
    all_families = family_repo.get_all_families()

    person_ids = {p.index for p in all_persons}

    for family in all_families:
        for child_id in family.children:
            assert child_id in person_ids, (
                f"Family #{family.index} references non-existent "
                f"child #{child_id}"
            )


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_person_families_exist(database_service):
    """Test that all person families reference existing families."""
    person_repo = PersonRepository(database_service)
    family_repo = FamilyRepository(database_service)

    all_persons = person_repo.get_all_persons()
    all_families = family_repo.get_all_families()

    family_ids = {f.index for f in all_families}

    for person in all_persons:
        for family_id in person.families:
            assert family_id in family_ids, (
                f"Person #{person.index} references non-existent "
                f"family #{family_id}"
            )


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_person_parents_exist(database_service):
    """Test that all person parents reference existing families."""
    person_repo = PersonRepository(database_service)
    family_repo = FamilyRepository(database_service)

    all_persons = person_repo.get_all_persons()
    all_families = family_repo.get_all_families()

    family_ids = {f.index for f in all_families}

    for person in all_persons:
        if person.ascend.parents is not None:
            assert person.ascend.parents in family_ids, (
                f"Person #{person.index} has parents from "
                f"non-existent family #{person.ascend.parents}"
            )


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_bidirectional_parent_child_links(database_service):
    """Test that parent-child relationships are bidirectional.

    If a person is listed as a child in a family, that family should be
    listed in the person's ascend.parents.
    """
    person_repo = PersonRepository(database_service)
    family_repo = FamilyRepository(database_service)

    all_persons = person_repo.get_all_persons()
    all_families = family_repo.get_all_families()

    persons_by_id = {p.index: p for p in all_persons}

    for family in all_families:
        for child_id in family.children:
            child = persons_by_id.get(child_id)
            if child:
                assert child.ascend.parents == family.index, (
                    f"Child #{child_id} in family #{family.index} "
                    f"doesn't have parents link back to this family "
                    f"(has: {child.ascend.parents})"
                )


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_bidirectional_family_person_links(database_service):
    """Test that family memberships are bidirectional.

    If a person lists a family in their families list, they should appear
    as a parent in that family.
    """
    person_repo = PersonRepository(database_service)
    family_repo = FamilyRepository(database_service)

    all_persons = person_repo.get_all_persons()
    all_families = family_repo.get_all_families()

    families_by_id = {f.index: f for f in all_families}

    for person in all_persons:
        for family_id in person.families:
            family = families_by_id.get(family_id)
            if family:
                assert person.index in family.parents.parents, (
                    f"Person #{person.index} lists family #{family_id} "
                    f"in their families, but family doesn't list them "
                    f"as a parent (has: {family.parents.parents})"
                )


@pytest.mark.parametrize("database_service",
                         ["test_minimal.db", "test_medium.db", "test_big.db"],
                         indirect=True)
def test_database_statistics(database_service):
    """Print database statistics (informational test)."""
    person_repo = PersonRepository(database_service)
    family_repo = FamilyRepository(database_service)

    all_persons = person_repo.get_all_persons()
    all_families = family_repo.get_all_families()

    print(f"\n{'=' * 70}")
    print("DATABASE STATISTICS")
    print('=' * 70)
    print(f"Total Persons: {len(all_persons)}")
    print(f"Total Families: {len(all_families)}")

    from collections import Counter
    sex_counts = Counter(p.sex.name if hasattr(p.sex, 'name')
                         else str(p.sex) for p in all_persons)
    print("\nPersons by sex:")
    for sex, count in sex_counts.items():
        print(f"  {sex}: {count}")

    relation_counts = Counter(
        f.relation_kind.name if hasattr(f.relation_kind, 'name')
        else str(f.relation_kind) for f in all_families
    )
    print("\nFamilies by relation kind:")
    for relation, count in relation_counts.items():
        print(f"  {relation}: {count}")

    with_children = sum(1 for f in all_families if f.children)
    without_children = len(all_families) - with_children
    print(f"\nFamilies with children: {with_children}")
    print(f"Families without children: {without_children}")

    print('=' * 70)

    assert True
