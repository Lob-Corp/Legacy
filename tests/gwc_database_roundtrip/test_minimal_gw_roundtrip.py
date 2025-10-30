"""
Comprehensive roundtrip tests for minimal.gw.

Tests EVERY field for EVERY person in minimal.gw:
- GW file -> gwc.py -> Database -> Repository -> Verification
"""

import pytest
import tempfile
import os
import subprocess
from pathlib import Path

from database.sqlite_database_service import SQLiteDatabaseService
from libraries.calendar_date import CalendarDate
from libraries.person import Sex
from repositories.person_repository import PersonRepository
from repositories.family_repository import FamilyRepository
from libraries.events import PersBirth


TEST_ASSETS_DIR = Path(__file__).parent.parent.parent / "test_assets"
GW_FILE = TEST_ASSETS_DIR / "minimal.gw"


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
    """Parse minimal.gw and save to database."""
    gwc_script = Path(
        __file__).parent.parent.parent / "src" / "script" / "gwc.py"
    venv_python = Path(
        __file__).parent.parent.parent / "venv" / "bin" / "python"
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


class TestMinimalGwPersons:
    """Test all persons from minimal.gw."""

    def test_person_count(self, db_with_data):
        """Verify exactly 1 person in minimal.gw."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        assert len(persons) == 1, "minimal.gw should have exactly 1 person"

    def test_john_index(self, db_with_data):
        """Verify John's index."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]
        assert john.index == 0, "John should have index 0"

    def test_john_first_name(self, db_with_data):
        """Verify John's first name."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]
        assert john.first_name == "John", "First name should be 'John'"

    def test_john_surname(self, db_with_data):
        """Verify John's surname."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]
        assert john.surname == "0", "Surname should be '0'"

    def test_john_sex(self, db_with_data):
        """Verify John's sex."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]
        # Default sex when not specified
        assert john.sex == Sex.NEUTER, \
            "Sex should be valid"

    def test_john_occ(self, db_with_data):
        """Verify John's occurrence number."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]
        assert john.occ == 0, "Occurrence should be 0"

    def test_john_occupation(self, db_with_data):
        """Verify John's occupation."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]
        assert john.occupation == "", "Occupation should be empty"

    def test_john_image(self, db_with_data):
        """Verify John's image."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]
        assert john.image == "", "Image should be empty"

    def test_john_public_name(self, db_with_data):
        """Verify John's public name."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]
        assert john.public_name == "", "Public name should be empty"


class TestMinimalGwPersonalEvents:
    """Test personal events for John."""

    def test_john_has_one_birth_event(self, db_with_data):
        """Verify John has exactly one birth event."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]

        birth_events = [
            e for e in john.personal_events
            if isinstance(e.name, PersBirth)
        ]
        assert len(birth_events) == 1, "John should have exactly 1 birth event"

    def test_john_birth_date(self, db_with_data):
        """Verify John's birth date."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]

        birth_events = [
            e for e in john.personal_events
            if isinstance(e.name, PersBirth)
        ]
        birth = birth_events[0]

        assert birth.date is not None, "Birth date should not be None"
        assert isinstance(
            birth.date, CalendarDate), "Birth DMY should not be None"
        assert birth.date.dmy.year == 1990, "Birth year should be 1990"
        assert birth.date.dmy.month == 0, "Birth month should be 0 (year only)"
        assert birth.date.dmy.day == 0, "Birth day should be 0 (year only)"

    def test_john_birth_place(self, db_with_data):
        """Verify John's birth place."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]

        birth_events = [
            e for e in john.personal_events
            if isinstance(e.name, PersBirth)
        ]
        birth = birth_events[0]

        assert birth.place == "Paris", "Birth place should be 'Paris'"

    def test_john_birth_source(self, db_with_data):
        """Verify John's birth source."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]

        birth_events = [
            e for e in john.personal_events
            if isinstance(e.name, PersBirth)
        ]
        birth = birth_events[0]

        assert birth.src == "Source", "Birth source should be 'Source'"

    def test_john_birth_witnesses(self, db_with_data):
        """Verify John's birth event has no witnesses."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]

        birth_events = [
            e for e in john.personal_events
            if isinstance(e.name, PersBirth)
        ]
        birth = birth_events[0]

        assert len(
            birth.witnesses) == 0, "Birth event should have no witnesses"


class TestMinimalGwFamilies:
    """Test families in minimal.gw."""

    def test_no_families(self, db_with_data):
        """Verify minimal.gw has no families."""
        family_repo = FamilyRepository(db_with_data)
        families = family_repo.get_all_families()
        assert len(families) == 0, "minimal.gw should have no families"


class TestMinimalGwFieldCompleteness:
    """Test that all fields are preserved in roundtrip."""

    def test_person_all_fields_present(self, db_with_data):
        """Verify all Person fields exist after roundtrip."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]

        # Check all essential fields exist
        assert hasattr(john, 'index')
        assert hasattr(john, 'first_name')
        assert hasattr(john, 'surname')
        assert hasattr(john, 'occ')
        assert hasattr(john, 'image')
        assert hasattr(john, 'public_name')
        assert hasattr(john, 'qualifiers')
        assert hasattr(john, 'aliases')
        assert hasattr(john, 'first_names_aliases')
        assert hasattr(john, 'surname_aliases')
        assert hasattr(john, 'titles')
        assert hasattr(john, 'non_native_parents_relation')
        assert hasattr(john, 'related_persons')
        assert hasattr(john, 'occupation')
        assert hasattr(john, 'sex')
        assert hasattr(john, 'access_right')
        assert hasattr(john, 'birth_date')
        assert hasattr(john, 'birth_place')
        assert hasattr(john, 'birth_note')
        assert hasattr(john, 'birth_src')
        assert hasattr(john, 'baptism_date')
        assert hasattr(john, 'baptism_place')
        assert hasattr(john, 'baptism_note')
        assert hasattr(john, 'baptism_src')
        assert hasattr(john, 'death_status')
        assert hasattr(john, 'death_place')
        assert hasattr(john, 'death_note')
        assert hasattr(john, 'death_src')
        assert hasattr(john, 'burial')
        assert hasattr(john, 'burial_place')
        assert hasattr(john, 'burial_note')
        assert hasattr(john, 'burial_src')
        assert hasattr(john, 'personal_events')
        assert hasattr(john, 'notes')
        assert hasattr(john, 'src')
        assert hasattr(john, 'families')

    def test_personal_event_all_fields_present(self, db_with_data):
        """Verify all PersonalEvent fields exist after roundtrip."""
        person_repo = PersonRepository(db_with_data)
        persons = person_repo.get_all_persons()
        john = persons[0]

        birth_events = [
            e for e in john.personal_events
            if isinstance(e.name, PersBirth)
        ]
        birth = birth_events[0]

        assert hasattr(birth, 'name')
        assert hasattr(birth, 'date')
        assert hasattr(birth, 'place')
        assert hasattr(birth, 'reason')
        assert hasattr(birth, 'note')
        assert hasattr(birth, 'src')
        assert hasattr(birth, 'witnesses')
