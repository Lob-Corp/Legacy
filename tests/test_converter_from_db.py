"""Tests for database to library converter functions."""
import pytest

from repositories.converter_from_db import (
    convert_precision_from_db,
    convert_date_from_db,
    convert_divorce_status_from_db,
    convert_fam_event_from_db,
    convert_family_from_db,
    convert_death_status_from_db,
    convert_burial_status_from_db,
    convert_title_name_from_db,
    convert_title_from_db,
    convert_relation_from_db,
    convert_pers_event_name_from_db,
    convert_personal_event_from_db,
    convert_person_from_db,
)

import database.date
import database.family
import database.family_witness
import database.family_event
import database.family_event_witness
import database.descend_children
import database.couple  # Import Couple so SQLAlchemy can resolve relationships
import database.descends  # Import Descends for the same reason
import database.person  # Import Person for SQLAlchemy relationships
import database.ascends  # Import Ascends for SQLAlchemy relationships
import database.unions  # Import Unions for SQLAlchemy relationships
import database.person_titles  # For title tests
import database.relation  # For relation tests
import database.personal_event  # For personal event tests
import database.person_event_witness  # For event witness tests

import libraries.date
import libraries.family
import libraries.events
import libraries.person
import libraries.death_info
import libraries.title


# ================== Precision Conversion Tests ==================

def test_convert_precision_sure():
    """Test conversion of SURE precision from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    result = convert_precision_from_db(db_precision)

    assert isinstance(result, libraries.date.Sure)


def test_convert_precision_about():
    """Test conversion of ABOUT precision from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.ABOUT
    db_precision.iso_date = None
    db_precision.delta = None

    result = convert_precision_from_db(db_precision)

    assert isinstance(result, libraries.date.About)


def test_convert_precision_maybe():
    """Test conversion of MAYBE precision from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.MAYBE
    db_precision.iso_date = None
    db_precision.delta = None

    result = convert_precision_from_db(db_precision)

    assert isinstance(result, libraries.date.Maybe)


def test_convert_precision_before():
    """Test conversion of BEFORE precision from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.BEFORE
    db_precision.iso_date = None
    db_precision.delta = None

    result = convert_precision_from_db(db_precision)

    assert isinstance(result, libraries.date.Before)


def test_convert_precision_after():
    """Test conversion of AFTER precision from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.AFTER
    db_precision.iso_date = None
    db_precision.delta = None

    result = convert_precision_from_db(db_precision)

    assert isinstance(result, libraries.date.After)


def test_convert_precision_oryear():
    """Test conversion of ORYEAR precision from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.ORYEAR
    db_precision.iso_date = "1900-06-15"
    db_precision.delta = 30

    result = convert_precision_from_db(db_precision)

    assert isinstance(result, libraries.date.OrYear)
    assert isinstance(result.date_value, libraries.date.DateValue)
    assert result.date_value.day == 15
    assert result.date_value.month == 6
    assert result.date_value.year == 1900
    assert result.date_value.delta == 30
    assert result.date_value.prec is None


def test_convert_precision_yearint():
    """Test conversion of YEARINT precision from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.YEARINT
    db_precision.iso_date = "1900-01-01"
    db_precision.delta = 365

    result = convert_precision_from_db(db_precision)

    assert isinstance(result, libraries.date.YearInt)
    assert isinstance(result.date_value, libraries.date.DateValue)
    assert result.date_value.day == 1
    assert result.date_value.month == 1
    assert result.date_value.year == 1900
    assert result.date_value.delta == 365
    assert result.date_value.prec is None


def test_convert_precision_invalid():
    """Test conversion raises error for invalid precision level."""
    db_precision = database.date.Precision()
    db_precision.precision_level = "INVALID"  # Invalid precision

    with pytest.raises(ValueError, match="Unknown precision level"):
        convert_precision_from_db(db_precision)


# ================== Date Conversion Tests ==================

def test_convert_date_gregorian():
    """Test conversion of a Gregorian date from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "1985-07-20"
    db_date.calendar = libraries.date.Calendar.GREGORIAN
    db_date.delta = 0
    db_date.precision_obj = db_precision

    result = convert_date_from_db(db_date)

    assert isinstance(result, libraries.date.CalendarDate)
    assert result.cal == libraries.date.Calendar.GREGORIAN
    assert result.dmy.day == 20
    assert result.dmy.month == 7
    assert result.dmy.year == 1985
    assert result.dmy.delta == 0
    assert isinstance(result.dmy.prec, libraries.date.Sure)


def test_convert_date_julian():
    """Test conversion of a Julian date from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.ABOUT
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "1700-03-15"
    db_date.calendar = libraries.date.Calendar.JULIAN
    db_date.delta = 0
    db_date.precision_obj = db_precision

    result = convert_date_from_db(db_date)

    assert isinstance(result, libraries.date.CalendarDate)
    assert result.cal == libraries.date.Calendar.JULIAN
    assert result.dmy.day == 15
    assert result.dmy.month == 3
    assert result.dmy.year == 1700
    assert isinstance(result.dmy.prec, libraries.date.About)


def test_convert_date_with_delta():
    """Test conversion of a date with delta (date range) from database."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "1900-06-01"
    db_date.calendar = libraries.date.Calendar.GREGORIAN
    db_date.delta = 30  # Represents a 30-day range
    db_date.precision_obj = db_precision

    result = convert_date_from_db(db_date)

    assert isinstance(result, libraries.date.CalendarDate)
    assert result.dmy.delta == 30
    assert result.dmy.day == 1
    assert result.dmy.month == 6
    assert result.dmy.year == 1900


