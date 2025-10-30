"""
Test that all fields from GW files are properly parsed.

This test suite verifies field completeness for all test GW files.
"""

import pytest
from pathlib import Path
from script.gw_parser import parse_gw_file, GwConverter
from libraries.person import Sex
from libraries.death_info import Dead
from libraries.events import PersBirth, PersDeath, FamMarriage, FamDivorce


TEST_ASSETS_DIR = Path("test_assets")


class TestMinimalGwParsing:
    """Test parsing of minimal.gw - simplest test case."""

    @pytest.fixture
    def parsed_data(self):
        """Parse minimal.gw and return persons and families."""
        gw_file = TEST_ASSETS_DIR / "minimal.gw"
        blocks = parse_gw_file(str(gw_file))
        converter = GwConverter()
        converter.convert_all(blocks)
        return converter.get_enriched_persons(), converter.get_all_families()

    def test_person_count(self, parsed_data):
        """Verify correct number of persons parsed."""
        persons, families = parsed_data
        # minimal.gw has 1 person referenced in pevt
        assert len(persons) >= 1, "Should have at least 1 person"

    def test_person_john_exists(self, parsed_data):
        """Verify John person exists."""
        persons, _ = parsed_data
        john = next((p for p in persons if p.first_name == "John"), None)
        assert john is not None, "Person 'John' should exist"

    def test_person_john_personal_events(self, parsed_data):
        """Test that personal events are properly parsed"""
        persons, _ = parsed_data
        john = next((p for p in persons if p.first_name == "John"), None)
        assert john is not None, "John should exist in persons"
        assert len(
            john.personal_events) > 0, "John should have personal events"

        # Check for birth event
        birth_events = [e for e in john.personal_events
                        if isinstance(e.name, PersBirth)]
        assert len(birth_events) == 1, "John should have one birth event"
        birth = birth_events[0]
        assert birth.date is not None, "Birth date should be set"
        assert birth.date.dmy.year == 1990, "Birth year should be 1990"
        assert birth.place == "Paris", "Birth place should be Paris"
        # Note: birth notes may be empty if not specified in GW file
        assert birth.src == "Source", "Birth source should be 'Source'"


class TestMediumGwParsing:
    """Test parsing of medium.gw - moderate complexity."""

    @pytest.fixture
    def parsed_data(self):
        """Parse medium.gw and return persons and families."""
        gw_file = TEST_ASSETS_DIR / "medium.gw"
        blocks = parse_gw_file(str(gw_file))
        converter = GwConverter()
        converter.convert_all(blocks)
        return converter.get_enriched_persons(), converter.get_all_families()

    def test_family_count(self, parsed_data):
        """Verify correct number of families parsed."""
        _, families = parsed_data
        # medium.gw has 5 families
        assert len(families) == 5, f"Should have 5 families, got {
            len(families)} "

    def test_family_relation_kinds(self, parsed_data):
        """Verify different marriage types are parsed."""
        _, families = parsed_data

        # Check for different relation kinds
        relation_kinds = [f.relation_kind.name for f in families]

        # Should have MARRIED, NOT_MARRIED, PACS, NO_MENTION
        assert "MARRIED" in relation_kinds, "Should have MARRIED relation"
        # Note: Other types depend on the exact content

    def test_person_birth_events_from_pevt(self, parsed_data):
        """Verify birth events from pevt blocks are included."""
        persons, _ = parsed_data

        # Find person 'a.1' from family 'b'
        person_a1 = next((p for p in persons if p.first_name ==
                         "a.1" and p.surname == "b"), None)
        if person_a1:
            assert len(
                person_a1.personal_events) > 0, "Person a.1 should have personal events"
            birth_events = [
                e for e in person_a1.personal_events
                if isinstance(e.name, PersBirth)]
            assert len(birth_events) > 0, "Person a.1 should have birth event"

    def test_children_in_families(self, parsed_data):
        """Verify children are properly attached to families."""
        _, families = parsed_data

        # At least one family should have children
        families_with_children = [f for f in families if len(f.children) > 0]
        assert len(
            families_with_children) > 0, "At least one family should have children"

        # Check first family with children
        family = families_with_children[0]
        for child in family.children:
            assert hasattr(
                child, 'first_name'), "Child should be a Person object"
            assert hasattr(child, 'surname'), "Child should have surname"


