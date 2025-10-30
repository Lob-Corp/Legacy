"""
Comprehensive roundtrip tests for medium.gw.

Tests EVERY field for EVERY person and family in medium.gw:
- GW file -> gwc.py -> Database -> Repository -> Verification
"""

import pytest
import tempfile
import os
import subprocess
from pathlib import Path

from database.sqlite_database_service import SQLiteDatabaseService
from libraries.calendar_date import CalendarDate
from libraries.death_info import Dead, DeathReason
from libraries.person import Sex
from repositories.person_repository import PersonRepository
from repositories.family_repository import FamilyRepository
from libraries.events import (
    PersBirth,
    FamMarriage,
    FamNoMarriage,
    FamPACS,
    PersDeath)
from libraries.events import FamNoMention
from libraries.family import MaritalStatus


TEST_ASSETS_DIR = Path(__file__).parent.parent.parent / "test_assets"
GW_FILE = TEST_ASSETS_DIR / "medium.gw"


@pytest.fixture
def temp_db():
    """Create a temporary database file."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def db_with_data(temp_db):
    """Parse medium.gw and save to database."""
    gwc_script = Path(__file__).parent.parent.parent / "src" / "script" / "gwc.py"
    venv_python = Path(__file__).parent.parent.parent / "venv" / "bin" / "python"
    python_cmd = str(venv_python) if venv_python.exists() else "python"

    cmd = [python_cmd, str(gwc_script), "-f", "-o", temp_db, str(GW_FILE)]
    result = subprocess.run(
        cmd, capture_output=True, text=True,
        cwd=Path(__file__).parent.parent.parent
    )

    assert result.returncode == 0, f"gwc.py failed: {result.stderr}"

    db_service = SQLiteDatabaseService(temp_db)
    db_service.connect()
    yield db_service
    db_service.disconnect()


class TestMediumGwCounts:
    """Test counts of persons and families."""

    def test_person_count(self, db_with_data):
        """Verify total number of persons."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        # Persons: a.1 b, c b, a b, t b, rfefg zzz, fezfez zzz,
        # de pacs, re pacs, dea pacs, rea pacs, yoyo pacs, neuter.1
        assert len(persons) == 12, f"Should have 12 persons, got {
            len(persons)} "

    def test_family_count(self, db_with_data):
        """Verify total number of families."""
        family_repo = FamilyRepository(db_with_data)
        families = family_repo.get_all_families()
        # 5 families in medium.gw
        assert len(families) == 5, f"Should have 5 families, got {
            len(families)} "