def test_convert_date_french_calendar():
    """Test conversion of a French Revolutionary calendar date."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "1793-09-22"
    db_date.calendar = libraries.date.Calendar.FRENCH
    db_date.delta = 0
    db_date.precision_obj = db_precision

    result = convert_date_from_db(db_date)

    assert result.cal == libraries.date.Calendar.FRENCH


def test_convert_date_hebrew_calendar():
    """Test conversion of a Hebrew calendar date."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "2000-01-01"
    db_date.calendar = libraries.date.Calendar.HEBREW
    db_date.delta = 0
    db_date.precision_obj = db_precision

    result = convert_date_from_db(db_date)

    assert result.cal == libraries.date.Calendar.HEBREW


# ================== Divorce Status Conversion Tests ==================

def test_convert_divorce_status_not_divorced():
    """Test conversion of NOT_DIVORCED status."""
    result = convert_divorce_status_from_db(
        database.family.DivorceStatus.NOT_DIVORCED,
        None
    )

    assert isinstance(result, libraries.family.NotDivorced)


def test_convert_divorce_status_separated():
    """Test conversion of SEPARATED status."""
    result = convert_divorce_status_from_db(
        database.family.DivorceStatus.SEPARATED,
        None
    )

    assert isinstance(result, libraries.family.Separated)


def test_convert_divorce_status_divorced():
    """Test conversion of DIVORCED status with date."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "2020-05-10"
    db_date.calendar = libraries.date.Calendar.GREGORIAN
    db_date.delta = 0
    db_date.precision_obj = db_precision

    result = convert_divorce_status_from_db(
        database.family.DivorceStatus.DIVORCED,
        db_date
    )

    assert isinstance(result, libraries.family.Divorced)
    assert isinstance(result.divorce_date, libraries.date.CalendarDate)
    assert result.divorce_date.dmy.day == 10
    assert result.divorce_date.dmy.month == 5
    assert result.divorce_date.dmy.year == 2020


def test_convert_divorce_status_divorced_no_date():
    """Test conversion of DIVORCED status raises error without date."""
    with pytest.raises(ValueError, match="Divorce date must be provided"):
        convert_divorce_status_from_db(
            database.family.DivorceStatus.DIVORCED,
            None
        )


# ================== Family Event Conversion Tests ==================

def test_convert_fam_event_marriage():
    """Test conversion of MARRIAGE family event."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "1950-06-15"
    db_date.calendar = libraries.date.Calendar.GREGORIAN
    db_date.delta = 0
    db_date.precision_obj = db_precision

    db_event = database.family_event.FamilyEvent()
    db_event.name = database.family_event.FamilyEventName.MARRIAGE
    db_event.date_obj = db_date
    db_event.place = "Paris, France"
    db_event.reason = "Love"
    db_event.note = "Beautiful ceremony"
    db_event.src = "Civil registry"

    db_witness1 = database.family_event_witness.FamilyEventWitness()
    db_witness1.person_id = 1
    db_witness1.kind = libraries.events.EventWitnessKind.WITNESS

    db_witness2 = database.family_event_witness.FamilyEventWitness()
    db_witness2.person_id = 2
    db_witness2.kind = libraries.events.EventWitnessKind.WITNESS_GODPARENT

    witnesses = [db_witness1, db_witness2]

    result = convert_fam_event_from_db(db_event, witnesses)

    assert isinstance(result, libraries.events.FamilyEvent)
    assert isinstance(result.name, libraries.events.FamMarriage)
    assert result.place == "Paris, France"
    assert result.reason == "Love"
    assert result.note == "Beautiful ceremony"
    assert result.src == "Civil registry"
    assert len(result.witnesses) == 2
    assert result.witnesses[0] == (
        1, libraries.events.EventWitnessKind.WITNESS)
    assert result.witnesses[1] == (
        2, libraries.events.EventWitnessKind.WITNESS_GODPARENT)


