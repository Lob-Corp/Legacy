"""
Ultimate Collection Bundle Premium GOTY Edition - Comprehensive Database Relationship Tests
Tests every relationship, foreign key, cascade behavior, and value constraint for all models.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database import Base
from database.person import Person, DeathStatus, BurialStatus
from database.family import Family, DivorceStatus
from database.couple import Couple
from database.ascends import Ascends
from database.descends import Descends
from database.descend_children import DescendChildren
from database.unions import Unions
from database.union_families import UnionFamilies
from database.date import Date, Precision, DatePrecision
from database.place import Place
from database.relation import Relation
from database.titles import Titles
from database.personal_event import PersonalEvent
from database.family_event import FamilyEvent
from database.person_events import PersonEvents
from database.family_events import FamilyEvents
from database.person_event_witness import PersonEventWitness
from database.family_event_witness import FamilyEventWitness
from database.person_relations import PersonRelations
from database.person_non_native_relations import PersonNonNativeRelations
from database.person_titles import PersonTitles
from database.family_witness import FamilyWitness
from database.personal_event import PersonalEventName
from database.family_event import FamilyEventName

from libraries.person import Sex
from libraries.title import AccessRight
from libraries.death_info import DeathReason
from libraries.family import MaritalStatus, RelationToParentType
from libraries.date import Calendar


@pytest.fixture(scope="function")
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


# ============================================================================
# DATE AND PRECISION TESTS
# ============================================================================

class TestDateAndPrecision:
    """Test Date and Precision models with all relationships."""

    def test_precision_creation(self, db_session: Session):
        """Test creating a Precision object with all fields."""
        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2023-01-15",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        db_session.add(precision)
        db_session.commit()

        assert precision.id is not None
        assert precision.precision_level == DatePrecision.SURE
        assert precision.iso_date == "2023-01-15"
        assert precision.calendar == Calendar.GREGORIAN
        assert precision.delta == 0

    def test_date_creation_with_precision(self, db_session: Session):
        """Test creating a Date with related Precision."""
        precision = Precision(
            precision_level=DatePrecision.ABOUT,
            iso_date="2020-06-01",
            calendar=Calendar.GREGORIAN,
            delta=5
        )
        date = Date(
            iso_date="2020-06-15",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )
        db_session.add(date)
        db_session.commit()

        assert date.id is not None
        assert date.precision_obj.precision_level == DatePrecision.ABOUT
        assert date.precision_obj.iso_date == "2020-06-01"

    def test_date_cascade_delete_precision(self, db_session: Session):
        """Test that deleting a Date cascades to delete Precision."""
        precision = Precision(
            precision_level=DatePrecision.MAYBE,
            iso_date=None,
            calendar=None,
            delta=None
        )
        date = Date(
            iso_date="1999-12-31",
            calendar=Calendar.JULIAN,
            precision_obj=precision,
            delta=10
        )
        db_session.add(date)
        db_session.commit()

        precision_id = precision.id
        db_session.delete(date)
        db_session.commit()

        # Precision should be deleted due to cascade
        deleted_precision = db_session.get(Precision, precision_id)
        assert deleted_precision is None

    def test_all_date_precision_enums(self, db_session: Session):
        """Test all DatePrecision enum values."""
        for precision_type in DatePrecision:
            precision = Precision(
                precision_level=precision_type,
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                delta=0
            )
            db_session.add(precision)
        db_session.commit()

        precisions = db_session.query(Precision).all()
        assert len(precisions) == len(DatePrecision)

    def test_all_calendar_types(self, db_session: Session):
        """Test all Calendar enum values."""
        for calendar_type in Calendar:
            precision = Precision(
                precision_level=DatePrecision.SURE,
                iso_date="2024-01-01",
                calendar=Calendar.GREGORIAN,
                delta=0
            )
            date = Date(
                iso_date="2024-01-01",
                calendar=calendar_type,
                precision_obj=precision,
                delta=0
            )
            db_session.add(date)
        db_session.commit()

        dates = db_session.query(Date).all()
        assert len(dates) == len(Calendar)


# ============================================================================
# PERSON TESTS
# ============================================================================

class TestPerson:
    """Test Person model with all relationships and fields."""

    def test_person_basic_creation(self, db_session: Session):
        """Test creating a Person with all basic fields."""
        person = Person(
            first_name="John",
            surname="Doe",
            occ=0,
            image="john_doe.jpg",
            public_name="John Doe",
            qualifiers="Sr.",
            aliases="Johnny",
            first_names_aliases="Jonathan",
            surname_aliases="Dough",
            occupation="Engineer",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="New York",
            birth_note="Born at home",
            birth_src="Birth certificate",
            baptism_place="St. Patrick's",
            baptism_note="Baptized",
            baptism_src="Church records",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="Test person",
            src="Test source"
        )
        db_session.add(person)
        db_session.commit()

        assert person.id is not None
        assert person.first_name == "John"
        assert person.surname == "Doe"
        assert person.sex == Sex.MALE

    def test_person_with_dates(self, db_session: Session):
        """Test Person with birth, baptism, death, and burial dates."""
        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1990-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        birth_date = Date(
            iso_date="1990-05-15",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )

        person = Person(
            first_name="Jane",
            surname="Smith",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="Doctor",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_date_obj=birth_date,
            birth_place="London",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        db_session.add(person)
        db_session.commit()

        assert person.birth_date_obj.iso_date == "1990-05-15"
        assert person.birth_date_obj.calendar == Calendar.GREGORIAN

    def test_person_death_statuses(self, db_session: Session):
        """Test all DeathStatus enum values."""
        for idx, status in enumerate(DeathStatus):
            person = Person(
                first_name=f"Person{idx}",
                surname="Test",
                occ=0,
                image="",
                public_name="",
                qualifiers="",
                aliases="",
                first_names_aliases="",
                surname_aliases="",
                occupation="",
                sex=Sex.MALE,
                access_right=AccessRight.PUBLIC,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=status,
                death_reason=DeathReason.MURDERED if status == DeathStatus.DEAD else None,
                death_place="",
                death_note="",
                death_src="",
                burial_status=BurialStatus.UNKNOWN_BURIAL,
                burial_place="",
                burial_note="",
                burial_src="",
                notes="",
                src=""
            )
            db_session.add(person)
        db_session.commit()

        persons = db_session.query(Person).all()
        assert len(persons) == len(DeathStatus)

    def test_person_burial_statuses(self, db_session: Session):
        """Test all BurialStatus enum values."""
        for idx, status in enumerate(BurialStatus):
            person = Person(
                first_name=f"Person{idx}",
                surname="Burial",
                occ=0,
                image="",
                public_name="",
                qualifiers="",
                aliases="",
                first_names_aliases="",
                surname_aliases="",
                occupation="",
                sex=Sex.FEMALE,
                access_right=AccessRight.PUBLIC,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=DeathStatus.DEAD,
                death_reason=None,
                death_place="",
                death_note="",
                death_src="",
                burial_status=status,
                burial_place="Cemetery" if status != BurialStatus.UNKNOWN_BURIAL else "",
                burial_note="",
                burial_src="",
                notes="",
                src=""
            )
            db_session.add(person)
        db_session.commit()

        persons = db_session.query(Person).all()
        assert len(persons) == len(BurialStatus)

    def test_person_with_ascends(self, db_session: Session):
        """Test Person with Ascends relationship."""
        ascends = Ascends(
            parents=None,
            consang=0
        )
        person = Person(
            first_name="Child",
            surname="WithParents",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            ascend=ascends,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        db_session.add(person)
        db_session.commit()

        assert person.ascend is not None
        assert person.ascend.consang == 0

    def test_person_with_unions(self, db_session: Session):
        """Test Person with Unions relationship."""
        unions = Unions()
        person = Person(
            first_name="Married",
            surname="Person",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            families=unions,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        db_session.add(person)
        db_session.commit()

        assert person.families is not None
        assert person.families.id is not None

    def test_person_cascade_delete_dates(self, db_session: Session):
        """Test that deleting Person cascades to delete all related dates."""
        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1980-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        birth_date = Date(
            iso_date="1980-03-20",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )

        person = Person(
            first_name="ToDelete",
            surname="Person",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_date_obj=birth_date,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        db_session.add(person)
        db_session.commit()

        birth_date_id = birth_date.id
        db_session.delete(person)
        db_session.commit()

        deleted_date = db_session.get(Date, birth_date_id)
        assert deleted_date is None


# ============================================================================
# COUPLE AND FAMILY TESTS
# ============================================================================

class TestCoupleAndFamily:
    """Test Couple and Family models with relationships."""

    def test_couple_creation(self, db_session: Session):
        """Test creating a Couple with father and mother."""
        father = Person(
            first_name="Father",
            surname="Doe",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="Mother",
            surname="Smith",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        couple = Couple(
            father_obj=father,
            mother_obj=mother
        )
        db_session.add(couple)
        db_session.commit()

        assert couple.id is not None
        assert couple.father_obj.first_name == "Father"
        assert couple.mother_obj.first_name == "Mother"

    def test_family_creation_with_couple(self, db_session: Session):
        """Test creating a Family with Couple."""
        father = Person(
            first_name="Dad",
            surname="Family",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="Mom",
            surname="Family",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        couple = Couple(father_obj=father, mother_obj=mother)

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2000-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="2000-06-15",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )

        descends = Descends()

        family = Family(
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="Church",
            marriage_note="Beautiful ceremony",
            marriage_src="Wedding album",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="Happy family",
            origin_file="test.ged",
            src="Test"
        )
        db_session.add(family)
        db_session.commit()

        assert family.id is not None
        assert family.parents.father_obj.first_name == "Dad"
        assert family.parents.mother_obj.first_name == "Mom"
        assert family.relation_kind == MaritalStatus.MARRIED

    def test_family_all_marital_statuses(self, db_session: Session):
        """Test all MaritalStatus enum values."""
        for idx, status in enumerate(MaritalStatus):
            father = Person(
                first_name=f"Father{idx}",
                surname="Test",
                occ=0,
                image="",
                public_name="",
                qualifiers="",
                aliases="",
                first_names_aliases="",
                surname_aliases="",
                occupation="",
                sex=Sex.MALE,
                access_right=AccessRight.PUBLIC,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=DeathStatus.NOT_DEAD,
                death_reason=None,
                death_place="",
                death_note="",
                death_src="",
                burial_status=BurialStatus.UNKNOWN_BURIAL,
                burial_place="",
                burial_note="",
                burial_src="",
                notes="",
                src=""
            )
            mother = Person(
                first_name=f"Mother{idx}",
                surname="Test",
                occ=0,
                image="",
                public_name="",
                qualifiers="",
                aliases="",
                first_names_aliases="",
                surname_aliases="",
                occupation="",
                sex=Sex.FEMALE,
                access_right=AccessRight.PUBLIC,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=DeathStatus.NOT_DEAD,
                death_reason=None,
                death_place="",
                death_note="",
                death_src="",
                burial_status=BurialStatus.UNKNOWN_BURIAL,
                burial_place="",
                burial_note="",
                burial_src="",
                notes="",
                src=""
            )
            couple = Couple(father_obj=father, mother_obj=mother)

            precision = Precision(
                precision_level=DatePrecision.SURE,
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                delta=0
            )
            marriage_date = Date(
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                precision_obj=precision,
                delta=0
            )
            descends = Descends()

            family = Family(
                parents=couple,
                children=descends,
                marriage_date_obj=marriage_date,
                marriage_place="",
                marriage_note="",
                marriage_src="",
                relation_kind=status,
                divorce_status=DivorceStatus.NOT_DIVORCED,
                divorce_date=None,
                comment="",
                origin_file="",
                src=""
            )
            db_session.add(family)
        db_session.commit()

        families = db_session.query(Family).all()
        assert len(families) == len(MaritalStatus)

    def test_family_all_divorce_statuses(self, db_session: Session):
        """Test all DivorceStatus enum values."""
        for idx, status in enumerate(DivorceStatus):
            father = Person(
                first_name=f"Father{idx}",
                surname="Divorce",
                occ=0,
                image="",
                public_name="",
                qualifiers="",
                aliases="",
                first_names_aliases="",
                surname_aliases="",
                occupation="",
                sex=Sex.MALE,
                access_right=AccessRight.PUBLIC,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=DeathStatus.NOT_DEAD,
                death_reason=None,
                death_place="",
                death_note="",
                death_src="",
                burial_status=BurialStatus.UNKNOWN_BURIAL,
                burial_place="",
                burial_note="",
                burial_src="",
                notes="",
                src=""
            )
            mother = Person(
                first_name=f"Mother{idx}",
                surname="Divorce",
                occ=0,
                image="",
                public_name="",
                qualifiers="",
                aliases="",
                first_names_aliases="",
                surname_aliases="",
                occupation="",
                sex=Sex.FEMALE,
                access_right=AccessRight.PUBLIC,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=DeathStatus.NOT_DEAD,
                death_reason=None,
                death_place="",
                death_note="",
                death_src="",
                burial_status=BurialStatus.UNKNOWN_BURIAL,
                burial_place="",
                burial_note="",
                burial_src="",
                notes="",
                src=""
            )
            couple = Couple(father_obj=father, mother_obj=mother)

            precision = Precision(
                precision_level=DatePrecision.SURE,
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                delta=0
            )
            marriage_date = Date(
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                precision_obj=precision,
                delta=0
            )
            descends = Descends()

            family = Family(
                parents=couple,
                children=descends,
                marriage_date_obj=marriage_date,
                marriage_place="",
                marriage_note="",
                marriage_src="",
                relation_kind=MaritalStatus.MARRIED,
                divorce_status=status,
                divorce_date=None,
                comment="",
                origin_file="",
                src=""
            )
            db_session.add(family)
        db_session.commit()

        families = db_session.query(Family).all()
        assert len(families) == len(DivorceStatus)

    def test_family_cascade_delete(self, db_session: Session):
        """Test that deleting Family cascades to Couple, Descends, and Dates."""
        father = Person(
            first_name="ToDelete",
            surname="Father",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="ToDelete",
            surname="Mother",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        couple = Couple(father_obj=father, mother_obj=mother)

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2000-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="2000-06-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )
        descends = Descends()

        family = Family(
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="",
            origin_file="",
            src=""
        )
        db_session.add(family)
        db_session.commit()

        couple_id = couple.id
        descends_id = descends.id
        marriage_date_id = marriage_date.id

        db_session.delete(family)
        db_session.commit()

        # Check cascade deletes
        assert db_session.get(Couple, couple_id) is None
        assert db_session.get(Descends, descends_id) is None
        assert db_session.get(Date, marriage_date_id) is None


# ============================================================================
# ASCENDS AND DESCENDS TESTS
# ============================================================================

class TestAscentAndDescent:
    """Test Ascends, Descends, and DescendChildren relationships."""

    def test_ascends_with_family(self, db_session: Session):
        """Test Ascends linking to Family."""
        father = Person(
            first_name="Father",
            surname="Ascend",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="Mother",
            surname="Ascend",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        couple = Couple(father_obj=father, mother_obj=mother)

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1990-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="1990-05-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )
        descends = Descends()

        family = Family(
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="",
            origin_file="",
            src=""
        )

        ascends = Ascends(
            parents_obj=family,
            consang=5
        )
        db_session.add(ascends)
        db_session.commit()

        assert ascends.id is not None
        assert ascends.parents_obj.id == family.id
        assert ascends.consang == 5

    def test_descend_children_relationship(self, db_session: Session):
        """Test DescendChildren linking Descends and Person."""
        descends = Descends()

        child = Person(
            first_name="Child",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        descend_child = DescendChildren(
            descend_obj=descends,
            person_obj=child
        )
        db_session.add(descend_child)
        db_session.commit()

        assert descend_child.id is not None
        assert descend_child.descend_obj.id == descends.id
        assert descend_child.person_obj.first_name == "Child"


# ============================================================================
# UNIONS AND UNION FAMILIES TESTS
# ============================================================================

class TestUnionsAndUnionFamilies:
    """Test Unions and UnionFamilies relationships."""

    def test_union_families_relationship(self, db_session: Session):
        """Test UnionFamilies linking Unions and Family."""
        unions = Unions()

        father = Person(
            first_name="UnionFather",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="UnionMother",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        couple = Couple(father_obj=father, mother_obj=mother)

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2000-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="2000-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )
        descends = Descends()

        family = Family(
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="",
            origin_file="",
            src=""
        )

        union_family = UnionFamilies(
            union_obj=unions,
            family_obj=family
        )
        db_session.add(union_family)
        db_session.commit()

        assert union_family.id is not None
        assert union_family.union_obj.id == unions.id
        assert union_family.family_obj.id == family.id


# ============================================================================
# PLACE TESTS
# ============================================================================

class TestPlace:
    """Test Place model with all fields."""

    def test_place_creation(self, db_session: Session):
        """Test creating a Place with all fields."""
        place = Place(
            town="Paris",
            township="1st Arrondissement",
            canton="Paris-1",
            district="Central",
            county="Paris",
            region="Île-de-France",
            country="France",
            other="Near the Louvre"
        )
        db_session.add(place)
        db_session.commit()

        assert place.id is not None
        assert place.town == "Paris"
        assert place.country == "France"

    def test_place_empty_fields(self, db_session: Session):
        """Test Place with empty optional fields."""
        place = Place(
            town="SmallTown",
            township="",
            canton="",
            district="",
            county="",
            region="",
            country="USA",
            other=""
        )
        db_session.add(place)
        db_session.commit()

        assert place.id is not None
        assert place.town == "SmallTown"


# ============================================================================
# RELATION TESTS
# ============================================================================

class TestRelation:
    """Test Relation model with all relationship types."""

    def test_relation_creation(self, db_session: Session):
        """Test creating a Relation between persons."""
        father = Person(
            first_name="BioDad",
            surname="Relation",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="BioMom",
            surname="Relation",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        relation = Relation(
            type=RelationToParentType.ADOPTION,
            father_obj=father,
            mother_obj=mother,
            sources="Adoption papers"
        )
        db_session.add(relation)
        db_session.commit()

        assert relation.id is not None
        assert relation.type == RelationToParentType.ADOPTION
        assert relation.father_obj.first_name == "BioDad"

    def test_all_relation_types(self, db_session: Session):
        """Test all RelationToParentType enum values."""
        for idx, rel_type in enumerate(RelationToParentType):
            father = Person(
                first_name=f"Father{idx}",
                surname="RelType",
                occ=0,
                image="",
                public_name="",
                qualifiers="",
                aliases="",
                first_names_aliases="",
                surname_aliases="",
                occupation="",
                sex=Sex.MALE,
                access_right=AccessRight.PUBLIC,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=DeathStatus.NOT_DEAD,
                death_reason=None,
                death_place="",
                death_note="",
                death_src="",
                burial_status=BurialStatus.UNKNOWN_BURIAL,
                burial_place="",
                burial_note="",
                burial_src="",
                notes="",
                src=""
            )
            mother = Person(
                first_name=f"Mother{idx}",
                surname="RelType",
                occ=0,
                image="",
                public_name="",
                qualifiers="",
                aliases="",
                first_names_aliases="",
                surname_aliases="",
                occupation="",
                sex=Sex.FEMALE,
                access_right=AccessRight.PUBLIC,
                birth_place="",
                birth_note="",
                birth_src="",
                baptism_place="",
                baptism_note="",
                baptism_src="",
                death_status=DeathStatus.NOT_DEAD,
                death_reason=None,
                death_place="",
                death_note="",
                death_src="",
                burial_status=BurialStatus.UNKNOWN_BURIAL,
                burial_place="",
                burial_note="",
                burial_src="",
                notes="",
                src=""
            )

            relation = Relation(
                type=rel_type,
                father_obj=father,
                mother_obj=mother,
                sources=""
            )
            db_session.add(relation)
        db_session.commit()

        relations = db_session.query(Relation).all()
        assert len(relations) == len(RelationToParentType)


# ============================================================================
# TITLES TESTS
# ============================================================================

class TestTitles:
    """Test Titles model with date relationships."""

    def test_titles_creation(self, db_session: Session):
        """Test creating Titles with start and end dates."""
        precision_start = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1800-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        start_date = Date(
            iso_date="1800-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_start,
            delta=0
        )
        precision_end = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1850-12-31",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        end_date = Date(
            iso_date="1850-12-31",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_end,
            delta=0
        )

        title = Titles(
            name="Duke",
            ident="duke_01",
            place="Westminster",
            date_start_obj=start_date,
            date_end_obj=end_date,
            nth=1
        )
        db_session.add(title)
        db_session.commit()

        assert title.id is not None
        assert title.name == "Duke"
        assert title.date_start_obj.iso_date == "1800-01-01"
        assert title.date_end_obj.iso_date == "1850-12-31"

    def test_titles_cascade_delete_dates(self, db_session: Session):
        """Test that deleting Titles cascades to delete dates."""
        precision_start = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1900-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        start_date = Date(
            iso_date="1900-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_start,
            delta=0
        )
        precision_end = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1950-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        end_date = Date(
            iso_date="1950-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_end,
            delta=0
        )

        title = Titles(
            name="Baron",
            ident="baron_01",
            place="London",
            date_start_obj=start_date,
            date_end_obj=end_date,
            nth=2
        )
        db_session.add(title)
        db_session.commit()

        start_date_id = start_date.id
        end_date_id = end_date.id

        db_session.delete(title)
        db_session.commit()

        assert db_session.get(Date, start_date_id) is None
        assert db_session.get(Date, end_date_id) is None


# ============================================================================
# COMPLEX INTEGRATION TESTS
# ============================================================================

class TestComplexIntegration:
    """Test complex scenarios with multiple related entities."""

    def test_full_family_tree_structure(self, db_session: Session):
        """Test creating a complete family tree with all relationships."""
        # Create grandparents
        grandfather = Person(
            first_name="Grandfather",
            surname="Smith",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="Farmer",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="Farm",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.DEAD,
            death_reason=DeathReason.UNSPECIFIED,
            death_place="Home",
            death_note="",
            death_src="",
            burial_status=BurialStatus.BURIAL,
            burial_place="Village Cemetery",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        grandmother = Person(
            first_name="Grandmother",
            surname="Jones",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="Housewife",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="Village",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.DEAD,
            death_reason=None,
            death_place="Hospital",
            death_note="",
            death_src="",
            burial_status=BurialStatus.BURIAL,
            burial_place="Village Cemetery",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        # Create grandparents couple and family
        grandparents_couple = Couple(
            father_obj=grandfather,
            mother_obj=grandmother
        )

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1950-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        grandparents_marriage = Date(
            iso_date="1950-06-15",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )

        grandparents_descends = Descends()

        grandparents_family = Family(
            parents=grandparents_couple,
            children=grandparents_descends,
            marriage_date_obj=grandparents_marriage,
            marriage_place="Village Church",
            marriage_note="Simple ceremony",
            marriage_src="Church records",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="Long marriage",
            origin_file="family.ged",
            src="Family Bible"
        )

        # Create parent (child of grandparents)
        father = Person(
            first_name="Father",
            surname="Smith",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="Teacher",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="Village",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        # Link father to grandparents
        father_ascends = Ascends(
            parents_obj=grandparents_family,
            consang=0
        )
        father.ascend = father_ascends

        descend_child_link = DescendChildren(
            descend_obj=grandparents_descends,
            person_obj=father
        )

        db_session.add_all([grandparents_family, father, descend_child_link])
        db_session.commit()

        # Verify the structure
        assert father.ascend.parents_obj.id == grandparents_family.id
        assert grandparents_family.parents.father_obj.first_name == "Grandfather"
        assert grandparents_family.parents.mother_obj.first_name == "Grandmother"

        # Query and verify
        retrieved_father = db_session.query(
            Person).filter_by(first_name="Father").first()
        assert retrieved_father.ascend.parents_obj.parents.father_obj.first_name == "Grandfather"

    def test_multiple_marriages(self, db_session: Session):
        """Test a person with multiple marriages through Unions."""
        person = Person(
            first_name="MultiMarried",
            surname="Person",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        unions = Unions()
        person.families = unions

        # First marriage
        spouse1 = Person(
            first_name="FirstSpouse",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        couple1 = Couple(father_obj=person, mother_obj=spouse1)
        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2000-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage1_date = Date(
            iso_date="2000-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )
        descends1 = Descends()

        family1 = Family(
            parents=couple1,
            children=descends1,
            marriage_date_obj=marriage1_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.DIVORCED,
            divorce_date=None,
            comment="First marriage",
            origin_file="",
            src=""
        )

        # Second marriage
        spouse2 = Person(
            first_name="SecondSpouse",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        couple2 = Couple(father_obj=person, mother_obj=spouse2)
        precision2 = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2010-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage2_date = Date(
            iso_date="2010-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision2,
            delta=0
        )
        descends2 = Descends()

        family2 = Family(
            parents=couple2,
            children=descends2,
            marriage_date_obj=marriage2_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="Second marriage",
            origin_file="",
            src=""
        )

        # Link families to unions
        union_family1 = UnionFamilies(union_obj=unions, family_obj=family1)
        union_family2 = UnionFamilies(union_obj=unions, family_obj=family2)

        db_session.add_all(
            [person, family1, family2, union_family1, union_family2])
        db_session.commit()

        # Verify multiple marriages
        assert person.families is not None
        union_families = db_session.query(
            UnionFamilies).filter_by(union_id=unions.id).all()
        assert len(union_families) == 2

        families = [uf.family_obj for uf in union_families]
        assert families[0].comment == "First marriage"
        assert families[1].comment == "Second marriage"


# ============================================================================
# PERSONAL EVENT TESTS
# ============================================================================

class TestPersonalEvent:
    """Test PersonalEvent model with all event types and witnesses."""

    def test_personal_event_creation(self, db_session: Session):
        """Test creating a PersonalEvent with all fields."""
        person = Person(
            first_name="EventPerson",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2020-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        event_date = Date(
            iso_date="2020-05-15",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )

        event = PersonalEvent(
            person_obj=person,
            name=PersonalEventName.GRADUATE,
            date_obj=event_date,
            place="University",
            reason="Completed studies",
            note="With honors",
            src="Diploma"
        )
        db_session.add(event)
        db_session.commit()

        assert event.id is not None
        assert event.name == PersonalEventName.GRADUATE
        assert event.person_obj.first_name == "EventPerson"
        assert event.date_obj.iso_date == "2020-05-15"

    def test_all_personal_event_names(self, db_session: Session):
        """Test all PersonalEventName enum values."""
        person = Person(
            first_name="AllEvents",
            surname="Person",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        for event_name in PersonalEventName:
            precision = Precision(
                precision_level=DatePrecision.SURE,
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                delta=0
            )
            event_date = Date(
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                precision_obj=precision,
                delta=0
            )
            event = PersonalEvent(
                person_obj=person,
                name=event_name,
                date_obj=event_date,
                place="",
                reason="",
                note="",
                src=""
            )
            db_session.add(event)
        db_session.commit()

        events = db_session.query(PersonalEvent).all()
        assert len(events) == len(PersonalEventName)

    def test_person_events_linking(self, db_session: Session):
        """Test PersonEvents junction table linking Person and PersonalEvent."""
        person = Person(
            first_name="LinkedPerson",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2015-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        event_date = Date(
            iso_date="2015-06-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )

        event = PersonalEvent(
            person_obj=person,
            name=PersonalEventName.RESIDENCE,
            date_obj=event_date,
            place="Paris",
            reason="Work",
            note="",
            src=""
        )

        person_event = PersonEvents(
            person_obj=person,
            event_obj=event
        )
        db_session.add(person_event)
        db_session.commit()

        assert person_event.id is not None
        assert person_event.person_obj.first_name == "LinkedPerson"
        assert person_event.event_obj.name == PersonalEventName.RESIDENCE

    def test_person_event_witness(self, db_session: Session):
        """Test PersonEventWitness with EventWitnessKind."""
        from libraries.events import EventWitnessKind

        person = Person(
            first_name="EventOwner",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        witness = Person(
            first_name="Witness",
            surname="Person",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2018-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        event_date = Date(
            iso_date="2018-03-15",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )

        event = PersonalEvent(
            person_obj=person,
            name=PersonalEventName.BAPTISM,
            date_obj=event_date,
            place="Church",
            reason="",
            note="",
            src=""
        )

        event_witness = PersonEventWitness(
            person_obj=witness,
            event_obj=event,
            kind=EventWitnessKind.WITNESS
        )
        db_session.add(event_witness)
        db_session.commit()

        assert event_witness.id is not None
        assert event_witness.person_obj.first_name == "Witness"
        assert event_witness.event_obj.person_obj.first_name == "EventOwner"
        assert event_witness.kind == EventWitnessKind.WITNESS

    def test_personal_event_cascade_delete(self, db_session: Session):
        """Test that deleting PersonalEvent cascades to delete Date."""
        person = Person(
            first_name="CascadePerson",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2010-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        event_date = Date(
            iso_date="2010-05-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )

        event = PersonalEvent(
            person_obj=person,
            name=PersonalEventName.MILITARY_SERVICE,
            date_obj=event_date,
            place="",
            reason="",
            note="",
            src=""
        )
        db_session.add(event)
        db_session.commit()

        date_id = event_date.id
        db_session.delete(event)
        db_session.commit()

        assert db_session.get(Date, date_id) is None


# ============================================================================
# FAMILY EVENT TESTS
# ============================================================================

class TestFamilyEvent:
    """Test FamilyEvent model with all event types and witnesses."""

    def test_family_event_creation(self, db_session: Session):
        """Test creating a FamilyEvent with all fields."""
        father = Person(
            first_name="FamilyEventDad",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="FamilyEventMom",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        couple = Couple(father_obj=father, mother_obj=mother)

        precision_marriage = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2005-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="2005-06-20",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_marriage,
            delta=0
        )
        precision_event = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2005-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        event_date = Date(
            iso_date="2005-06-20",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_event,
            delta=0
        )
        descends = Descends()

        family = Family(
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="Cathedral",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="",
            origin_file="",
            src=""
        )

        family_event = FamilyEvent(
            family_obj=family,
            name=FamilyEventName.MARRIAGE,
            date_obj=event_date,
            place="Cathedral",
            reason="Love",
            note="Beautiful ceremony",
            src="Wedding certificate"
        )
        db_session.add(family_event)
        db_session.commit()

        assert family_event.id is not None
        assert family_event.name == FamilyEventName.MARRIAGE
        assert family_event.family_obj.parents.father_obj.first_name == "FamilyEventDad"

    def test_all_family_event_names(self, db_session: Session):
        """Test all FamilyEventName enum values."""
        father = Person(
            first_name="AllFamilyEvents",
            surname="Dad",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="AllFamilyEvents",
            surname="Mom",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        couple = Couple(father_obj=father, mother_obj=mother)

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2000-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="2000-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )
        descends = Descends()

        family = Family(
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="",
            origin_file="",
            src=""
        )

        for event_name in FamilyEventName:
            precision = Precision(
                precision_level=DatePrecision.SURE,
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                delta=0
            )
            event_date = Date(
                iso_date="2000-01-01",
                calendar=Calendar.GREGORIAN,
                precision_obj=precision,
                delta=0
            )
            event = FamilyEvent(
                family_obj=family,
                name=event_name,
                date_obj=event_date,
                place="",
                reason="",
                note="",
                src=""
            )
            db_session.add(event)
        db_session.commit()

        events = db_session.query(FamilyEvent).all()
        assert len(events) == len(FamilyEventName)

    def test_family_events_linking(self, db_session: Session):
        """Test FamilyEvents junction table linking Family and FamilyEvent."""
        father = Person(
            first_name="LinkedFamilyDad",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="LinkedFamilyMom",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        couple = Couple(father_obj=father, mother_obj=mother)

        precision_marriage = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2010-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="2010-05-15",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_marriage,
            delta=0
        )
        precision_event = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2010-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        event_date = Date(
            iso_date="2010-05-15",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_event,
            delta=0
        )
        descends = Descends()

        family = Family(
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="",
            origin_file="",
            src=""
        )

        family_event = FamilyEvent(
            family_obj=family,
            name=FamilyEventName.MARRIAGE_CONTRACT,
            date_obj=event_date,
            place="Notary office",
            reason="",
            note="",
            src=""
        )

        family_events_link = FamilyEvents(
            family_obj=family,
            event_obj=family_event
        )
        db_session.add(family_events_link)
        db_session.commit()

        assert family_events_link.id is not None
        assert family_events_link.family_obj.id == family.id
        assert family_events_link.event_obj.name == FamilyEventName.MARRIAGE_CONTRACT

    def test_family_event_witness(self, db_session: Session):
        """Test FamilyEventWitness with EventWitnessKind."""
        from libraries.events import EventWitnessKind

        father = Person(
            first_name="WitnessFamilyDad",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            first_name="WitnessFamilyMom",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        witness = Person(
            first_name="FamilyWitness",
            surname="Person",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        couple = Couple(father_obj=father, mother_obj=mother)

        precision_marriage = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2012-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="2012-07-14",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_marriage,
            delta=0
        )
        precision_event = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2012-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        event_date = Date(
            iso_date="2012-07-14",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_event,
            delta=0
        )
        descends = Descends()

        family = Family(
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="",
            origin_file="",
            src=""
        )

        family_event = FamilyEvent(
            family_obj=family,
            name=FamilyEventName.MARRIAGE,
            date_obj=event_date,
            place="Town Hall",
            reason="",
            note="",
            src=""
        )

        event_witness = FamilyEventWitness(
            person_obj=witness,
            event_obj=family_event,
            kind=EventWitnessKind.WITNESS
        )
        db_session.add(event_witness)
        db_session.commit()

        assert event_witness.id is not None
        assert event_witness.person_obj.first_name == "FamilyWitness"
        assert event_witness.event_obj.name == FamilyEventName.MARRIAGE
        assert event_witness.kind == EventWitnessKind.WITNESS

    def test_family_witness_table(self, db_session: Session):
        """Test FamilyWitness junction table linking Family and Person."""
        father = Person(
            id=0,
            first_name="FamilyWithWitnessDad",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )
        mother = Person(
            id=1,
            first_name="FamilyWithWitnessMom",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        witness = Person(
            id=2,
            first_name="GeneralWitness",
            surname="Person",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        couple = Couple(father_obj=father, mother_obj=mother)

        precision = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="2015-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        marriage_date = Date(
            iso_date="2015-08-22",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision,
            delta=0
        )
        descends = Descends()

        family = Family(
            id=0,
            parents=couple,
            children=descends,
            marriage_date_obj=marriage_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            relation_kind=MaritalStatus.MARRIED,
            divorce_status=DivorceStatus.NOT_DIVORCED,
            divorce_date=None,
            comment="",
            origin_file="",
            src=""
        )

        family_witness = FamilyWitness(
            family_id=family.id,
            person_id=witness.id
        )
        db_session.add_all([family, witness, family_witness])
        db_session.commit()

        assert family_witness.id is not None
        assert family_witness.family_id == family.id
        assert family_witness.person_id == witness.id


# ============================================================================
# PERSON RELATIONS AND TITLES TESTS
# ============================================================================

class TestPersonRelationsAndTitles:
    """Test PersonRelations, PersonNonNativeRelations, and PersonTitles."""

    def test_person_relations(self, db_session: Session):
        """Test PersonRelations linking two Person objects."""
        person1 = Person(
            first_name="Person1",
            surname="Related",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        person2 = Person(
            first_name="Person2",
            surname="Related",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        relation = PersonRelations(
            person_obj=person1,
            related_person_obj=person2
        )
        db_session.add(relation)
        db_session.commit()

        assert relation.id is not None
        assert relation.person_obj.first_name == "Person1"
        assert relation.related_person_obj.first_name == "Person2"

    def test_person_non_native_relations(self, db_session: Session):
        """Test PersonNonNativeRelations linking Person and Relation."""
        person = Person(
            id=0,
            first_name="AdoptedChild",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        adoptive_father = Person(
            id=1,
            first_name="AdoptiveFather",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        adoptive_mother = Person(
            id=2,
            first_name="AdoptiveMother",
            surname="Test",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        relation = Relation(
            id=0,
            type=RelationToParentType.ADOPTION,
            father_obj=adoptive_father,
            mother_obj=adoptive_mother,
            sources="Adoption papers"
        )

        person_non_native_rel = PersonNonNativeRelations(
            person_id=person.id,
            relation_id=relation.id
        )
        db_session.add_all([person, relation, person_non_native_rel])
        db_session.commit()

        assert person_non_native_rel.id is not None
        assert person_non_native_rel.person_id == person.id
        assert person_non_native_rel.relation_id == relation.id

    def test_person_titles(self, db_session: Session):
        """Test PersonTitles linking Person and Titles."""
        person = Person(
            first_name="Noble",
            surname="Person",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="Nobility",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        precision_start = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1800-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        start_date = Date(
            iso_date="1800-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_start,
            delta=0
        )
        precision_end = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1850-12-31",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        end_date = Date(
            iso_date="1850-12-31",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_end,
            delta=0
        )

        title = Titles(
            name="Count",
            ident="count_01",
            place="France",
            date_start_obj=start_date,
            date_end_obj=end_date,
            nth=1
        )

        person_title = PersonTitles(
            person_obj=person,
            title_obj=title
        )
        db_session.add(person_title)
        db_session.commit()

        assert person_title.id is not None
        assert person_title.person_obj.first_name == "Noble"
        assert person_title.title_obj.name == "Count"

    def test_multiple_titles_for_person(self, db_session: Session):
        """Test a person having multiple titles over time."""
        person = Person(
            first_name="MultiTitle",
            surname="Noble",
            occ=0,
            image="",
            public_name="",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

        # First title: Baron
        precision_baron_start = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1700-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        baron_start = Date(
            iso_date="1700-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_baron_start,
            delta=0
        )
        precision_baron_end = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1750-12-31",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        baron_end = Date(
            iso_date="1750-12-31",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_baron_end,
            delta=0
        )
        baron_title = Titles(
            name="Baron",
            ident="baron_01",
            place="England",
            date_start_obj=baron_start,
            date_end_obj=baron_end,
            nth=1
        )

        # Second title: Earl
        precision_earl_start = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1751-01-01",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        earl_start = Date(
            iso_date="1751-01-01",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_earl_start,
            delta=0
        )
        precision_earl_end = Precision(
            precision_level=DatePrecision.SURE,
            iso_date="1800-12-31",
            calendar=Calendar.GREGORIAN,
            delta=0
        )
        earl_end = Date(
            iso_date="1800-12-31",
            calendar=Calendar.GREGORIAN,
            precision_obj=precision_earl_end,
            delta=0
        )
        earl_title = Titles(
            name="Earl",
            ident="earl_01",
            place="England",
            date_start_obj=earl_start,
            date_end_obj=earl_end,
            nth=2
        )

        person_title1 = PersonTitles(person_obj=person, title_obj=baron_title)
        person_title2 = PersonTitles(person_obj=person, title_obj=earl_title)

        db_session.add_all([person_title1, person_title2])
        db_session.commit()

        # Query all titles for the person
        person_titles = db_session.query(
            PersonTitles).filter_by(person_id=person.id).all()
        assert len(person_titles) == 2

        titles = [pt.title_obj for pt in person_titles]
        title_names = [t.name for t in titles]
        assert "Baron" in title_names
        assert "Earl" in title_names