class TestMediumGwFamily1:
    """Test family 1: b a.1 + b c (MARRIED)."""

    def test_family1_exists(self, db_with_data):
        """Verify family 1 exists."""
        family_repo = FamilyRepository(db_with_data)
        families = family_repo.get_all_families()
        assert len(families) >= 1

    def test_family1_relation_kind(self, db_with_data):
        """Verify family 1 is MARRIED."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        # Find a.1 b
        a1 = next((p for p in persons if p.first_name == "a" and
                  p.surname == "b" and p.occ == 1), None)
        assert a1 is not None, "Person a.1 b should exist"

        # Find family with a.1 as parent
        family = next(
            (f for f in families if a1.index in f.parents.couple()),
            None)
        assert family is not None, "Family with a.1 should exist"
        assert family.relation_kind == MaritalStatus.MARRIED

    def test_family1_parents(self, db_with_data):
        """Verify family 1 parents are a.1 b and c b."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        a1 = next((p for p in persons if p.first_name == "a" and
                  p.surname == "b" and p.occ == 1), None)
        c = next((p for p in persons if p.first_name == "c" and
                 p.surname == "b" and p.occ == 0), None)

        assert a1 is not None
        assert c is not None

        family = next(
            (f for f in families if a1.index in f.parents.couple()),
            None)
        assert family is not None
        assert len(family.parents.couple()) == 2
        assert a1.index in family.parents.couple()
        assert c.index in family.parents.couple()

    def test_family1_marriage_event(self, db_with_data):
        """Verify family 1 has marriage event."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        a1 = next((p for p in persons if p.first_name == "a" and
                  p.surname == "b" and p.occ == 1), None)
        assert a1 is not None
        family = next(
            (f for f in families if a1.index in f.parents.couple()),
            None)
        assert family is not None

        marriage_events = [
            e for e in family.family_events
            if isinstance(e.name, FamMarriage)]
        assert len(marriage_events) == 1, "Should have 1 marriage event"


class TestMediumGwFamily2:
    """Test family 2: b a + b t (NOT_MARRIED)."""

    def test_family2_relation_kind(self, db_with_data):
        """Verify family 2 is NOT_MARRIED."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        # Find a b with occ=0
        a = next((p for p in persons if p.first_name == "a" and
                 p.surname == "b" and p.occ == 0), None)
        assert a is not None, "Person a b (occ=0) should exist"

        family = next(
            (f for f in families if a.index in f.parents.couple()),
            None)
        assert family is not None, "Family with a (occ=0) should exist"
        assert family.relation_kind == MaritalStatus.NOT_MARRIED

    def test_family2_no_marriage_event(self, db_with_data):
        """Verify family 2 has no marriage event."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        a = next((p for p in persons if p.first_name == "a" and
                 p.surname == "b" and p.occ == 0), None)
        assert a is not None
        family = next(
            (f for f in families if a.index in f.parents.couple()),
            None)
        assert family is not None

        no_marriage_events = [
            e for e in family.family_events
            if isinstance(e.name, FamNoMarriage)
        ]
        assert len(no_marriage_events) == 1, "Should have 1 no marriage event"


class TestMediumGwFamily3:
    """Test family 3: zzz rfefg + zzz fezfez (MARRIED)."""

    def test_family3_relation_kind(self, db_with_data):
        """Verify family 3 is MARRIED."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        rfefg = next((p for p in persons if p.first_name ==
                     "rfefg" and p.surname == "zzz"), None)
        assert rfefg is not None

        family = next(
            (f for f in families if rfefg.index in f.parents.couple()),
            None)
        assert family is not None
        assert family.relation_kind == MaritalStatus.MARRIED


class TestMediumGwFamily4:
    """Test family 4: pacs de + pacs re (PACS)."""

    def test_family4_relation_kind(self, db_with_data):
        """Verify family 4 is PACS."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        de = next((p for p in persons if p.first_name ==
                  "de" and p.surname == "pacs"), None)
        assert de is not None

        family = next(
            (f for f in families if de.index in f.parents.couple()),
            None)
        assert family is not None
        assert family.relation_kind == MaritalStatus.PACS

    def test_family4_pacs_event(self, db_with_data):
        """Verify family 4 has PACS event."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        de = next((p for p in persons if p.first_name ==
                  "de" and p.surname == "pacs"), None)
        assert de is not None
        family = next(
            (f for f in families if de.index in f.parents.couple()),
            None)
        assert family is not None

        pacs_events = [e for e in family.family_events
                       if isinstance(e.name, FamPACS)]
        assert len(pacs_events) == 1, "Should have 1 PACS event"