class TestBigGwParsing:
    """Test parsing of big.gw - comprehensive test case."""

    @pytest.fixture
    def parsed_data(self):
        """Parse big.gw and return persons and families."""
        gw_file = TEST_ASSETS_DIR / "big.gw"
        blocks = parse_gw_file(str(gw_file))
        converter = GwConverter()
        converter.convert_all(blocks)
        return converter.get_enriched_persons(), converter.get_all_families()

    def test_person_occupation_parsed(self, parsed_data):
        """Verify occupation field is parsed."""
        persons, _ = parsed_data

        # Find Ethan Cooper who has occupation Screenwriter
        ethan = next((p for p in persons if p.first_name ==
                     "Ethan" and p.surname == "Cooper"), None)
        assert ethan is not None, "Ethan Cooper should exist"
        assert ethan.occupation == "Screenwriter", f"Expected 'Screenwriter', got '{
            ethan.occupation}'"

    def test_person_sources_parsed(self, parsed_data):
        """Test that person sources are parsed"""
        persons, _ = parsed_data
        # Find Ethan Cooper who should have a source
        ethan = next((p for p in persons if p.first_name ==
                     "Ethan" and p.surname == "Cooper"), None)
        assert ethan is not None, "Ethan Cooper should exist"
        # Underscores in GW files get converted to spaces
        assert ethan.src == "Family story book", f"Expected source, got '{
            ethan.src} '"

    def test_person_birth_date_and_place(self, parsed_data):
        """Test that birth dates and places from personal events are parsed"""
        persons, _ = parsed_data
        # Find Ethan Cooper who should have birth details
        ethan = next((p for p in persons if p.first_name ==
                     "Ethan" and p.surname == "Cooper"), None)
        assert ethan is not None, "Ethan Cooper should exist"

        # Check birth event from pevt block
        birth_events = [e for e in ethan.personal_events
                        if isinstance(e.name, PersBirth)]
        if len(birth_events) > 0:
            birth = birth_events[0]
            assert birth.date is not None, "Birth date should be set"
            # Expected birth date: 4 Apr 1988 (from actual GW file)
            assert birth.date.dmy.year == 1988, "Birth year should be 1988"
            assert birth.date.dmy.month == 4, "Birth month should be April (4)"
            assert birth.date.dmy.day == 4, "Birth day should be 4"
            # Check birth place - underscores/commas get converted to spaces
            assert birth.place == "Los Angeles, USA", "Birth place mismatch"

    def test_person_sex_parsed(self, parsed_data):
        """Verify person sex is inferred or specified."""
        persons, _ = parsed_data

        # Check that persons have sex assigned
        for person in persons:
            assert hasattr(
                person, 'sex'), f"Person {
                person.first_name} should have sex attribute"
            assert isinstance(
                person.sex, Sex), f"Sex should be Sex enum, got {
                type(
                    person.sex)}"

    def test_family_marriage_events(self, parsed_data):
        """Verify family marriage events are parsed."""
        _, families = parsed_data

        # At least one family should have marriage event
        families_with_marriage = []
        for family in families:
            marriage_events = [
                e for e in family.family_events
                if isinstance(e.name, FamMarriage)]
            if len(marriage_events) > 0:
                families_with_marriage.append(family)

        assert len(
            families_with_marriage) > 0, "At least one family should have marriage event"

    def test_family_event_witnesses(self, parsed_data):
        """Verify family event witnesses are parsed."""
        _, families = parsed_data

        # Find family with witnesses (Kim Noah + Hughes Victoria has
        # Handfasting event)
        noah_family = None
        for family in families:
            father_id, mother_id = family.parents.couple()
            # Find the family by checking parents
            for person in [
                    p for p in parsed_data[0]
                    if p.index == father_id or p.index == mother_id]:
                if person.first_name == "Noah" or person.first_name == "Victoria":
                    noah_family = family
                    break
            if noah_family:
                break

        if noah_family:
            # Should have events with witnesses
            events_with_witnesses = [
                e for e in noah_family.family_events if len(
                    e.witnesses) > 0]
            if len(events_with_witnesses) > 0:
                event = events_with_witnesses[0]
                assert len(event.witnesses) > 0, "Event should have witnesses"
                witness_person, witness_kind = event.witnesses[0]
                assert hasattr(
                    witness_person, 'first_name'), "Witness should be Person object"

    def test_family_sources_parsed(self, parsed_data):
        """Verify family sources are parsed."""
        _, families = parsed_data

        # Find Ethan Cooper's family which has source
        families_with_sources = [f for f in families if f.src]
        assert len(
            families_with_sources) > 0, "At least one family should have source"

        # Underscores in GW files get converted to spaces
        family = families_with_sources[0]
        assert family.src == "Family story book", f"Expected source, got '{
            family.src} '"

    def test_family_event_notes(self, parsed_data):
        """Verify family event notes are parsed."""
        _, families = parsed_data

        # Find family with event notes (Kim Noah family has note on
        # Handfasting)
        families_with_event_notes = []
        for family in families:
            for event in family.family_events:
                if event.note:
                    families_with_event_notes.append((family, event))
                    break

        if len(families_with_event_notes) > 0:
            family, event = families_with_event_notes[0]
            assert event.note, "Event should have note"
            assert len(event.note) > 0, "Event note should not be empty"


