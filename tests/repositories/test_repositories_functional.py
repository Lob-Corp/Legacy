"""Functional tests for Person and Family repositories.

Tests the complete workflow of creating persons and families, including
person-family bidirectional links and edge cases.
"""
import tempfile
import os
import pytest

import libraries.person as app_person
import libraries.family as app_family
import libraries.date as app_date
import libraries.death_info as death_info
import libraries.burial_info as burial_info
import libraries.title as title
import libraries.consanguinity_rate as consanguinity_rate
import database.person as db_person

# Import all database models to register them with SQLAlchemy
import database.couple  # noqa: F401
import database.ascends  # noqa: F401
import database.unions  # noqa: F401
import database.descends  # noqa: F401
import database.family as db_family  # noqa: F401
import database.relation as db_relation  # noqa: F401
import database.titles  # noqa: F401
import database.family_events  # noqa: F401
import database.person_events  # noqa: F401
import database.person_titles  # noqa: F401
import database.person_non_native_relations  # noqa: F401
import database.date  # noqa: F401
import database.place  # noqa: F401

from database.sqlite_database_service import SQLiteDatabaseService
from repositories.person_repository import PersonRepository
from repositories.family_repository import FamilyRepository


def _create_default_date() -> app_date.CompressedDate:
    """Helper to create a default date for testing."""
    return app_date.CalendarDate(
        dmy=app_date.DateValue(
            day=1, month=1, year=2000,
            prec=app_date.Sure(), delta=0
        ),
        cal=app_date.Calendar.GREGORIAN
    )


