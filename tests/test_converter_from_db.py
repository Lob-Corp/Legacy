"""Tests for database to library converter functions."""
import pytest

from repositories.converter_from_db import (
    convert_precision_from_db,
    convert_date_from_db,
    convert_divorce_status_from_db,
    convert_fam_event_from_db,
    convert_family_from_db,
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

import libraries.date
import libraries.family
import libraries.events


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
    assert result.origin_file == "data.gw"
    assert result.src == "Multiple sources"