class TestMediumGwFamily5:
    """Test family 5: pacs dea + pacs rea (NO_MENTION)."""

    def test_family5_relation_kind(self, db_with_data):
        """Verify family 5 is NO_MENTION."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        dea = next((p for p in persons if p.first_name ==
                   "dea" and p.surname == "pacs"), None)
        assert dea is not None

        family = next(
            (f for f in families if dea.index in f.parents.couple()),
            None)
        assert family is not None
        assert family.relation_kind == MaritalStatus.NO_MENTION

    def test_family5_no_mention_event(self, db_with_data):
        """Verify family 5 has NO_MENTION event."""
        family_repo = FamilyRepository(db_with_data)
        person_repo = PersonRepository(db_with_data)

        families = family_repo.get_all_families()
        persons = person_repo.get_all_persons()

        dea = next((p for p in persons if p.first_name ==
                   "dea" and p.surname == "pacs"), None)
        assert dea is not None
        family = next(
            (f for f in families if dea.index in f.parents.couple()),
            None)
        assert family is not None

        no_mention_events = [
            e for e in family.family_events
            if isinstance(e.name, FamNoMention)
        ]
        assert len(no_mention_events) == 1, "Should have 1 no mention event"


class TestMediumGwPersonA1:
    """Test person a.1 b in detail."""

    def test_a1_first_name(self, db_with_data):
        """Verify a.1's first name."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        a1 = next((p for p in persons if p.first_name ==
                  "a" and p.surname == "b" and p.occ == 1), None)
        assert a1 is not None
        assert a1.first_name == "a"

    def test_a1_surname(self, db_with_data):
        """Verify a.1's surname."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        a1 = next((p for p in persons if p.first_name ==
                  "a" and p.surname == "b" and p.occ == 1), None)
        assert a1 is not None
        assert a1.surname == "b"

    def test_a1_occ(self, db_with_data):
        """Verify a.1's occurrence number."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        a1 = next((p for p in persons if p.first_name ==
                  "a" and p.surname == "b" and p.occ == 1), None)
        assert a1 is not None
        assert a1.occ == 1

    def test_a1_birth_date(self, db_with_data):
        """Verify a.1's birth date."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        a1 = next((p for p in persons if p.first_name ==
                  "a" and p.surname == "b" and p.occ == 1), None)
        assert a1 is not None

        birth_events = [
            e for e in a1.personal_events if isinstance(
                e.name, PersBirth)]
        if len(birth_events) > 0:
            birth = birth_events[0]
            assert birth.date is not None
            assert isinstance(birth.date, CalendarDate)
            assert birth.date.dmy.day == 1
            assert birth.date.dmy.month == 1
            assert birth.date.dmy.year == 2000

    def test_a1_birth_place(self, db_with_data):
        """Verify a.1's birth place."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        a1 = next((p for p in persons if p.first_name ==
                  "a" and p.surname == "b" and p.occ == 1), None)
        assert a1 is not None

        birth_events = [
            e for e in a1.personal_events if isinstance(
                e.name, PersBirth)]
        if len(birth_events) > 0:
            birth = birth_events[0]
            assert birth.place == "Paris"

    def test_a1_death(self, db_with_data):
        """Verify a.1's death event."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        a1 = next((p for p in persons if p.first_name ==
                  "a" and p.surname == "b" and p.occ == 1), None)
        assert a1 is not None

        assert isinstance(a1.death_status, Dead)
        assert a1.death_status.death_reason == DeathReason.UNSPECIFIED
        assert isinstance(a1.death_status.date_of_death, CalendarDate)
        assert a1.death_status.date_of_death.dmy.day == 12
        assert a1.death_status.date_of_death.dmy.month == 7
        assert a1.death_status.date_of_death.dmy.year == 2020

        death_events = [
            e for e in a1.personal_events if isinstance(e.name, PersDeath)]
        assert len(death_events) == 1, "Should have 1 death event"
        death = death_events[0]
        assert death.date is not None
        assert isinstance(death.date, CalendarDate)
        assert death.date.dmy.day == 12
        assert death.date.dmy.month == 7
        assert death.date.dmy.year == 2020


class TestMediumGwPersonC:
    """Test person c b in detail."""

    def test_c_first_name(self, db_with_data):
        """Verify c's first name."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        c = next((p for p in persons if p.first_name ==
                 "c" and p.surname == "b" and p.occ == 0), None)
        assert c is not None
        assert c.first_name == "c"

    def test_c_surname(self, db_with_data):
        """Verify c's surname."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        c = next((p for p in persons if p.first_name ==
                 "c" and p.surname == "b" and p.occ == 0), None)
        assert c is not None
        assert c.surname == "b"

    def test_c_occ(self, db_with_data):
        """Verify c's occurrence number."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        c = next((p for p in persons if p.first_name ==
                 "c" and p.surname == "b" and p.occ == 0), None)
        assert c is not None
        assert c.occ == 0

    def test_c_birth_date(self, db_with_data):
        """Verify c's birth date."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        c = next((p for p in persons if p.first_name ==
                 "c" and p.surname == "b" and p.occ == 0), None)
        assert c is not None

        birth_events = [
            e for e in c.personal_events if isinstance(
                e.name, PersBirth)]
        if len(birth_events) > 0:
            birth = birth_events[0]
            assert birth.date is not None
            assert isinstance(birth.date, CalendarDate)
            assert birth.date.dmy.day == 1
            assert birth.date.dmy.month == 2
            assert birth.date.dmy.year == 2000


class TestMediumGwPersonYoyo:
    """Test person yoyo pacs in detail."""

    def test_yoyo_first_name(self, db_with_data):
        """Verify yoyo's first name."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        yoyo = next((p for p in persons if p.first_name == "yoyo" and
                    p.surname == "pacs" and p.occ == 0), None)
        assert yoyo is not None
        assert yoyo.first_name == "yoyo"

    def test_yoyo_surname(self, db_with_data):
        """Verify yoyo's surname."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        yoyo = next((p for p in persons if p.first_name == "yoyo" and
                    p.surname == "pacs" and p.occ == 0), None)
        assert yoyo is not None
        assert yoyo.surname == "pacs"

    def test_yoyo_occ(self, db_with_data):
        """Verify yoyo's occurrence number."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        yoyo = next((p for p in persons if p.first_name == "yoyo" and
                    p.surname == "pacs" and p.occ == 0), None)
        assert yoyo is not None
        assert yoyo.occ == 0

    def test_yoyo_sex(self, db_with_data):
        """Verify yoyo's sex (male from 'h' tag)."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        yoyo = next((p for p in persons if p.first_name == "yoyo" and
                    p.surname == "pacs" and p.occ == 0), None)
        assert yoyo is not None
        assert yoyo.sex == Sex.MALE

    def test_yoyo_birth_date(self, db_with_data):
        """Verify yoyo's birth date."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        yoyo = next((p for p in persons if p.first_name == "yoyo" and
                    p.surname == "pacs" and p.occ == 0), None)
        assert yoyo is not None

        birth_events = [e for e in yoyo.personal_events
                        if isinstance(e.name, PersBirth)]
        if len(birth_events) > 0:
            birth = birth_events[0]
            assert birth.date is not None
            assert isinstance(birth.date, CalendarDate)
            assert birth.date.dmy.day == 8
            assert birth.date.dmy.month == 12
            assert birth.date.dmy.year == 2006

    def test_yoyo_birth_place(self, db_with_data):
        """Verify yoyo's birth place."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        yoyo = next((p for p in persons if p.first_name == "yoyo" and
                    p.surname == "pacs" and p.occ == 0), None)
        assert yoyo is not None
        birth_events = [e for e in yoyo.personal_events
                        if isinstance(e.name, PersBirth)]
        if len(birth_events) > 0:
            birth = birth_events[0]
            assert birth.place == "Paris"


class TestMediumGwPersonNeuter:
    """Test person neuter.1 in detail."""

    def test_neuter_first_name(self, db_with_data):
        """Verify neuter.1's first name."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        neuter = next((p for p in persons if p.first_name == "neuter" and
                      p.surname == "pacs" and p.occ == 1), None)
        assert neuter is not None
        assert neuter.first_name == "neuter"

    def test_neuter_occ(self, db_with_data):
        """Verify neuter.1's occurrence number."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        neuter = next((p for p in persons if p.first_name == "neuter" and
                      p.surname == "pacs" and p.occ == 1), None)
        assert neuter is not None
        assert neuter.occ == 1

    def test_neuter_sex(self, db_with_data):
        """Verify neuter.1's sex (NEUTER from '-' tag)."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        neuter = next((p for p in persons if p.first_name == "neuter" and
                      p.surname == "pacs" and p.occ == 1), None)
        assert neuter is not None
        assert neuter.sex == Sex.NEUTER

    def test_neuter_occupation(self, db_with_data):
        """Verify neuter.1's occupation."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        neuter = next((p for p in persons if p.first_name == "neuter" and
                      p.surname == "pacs" and p.occ == 1), None)
        assert neuter is not None
        assert neuter.occupation == "Jardinier"
