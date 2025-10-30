"""Tests for converter_to_db module.

Tests the conversion from library types to database models.
"""
import pytest
import libraries.date
import database.date
import libraries.family
import database.family
import database.family_witness
import database.family_event
import database.family_event_witness
import libraries.events
import database.descend_children
import libraries.person
import database.person
import libraries.death_info
import libraries.title
import database.titles
import database.personal_event
import database.person_event_witness
import database.relation
import database.person_relations
import libraries.consanguinity_rate
import database.couple
import database.ascends
import database.descends
import database.unions

from repositories.converter_to_db import (
    convert_precision_to_db,
    convert_date_to_db,
    convert_divorce_status_to_db,
    convert_fam_event_name_to_db,
    convert_fam_event_to_db,
    convert_family_to_db,
    convert_death_status_to_db,
    convert_burial_status_to_db,
    convert_title_name_to_db,
    convert_title_to_db,
    convert_relation_to_db,
    convert_pers_event_name_to_db,
    convert_personal_event_to_db,
    convert_person_to_db,
)


# ============================================================================
# PRECISION CONVERSION TESTS
# ============================================================================

def test_convert_precision_sure_to_db() -> None:
    """Test converting Sure precision to database."""
    lib_precision = libraries.date.Sure()

    result = convert_precision_to_db(
        lib_precision, libraries.date.Calendar.GREGORIAN
    )

    assert result.precision_level == database.date.DatePrecision.SURE
    assert result.iso_date is None
    assert result.delta is None
    assert result.calendar == libraries.date.Calendar.GREGORIAN


def test_convert_precision_about_to_db():
    """Test converting About precision to database."""
    lib_precision = libraries.date.About()

    result = convert_precision_to_db(lib_precision)

    assert result.precision_level == database.date.DatePrecision.ABOUT
    assert result.iso_date is None
    assert result.delta is None


def test_convert_precision_maybe_to_db():
    """Test converting Maybe precision to database."""
    lib_precision = libraries.date.Maybe()

    result = convert_precision_to_db(lib_precision)

    assert result.precision_level == database.date.DatePrecision.MAYBE


def test_convert_precision_before_to_db():
    """Test converting Before precision to database."""
    lib_precision = libraries.date.Before()

    result = convert_precision_to_db(lib_precision)

    assert result.precision_level == database.date.DatePrecision.BEFORE


def test_convert_precision_after_to_db():
    """Test converting After precision to database."""
    lib_precision = libraries.date.After()

    result = convert_precision_to_db(lib_precision)

    assert result.precision_level == database.date.DatePrecision.AFTER


def test_convert_precision_oryear_to_db():
    """Test converting OrYear precision to database."""
    date_value = libraries.date.DateValue(
        day=15, month=6, year=1990, prec=None, delta=5
    )
    lib_precision = libraries.date.OrYear(date_value=date_value)

    result = convert_precision_to_db(lib_precision)

    assert result.precision_level == database.date.DatePrecision.ORYEAR
    assert result.iso_date == "1990-06-15"
    assert result.delta == 5


def test_convert_precision_yearint_to_db():
    """Test converting YearInt precision to database."""
    date_value = libraries.date.DateValue(
        day=1, month=1, year=2000, prec=None, delta=2
    )
    lib_precision = libraries.date.YearInt(date_value=date_value)

    result = convert_precision_to_db(lib_precision)

    assert result.precision_level == database.date.DatePrecision.YEARINT
    assert result.iso_date == "2000-01-01"
    assert result.delta == 2


# ============================================================================
# DATE CONVERSION TESTS
# ============================================================================

def test_convert_date_to_db():
    """Test converting CalendarDate to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=10, month=5, year=1995,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )

    result = convert_date_to_db(lib_date)

    assert result is not None
    assert result.iso_date == "1995-05-10"
    assert result.calendar == libraries.date.Calendar.GREGORIAN
    assert result.delta == 0
    precision_level = result.precision_obj.precision_level
    assert precision_level == database.date.DatePrecision.SURE


def test_convert_date_none_to_db():
    """Test converting None date to database."""
    result = convert_date_to_db(None)

    assert result is None


def test_convert_date_string_raises_error():
    """Test that converting string date raises ValueError."""
    with pytest.raises(
        ValueError,
        match="Cannot convert non empty free-form string"
    ):
        convert_date_to_db("1990")


def test_convert_date_tuple_raises_error():
    """Test that converting tuple date raises ValueError."""
    with pytest.raises(ValueError, match="Cannot convert tuple date"):
        convert_date_to_db((libraries.date.Calendar.GREGORIAN, 1990))


def test_convert_date_with_year_zero_returns_none():
    """Test that dates with year 0 return None."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=0,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )

    result = convert_date_to_db(lib_date)

    assert result is None