def test_convert_fam_event_divorce():
    """Test conversion of DIVORCE family event."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.ABOUT
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "1960-03-10"
    db_date.calendar = libraries.date.Calendar.GREGORIAN
    db_date.delta = 0
    db_date.precision_obj = db_precision

    db_event = database.family_event.FamilyEvent()
    db_event.name = database.family_event.FamilyEventName.DIVORCE
    db_event.date_obj = db_date
    db_event.place = "Court"
    db_event.reason = ""
    db_event.note = ""
    db_event.src = ""

    result = convert_fam_event_from_db(db_event, [])

    assert isinstance(result.name, libraries.events.FamDivorce)
    assert result.place == "Court"
    assert len(result.witnesses) == 0


def test_convert_fam_event_all_types():
    """Test conversion of all family event types."""
    event_mapping = {
        database.family_event.FamilyEventName.MARRIAGE: libraries.events.FamMarriage,
        database.family_event.FamilyEventName.NO_MARRIAGE: libraries.events.FamNoMarriage,
        database.family_event.FamilyEventName.NO_MENTION: libraries.events.FamNoMention,
        database.family_event.FamilyEventName.DIVORCE: libraries.events.FamDivorce,
        database.family_event.FamilyEventName.ENGAGE: libraries.events.FamEngage,
        database.family_event.FamilyEventName.SEPARATED: libraries.events.FamSeparated,
        database.family_event.FamilyEventName.ANNULATION: libraries.events.FamAnnulation,
        database.family_event.FamilyEventName.MARRIAGE_BANN: libraries.events.FamMarriageBann,
        database.family_event.FamilyEventName.MARRIAGE_CONTRACT: libraries.events.FamMarriageContract,
        database.family_event.FamilyEventName.MARRIAGE_LICENSE: libraries.events.FamMarriageLicense,
        database.family_event.FamilyEventName.PACS: libraries.events.FamPACS,
        database.family_event.FamilyEventName.RESIDENCE: libraries.events.FamResidence,
    }

    for db_event_name, expected_class in event_mapping.items():
        db_precision = database.date.Precision()
        db_precision.precision_level = database.date.DatePrecision.SURE
        db_precision.iso_date = None
        db_precision.delta = None

        db_date = database.date.Date()
        db_date.iso_date = "2000-01-01"
        db_date.calendar = libraries.date.Calendar.GREGORIAN
        db_date.delta = 0
        db_date.precision_obj = db_precision

        db_event = database.family_event.FamilyEvent()
        db_event.name = db_event_name
        db_event.date_obj = db_date
        db_event.place = ""
        db_event.reason = ""
        db_event.note = ""
        db_event.src = ""

        result = convert_fam_event_from_db(db_event, [])

        assert isinstance(result.name, expected_class), \
            f"Failed for {db_event_name}: expected {expected_class}, got {type(result.name)}"


def test_convert_fam_event_named_event():
    """Test conversion of NAMED_EVENT (custom event)."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = "2000-01-01"
    db_date.calendar = libraries.date.Calendar.GREGORIAN
    db_date.delta = 0
    db_date.precision_obj = db_precision

    db_event = database.family_event.FamilyEvent()
    db_event.name = database.family_event.FamilyEventName.NAMED_EVENT
    db_event.date_obj = db_date
    db_event.place = ""
    db_event.reason = ""
    db_event.note = ""
    db_event.src = ""

    result = convert_fam_event_from_db(db_event, [])

    assert isinstance(result.name, libraries.events.FamNamedEvent)
    assert result.name.name == database.family_event.FamilyEventName.NAMED_EVENT.value


# ================== Family Conversion Tests ==================

def create_mock_couple():
    """Helper to create a Couple object."""
    import database.couple
    couple = database.couple.Couple()
    couple.father_id = 10
    couple.mother_id = 20
    return couple


def create_mock_date(year=2000, month=1, day=1, delta=0):
    """Helper to create a mock Date object."""
    db_precision = database.date.Precision()
    db_precision.precision_level = database.date.DatePrecision.SURE
    db_precision.iso_date = None
    db_precision.delta = None

    db_date = database.date.Date()
    db_date.iso_date = f"{year:04d}-{month:02d}-{day:02d}"
    db_date.calendar = libraries.date.Calendar.GREGORIAN
    db_date.delta = delta
    db_date.precision_obj = db_precision

    return db_date


def test_convert_family_basic():
    """Test basic family conversion from database."""
    db_family = database.family.Family()
    db_family.id = 1
    db_family.marriage_date_obj = create_mock_date(1980, 6, 15)
    db_family.marriage_place = "City Hall"
    db_family.marriage_note = "Note"
    db_family.marriage_src = "Source"
    db_family.relation_kind = libraries.family.MaritalStatus.MARRIED
    db_family.divorce_status = database.family.DivorceStatus.NOT_DIVORCED
    db_family.divorce_date = None
    db_family.comment = "Happy family"
    db_family.origin_file = "family.gw"
    db_family.src = "Registry"
    db_family.parents = create_mock_couple()

    witnesses = []
    events_and_witnesses = []
    children = []

    result = convert_family_from_db(
        db_family,
        witnesses,
        events_and_witnesses,
        children
    )

    assert isinstance(result, libraries.family.Family)
    assert result.index == 1
    assert result.marriage_place == "City Hall"
    assert result.marriage_note == "Note"
    assert result.marriage_src == "Source"
    assert result.relation_kind == libraries.family.MaritalStatus.MARRIED
    assert isinstance(result.divorce_status, libraries.family.NotDivorced)
    assert result.comment == "Happy family"
    assert result.origin_file == "family.gw"
    assert result.src == "Registry"
    assert isinstance(result.parents, libraries.family.Parents)
    assert result.parents.father() == 10
    assert result.parents.mother() == 20
    assert result.children == []