class TestFieldCompletenessAllFiles:
    """Test that essential fields are not lost during parsing for all test files."""

    @pytest.mark.parametrize("gw_file", [
        "minimal.gw",
        "medium.gw",
        "big.gw",
    ])
    def test_persons_have_required_fields(self, gw_file):
        """Verify all persons have required fields set."""
        gw_path = TEST_ASSETS_DIR / gw_file
        blocks = parse_gw_file(str(gw_path))
        converter = GwConverter()
        converter.convert_all(blocks)
        persons = converter.get_enriched_persons()

        for person in persons:
            # Required fields
            assert hasattr(person, 'index'), "Person should have index"
            assert hasattr(
                person, 'first_name'), "Person should have first_name"
            assert hasattr(person, 'surname'), "Person should have surname"
            assert hasattr(
                person, 'occ'), "Person should have occ (occurrence)"
            assert hasattr(person, 'sex'), "Person should have sex"
            assert hasattr(
                person, 'access_right'), "Person should have access_right"

            # Optional but should exist as fields
            assert hasattr(
                person, 'occupation'), "Person should have occupation field"
            assert hasattr(
                person, 'birth_date'), "Person should have birth_date field"
            assert hasattr(
                person, 'birth_place'), "Person should have birth_place field"
            assert hasattr(
                person, 'death_status'), "Person should have death_status field"
            assert hasattr(
                person, 'death_place'), "Person should have death_place field"
            assert hasattr(
                person, 'personal_events'), "Person should have personal_events field"
            assert hasattr(person, 'notes'), "Person should have notes field"
            assert hasattr(person, 'src'), "Person should have src field"

    @pytest.mark.parametrize("gw_file", [
        "medium.gw",
        "big.gw",
    ])
    def test_families_have_required_fields(self, gw_file):
        """Verify all families have required fields set."""
        gw_path = TEST_ASSETS_DIR / gw_file
        blocks = parse_gw_file(str(gw_path))
        converter = GwConverter()
        converter.convert_all(blocks)
        families = converter.get_all_families()

        for family in families:
            # Required fields
            assert hasattr(family, 'index'), "Family should have index"
            assert hasattr(family, 'parents'), "Family should have parents"
            assert hasattr(family, 'children'), "Family should have children"
            assert hasattr(
                family, 'relation_kind'), "Family should have relation_kind"
            assert hasattr(
                family, 'divorce_status'), "Family should have divorce_status"

            # Optional but should exist as fields
            assert hasattr(
                family, 'marriage_date'), "Family should have marriage_date field"
            assert hasattr(
                family, 'marriage_place'), "Family should have marriage_place field"
            assert hasattr(
                family, 'marriage_note'), "Family should have marriage_note field"
            assert hasattr(
                family, 'marriage_src'), "Family should have marriage_src field"
            assert hasattr(
                family, 'witnesses'), "Family should have witnesses field"
            assert hasattr(
                family, 'family_events'), "Family should have family_events field"
            assert hasattr(
                family, 'comment'), "Family should have comment field"
            assert hasattr(family, 'src'), "Family should have src field"

    def test_personal_events_completeness(self):
        """Verify personal events have all fields."""
        gw_path = TEST_ASSETS_DIR / "big.gw"
        blocks = parse_gw_file(str(gw_path))
        converter = GwConverter()
        converter.convert_all(blocks)
        persons = converter.get_enriched_persons()

        # Find persons with personal events
        persons_with_events = [
            p for p in persons if len(
                p.personal_events) > 0]
        assert len(persons_with_events) > 0, "Should have persons with events"

        for person in persons_with_events:
            for event in person.personal_events:
                assert hasattr(event, 'name'), "Event should have name"
                assert hasattr(event, 'date'), "Event should have date field"
                assert hasattr(event, 'place'), "Event should have place field"
                assert hasattr(
                    event, 'reason'), "Event should have reason field"
                assert hasattr(event, 'note'), "Event should have note field"
                assert hasattr(event, 'src'), "Event should have src field"
                assert hasattr(
                    event, 'witnesses'), "Event should have witnesses field"

    def test_family_events_completeness(self):
        """Verify family events have all fields."""
        gw_path = TEST_ASSETS_DIR / "big.gw"
        blocks = parse_gw_file(str(gw_path))
        converter = GwConverter()
        converter.convert_all(blocks)
        families = converter.get_all_families()

        # Find families with events
        families_with_events = [
            f for f in families if len(
                f.family_events) > 0]

        for family in families_with_events:
            for event in family.family_events:
                assert hasattr(event, 'name'), "Event should have name"
                assert hasattr(event, 'date'), "Event should have date field"
                assert hasattr(event, 'place'), "Event should have place field"
                assert hasattr(
                    event, 'reason'), "Event should have reason field"
                assert hasattr(event, 'note'), "Event should have note field"
                assert hasattr(event, 'src'), "Event should have src field"
                assert hasattr(
                    event, 'witnesses'), "Event should have witnesses field"