def test_convert_date_without_precision():
    """Test converting date without precision object."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=15, month=3, year=2020,
            prec=None, delta=0
        ),
        cal=libraries.date.Calendar.JULIAN
    )

    result = convert_date_to_db(lib_date)

    assert result is not None
    assert result.iso_date == "2020-03-15"
    assert result.calendar == libraries.date.Calendar.JULIAN
    precision_level = result.precision_obj.precision_level
    assert precision_level == database.date.DatePrecision.SURE


# ============================================================================
# DIVORCE STATUS CONVERSION TESTS
# ============================================================================

def test_convert_divorce_not_divorced_to_db():
    """Test converting NotDivorced to database."""
    lib_divorce = libraries.family.NotDivorced()

    status, divorce_date = convert_divorce_status_to_db(lib_divorce)

    assert status == database.family.DivorceStatus.NOT_DIVORCED
    assert divorce_date is None


def test_convert_divorce_separated_to_db():
    """Test converting Separated to database."""
    lib_divorce = libraries.family.Separated()

    status, divorce_date = convert_divorce_status_to_db(lib_divorce)

    assert status == database.family.DivorceStatus.SEPARATED
    assert divorce_date is None


def test_convert_divorce_divorced_to_db():
    """Test converting Divorced with date to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=20, month=8, year=2000,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_divorce = libraries.family.Divorced(divorce_date=lib_date)

    status, divorce_date = convert_divorce_status_to_db(lib_divorce)

    assert status == database.family.DivorceStatus.DIVORCED
    assert divorce_date is not None
    assert divorce_date.iso_date == "2000-08-20"


# ============================================================================
# FAMILY EVENT NAME CONVERSION TESTS
# ============================================================================

def test_convert_fam_event_name_marriage_to_db():
    """Test converting FamMarriage to database."""
    lib_event_name = libraries.events.FamMarriage()

    event_name, custom_name = convert_fam_event_name_to_db(lib_event_name)

    assert event_name == database.family_event.FamilyEventName.MARRIAGE
    assert custom_name is None


def test_convert_fam_event_name_divorce_to_db():
    """Test converting FamDivorce to database."""
    lib_event_name = libraries.events.FamDivorce()

    event_name, custom_name = convert_fam_event_name_to_db(lib_event_name)

    assert event_name == database.family_event.FamilyEventName.DIVORCE
    assert custom_name is None


def test_convert_fam_event_name_named_event_to_db():
    """Test converting FamNamedEvent to database."""
    lib_event_name = libraries.events.FamNamedEvent(name="Custom Wedding")

    event_name, custom_name = convert_fam_event_name_to_db(lib_event_name)

    assert event_name == database.family_event.FamilyEventName.NAMED_EVENT
    assert custom_name == "Custom Wedding"


def test_convert_fam_event_name_pacs_to_db():
    """Test converting FamPACS to database."""
    lib_event_name = libraries.events.FamPACS()

    event_name, custom_name = convert_fam_event_name_to_db(lib_event_name)

    assert event_name == database.family_event.FamilyEventName.PACS
    assert custom_name is None


def test_convert_all_fam_event_names_to_db():
    """Test converting all family event types to database."""
    FEN = database.family_event.FamilyEventName
    event_mapping = {
        libraries.events.FamMarriage(): FEN.MARRIAGE,
        libraries.events.FamNoMarriage(): FEN.NO_MARRIAGE,
        libraries.events.FamNoMention(): FEN.NO_MENTION,
        libraries.events.FamDivorce(): FEN.DIVORCE,
        libraries.events.FamEngage(): FEN.ENGAGE,
        libraries.events.FamSeparated(): FEN.SEPARATED,
        libraries.events.FamAnnulation(): FEN.ANNULATION,
        libraries.events.FamMarriageBann(): FEN.MARRIAGE_BANN,
        libraries.events.FamMarriageContract(): FEN.MARRIAGE_CONTRACT,
        libraries.events.FamMarriageLicense(): FEN.MARRIAGE_LICENSE,
        libraries.events.FamPACS(): FEN.PACS,
        libraries.events.FamResidence(): FEN.RESIDENCE,
    }

    for lib_event, expected_db_event in event_mapping.items():
        event_name, custom_name = convert_fam_event_name_to_db(lib_event)
        assert event_name == expected_db_event, (
            f"Failed for {type(lib_event).__name__}"
        )
        assert custom_name is None, (
            f"Expected no custom name for {type(lib_event).__name__}"
        )


# ============================================================================
# FAMILY EVENT CONVERSION TESTS
# ============================================================================

def test_convert_fam_event_to_db():
    """Test converting FamilyEvent to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=2000,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_event: libraries.family.FamilyEvent[int, str] = (
        libraries.family.FamilyEvent(
            name=libraries.events.FamMarriage(),
            date=lib_date,
            place="Paris",
            reason="Love",
            note="Beautiful ceremony",
            src="Certificate",
            witnesses=[(1, libraries.events.EventWitnessKind.WITNESS),
                       (2, libraries.events.EventWitnessKind.WITNESS)]
        )
    )

    db_event, witnesses = convert_fam_event_to_db(lib_event)

    assert db_event.name == database.family_event.FamilyEventName.MARRIAGE
    assert db_event.date_obj.iso_date == "2000-01-01"
    assert db_event.place == "Paris"
    assert db_event.reason == "Love"
    assert db_event.note == "Beautiful ceremony"
    assert db_event.src == "Certificate"
    assert len(witnesses) == 2
    assert witnesses[0].person_id == 1
    assert witnesses[0].kind == libraries.events.EventWitnessKind.WITNESS
    assert witnesses[1].person_id == 2


# ============================================================================
# FAMILY CONVERSION TESTS
# ============================================================================

def test_convert_family_minimal_to_db():
    """Test converting minimal Family to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=15, month=6, year=1990,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_family: libraries.family.Family[int, int, str] = (
        libraries.family.Family(
            index=1,
            marriage_date=lib_date,
            marriage_place="City Hall",
            marriage_note="",
            marriage_src="",
            witnesses=[],
            relation_kind=libraries.family.MaritalStatus.MARRIED,
            divorce_status=libraries.family.NotDivorced(),
            family_events=[],
            comment="",
            origin_file="",
            src="",
            parents=libraries.family.Parents([10, 20]),
            children=[]
        )
    )

    db_family, witnesses, events, children = convert_family_to_db(
        lib_family, couple_id=100
    )

    assert db_family.id == 1
    assert db_family.marriage_date_obj.iso_date == "1990-06-15"
    assert db_family.marriage_place == "City Hall"
    assert db_family.relation_kind == libraries.family.MaritalStatus.MARRIED
    divorce_status = db_family.divorce_status
    assert divorce_status == database.family.DivorceStatus.NOT_DIVORCED
    assert db_family.divorce_date_obj is None
    assert db_family.parents_id == 100
    assert len(witnesses) == 0
    assert len(events) == 0
    assert len(children) == 0