def test_convert_family_with_witnesses():
    """Test family conversion with witnesses."""
    db_family = database.family.Family()
    db_family.id = 2
    db_family.marriage_date_obj = create_mock_date(1990, 12, 25)
    db_family.marriage_place = ""
    db_family.marriage_note = ""
    db_family.marriage_src = ""
    db_family.relation_kind = libraries.family.MaritalStatus.MARRIED
    db_family.divorce_status = database.family.DivorceStatus.NOT_DIVORCED
    db_family.divorce_date = None
    db_family.comment = ""
    db_family.origin_file = ""
    db_family.src = ""
    db_family.parents = create_mock_couple()

    witness1 = database.family_witness.FamilyWitness()
    witness1.person_id = 100

    witness2 = database.family_witness.FamilyWitness()
    witness2.person_id = 101

    witnesses = [witness1, witness2]

    result = convert_family_from_db(
        db_family,
        witnesses,
        [],
        []
    )

    assert len(result.witnesses) == 2
    assert result.witnesses == [100, 101]


def test_convert_family_with_children():
    """Test family conversion with children."""
    db_family = database.family.Family()
    db_family.id = 3
    db_family.marriage_date_obj = create_mock_date(1970, 5, 20)
    db_family.marriage_place = ""
    db_family.marriage_note = ""
    db_family.marriage_src = ""
    db_family.relation_kind = libraries.family.MaritalStatus.MARRIED
    db_family.divorce_status = database.family.DivorceStatus.NOT_DIVORCED
    db_family.divorce_date = None
    db_family.comment = ""
    db_family.origin_file = ""
    db_family.src = ""
    db_family.parents = create_mock_couple()

    child1 = database.descend_children.DescendChildren()
    child1.person_id = 200

    child2 = database.descend_children.DescendChildren()
    child2.person_id = 201

    child3 = database.descend_children.DescendChildren()
    child3.person_id = 202

    children = [child1, child2, child3]

    result = convert_family_from_db(
        db_family,
        [],
        [],
        children
    )

    assert len(result.children) == 3
    assert result.children == [200, 201, 202]


def test_convert_family_with_events():
    """Test family conversion with events."""
    db_family = database.family.Family()
    db_family.id = 4
    db_family.marriage_date_obj = create_mock_date(1985, 3, 10)
    db_family.marriage_place = ""
    db_family.marriage_note = ""
    db_family.marriage_src = ""
    db_family.relation_kind = libraries.family.MaritalStatus.MARRIED
    db_family.divorce_status = database.family.DivorceStatus.NOT_DIVORCED
    db_family.divorce_date = None
    db_family.comment = ""
    db_family.origin_file = ""
    db_family.src = ""
    db_family.parents = create_mock_couple()

    db_event = database.family_event.FamilyEvent()
    db_event.name = database.family_event.FamilyEventName.MARRIAGE
    db_event.date_obj = create_mock_date(1985, 3, 10)
    db_event.place = "Church"
    db_event.reason = ""
    db_event.note = ""
    db_event.src = ""

    events_and_witnesses = [(db_event, [])]

    result = convert_family_from_db(
        db_family,
        [],
        events_and_witnesses,
        []
    )

    assert len(result.family_events) == 1
    assert isinstance(result.family_events[0], libraries.events.FamilyEvent)
    assert isinstance(
        result.family_events[0].name,
        libraries.events.FamMarriage)
    assert result.family_events[0].place == "Church"


def test_convert_family_divorced():
    """Test family conversion with divorced status."""
    db_family = database.family.Family()
    db_family.id = 5
    db_family.marriage_date_obj = create_mock_date(1975, 8, 5)
    db_family.marriage_place = ""
    db_family.marriage_note = ""
    db_family.marriage_src = ""
    db_family.relation_kind = libraries.family.MaritalStatus.MARRIED
    db_family.divorce_status = database.family.DivorceStatus.DIVORCED
    db_family.divorce_date_obj = create_mock_date(1980, 12, 31)
    db_family.comment = ""
    db_family.origin_file = ""
    db_family.src = ""
    db_family.parents = create_mock_couple()

    result = convert_family_from_db(
        db_family,
        [],
        [],
        []
    )

    assert isinstance(result.divorce_status, libraries.family.Divorced)
    assert result.divorce_status.divorce_date.dmy.year == 1980
    assert result.divorce_status.divorce_date.dmy.month == 12
    assert result.divorce_status.divorce_date.dmy.day == 31


def test_convert_family_separated():
    """Test family conversion with separated status."""
    db_family = database.family.Family()
    db_family.id = 6
    db_family.marriage_date_obj = create_mock_date(1965, 4, 1)
    db_family.marriage_place = ""
    db_family.marriage_note = ""
    db_family.marriage_src = ""
    db_family.relation_kind = libraries.family.MaritalStatus.MARRIED
    db_family.divorce_status = database.family.DivorceStatus.SEPARATED
    db_family.divorce_date = None
    db_family.comment = ""
    db_family.origin_file = ""
    db_family.src = ""
    db_family.parents = create_mock_couple()

    result = convert_family_from_db(
        db_family,
        [],
        [],
        []
    )

    assert isinstance(result.divorce_status, libraries.family.Separated)