def test_create_couple_and_family() -> None:
    """Test creating a couple and their family."""
    # Create temporary database
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        # Initialize database service
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()

        # Initialize repositories
        person_repo = PersonRepository(db_service)
        family_repo = FamilyRepository(db_service)

        # Create first person (father)
        birth_date_father: app_date.CompressedDate = app_date.CalendarDate(
            dmy=app_date.DateValue(
                day=15, month=3, year=1980,
                prec=app_date.Sure(), delta=0
            ),
            cal=app_date.Calendar.GREGORIAN
        )

        father: app_person.Person[int, int, str, int] = (
            app_person.Person(
                index=1,
                first_name="John",
                surname="Doe",
                occ=0,
                image="",
                public_name="",
                qualifiers=[],
                aliases=[],
                first_names_aliases=[],
                surname_aliases=[],
                titles=[],
                non_native_parents_relation=[],
                related_persons=[],
                occupation="Engineer",
                sex=db_person.Sex.MALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=birth_date_father,
                birth_place="New York",
                birth_note="",
                birth_src="",
                baptism_date=None,
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=death_info.NotDead(),
                death_place="",
                death_note="",
                death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="",
                burial_note="",
                burial_src="",
                personal_events=[],
                notes="",
                src="",
                ascend=app_family.Ascendants(
                    parents=None,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
        )

        # Create second person (mother)
        birth_date_mother: app_date.CompressedDate = app_date.CalendarDate(
            dmy=app_date.DateValue(
                day=20, month=6, year=1982,
                prec=app_date.Sure(), delta=0
            ),
            cal=app_date.Calendar.GREGORIAN
        )

        mother: app_person.Person[int, int, str, int] = (
            app_person.Person(
                index=2,
                first_name="Jane",
                surname="Smith",
                occ=0,
                image="",
                public_name="",
                qualifiers=[],
                aliases=[],
                first_names_aliases=[],
                surname_aliases=[],
                titles=[],
                non_native_parents_relation=[],
                related_persons=[],
                occupation="Doctor",
                sex=db_person.Sex.FEMALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=birth_date_mother,
                birth_place="Boston",
                birth_note="",
                birth_src="",
                baptism_date=None,
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=death_info.NotDead(),
                death_place="",
                death_note="",
                death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="",
                burial_note="",
                burial_src="",
                personal_events=[],
                notes="",
                src="",
                ascend=app_family.Ascendants(
                    parents=None,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
        )

        # Add persons to database
        assert person_repo.add_person(father) is True
        assert person_repo.add_person(mother) is True

        # Verify persons were added
        retrieved_father = person_repo.get_person_by_id(1)
        assert retrieved_father.first_name == "John"
        assert retrieved_father.surname == "Doe"
        assert retrieved_father.occupation == "Engineer"
        assert retrieved_father.birth_place == "New York"

        retrieved_mother = person_repo.get_person_by_id(2)
        assert retrieved_mother.first_name == "Jane"
        assert retrieved_mother.surname == "Smith"
        assert retrieved_mother.occupation == "Doctor"
        assert retrieved_mother.birth_place == "Boston"

        # Create family for the couple
        marriage_date: app_date.CompressedDate = app_date.CalendarDate(
            dmy=app_date.DateValue(
                day=15, month=6, year=2005,
                prec=app_date.Sure(), delta=0
            ),
            cal=app_date.Calendar.GREGORIAN
        )

        family: app_family.Family[int, int, str] = app_family.Family(
            index=1,
            marriage_date=marriage_date,
            marriage_place="City Hall, New York",
            marriage_note="Beautiful ceremony",
            marriage_src="Marriage certificate",
            witnesses=[],
            relation_kind=app_family.MaritalStatus.MARRIED,
            divorce_status=app_family.NotDivorced(),
            family_events=[],
            comment="Happy couple",
            origin_file="",
            src="",
            parents=app_family.Parents([1, 2]),  # John and Jane
            children=[]
        )

        # Add family to database
        assert family_repo.add_family(family) is True

        # Verify family was added
        retrieved_family = family_repo.get_family_by_id(1)
        assert retrieved_family.marriage_place == "City Hall, New York"
        assert retrieved_family.marriage_note == "Beautiful ceremony"
        marital_status = retrieved_family.relation_kind
        assert marital_status == app_family.MaritalStatus.MARRIED
        assert retrieved_family.parents[0] == 1  # Father ID
        assert retrieved_family.parents[1] == 2  # Mother ID
        assert len(retrieved_family.children) == 0

        # Test get_all methods
        all_persons = person_repo.get_all_persons()
        assert len(all_persons) == 2

        all_families = family_repo.get_all_families()
        assert len(all_families) == 1

        print("✓ Successfully created couple and family")
        father_name = (f"{retrieved_father.first_name} "
                       f"{retrieved_father.surname}")
        print(f"✓ Father: {father_name}")
        mother_name = (f"{retrieved_mother.first_name} "
                       f"{retrieved_mother.surname}")
        print(f"✓ Mother: {mother_name}")
        print(f"✓ Marriage: {retrieved_family.marriage_place}")

    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_create_family_with_children() -> None:
    """Test creating a family with children."""
    # Create temporary database
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        # Initialize database service
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()

        # Initialize repositories
        person_repo = PersonRepository(db_service)
        family_repo = FamilyRepository(db_service)

        # Create parents
        father: app_person.Person[int, int, str, int] = (
            app_person.Person(
                index=1,
                first_name="Robert",
                surname="Johnson",
                occ=0,
                image="",
                public_name="Bob",
                qualifiers=[],
                aliases=["Bob"],
                first_names_aliases=[],
                surname_aliases=[],
                titles=[],
                non_native_parents_relation=[],
                related_persons=[],
                occupation="Teacher",
                sex=db_person.Sex.MALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_date=None,
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=death_info.NotDead(),
                death_place="",
                death_note="",
                death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="",
                burial_note="",
                burial_src="",
                personal_events=[],
                notes="",
                src="",
                ascend=app_family.Ascendants(
                    parents=None,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
        )

        mother: app_person.Person[int, int, str, int] = (
            app_person.Person(
                index=2,
                first_name="Mary",
                surname="Johnson",
                occ=0,
                image="",
                public_name="",
                qualifiers=[],
                aliases=[],
                first_names_aliases=[],
                surname_aliases=[],
                titles=[],
                non_native_parents_relation=[],
                related_persons=[],
                occupation="Nurse",
                sex=db_person.Sex.FEMALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_date=None,
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=death_info.NotDead(),
                death_place="",
                death_note="",
                death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="",
                burial_note="",
                burial_src="",
                personal_events=[],
                notes="",
                src="",
                ascend=app_family.Ascendants(
                    parents=None,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
        )

        # Create children
        child1: app_person.Person[int, int, str, int] = (
            app_person.Person(
                index=3,
                first_name="Alice",
                surname="Johnson",
                occ=0,
                image="",
                public_name="",
                qualifiers=[],
                aliases=[],
                first_names_aliases=[],
                surname_aliases=[],
                titles=[],
                non_native_parents_relation=[],
                related_persons=[],
                occupation="",
                sex=db_person.Sex.FEMALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_date=None,
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=death_info.NotDead(),
                death_place="",
                death_note="",
                death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="",
                burial_note="",
                burial_src="",
                personal_events=[],
                notes="",
                src="",
                ascend=app_family.Ascendants(
                    parents=1,  # Will be the family ID
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
        )

        child2: app_person.Person[int, int, str, int] = (
            app_person.Person(
                index=4,
                first_name="Charlie",
                surname="Johnson",
                occ=1,
                image="",
                public_name="",
                qualifiers=[],
                aliases=[],
                first_names_aliases=[],
                surname_aliases=[],
                titles=[],
                non_native_parents_relation=[],
                related_persons=[],
                occupation="",
                sex=db_person.Sex.MALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_date=None,
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=death_info.NotDead(),
                death_place="",
                death_note="",
                death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="",
                burial_note="",
                burial_src="",
                personal_events=[],
                notes="",
                src="",
                ascend=app_family.Ascendants(
                    parents=1,  # Will be the family ID
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
        )

        # Add all persons
        assert person_repo.add_person(father) is True
        assert person_repo.add_person(mother) is True
        assert person_repo.add_person(child1) is True
        assert person_repo.add_person(child2) is True

        # Create family with children
        marriage_date: app_date.CompressedDate = app_date.CalendarDate(
            dmy=app_date.DateValue(
                day=10, month=5, year=2000,
                prec=app_date.Sure(), delta=0
            ),
            cal=app_date.Calendar.GREGORIAN
        )

        family: app_family.Family[int, int, str] = app_family.Family(
            index=1,
            marriage_date=marriage_date,
            marriage_place="Church",
            marriage_note="",
            marriage_src="",
            witnesses=[],
            relation_kind=app_family.MaritalStatus.MARRIED,
            divorce_status=app_family.NotDivorced(),
            family_events=[],
            comment="Family with two children",
            origin_file="",
            src="",
            parents=app_family.Parents([1, 2]),
            children=[3, 4]  # Alice and Charlie
        )

        # Add family
        assert family_repo.add_family(family) is True

        # Verify family with children
        retrieved_family = family_repo.get_family_by_id(1)
        assert len(retrieved_family.children) == 2
        assert 3 in retrieved_family.children
        assert 4 in retrieved_family.children
        assert retrieved_family.comment == "Family with two children"

        # Verify all persons exist
        all_persons = person_repo.get_all_persons()
        assert len(all_persons) == 4

        print("✓ Successfully created family with children")
        print(f"✓ Parents: {father.first_name} & {mother.first_name}")
        children_count = len(retrieved_family.children)
        print(f"✓ Children: Alice & Charlie ({children_count} total)")

    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_edit_person_and_family() -> None:
    """Test editing persons and families."""
    # Create temporary database
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        # Initialize database service
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()

        # Initialize repositories
        person_repo = PersonRepository(db_service)

        # Create and add initial person
        person: app_person.Person[int, int, str, int] = (
            app_person.Person(
                index=1,
                first_name="John",
                surname="Doe",
                occ=0,
                image="",
                public_name="",
                qualifiers=[],
                aliases=[],
                first_names_aliases=[],
                surname_aliases=[],
                titles=[],
                non_native_parents_relation=[],
                related_persons=[],
                occupation="Engineer",
                sex=db_person.Sex.MALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None,
                birth_place="New York",
                birth_note="",
                birth_src="",
                baptism_date=None,
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=death_info.NotDead(),
                death_place="",
                death_note="",
                death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="",
                burial_note="",
                burial_src="",
                personal_events=[],
                notes="Original notes",
                src="",
                ascend=app_family.Ascendants(
                    parents=None,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
        )

        assert person_repo.add_person(person) is True

        # Edit the person
        edited_person: app_person.Person[int, int, str, int] = (
            app_person.Person(
                index=1,
                first_name="John",
                surname="Doe",
                occ=0,
                image="photo.jpg",
                public_name="Johnny",
                qualifiers=["Dr"],
                aliases=["JD"],
                first_names_aliases=[],
                surname_aliases=[],
                titles=[],
                non_native_parents_relation=[],
                related_persons=[],
                occupation="Senior Engineer",
                sex=db_person.Sex.MALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None,
                birth_place="New York",
                birth_note="",
                birth_src="",
                baptism_date=None,
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=death_info.NotDead(),
                death_place="",
                death_note="",
                death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="",
                burial_note="",
                burial_src="",
                personal_events=[],
                notes="Updated notes",
                src="",
                ascend=app_family.Ascendants(
                    parents=None,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
        )

        assert person_repo.edit_person(edited_person) is True

        # Verify edits
        retrieved = person_repo.get_person_by_id(1)
        assert retrieved.public_name == "Johnny"
        assert retrieved.occupation == "Senior Engineer"
        assert retrieved.image == "photo.jpg"
        assert retrieved.qualifiers == ["Dr"]
        assert retrieved.aliases == ["JD"]
        assert retrieved.notes == "Updated notes"

        print("✓ Successfully edited person")
        print(f"✓ Updated occupation: {retrieved.occupation}")
        print(f"✓ Updated public name: {retrieved.public_name}")

    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_person_family_bidirectional_links() -> None:
    """Test that person.families and family.children are correctly linked."""
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)
        family_repo = FamilyRepository(db_service)

        # Create parents
        father = app_person.Person[int, int, str, int](
            index=1, first_name="Father", surname="Test",
            occ=0, image="", public_name="", qualifiers=[],
            aliases=[], first_names_aliases=[], surname_aliases=[],
            titles=[], non_native_parents_relation=[],
            related_persons=[], occupation="",
            sex=db_person.Sex.MALE,
            access_right=title.AccessRight.PUBLIC,
            birth_date=None, birth_place="", birth_note="",
            birth_src="", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=app_family.Ascendants(
                parents=None,
                consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[1, 2]  # Person belongs to 2 families
        )

        mother = app_person.Person[int, int, str, int](
            index=2, first_name="Mother", surname="Test",
            occ=0, image="", public_name="", qualifiers=[],
            aliases=[], first_names_aliases=[], surname_aliases=[],
            titles=[], non_native_parents_relation=[],
            related_persons=[], occupation="",
            sex=db_person.Sex.FEMALE,
            access_right=title.AccessRight.PUBLIC,
            birth_date=None, birth_place="", birth_note="",
            birth_src="", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=app_family.Ascendants(
                parents=None,
                consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[1]  # Person belongs to 1 family
        )

        # Create child
        child = app_person.Person[int, int, str, int](
            index=3, first_name="Child", surname="Test",
            occ=0, image="", public_name="", qualifiers=[],
            aliases=[], first_names_aliases=[], surname_aliases=[],
            titles=[], non_native_parents_relation=[],
            related_persons=[], occupation="",
            sex=db_person.Sex.MALE,
            access_right=title.AccessRight.PUBLIC,
            birth_date=None, birth_place="", birth_note="",
            birth_src="", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=app_family.Ascendants(
                parents=1,  # Child has parents from family 1
                consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[]  # Child not married yet
        )

        person_repo.add_person(father)
        person_repo.add_person(mother)
        person_repo.add_person(child)

        # Create family
        family = app_family.Family(
            index=1, marriage_date=_create_default_date(), marriage_place="",
            marriage_note="", marriage_src="", witnesses=[],
            relation_kind=app_family.MaritalStatus.MARRIED,
            divorce_status=app_family.NotDivorced(),
            family_events=[], comment="", origin_file="", src="",
            parents=app_family.Parents([1, 2]),
            children=[3]  # Family has 1 child
        )

        family_repo.add_family(family)

        # Verify bidirectional links
        retrieved_family = family_repo.get_family_by_id(1)
        assert 3 in retrieved_family.children, "Child should be in family"

        retrieved_child = person_repo.get_person_by_id(3)
        assert retrieved_child.ascend.parents == 1, \
            "Child should have parents link to family 1"

        retrieved_father = person_repo.get_person_by_id(1)
        assert 1 in retrieved_father.families, \
            "Father should be in family 1"
        assert 2 in retrieved_father.families, \
            "Father should be in family 2"

        retrieved_mother = person_repo.get_person_by_id(2)
        assert 1 in retrieved_mother.families, \
            "Mother should be in family 1"

        print("✓ Bidirectional links verified")
        print(f"✓ Family has {len(retrieved_family.children)} child(ren)")
        print(f"✓ Father belongs to {len(retrieved_father.families)} families")
        print(f"✓ Child's parents: Family {retrieved_child.ascend.parents}")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_multiple_marriages() -> None:
    """Test a person with multiple marriages (families)."""
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)
        family_repo = FamilyRepository(db_service)

        # Create person who will have 2 marriages
        person = app_person.Person[int, int, str, int](
            index=1, first_name="John", surname="MultiMarriage",
            occ=0, image="", public_name="", qualifiers=[],
            aliases=[], first_names_aliases=[], surname_aliases=[],
            titles=[], non_native_parents_relation=[],
            related_persons=[], occupation="",
            sex=db_person.Sex.MALE,
            access_right=title.AccessRight.PUBLIC,
            birth_date=None, birth_place="", birth_note="",
            birth_src="", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=app_family.Ascendants(
                parents=None,
                consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[1, 2]  # Two marriages
        )

        # Create first spouse
        spouse1 = app_person.Person[int, int, str, int](
            index=2, first_name="Mary", surname="First",
            occ=0, image="", public_name="", qualifiers=[],
            aliases=[], first_names_aliases=[], surname_aliases=[],
            titles=[], non_native_parents_relation=[],
            related_persons=[], occupation="",
            sex=db_person.Sex.FEMALE,
            access_right=title.AccessRight.PUBLIC,
            birth_date=None, birth_place="", birth_note="",
            birth_src="", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=app_family.Ascendants(
                parents=None,
                consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[1]
        )

        # Create second spouse
        spouse2 = app_person.Person[int, int, str, int](
            index=3, first_name="Jane", surname="Second",
            occ=0, image="", public_name="", qualifiers=[],
            aliases=[], first_names_aliases=[], surname_aliases=[],
            titles=[], non_native_parents_relation=[],
            related_persons=[], occupation="",
            sex=db_person.Sex.FEMALE,
            access_right=title.AccessRight.PUBLIC,
            birth_date=None, birth_place="", birth_note="",
            birth_src="", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=app_family.Ascendants(
                parents=None,
                consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[2]
        )

        person_repo.add_person(person)
        person_repo.add_person(spouse1)
        person_repo.add_person(spouse2)

        # Create first marriage (divorced)
        family1 = app_family.Family(
            index=1, marriage_date=_create_default_date(),
            marriage_place="Church",
            marriage_note="", marriage_src="", witnesses=[],
            relation_kind=app_family.MaritalStatus.MARRIED,
            divorce_status=app_family.Divorced(_create_default_date()),
            family_events=[], comment="First marriage", origin_file="",
            src="", parents=app_family.Parents([1, 2]), children=[]
        )

        # Create second marriage (current)
        family2 = app_family.Family(
            index=2, marriage_date=_create_default_date(),
            marriage_place="City Hall",
            marriage_note="", marriage_src="", witnesses=[],
            relation_kind=app_family.MaritalStatus.MARRIED,
            divorce_status=app_family.NotDivorced(),
            family_events=[], comment="Second marriage", origin_file="",
            src="", parents=app_family.Parents([1, 3]), children=[]
        )

        family_repo.add_family(family1)
        family_repo.add_family(family2)

        # Verify person has 2 families
        retrieved_person = person_repo.get_person_by_id(1)
        assert len(retrieved_person.families) == 2, \
            "Person should have 2 families"
        assert 1 in retrieved_person.families
        assert 2 in retrieved_person.families

        # Verify each family
        fam1 = family_repo.get_family_by_id(1)
        assert isinstance(fam1.divorce_status, app_family.Divorced), \
            "First marriage should be divorced"
        assert fam1.comment == "First marriage"

        fam2 = family_repo.get_family_by_id(2)
        assert isinstance(fam2.divorce_status, app_family.NotDivorced), \
            "Second marriage should not be divorced"
        assert fam2.comment == "Second marriage"

        print("✓ Multiple marriages verified")
        print(f"✓ Person has {len(retrieved_person.families)} families")
        print(f"✓ First marriage: {fam1.divorce_status.__class__.__name__}")
        print(f"✓ Second marriage: {fam2.divorce_status.__class__.__name__}")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_edge_case_empty_fields() -> None:
    """Test handling of persons/families with minimal/empty fields."""
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)

        # Create person with minimal fields
        minimal_person = app_person.Person[int, int, str, int](
            index=1, first_name="", surname="",  # Empty names
            occ=0, image="", public_name="", qualifiers=[],
            aliases=[], first_names_aliases=[], surname_aliases=[],
            titles=[], non_native_parents_relation=[],
            related_persons=[], occupation="",
            sex=db_person.Sex.NEUTER,  # Using NEUTER as unknown/unspecified
            access_right=title.AccessRight.PRIVATE,
            birth_date=None, birth_place="", birth_note="",
            birth_src="", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=death_info.DontKnowIfDead(),
            death_place="", death_note="", death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=app_family.Ascendants(
                parents=None,
                consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[]
        )

        person_repo.add_person(minimal_person)
        retrieved = person_repo.get_person_by_id(1)

        assert retrieved.first_name == ""
        assert retrieved.surname == ""
        assert retrieved.sex == db_person.Sex.NEUTER
        assert isinstance(retrieved.death_status, death_info.DontKnowIfDead)
        assert len(retrieved.families) == 0

        print("✓ Minimal person handled correctly")
        print(f"✓ Sex: {retrieved.sex.name}")
        print(f"✓ Death status: {retrieved.death_status.__class__.__name__}")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_edge_case_large_family() -> None:
    """Test a family with many children."""
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)
        family_repo = FamilyRepository(db_service)

        # Create parents
        for i in range(1, 3):
            person = app_person.Person[int, int, str, int](
                index=i, first_name=f"Parent{i}", surname="Large",
                occ=0, image="", public_name="", qualifiers=[],
                aliases=[], first_names_aliases=[], surname_aliases=[],
                titles=[], non_native_parents_relation=[],
                related_persons=[], occupation="",
                sex=db_person.Sex.MALE if i == 1 else db_person.Sex.FEMALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None, birth_place="", birth_note="",
                birth_src="", baptism_date=None, baptism_place="",
                baptism_note="", baptism_src="",
                death_status=death_info.NotDead(),
                death_place="", death_note="", death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="", burial_note="", burial_src="",
                personal_events=[], notes="", src="",
                ascend=app_family.Ascendants(
                    parents=None,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[1]
            )
            person_repo.add_person(person)

        # Create 10 children
        num_children = 10
        for i in range(3, 3 + num_children):
            child = app_person.Person[int, int, str, int](
                index=i, first_name=f"Child{i - 2}", surname="Large",
                occ=0, image="", public_name="", qualifiers=[],
                aliases=[], first_names_aliases=[], surname_aliases=[],
                titles=[], non_native_parents_relation=[],
                related_persons=[], occupation="",
                sex=db_person.Sex.MALE if i % 2 else db_person.Sex.FEMALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None, birth_place="", birth_note="",
                birth_src="", baptism_date=None, baptism_place="",
                baptism_note="", baptism_src="",
                death_status=death_info.NotDead(),
                death_place="", death_note="", death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="", burial_note="", burial_src="",
                personal_events=[], notes="", src="",
                ascend=app_family.Ascendants(
                    parents=1,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[]
            )
            person_repo.add_person(child)

        # Create family with all children
        family = app_family.Family(
            index=1, marriage_date=_create_default_date(), marriage_place="",
            marriage_note="", marriage_src="", witnesses=[],
            relation_kind=app_family.MaritalStatus.MARRIED,
            divorce_status=app_family.NotDivorced(),
            family_events=[], comment="Large family", origin_file="",
            src="", parents=app_family.Parents([1, 2]),
            children=list(range(3, 3 + num_children))
        )

        family_repo.add_family(family)

        # Verify all children are linked
        retrieved_family = family_repo.get_family_by_id(1)
        assert len(retrieved_family.children) == num_children
        for i in range(3, 3 + num_children):
            assert i in retrieved_family.children

        # Verify each child has correct parent link
        for i in range(3, 3 + num_children):
            child = person_repo.get_person_by_id(i)
            assert child.ascend.parents == 1

        print(f"✓ Large family with {num_children} children verified")
        print(f"✓ All {len(retrieved_family.children)} children linked")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_edge_case_nonexistent_ids() -> None:
    """Test querying for non-existent person/family IDs."""
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)

        # Try to get non-existent person
        with pytest.raises(ValueError, match="Person with id 999 not found"):
            person_repo.get_person_by_id(999)

        # Try to get non-existent family
        with pytest.raises(ValueError, match="Family with id 999 not found"):
            FamilyRepository(db_service).get_family_by_id(999)

        print("✓ Non-existent ID errors raised correctly")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_edge_case_orphan_child() -> None:
    """Test a child with no parents (orphan)."""
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)

        # Create orphan (no parents)
        orphan = app_person.Person[int, int, str, int](
            index=1, first_name="Orphan", surname="NoParents",
            occ=0, image="", public_name="", qualifiers=[],
            aliases=[], first_names_aliases=[], surname_aliases=[],
            titles=[], non_native_parents_relation=[],
            related_persons=[], occupation="",
            sex=db_person.Sex.MALE,
            access_right=title.AccessRight.PUBLIC,
            birth_date=None, birth_place="", birth_note="",
            birth_src="", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=app_family.Ascendants(
                parents=None,  # No parents
                consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[]
        )

        person_repo.add_person(orphan)
        retrieved = person_repo.get_person_by_id(1)

        assert retrieved.ascend.parents is None
        assert int(retrieved.ascend.consanguinity_rate) == 0

        print("✓ Orphan (no parents) handled correctly")
        print(f"✓ Parents: {retrieved.ascend.parents}")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_edge_case_childless_family() -> None:
    """Test a family with no children."""
    with tempfile.NamedTemporaryFile(
            mode='w', suffix='.db', delete=False) as tmp:
        db_path = tmp.name

    try:
        db_service = SQLiteDatabaseService(db_path)
        db_service.connect()
        person_repo = PersonRepository(db_service)
        family_repo = FamilyRepository(db_service)

        # Create couple
        for i in range(1, 3):
            person = app_person.Person[int, int, str, int](
                index=i, first_name=f"Person{i}", surname="NoKids",
                occ=0, image="", public_name="", qualifiers=[],
                aliases=[], first_names_aliases=[], surname_aliases=[],
                titles=[], non_native_parents_relation=[],
                related_persons=[], occupation="",
                sex=db_person.Sex.MALE if i == 1 else db_person.Sex.FEMALE,
                access_right=title.AccessRight.PUBLIC,
                birth_date=None, birth_place="", birth_note="",
                birth_src="", baptism_date=None, baptism_place="",
                baptism_note="", baptism_src="",
                death_status=death_info.NotDead(),
                death_place="", death_note="", death_src="",
                burial=burial_info.UnknownBurial(),
                burial_place="", burial_note="", burial_src="",
                personal_events=[], notes="", src="",
                ascend=app_family.Ascendants(
                    parents=None,
                    consanguinity_rate=consanguinity_rate.ConsanguinityRate(0)
                ),
                families=[1]
            )
            person_repo.add_person(person)

        # Create childless family
        family = app_family.Family(
            index=1, marriage_date=_create_default_date(), marriage_place="",
            marriage_note="", marriage_src="", witnesses=[],
            relation_kind=app_family.MaritalStatus.MARRIED,
            divorce_status=app_family.NotDivorced(),
            family_events=[], comment="Childless", origin_file="",
            src="", parents=app_family.Parents([1, 2]),
            children=[]  # No children
        )

        family_repo.add_family(family)
        retrieved_family = family_repo.get_family_by_id(1)

        assert len(retrieved_family.children) == 0
        assert retrieved_family.comment == "Childless"

        print("✓ Childless family handled correctly")
        print(f"✓ Children count: {len(retrieved_family.children)}")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)