def test_convert_family_with_divorce_to_db():
    """Test converting Family with divorce to database."""
    marriage_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=15, month=6, year=1990,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    divorce_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=20, month=8, year=2000,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_family: libraries.family.Family[int, int, str] = (
        libraries.family.Family(
            index=2,
            marriage_date=marriage_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            witnesses=[],
            relation_kind=libraries.family.MaritalStatus.MARRIED,
            divorce_status=libraries.family.Divorced(
                divorce_date=divorce_date),
            family_events=[],
            comment="",
            origin_file="",
            src="",
            parents=libraries.family.Parents([30, 40]),
            children=[]
        )
    )

    db_family, _, _, _ = convert_family_to_db(lib_family, couple_id=200)

    assert db_family.divorce_status == database.family.DivorceStatus.DIVORCED
    assert db_family.divorce_date_obj is not None
    assert db_family.divorce_date_obj.iso_date == "2000-08-20"


def test_convert_family_with_witnesses_to_db():
    """Test converting Family with witnesses to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=2000,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_family: libraries.family.Family[int, int, str] = (
        libraries.family.Family(
            index=3,
            marriage_date=lib_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            witnesses=[5, 6, 7],
            relation_kind=libraries.family.MaritalStatus.MARRIED,
            divorce_status=libraries.family.NotDivorced(),
            family_events=[],
            comment="",
            origin_file="",
            src="",
            parents=libraries.family.Parents([50, 60]),
            children=[]
        )
    )

    _, witnesses, _, _ = convert_family_to_db(lib_family, couple_id=300)

    assert len(witnesses) == 3
    assert witnesses[0].person_id == 5
    assert witnesses[1].person_id == 6
    assert witnesses[2].person_id == 7


def test_convert_family_with_events_to_db():
    """Test converting Family with events to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=2000,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_event: libraries.family.FamilyEvent[int, str] = (
        libraries.family.FamilyEvent(
            name=libraries.events.FamMarriage(),
            date=lib_date,
            place="Church",
            reason="",
            note="",
            src="",
            witnesses=[]
        )
    )
    lib_family: libraries.family.Family[int, int, str] = (
        libraries.family.Family(
            index=4,
            marriage_date=lib_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            witnesses=[],
            relation_kind=libraries.family.MaritalStatus.MARRIED,
            divorce_status=libraries.family.NotDivorced(),
            family_events=[lib_event],
            comment="",
            origin_file="",
            src="",
            parents=libraries.family.Parents([70, 80]),
            children=[]
        )
    )

    _, _, events, _ = convert_family_to_db(lib_family, couple_id=400)

    assert len(events) == 1
    db_event, event_witnesses = events[0]
    assert db_event.name == database.family_event.FamilyEventName.MARRIAGE
    assert db_event.place == "Church"


def test_convert_family_with_children_to_db():
    """Test converting Family with children to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=2000,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_family: libraries.family.Family[int, int, str] = (
        libraries.family.Family(
            index=5,
            marriage_date=lib_date,
            marriage_place="",
            marriage_note="",
            marriage_src="",
            witnesses=[],
            relation_kind=libraries.family.MaritalStatus.MARRIED,
            divorce_status=libraries.family.NotDivorced(),
            family_events=[],
            comment="",
            origin_file="",
            src="",
            parents=libraries.family.Parents([90, 100]),
            children=[101, 102, 103]
        )
    )

    _, _, _, children = convert_family_to_db(lib_family, couple_id=500)

    assert len(children) == 3
    assert children[0].person_id == 101
    assert children[1].person_id == 102
    assert children[2].person_id == 103


def test_convert_family_complete_to_db():
    """Test converting complete Family to database."""
    marriage_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=15, month=6, year=1990,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    event_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=14, month=6, year=1990,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_event: libraries.family.FamilyEvent[int, str] = (
        libraries.family.FamilyEvent(
            name=libraries.events.FamEngage(),
            date=event_date,
            place="Restaurant",
            reason="Proposal",
            note="Romantic",
            src="Photo",
            witnesses=[(
                201, libraries.events.EventWitnessKind.WITNESS_GODPARENT)]
        )
    )
    lib_family: libraries.family.Family[int, int, str] = (
        libraries.family.Family(
            index=6,
            marriage_date=marriage_date,
            marriage_place="Cathedral",
            marriage_note="Grand ceremony",
            marriage_src="Official record",
            witnesses=[200, 201],
            relation_kind=libraries.family.MaritalStatus.MARRIED,
            divorce_status=libraries.family.NotDivorced(),
            family_events=[lib_event],
            comment="Happy family",
            origin_file="import.ged",
            src="Family Bible",
            parents=libraries.family.Parents([110, 120]),
            children=[121, 122]
        )
    )

    db_family, witnesses, events, children = convert_family_to_db(
        lib_family, couple_id=600
    )

    assert db_family.id == 6
    assert db_family.marriage_place == "Cathedral"
    assert db_family.marriage_note == "Grand ceremony"
    assert db_family.marriage_src == "Official record"
    assert db_family.comment == "Happy family"
    assert db_family.origin_file == "import.ged"
    assert db_family.src == "Family Bible"
    assert len(witnesses) == 2
    assert len(events) == 1
    assert len(children) == 2


# ============================================================================
# DEATH STATUS CONVERSION TESTS
# ============================================================================

def test_convert_death_not_dead_to_db():
    """Test converting NotDead to database."""
    lib_death = libraries.death_info.NotDead()

    status, reason, death_date = convert_death_status_to_db(lib_death)

    assert status == database.person.DeathStatus.NOT_DEAD
    assert reason is None
    assert death_date is None


def test_convert_death_dead_to_db():
    """Test converting Dead with reason and date to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=10, month=10, year=2020,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_death = libraries.death_info.Dead(
        death_reason=database.person.DeathReason.KILLED,
        date_of_death=lib_date
    )

    status, reason, death_date = convert_death_status_to_db(lib_death)

    assert status == database.person.DeathStatus.DEAD
    assert reason == database.person.DeathReason.KILLED
    assert death_date is not None
    assert death_date.iso_date == "2020-10-10"