def test_convert_family_complete():
    """Test complete family conversion with all features."""
    db_family = database.family.Family()
    db_family.id = 7
    db_family.marriage_date_obj = create_mock_date(1955, 11, 20)
    db_family.marriage_place = "Cathedral"
    db_family.marriage_note = "Grand ceremony"
    db_family.marriage_src = "Parish records"
    db_family.relation_kind = libraries.family.MaritalStatus.MARRIED
    db_family.divorce_status = database.family.DivorceStatus.NOT_DIVORCED
    db_family.divorce_date = None
    db_family.comment = "Large family"
    db_family.origin_file = "data.gw"
    db_family.src = "Multiple sources"
    db_family.parents = create_mock_couple()

    # Create witnesses
    witness1 = database.family_witness.FamilyWitness()
    witness1.person_id = 500
    witnesses = [witness1]

    # Create children
    child1 = database.descend_children.DescendChildren()
    child1.person_id = 600
    child2 = database.descend_children.DescendChildren()
    child2.person_id = 601
    children = [child1, child2]

    # Create events
    db_event = database.family_event.FamilyEvent()
    db_event.name = database.family_event.FamilyEventName.MARRIAGE
    db_event.date_obj = create_mock_date(1955, 11, 20)
    db_event.place = "Cathedral"
    db_event.reason = "Religious ceremony"
    db_event.note = "Big event"
    db_event.src = "Parish"

    db_event_witness = database.family_event_witness.FamilyEventWitness()
    db_event_witness.person_id = 700
    db_event_witness.kind = libraries.events.EventWitnessKind.WITNESS

    events_and_witnesses = [(db_event, [db_event_witness])]

    result = convert_family_from_db(
        db_family,
        witnesses,
        events_and_witnesses,
        children
    )

    # Verify all aspects
    assert result.index == 7
    assert result.marriage_place == "Cathedral"
    assert result.marriage_note == "Grand ceremony"
    assert result.marriage_src == "Parish records"
    assert len(result.witnesses) == 1
    assert result.witnesses[0] == 500
    assert len(result.children) == 2
    assert result.children == [600, 601]
    assert len(result.family_events) == 1
    assert result.family_events[0].place == "Cathedral"
    assert len(result.family_events[0].witnesses) == 1
    assert result.family_events[0].witnesses[0] == (
        700, libraries.events.EventWitnessKind.WITNESS)
    assert result.comment == "Large family"


# =================== Death Status Conversion Tests ===================


def test_convert_death_status_not_dead():
    """Test conversion of NotDead death status."""
    result = convert_death_status_from_db(
        database.person.DeathStatus.NOT_DEAD,
        None,
        None
    )

    assert isinstance(result, libraries.death_info.NotDead)


def test_convert_death_status_dead():
    """Test conversion of Dead death status with reason and date."""
    db_date = create_mock_date(year=1950, month=5, day=10)

    result = convert_death_status_from_db(
        database.person.DeathStatus.DEAD,
        database.person.DeathReason.KILLED,
        db_date
    )

    assert isinstance(result, libraries.death_info.Dead)
    assert result.death_reason == (
        database.person.DeathReason.KILLED)
    assert result.date_of_death is not None