def test_convert_death_dead_young_to_db():
    """Test converting DeadYoung to database."""
    lib_death = libraries.death_info.DeadYoung()

    status, reason, death_date = convert_death_status_to_db(lib_death)

    assert status == database.person.DeathStatus.DEAD_YOUNG
    assert reason is None
    assert death_date is None


def test_convert_death_dead_dont_know_when_to_db():
    """Test converting DeadDontKnowWhen to database."""
    lib_death = libraries.death_info.DeadDontKnowWhen()

    status, reason, death_date = convert_death_status_to_db(lib_death)

    assert status == database.person.DeathStatus.DEAD_DONT_KNOW_WHEN
    assert reason is None
    assert death_date is None


def test_convert_death_dont_know_if_dead_to_db():
    """Test converting DontKnowIfDead to database."""
    lib_death = libraries.death_info.DontKnowIfDead()

    status, reason, death_date = convert_death_status_to_db(lib_death)

    assert status == database.person.DeathStatus.DONT_KNOW_IF_DEAD
    assert reason is None
    assert death_date is None


def test_convert_death_of_course_dead_to_db():
    """Test converting OfCourseDead to database."""
    lib_death = libraries.death_info.OfCourseDead()

    status, reason, death_date = convert_death_status_to_db(lib_death)

    assert status == database.person.DeathStatus.OF_COURSE_DEAD
    assert reason is None
    assert death_date is None


# ============================================================================
# BURIAL STATUS CONVERSION TESTS
# ============================================================================

def test_convert_burial_unknown_to_db():
    """Test converting UnknownBurial to database."""
    lib_burial = libraries.burial_info.UnknownBurial()

    status, burial_date = convert_burial_status_to_db(lib_burial)

    assert status == database.person.BurialStatus.UNKNOWN_BURIAL
    assert burial_date is None


def test_convert_burial_buried_to_db():
    """Test converting Burial with date to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=15, month=10, year=2020,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_burial = libraries.burial_info.Burial(burial_date=lib_date)

    status, burial_date = convert_burial_status_to_db(lib_burial)

    assert status == database.person.BurialStatus.BURIAL
    assert burial_date is not None
    assert burial_date.iso_date == "2020-10-15"


def test_convert_burial_cremated_to_db():
    """Test converting Cremated with date to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=20, month=10, year=2020,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_burial = libraries.burial_info.Cremated(cremation_date=lib_date)

    status, burial_date = convert_burial_status_to_db(lib_burial)

    assert status == database.person.BurialStatus.CREMATED
    assert burial_date is not None
    assert burial_date.iso_date == "2020-10-20"


# ============================================================================
# TITLE CONVERSION TESTS
# ============================================================================

def test_convert_title_name_no_title_to_db():
    """Test converting NoTitle to database."""
    lib_title_name = libraries.title.NoTitle()

    result = convert_title_name_to_db(lib_title_name)

    assert result == ""


def test_convert_title_name_use_main_title_to_db():
    """Test converting UseMainTitle to database."""
    lib_title_name = libraries.title.UseMainTitle()

    result = convert_title_name_to_db(lib_title_name)

    assert result == "main"


def test_convert_title_name_title_name_to_db():
    """Test converting TitleName to database."""
    lib_title_name = libraries.title.TitleName(title_name="Duke")

    result = convert_title_name_to_db(lib_title_name)

    assert result == "Duke"


def test_convert_title_to_db():
    """Test converting complete Title to database."""
    start_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=1900,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    end_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=31, month=12, year=1950,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_title: libraries.title.Title[str] = (
        libraries.title.Title(
            title_name=libraries.title.TitleName(title_name="Count"),
            ident="ID123",
            place="London",
            date_start=start_date,
            date_end=end_date,
            nth=3
        )
    )

    result = convert_title_to_db(lib_title)

    assert result.name == "Count"
    assert result.ident == "ID123"
    assert result.place == "London"
    assert result.date_start_obj is not None
    assert result.date_start_obj.iso_date == "1900-01-01"
    assert result.date_end_obj is not None
    assert result.date_end_obj.iso_date == "1950-12-31"
    assert result.nth == 3


# ============================================================================
# RELATION CONVERSION TESTS
# ============================================================================