def test_convert_death_status_dead_no_date_raises_error():
    """Test that Dead without date raises ValueError."""
    try:
        convert_death_status_from_db(
            database.person.DeathStatus.DEAD,
            database.person.DeathReason.KILLED,
            None
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "death date" in str(e).lower()


def test_convert_death_status_dead_no_reason_raises_error():
    """Test that Dead without reason raises ValueError."""
    db_date = create_mock_date(year=1950, month=5, day=10)

    try:
        convert_death_status_from_db(
            database.person.DeathStatus.DEAD,
            None,
            db_date
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "death reason" in str(e).lower()


def test_convert_death_status_dead_young():
    """Test conversion of DeadYoung death status."""
    result = convert_death_status_from_db(
        database.person.DeathStatus.DEAD_YOUNG,
        None,
        None
    )

    assert isinstance(result, libraries.death_info.DeadYoung)


def test_convert_death_status_dead_dont_know_when():
    """Test conversion of DeadDontKnowWhen death status."""
    result = convert_death_status_from_db(
        database.person.DeathStatus.DEAD_DONT_KNOW_WHEN,
        None,
        None
    )

    assert isinstance(result,
                      libraries.death_info.DeadDontKnowWhen)


def test_convert_death_status_dont_know_if_dead():
    """Test conversion of DontKnowIfDead death status."""
    result = convert_death_status_from_db(
        database.person.DeathStatus.DONT_KNOW_IF_DEAD,
        None,
        None
    )

    assert isinstance(result,
                      libraries.death_info.DontKnowIfDead)


def test_convert_death_status_of_course_dead():
    """Test conversion of OfCourseDead death status."""
    result = convert_death_status_from_db(
        database.person.DeathStatus.OF_COURSE_DEAD,
        None,
        None
    )

    assert isinstance(result, libraries.death_info.OfCourseDead)


# =================== Burial Status Conversion Tests ===================


def test_convert_burial_status_unknown_burial():
    """Test conversion of UnknownBurial burial status."""
    result = convert_burial_status_from_db(
        database.person.BurialStatus.UNKNOWN_BURIAL,
        None
    )

    assert isinstance(result, libraries.death_info.UnknownBurial)


def test_convert_burial_status_burial():
    """Test conversion of Burial burial status with date."""
    db_date = create_mock_date(year=1950, month=5, day=12)

    result = convert_burial_status_from_db(
        database.person.BurialStatus.BURIAL,
        db_date
    )

    assert isinstance(result, libraries.death_info.Burial)
    assert result.burial_date is not None


def test_convert_burial_status_burial_no_date_raises_error():
    """Test that Burial without date raises ValueError."""
    try:
        convert_burial_status_from_db(
            database.person.BurialStatus.BURIAL,
            None
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "burial date" in str(e).lower()


def test_convert_burial_status_cremated():
    """Test conversion of Cremated burial status with date."""
    db_date = create_mock_date(year=1950, month=5, day=15)

    result = convert_burial_status_from_db(
        database.person.BurialStatus.CREMATED,
        db_date
    )

    assert isinstance(result, libraries.death_info.Cremated)
    assert result.cremation_date is not None


def test_convert_burial_status_cremated_no_date_raises_error():
    """Test that Cremated without date raises ValueError."""
    try:
        convert_burial_status_from_db(
            database.person.BurialStatus.CREMATED,
            None
        )
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "burial date" in str(e).lower()


# =================== Title Conversion Tests ===================


def test_convert_title_name_no_title():
    """Test conversion of empty string to NoTitle."""
    result = convert_title_name_from_db("")

    assert isinstance(result, libraries.title.NoTitle)


def test_convert_title_name_use_main_title():
    """Test conversion of 'main' to UseMainTitle."""
    result = convert_title_name_from_db("main")

    assert isinstance(result, libraries.title.UseMainTitle)


def test_convert_title_name_title_name():
    """Test conversion of custom name to TitleName."""
    result = convert_title_name_from_db("Duke")

    assert isinstance(result, libraries.title.TitleName)
    assert result.title_name == "Duke"


def test_convert_title_complete():
    """Test conversion of complete Title with all fields."""
    db_start_date = create_mock_date(year=1900, month=1, day=1)
    db_end_date = create_mock_date(year=1950, month=12, day=31)

    db_title = database.titles.Titles()
    db_title.name = "Count"
    db_title.ident = "of Paris"
    db_title.place = "Paris"
    db_title.date_start_obj = db_start_date
    db_title.date_end_obj = db_end_date
    db_title.nth = 3

    result = convert_title_from_db(db_title)

    assert isinstance(result, libraries.title.Title)
    assert isinstance(result.title_name, libraries.title.TitleName)
    assert result.title_name.title_name == "Count"
    assert result.ident == "of Paris"
    assert result.place == "Paris"
    assert result.date_start is not None
    assert result.date_end is not None
    assert result.nth == 3


# =================== Relation Conversion Tests ===================


def test_convert_relation_basic():
    """Test conversion of basic Relation."""
    db_relation = database.relation.Relation()
    db_relation.type = (
        libraries.family.RelationToParentType.ADOPTION)
    db_relation.father_id = 100
    db_relation.mother_id = 200
    db_relation.sources = "Adoption records"

    result = convert_relation_from_db(db_relation)

    assert isinstance(result, libraries.family.Relation)
    assert result.father == 100
    assert result.mother == 200
    assert result.type == (
        libraries.family.RelationToParentType.ADOPTION)
    assert result.sources == "Adoption records"


# =============== Personal Event Name Conversion Tests ================


def test_convert_pers_event_name_baptism():
    """Test conversion of Baptism event name."""
    result = convert_pers_event_name_from_db(
        database.personal_event.PersonalEventName.BAPTISM
    )

    assert isinstance(result, libraries.events.PersBaptism)


def test_convert_pers_event_name_bar_mitzvah():
    """Test conversion of BarMitzvah event name."""
    result = convert_pers_event_name_from_db(
        database.personal_event.PersonalEventName.BAR_MITZVAH
    )

    assert isinstance(result, libraries.events.PersBarMitzvah)


def test_convert_pers_event_name_named_event():
    """Test conversion of NamedEvent with name stored in value."""
    result = convert_pers_event_name_from_db(
        database.personal_event.PersonalEventName.NAMED_EVENT
    )

    assert isinstance(result, libraries.events.PersNamedEvent)
    assert result.name == (
        database.personal_event.PersonalEventName.NAMED_EVENT.value)


# ============== Personal Event Conversion Tests ==============


def test_convert_personal_event_basic():
    """Test conversion of basic personal event."""
    db_date = create_mock_date(year=1920, month=6, day=5)

    db_event = database.personal_event.PersonalEvent()
    db_event.name = (
        database.personal_event.PersonalEventName.BAPTISM)
    db_event.date_obj = db_date
    db_event.place = "Church"
    db_event.reason = ""
    db_event.note = "Special ceremony"
    db_event.src = "Parish register"

    result = convert_personal_event_from_db(db_event, [])

    assert isinstance(result, libraries.events.PersonalEvent)
    assert isinstance(result.name, libraries.events.PersBaptism)
    assert result.date is not None
    assert result.place == "Church"
    assert result.note == "Special ceremony"
    assert result.src == "Parish register"


def test_convert_personal_event_with_witnesses():
    """Test conversion of personal event with witnesses."""
    db_date = create_mock_date(year=1930, month=7, day=10)

    db_witness = database.person_event_witness.PersonEventWitness()
    db_witness.person_id = 300
    db_witness.kind = (
        libraries.events.EventWitnessKind.WITNESS)

    db_event = database.personal_event.PersonalEvent()
    db_event.name = (
        database.personal_event.PersonalEventName.BAPTISM)
    db_event.date_obj = db_date
    db_event.place = "Cathedral"
    db_event.reason = ""
    db_event.note = ""
    db_event.src = ""

    result = convert_personal_event_from_db(
        db_event, [db_witness]
    )

    assert len(result.witnesses) == 1
    assert result.witnesses[0] == (
        300, libraries.events.EventWitnessKind.WITNESS)


# =================== Person Conversion Tests ===================


def create_mock_person():
    """Helper to create a basic mock Person."""
    db_person = database.person.Person()
    db_person.id = 1
    db_person.first_name = "John"
    db_person.surname = "Doe"
    db_person.sex = libraries.person.Sex.MALE
    db_person.death_status = (
        database.person.DeathStatus.NOT_DEAD)
    db_person.burial_status = (
        database.person.BurialStatus.UNKNOWN_BURIAL)
    db_person.occ = 0
    db_person.image = ""
    db_person.public_name = ""
    db_person.qualifiers = ""
    db_person.aliases = ""
    db_person.first_names_aliases = ""
    db_person.surname_aliases = ""
    db_person.occupation = ""
    db_person.src = ""
    db_person.notes = ""
    db_person.access_right = libraries.title.AccessRight.PUBLIC
    db_person.birth_place = ""
    db_person.birth_note = ""
    db_person.birth_src = ""
    db_person.baptism_place = ""
    db_person.baptism_note = ""
    db_person.baptism_src = ""
    db_person.death_place = ""
    db_person.death_note = ""
    db_person.death_src = ""
    db_person.burial_place = ""
    db_person.burial_note = ""
    db_person.burial_src = ""
    return db_person


def test_convert_person_minimal():
    """Test conversion of person with minimal required fields."""
    db_person = create_mock_person()

    result = convert_person_from_db(
        db_person, [], [], [], [], []
    )

    assert isinstance(result, libraries.person.Person)
    assert result.index == 1
    assert result.first_name == "John"
    assert result.surname == "Doe"
    assert result.sex == libraries.person.Sex.MALE
    assert isinstance(result.death_status,
                      libraries.death_info.NotDead)
    assert isinstance(result.burial,
                      libraries.death_info.UnknownBurial)


def test_convert_person_with_birth_date():
    """Test conversion of person with birth date."""
    db_date = create_mock_date(year=1880, month=3, day=15)

    db_person = create_mock_person()
    db_person.birth_date_obj = db_date
    db_person.birth_place = "London"
    db_person.birth_note = "At home"
    db_person.birth_src = "Birth certificate"

    result = convert_person_from_db(
        db_person, [], [], [], [], []
    )

    assert result.birth_date is not None
    assert result.birth_place == "London"
    assert result.birth_note == "At home"
    assert result.birth_src == "Birth certificate"


def test_convert_person_with_baptism_date():
    """Test conversion of person with baptism date."""
    db_date = create_mock_date(year=1880, month=3, day=20)

    db_person = create_mock_person()
    db_person.baptism_date_obj = db_date
    db_person.baptism_place = "Church"
    db_person.baptism_note = "Baptism ceremony"
    db_person.baptism_src = "Church register"

    result = convert_person_from_db(
        db_person, [], [], [], [], []
    )

    assert result.baptism_date is not None
    assert result.baptism_place == "Church"
    assert result.baptism_note == "Baptism ceremony"
    assert result.baptism_src == "Church register"


def test_convert_person_with_titles():
    """Test conversion of person with titles."""
    db_start_date = create_mock_date(year=1900, month=1, day=1)
    db_end_date = create_mock_date(year=1950, month=12, day=31)

    db_title = database.titles.Titles()
    db_title.name = "Sir"
    db_title.ident = "Knight"
    db_title.place = ""
    db_title.date_start_obj = db_start_date
    db_title.date_end_obj = db_end_date
    db_title.nth = 0

    db_person = create_mock_person()

    result = convert_person_from_db(
        db_person, [db_title], [], [], [], []
    )

    assert len(result.titles) == 1
    assert isinstance(result.titles[0], libraries.title.Title)
    assert result.titles[0].ident == "Knight"


def test_convert_person_with_relations():
    """Test conversion of person with relations."""
    db_relation = database.relation.Relation()
    db_relation.type = (
        libraries.family.RelationToParentType.ADOPTION)
    db_relation.father_id = 50
    db_relation.mother_id = 51
    db_relation.sources = "Adoption records"

    db_person = create_mock_person()

    result = convert_person_from_db(
        db_person, [], [db_relation], [], [], []
    )

    assert len(result.non_native_parents_relation) == 1
    assert result.non_native_parents_relation[0].father == 50
    assert result.non_native_parents_relation[0].type == (
        libraries.family.RelationToParentType.ADOPTION)


def test_convert_person_with_personal_events():
    """Test conversion of person with personal events."""
    db_date = create_mock_date(year=1920, month=6, day=10)

    db_event = database.personal_event.PersonalEvent()
    db_event.name = (
        database.personal_event.PersonalEventName.BAPTISM)
    db_event.date_obj = db_date
    db_event.place = "Cathedral"
    db_event.reason = ""
    db_event.note = ""
    db_event.src = ""

    db_person = create_mock_person()

    result = convert_person_from_db(
        db_person, [], [], [], [(db_event, [])], []
    )

    assert len(result.personal_events) == 1
    assert isinstance(result.personal_events[0].name,
                      libraries.events.PersBaptism)


def test_convert_person_with_qualifiers():
    """Test conversion of person with qualifiers."""
    db_person = create_mock_person()
    db_person.qualifiers = "qualifier1,qualifier2,qualifier3"

    result = convert_person_from_db(
        db_person, [], [], [], [], []
    )

    assert len(result.qualifiers) == 3
    assert "qualifier1" in result.qualifiers
    assert "qualifier2" in result.qualifiers
    assert "qualifier3" in result.qualifiers


def test_convert_person_with_aliases():
    """Test conversion of person with aliases."""
    db_person = create_mock_person()
    db_person.aliases = "Johnny,Jack,J.D."

    result = convert_person_from_db(
        db_person, [], [], [], [], []
    )

    assert len(result.aliases) == 3
    assert "Johnny" in result.aliases
    assert "Jack" in result.aliases
    assert "J.D." in result.aliases


def test_convert_person_complete():
    """Test conversion of person with many optional fields."""
    # Create dates
    db_birth_date = create_mock_date(year=1900, month=1, day=1)
    db_baptism_date = create_mock_date(year=1900, month=1, day=8)
    db_death_date = create_mock_date(year=1980, month=1, day=1)
    db_burial_date = create_mock_date(year=1980, month=1, day=5)

    # Create title
    db_title_start = create_mock_date(year=1920, month=1, day=1)
    db_title_end = create_mock_date(year=1970, month=1, day=1)
    db_title = database.titles.Titles()
    db_title.name = "Sir"
    db_title.ident = "Knight"
    db_title.place = ""
    db_title.date_start_obj = db_title_start
    db_title.date_end_obj = db_title_end
    db_title.nth = 0

    # Create relation
    db_relation = database.relation.Relation()
    db_relation.type = (
        libraries.family.RelationToParentType.ADOPTION)
    db_relation.father_id = 50
    db_relation.mother_id = 51
    db_relation.sources = ""

    # Create personal event
    db_event = database.personal_event.PersonalEvent()
    db_event.name = (
        database.personal_event.PersonalEventName.BAPTISM)
    db_event.date_obj = db_baptism_date
    db_event.place = ""
    db_event.reason = ""
    db_event.note = ""
    db_event.src = ""

    # Create person
    db_person = database.person.Person()
    db_person.id = 100
    db_person.first_name = "John"
    db_person.surname = "Smith"
    db_person.sex = database.person.Sex.MALE
    db_person.first_name_aliases = "Johnny,Jack"
    db_person.surname_aliases = "Smithson"
    db_person.public_name = "John Smith Sr."
    db_person.qualifiers = "Jr,III"
    db_person.aliases = "J.S.,Johnny"
    db_person.first_names_aliases = "Johnny,Jack"
    db_person.occ = 0
    db_person.occupation = "Doctor"
    db_person.image = "portrait.jpg"
    db_person.access_right = libraries.title.AccessRight.PUBLIC
    db_person.src = "Multiple sources"
    db_person.birth_date_obj = db_birth_date
    db_person.birth_place = "London"
    db_person.birth_note = "Home birth"
    db_person.birth_src = "Certificate"
    db_person.baptism_date_obj = db_baptism_date
    db_person.baptism_place = "Church"
    db_person.baptism_note = "Ceremony"
    db_person.baptism_src = "Church register"
    db_person.death_status = database.person.DeathStatus.DEAD
    db_person.death_reason = (
        database.person.DeathReason.UNSPECIFIED)
    db_person.death_date_obj = db_death_date
    db_person.death_place = "Hospital"
    db_person.death_note = "Peaceful"
    db_person.death_src = "Death certificate"
    db_person.burial_status = (
        database.person.BurialStatus.BURIAL)
    db_person.burial_date_obj = db_burial_date
    db_person.burial_place = "Cemetery"
    db_person.burial_note = "Family plot"
    db_person.burial_src = "Burial record"
    db_person.notes = "Important person"

    result = convert_person_from_db(
        db_person,
        [db_title],
        [db_relation],
        [],
        [(db_event, [])],
        []
    )

    assert result.index == 100
    assert result.first_name == "John"
    assert result.surname == "Smith"
    assert result.sex == libraries.person.Sex.MALE
    assert result.public_name == "John Smith Sr."
    assert len(result.qualifiers) == 2
    assert len(result.aliases) == 2
    assert result.occupation == "Doctor"
    assert result.image == "portrait.jpg"
    assert result.birth_date is not None
    assert result.birth_place == "London"
    assert result.baptism_date is not None
    assert result.baptism_place == "Church"
    assert isinstance(result.death_status,
                      libraries.death_info.Dead)
    assert result.death_place == "Hospital"
    assert isinstance(result.burial,
                      libraries.death_info.Burial)
    assert result.burial_place == "Cemetery"
    assert result.notes == "Important person"
    assert result.src == "Multiple sources"
    assert len(result.titles) == 1
    assert len(result.non_native_parents_relation) == 1
    assert len(result.personal_events) == 1