def test_convert_relation_to_db():
    """Test converting Relation to database."""
    lib_relation: libraries.family.Relation[int, str] = (
        libraries.family.Relation(
            type=libraries.family.RelationToParentType.ADOPTION,
            father=10,
            mother=20,
            sources="Adoption papers"
        )
    )

    result = convert_relation_to_db(lib_relation)

    assert result.type == libraries.family.RelationToParentType.ADOPTION
    assert result.father_id == 10
    assert result.mother_id == 20
    assert result.sources == "Adoption papers"


def test_convert_relation_no_father_to_db():
    """Test converting Relation with no father to database."""
    lib_relation: libraries.family.Relation[int, str] = (
        libraries.family.Relation(
            type=libraries.family.RelationToParentType.RECOGNITION,
            father=None,
            mother=30,
            sources=""
        )
    )

    result = convert_relation_to_db(lib_relation)

    assert result.father_id == 0
    assert result.mother_id == 30


# ============================================================================
# PERSONAL EVENT NAME CONVERSION TESTS
# ============================================================================

def test_convert_pers_event_name_baptism_to_db():
    """Test converting PersBaptism to database."""
    lib_event_name = libraries.events.PersBaptism()

    event_name, custom_name = convert_pers_event_name_to_db(lib_event_name)

    assert event_name == database.personal_event.PersonalEventName.BAPTISM
    assert custom_name is None


def test_convert_pers_event_name_bar_mitzvah_to_db():
    """Test converting PersBarMitzvah to database."""
    lib_event_name = libraries.events.PersBarMitzvah()

    event_name, custom_name = convert_pers_event_name_to_db(lib_event_name)

    assert event_name == database.personal_event.PersonalEventName.BAR_MITZVAH
    assert custom_name is None


def test_convert_pers_event_name_named_event_to_db():
    """Test converting PersNamedEvent to database."""
    lib_event_name = libraries.events.PersNamedEvent(name="Graduation")

    event_name, custom_name = convert_pers_event_name_to_db(lib_event_name)

    assert event_name == database.personal_event.PersonalEventName.NAMED_EVENT
    assert custom_name == "Graduation"


def test_convert_all_pers_event_names_to_db():
    """Test converting all personal event types to database."""
    PEN = database.personal_event.PersonalEventName
    event_mapping = {
        libraries.events.PersBirth(): PEN.BIRTH,
        libraries.events.PersBaptism(): PEN.BAPTISM,
        libraries.events.PersDeath(): PEN.DEATH,
        libraries.events.PersBurial(): PEN.BURIAL,
        libraries.events.PersCremation(): PEN.CREMATION,
        libraries.events.PersAccomplishment(): PEN.ACCOMPLISHMENT,
        libraries.events.PersAcquisition(): PEN.ACQUISITION,
        libraries.events.PersAdhesion(): PEN.ADHESION,
        libraries.events.PersBaptismLDS(): PEN.BAPTISM_LDS,
        libraries.events.PersBarMitzvah(): PEN.BAR_MITZVAH,
        libraries.events.PersBatMitzvah(): PEN.BAT_MITZVAH,
        libraries.events.PersBenediction(): PEN.BENEDICTION,
        libraries.events.PersChangeName(): PEN.CHANGE_NAME,
        libraries.events.PersCircumcision(): PEN.CIRCUMCISION,
        libraries.events.PersConfirmation(): PEN.CONFIRMATION,
        libraries.events.PersConfirmationLDS(): PEN.CONFIRMATION_LDS,
        libraries.events.PersDecoration(): PEN.DECORATION,
        libraries.events.PersDemobilisationMilitaire():
            PEN.DEMOBILISATION_MILITAIRE,
        libraries.events.PersDiploma(): PEN.DIPLOMA,
        libraries.events.PersDistinction(): PEN.DISTINCTION,
        libraries.events.PersDotation(): PEN.DOTATION,
        libraries.events.PersDotationLDS(): PEN.DOTATION_LDS,
        libraries.events.PersEducation(): PEN.EDUCATION,
        libraries.events.PersElection(): PEN.ELECTION,
        libraries.events.PersEmigration(): PEN.EMIGRATION,
        libraries.events.PersExcommunication(): PEN.EXCOMMUNICATION,
        libraries.events.PersFamilyLinkLDS(): PEN.FAMILY_LINK_LDS,
        libraries.events.PersFirstCommunion(): PEN.FIRST_COMMUNION,
        libraries.events.PersFuneral(): PEN.FUNERAL,
        libraries.events.PersGraduate(): PEN.GRADUATE,
        libraries.events.PersHospitalisation(): PEN.HOSPITALISATION,
        libraries.events.PersIllness(): PEN.ILLNESS,
        libraries.events.PersImmigration(): PEN.IMMIGRATION,
        libraries.events.PersListePassenger(): PEN.LISTE_PASSENGER,
        libraries.events.PersMilitaryDistinction(): PEN.MILITARY_DISTINCTION,
        libraries.events.PersMilitaryPromotion(): PEN.MILITARY_PROMOTION,
        libraries.events.PersMilitaryService(): PEN.MILITARY_SERVICE,
        libraries.events.PersMobilisationMilitaire():
            PEN.MOBILISATION_MILITAIRE,
        libraries.events.PersNaturalisation(): PEN.NATURALISATION,
        libraries.events.PersOccupation(): PEN.OCCUPATION,
        libraries.events.PersOrdination(): PEN.ORDINATION,
        libraries.events.PersProperty(): PEN.PROPERTY,
        libraries.events.PersRecensement(): PEN.RECENSEMENT,
        libraries.events.PersResidence(): PEN.RESIDENCE,
        libraries.events.PersRetired(): PEN.RETIRED,
        libraries.events.PersScellentChildLDS(): PEN.SCELLENT_CHILD_LDS,
        libraries.events.PersScellentParentLDS(): PEN.SCELLENT_PARENT_LDS,
        libraries.events.PersScellentSpouseLDS(): PEN.SCELLENT_SPOUSE_LDS,
        libraries.events.PersVenteBien(): PEN.VENTE_BIEN,
        libraries.events.PersWill(): PEN.WILL,
    }

    for lib_event, expected_db_event in event_mapping.items():
        event_name, custom_name = convert_pers_event_name_to_db(lib_event)
        assert event_name == expected_db_event, (
            f"Failed for {type(lib_event).__name__}"
        )
        assert custom_name is None, (
            f"Expected no custom name for {type(lib_event).__name__}"
        )


# ============================================================================
# PERSONAL EVENT CONVERSION TESTS
# ============================================================================

def test_convert_personal_event_to_db():
    """Test converting PersonalEvent to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=5, month=5, year=2005,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_event: libraries.events.PersonalEvent[int, str] = (
        libraries.events.PersonalEvent(
            name=libraries.events.PersBaptism(),
            date=lib_date,
            place="Church",
            reason="Religious",
            note="Family attended",
            src="Church records",
            witnesses=[
                (50, libraries.events.EventWitnessKind.WITNESS_GODPARENT),
                (51, libraries.events.EventWitnessKind.WITNESS_GODPARENT)]
        )
    )

    db_event, witnesses = convert_personal_event_to_db(lib_event)

    assert db_event.name == database.personal_event.PersonalEventName.BAPTISM
    assert db_event.date_obj.iso_date == "2005-05-05"
    assert db_event.place == "Church"
    assert db_event.reason == "Religious"
    assert db_event.note == "Family attended"
    assert db_event.src == "Church records"
    assert len(witnesses) == 2
    assert witnesses[0].person_id == 50
    assert witnesses[0].kind == libraries.events.EventWitnessKind.WITNESS_GODPARENT


def test_convert_personal_event_no_witnesses_to_db():
    """Test converting PersonalEvent without witnesses to database."""
    lib_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=10, month=10, year=2010,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_event: libraries.events.PersonalEvent[int, str] = (
        libraries.events.PersonalEvent(
            name=libraries.events.PersBarMitzvah(),
            date=lib_date,
            place="Synagogue",
            reason="",
            note="",
            src="",
            witnesses=[]
        )
    )

    db_event, witnesses = convert_personal_event_to_db(lib_event)

    assert db_event.name == database.personal_event.PersonalEventName.BAR_MITZVAH
    assert len(witnesses) == 0


# ============================================================================
# PERSON CONVERSION TESTS
# ============================================================================

def test_convert_person_minimal_to_db():
    """Test converting minimal Person to database."""
    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=1, first_name="John", surname="Doe", occ=0, image="",
            public_name="", qualifiers=[],
            aliases=[],
            first_names_aliases=[],
            surname_aliases=[],
            titles=[],
            non_native_parents_relation=[],
            related_persons=[],
            occupation="", sex=database.person.Sex.MALE,
            access_right=libraries.title.AccessRight.PRIVATE, birth_date=None,
            birth_place="", birth_note="", birth_src="", baptism_date=None,
            baptism_place="", baptism_note="", baptism_src="",
            death_status=libraries.death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=libraries.burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="", personal_events=[],
            notes="", src="", ascend=libraries.family.Ascendants(
                parents=None,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(
                        0)),
            families=[])
    )

    db_person, titles, relations, related, events = convert_person_to_db(
        lib_person
    )

    assert db_person.id == 1
    assert db_person.first_name == "John"
    assert db_person.surname == "Doe"
    assert db_person.occ == 0
    assert db_person.sex == database.person.Sex.MALE
    assert db_person.access_right == libraries.title.AccessRight.PRIVATE
    assert db_person.death_status == database.person.DeathStatus.NOT_DEAD
    assert db_person.burial_status == database.person.BurialStatus.UNKNOWN_BURIAL
    assert len(titles) == 0
    assert len(relations) == 0
    assert len(related) == 0
    assert len(events) == 0


def test_convert_person_with_birth_date_to_db():
    """Test converting Person with birth date to database."""
    birth_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=15, month=3, year=1980,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=2, first_name="Jane", surname="Smith", occ=0, image="",
            public_name="", qualifiers=[],
            aliases=[],
            first_names_aliases=[],
            surname_aliases=[],
            titles=[],
            non_native_parents_relation=[],
            related_persons=[],
            occupation="", sex=database.person.Sex.FEMALE,
            access_right=libraries.title.AccessRight.PUBLIC,
            birth_date=birth_date,
            birth_place="New York", birth_note="Hospital birth",
            birth_src="Birth certificate", baptism_date=None, baptism_place="",
            baptism_note="", baptism_src="",
            death_status=libraries.death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=libraries.burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="", personal_events=[],
            notes="", src="", ascend=libraries.family.Ascendants(
                parents=None,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(
                    0)),
            families=[])
    )

    db_person, _, _, _, _ = convert_person_to_db(lib_person)

    assert db_person.birth_date_obj is not None
    assert db_person.birth_date_obj.iso_date == "1980-03-15"
    assert db_person.birth_place == "New York"
    assert db_person.birth_note == "Hospital birth"
    assert db_person.birth_src == "Birth certificate"


def test_convert_person_with_baptism_date_to_db():
    """Test converting Person with baptism date to database."""
    baptism_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=20, month=4, year=1980,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=3, first_name="Bob", surname="Johnson", occ=0, image="",
            public_name="", qualifiers=[],
            aliases=[],
            first_names_aliases=[],
            surname_aliases=[],
            titles=[],
            non_native_parents_relation=[],
            related_persons=[],
            occupation="", sex=database.person.Sex.MALE,
            access_right=libraries.title.AccessRight.PUBLIC,
            birth_date=None,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_date=baptism_date,
            baptism_place="St. Mary's", baptism_note="Family ceremony",
            baptism_src="Church register",
            death_status=libraries.death_info.NotDead(),
            death_place="",
            death_note="",
            death_src="",
            burial=libraries.burial_info.UnknownBurial(),
            burial_place="",
            burial_note="",
            burial_src="",
            personal_events=[],
            notes="",
            src="",
            ascend=libraries.family.Ascendants(
                parents=None,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(
                    0)
            ),
            families=[])
    )

    db_person, _, _, _, _ = convert_person_to_db(lib_person)

    assert db_person.baptism_date_obj is not None
    assert db_person.baptism_place == "St. Mary's"


def test_convert_person_with_titles_to_db():
    """Test converting Person with titles to database."""
    title_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=1900,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_title: libraries.title.Title[str] = (
        libraries.title.Title(
            title_name=libraries.title.TitleName(title_name="Sir"),
            ident="",
            place="",
            date_start=title_date,
            date_end=title_date,
            nth=1
        )
    )
    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=4, first_name="Arthur", surname="Knight", occ=0, image="",
            public_name="", qualifiers=[],
            aliases=[],
            first_names_aliases=[],
            surname_aliases=[],
            titles=[lib_title],
            non_native_parents_relation=[],
            related_persons=[],
            occupation="", sex=database.person.Sex.MALE,
            access_right=libraries.title.AccessRight.PUBLIC, birth_date=None,
            birth_place="", birth_note="", birth_src="", baptism_date=None,
            baptism_place="", baptism_note="", baptism_src="",
            death_status=libraries.death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=libraries.burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="", personal_events=[],
            notes="", src="", ascend=libraries.family.Ascendants(
                parents=None,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(
                    0)),
            families=[])
    )

    _, titles, _, _, _ = convert_person_to_db(lib_person)

    assert len(titles) == 1
    assert titles[0].name == "Sir"


def test_convert_person_with_relations_to_db():
    """Test converting Person with non-native parent relations to database."""
    lib_relation: libraries.family.Relation[int, str] = (
        libraries.family.Relation(
            type=libraries.family.RelationToParentType.ADOPTION,
            father=100,
            mother=101,
            sources="Adoption papers"
        )
    )
    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=5, first_name="Alice", surname="Brown", occ=0, image="",
            public_name="", qualifiers=[],
            aliases=[],
            first_names_aliases=[],
            surname_aliases=[],
            titles=[],
            non_native_parents_relation=[lib_relation],
            related_persons=[],
            occupation="", sex=database.person.Sex.FEMALE,
            access_right=libraries.title.AccessRight.PUBLIC, birth_date=None,
            birth_place="", birth_note="", birth_src="", baptism_date=None,
            baptism_place="", baptism_note="", baptism_src="",
            death_status=libraries.death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=libraries.burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="", personal_events=[],
            notes="", src="", ascend=libraries.family.Ascendants(
                parents=None,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(
                    0)),
            families=[])
    )

    _, _, relations, _, _ = convert_person_to_db(lib_person)

    assert len(relations) == 1
    assert relations[0].type == libraries.family.RelationToParentType.ADOPTION


def test_convert_person_with_events_to_db():
    """Test converting Person with personal events to database."""
    event_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=10, month=6, year=2000,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    lib_event: libraries.events.PersonalEvent[int, str] = (
        libraries.events.PersonalEvent(
            name=libraries.events.PersBaptism(),
            date=event_date,
            place="Church",
            reason="",
            note="",
            src="",
            witnesses=[]
        )
    )
    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=6, first_name="Charlie", surname="Davis", occ=0, image="",
            public_name="", qualifiers=[],
            aliases=[],
            first_names_aliases=[],
            surname_aliases=[],
            titles=[],
            non_native_parents_relation=[],
            related_persons=[],
            occupation="", sex=database.person.Sex.MALE,
            access_right=libraries.title.AccessRight.PUBLIC, birth_date=None,
            birth_place="", birth_note="", birth_src="", baptism_date=None,
            baptism_place="", baptism_note="", baptism_src="",
            death_status=libraries.death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=libraries.burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[lib_event],
            notes="", src="", ascend=libraries.family.Ascendants(
                parents=None,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(
                    0)),
            families=[])
    )

    _, _, _, _, events = convert_person_to_db(lib_person)

    assert len(events) == 1
    db_event, witnesses = events[0]
    assert db_event.name == database.personal_event.PersonalEventName.BAPTISM


def test_convert_person_with_qualifiers_and_aliases_to_db():
    """Test converting Person with qualifiers and aliases to database."""
    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=7, first_name="David", surname="Wilson", occ=0, image="",
            public_name="Dave", qualifiers=["Junior", "III"],
            aliases=["Davey", "Dave W"],
            first_names_aliases=["Davie"],
            surname_aliases=["Willson"],
            titles=[],
            non_native_parents_relation=[],
            related_persons=[],
            occupation="Engineer", sex=database.person.Sex.MALE,
            access_right=libraries.title.AccessRight.PUBLIC, birth_date=None,
            birth_place="", birth_note="", birth_src="", baptism_date=None,
            baptism_place="", baptism_note="", baptism_src="",
            death_status=libraries.death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=libraries.burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="", personal_events=[],
            notes="Personal notes", src="Family records",
            ascend=libraries.family.Ascendants(
                parents=None,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(
                    0)),
            families=[])
    )

    db_person, _, _, _, _ = convert_person_to_db(lib_person)

    assert db_person.public_name == "Dave"
    assert db_person.qualifiers == "Junior,III"
    assert db_person.aliases == "Davey,Dave W"
    assert db_person.first_names_aliases == "Davie"
    assert db_person.surname_aliases == "Willson"
    assert db_person.occupation == "Engineer"
    assert db_person.notes == "Personal notes"
    assert db_person.src == "Family records"


def test_convert_person_with_related_persons_to_db():
    """Test converting Person with related persons to database."""
    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=8, first_name="Eve", surname="Martin", occ=0, image="",
            public_name="", qualifiers=[],
            aliases=[],
            first_names_aliases=[],
            surname_aliases=[],
            titles=[],
            non_native_parents_relation=[],
            related_persons=[200, 201, 202],
            occupation="", sex=database.person.Sex.FEMALE,
            access_right=libraries.title.AccessRight.PUBLIC, birth_date=None,
            birth_place="", birth_note="", birth_src="", baptism_date=None,
            baptism_place="", baptism_note="", baptism_src="",
            death_status=libraries.death_info.NotDead(),
            death_place="", death_note="", death_src="",
            burial=libraries.burial_info.UnknownBurial(),
            burial_place="", burial_note="", burial_src="", personal_events=[],
            notes="", src="", ascend=libraries.family.Ascendants(
                parents=None,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(
                    0)),
            families=[])
    )

    _, _, _, related, _ = convert_person_to_db(lib_person)

    assert len(related) == 3
    assert related[0].related_person_id == 200
    assert related[1].related_person_id == 201
    assert related[2].related_person_id == 202


def test_convert_person_complete_to_db():
    """Test converting complete Person to database."""
    birth_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=1950,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    death_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=31, month=12, year=2020,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    burial_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=5, month=1, year=2021,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )
    title_date = libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(
            day=1, month=1, year=2000,
            prec=libraries.date.Sure(), delta=0
        ),
        cal=libraries.date.Calendar.GREGORIAN
    )

    lib_person: libraries.person.Person[int, int, str, int] = (
        libraries.person.Person(
            index=9,
            first_name="Complete",
            surname="Person",
            occ=5,
            image="photo.jpg",
            public_name="CP",
            qualifiers=["Dr", "PhD"],
            aliases=["Complete P"],
            first_names_aliases=["Comp"],
            surname_aliases=["Per"],
            titles=[libraries.title.Title(
                title_name=libraries.title.TitleName(title_name="Doctor"),
                ident="",
                place="",
                date_start=title_date,
                date_end=title_date,
                nth=1
            )],
            non_native_parents_relation=[libraries.family.Relation(
                type=libraries.family.RelationToParentType.ADOPTION,
                father=300,
                mother=301,
                sources=""
            )],
            related_persons=[400, 401],
            occupation="Scientist",
            sex=database.person.Sex.MALE,
            access_right=libraries.title.AccessRight.PRIVATE,
            birth_date=birth_date,
            birth_place="Boston",
            birth_note="Born at home",
            birth_src="Birth record",
            baptism_date=birth_date,
            baptism_place="Church",
            baptism_note="",
            baptism_src="",
            death_status=libraries.death_info.Dead(
                death_reason=database.person.DeathReason.UNSPECIFIED,
                date_of_death=death_date
            ),
            death_place="Hospital",
            death_note="Peaceful",
            death_src="Death certificate",
            burial=libraries.burial_info.Burial(burial_date=burial_date),
            burial_place="Cemetery",
            burial_note="Family plot",
            burial_src="Cemetery records",
            personal_events=[libraries.events.PersonalEvent(
                name=libraries.events.PersGraduate(),
                date=title_date,
                place="University",
                reason="",
                note="",
                src="",
                witnesses=[]
            )],
            notes="Comprehensive notes",
            src="Multiple sources",
            ascend=libraries.family.Ascendants(
                parents=500,
                consanguinity_rate=libraries.consanguinity_rate.ConsanguinityRate(0)
            ),
            families=[600, 601]
        )
    )

    db_person, titles, relations, related, events = convert_person_to_db(
        lib_person, ascend_id=5000, families_id=6000
    )

    assert db_person.id == 9
    assert db_person.first_name == "Complete"
    assert db_person.surname == "Person"
    assert db_person.occ == 5
    assert db_person.image == "photo.jpg"
    assert db_person.public_name == "CP"
    assert db_person.occupation == "Scientist"
    assert db_person.birth_date_obj is not None
    assert db_person.birth_place == "Boston"
    assert db_person.death_status == database.person.DeathStatus.DEAD
    assert db_person.death_date_obj is not None
    assert db_person.burial_status == database.person.BurialStatus.BURIAL
    assert db_person.burial_date_obj is not None
    assert db_person.ascend_id == 5000
    assert db_person.families_id == 6000
    assert len(titles) == 1
    assert len(relations) == 1
    assert len(related) == 2
    assert len(events) == 1
