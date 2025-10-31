"""
Comprehensive tests for the details route.
"""
from unittest.mock import Mock
from wserver.routes.details import (
    get_person_basic_info,
    get_person_vital_events,
    get_family_info,
    get_children_info,
    get_witness_info,
    get_sort_key,
    get_timeline_events,
    get_notes,
    get_event_name,
    get_sources,
    format_date,
)
from libraries.person import Person, Sex
from libraries.date import CalendarDate, Calendar, DateValue
from libraries.precision import Sure
from libraries.death_info import (
    Dead, NotDead, DeathReason, DeadYoung, DeadDontKnowWhen
)
from libraries.burial_info import UnknownBurial
from libraries.title import AccessRight
from libraries.family import (
    Ascendants, Family, Parents, NotDivorced,
    Divorced, Separated, MaritalStatus
)
from libraries.consanguinity_rate import ConsanguinityRate
from libraries.events import (
    FamMarriage, FamDivorce, FamSeparated, FamilyEvent,
    PersBirth, PersDeath
)


# ===== Helper Functions =====

def create_basic_person(**kwargs):
    """Create a basic person with default values."""
    defaults = {
        'index': 1,
        'first_name': 'John',
        'surname': 'Doe',
        'occ': 1,
        'image': '',
        'public_name': '',
        'qualifiers': [],
        'aliases': [],
        'first_names_aliases': [],
        'surname_aliases': [],
        'titles': [],
        'non_native_parents_relation': [],
        'related_persons': [],
        'occupation': '',
        'sex': Sex.MALE,
        'access_right': AccessRight.PUBLIC,
        'birth_date': None,
        'birth_place': '',
        'birth_note': '',
        'birth_src': '',
        'baptism_date': None,
        'baptism_place': '',
        'baptism_note': '',
        'baptism_src': '',
        'death_status': NotDead(),
        'death_place': '',
        'death_note': '',
        'death_src': '',
        'burial': UnknownBurial(),
        'burial_place': '',
        'burial_note': '',
        'burial_src': '',
        'personal_events': [],
        'notes': '',
        'src': '',
        'ascend': Ascendants(
            parents=None,
            consanguinity_rate=ConsanguinityRate.from_integer(0)
        ),
        'families': [],
    }
    defaults.update(kwargs)
    return Person(**defaults)


def create_basic_family(**kwargs):
    """Create a basic family with default values."""
    defaults = {
        'index': 1,
        'parents': Parents.from_couple(1, 2),
        'children': [],
        'marriage_date': None,
        'marriage_place': '',
        'marriage_note': '',
        'marriage_src': '',
        'relation_kind': MaritalStatus.MARRIED,
        'divorce_status': NotDivorced(),
        'family_events': [],
        'witnesses': [],
        'comment': '',
        'src': '',
        'origin_file': '',
    }
    defaults.update(kwargs)
    return Family(**defaults)


# ===== Test get_person_basic_info =====

def test_get_person_basic_info():
    """Test extracting basic person information with occupation."""
    person = create_basic_person(
        first_name="John",
        surname="Doe",
        occupation="Engineer"
    )

    result = get_person_basic_info(person)

    assert result['person_id'] == 1
    assert result['first_name'] == "John"
    assert result['surname'] == "Doe"
    assert result['occupation'] == "Engineer"


def test_get_person_basic_info_no_occupation():
    """Test extracting basic person information without occupation."""
    person = create_basic_person(
        first_name="Jane",
        surname="Smith",
        occupation=""
    )

    result = get_person_basic_info(person)

    assert result['person_id'] == 1
    assert result['first_name'] == "Jane"
    assert result['surname'] == "Smith"
    assert result['occupation'] is None


# ===== Test get_person_vital_events =====

def test_get_person_vital_events_with_birth_tuple():
    """Test extracting vital events with tuple birth date."""
    person = create_basic_person(
        birth_date=("ABOUT", 1985),
        birth_place="London"
    )

    result = get_person_vital_events(person)

    assert result['birth_year'] == 1985
    assert result['birth_date'] is None
    assert result['birth_place'] == "London"

# ===== Test get_family_info =====

def test_get_family_info_no_families():
    """Test family info extraction with no families."""
    person = create_basic_person()

    family_repo = Mock()
    person_repo = Mock()

    result = get_family_info(person, family_repo, person_repo)

    assert result['family_id'] is None
    assert result['spouse_id'] is None
    assert result['spouse_first_name'] is None
    assert result['spouse_surname'] is None


def test_get_family_info_with_spouse():
    """Test family info extraction with spouse."""
    person = create_basic_person(index=1, families=[1])
    spouse = create_basic_person(
        index=2,
        first_name="Jane",
        surname="Smith",
        birth_date=CalendarDate(
            cal=Calendar.GREGORIAN,
            dmy=DateValue(day=10, month=5, year=1992, prec=Sure())
        )
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        marriage_date=CalendarDate(
            cal=Calendar.GREGORIAN,
            dmy=DateValue(day=20, month=6, year=2015, prec=Sure())
        ),
        marriage_place="New York"
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_family_info(person, family_repo, person_repo)

    assert result['family_id'] == 1
    assert result['spouse_id'] == 2
    assert result['spouse_first_name'] == "Jane"
    assert result['spouse_surname'] == "Smith"
    assert result['spouse_birth_year'] == 1992
    assert result['marriage_date'] == "20 June 2015"
    assert result['marriage_place'] == "New York"
    assert result['divorce_date'] is None


def test_get_family_info_with_divorce():
    """Test family info extraction with divorce."""
    person = create_basic_person(index=1, families=[1])
    spouse = create_basic_person(index=2, first_name="Jane", surname="Smith")

    divorce_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=15, month=3, year=2020, prec=Sure())
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        divorce_status=Divorced(divorce_date=divorce_date)
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_family_info(person, family_repo, person_repo)

    assert result['divorce_date'] == "15 March 2020"


def test_get_family_info_with_separation():
    """Test family info extraction with separation."""
    person = create_basic_person(index=1, families=[1])
    spouse = create_basic_person(index=2, first_name="Jane", surname="Smith")

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        divorce_status=Separated()
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_family_info(person, family_repo, person_repo)

    # Separated has no date associated with it
    assert result['divorce_date'] is None


def test_get_family_info_spouse_with_tuple_dates():
    """Test family info with spouse having tuple dates."""
    person = create_basic_person(index=1, families=[1])
    spouse = create_basic_person(
        index=2,
        first_name="Jane",
        surname="Smith",
        birth_date=("ABOUT", 1990),
        death_status=Dead(
            death_reason=DeathReason.UNSPECIFIED,
            date_of_death=("BEFORE", 2020)
        )
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2)
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_family_info(person, family_repo, person_repo)

    assert result['spouse_birth_year'] == 1990
    assert result['spouse_death_year'] == 2020


# ===== Test get_children_info =====

def test_get_children_info_no_families():
    """Test children info with no families."""
    person = create_basic_person()

    family_repo = Mock()
    person_repo = Mock()

    result = get_children_info(person, family_repo, person_repo)

    assert result == []


def test_get_children_info_with_children():
    """Test children info extraction."""
    person = create_basic_person(index=1, families=[1])

    child1 = create_basic_person(
        index=3,
        first_name="Alice",
        surname="Doe",
        birth_date=CalendarDate(
            cal=Calendar.GREGORIAN,
            dmy=DateValue(day=1, month=1, year=2010, prec=Sure())
        )
    )

    child2 = create_basic_person(
        index=4,
        first_name="Bob",
        surname="Doe",
        birth_date=CalendarDate(
            cal=Calendar.GREGORIAN,
            dmy=DateValue(day=15, month=6, year=2012, prec=Sure())
        ),
        death_status=Dead(
            death_reason=DeathReason.UNSPECIFIED,
            date_of_death=CalendarDate(
                cal=Calendar.GREGORIAN,
                dmy=DateValue(day=20, month=7, year=2015, prec=Sure())
            )
        )
    )

    family = create_basic_family(
        index=1,
        children=[3, 4]
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.side_effect = [child1, child2]

    result = get_children_info(person, family_repo, person_repo)

    assert len(result) == 2
    assert result[0]['id'] == 3
    assert result[0]['first_name'] == "Alice"
    assert result[0]['birth_year'] == 2010

    assert result[1]['id'] == 4
    assert result[1]['first_name'] == "Bob"
    assert result[1]['birth_year'] == 2012
    assert result[1]['death_year'] == 2015
    assert result[1]['age_years'] == 3


def test_get_children_info_with_tuple_dates():
    """Test children info with tuple dates."""
    person = create_basic_person(index=1, families=[1])

    child = create_basic_person(
        index=3,
        first_name="Charlie",
        surname="Doe",
        birth_date=("ABOUT", 2005),
        death_status=Dead(
            death_reason=DeathReason.UNSPECIFIED,
            date_of_death=("BEFORE", 2010)
        )
    )

    family = create_basic_family(index=1, children=[3])

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = child

    result = get_children_info(person, family_repo, person_repo)

    assert result[0]['birth_year'] == 2005
    assert result[0]['death_year'] == 2010
    assert result[0]['age_years'] == 5


# ===== Test get_witness_info =====

def test_get_witness_info_with_tuple_dates():
    """Test witness info with tuple dates."""
    witness = create_basic_person(
        index=11,
        first_name="Old",
        surname="Witness",
        birth_date=("ABOUT", 1900),
        death_status=Dead(
            death_reason=DeathReason.UNSPECIFIED,
            date_of_death=("BEFORE", 1980)
        )
    )

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = witness

    result = get_witness_info(11, person_repo)

    assert result['date_range'] == "1900-1980"


def test_get_witness_info_only_birth():
    """Test witness info with only birth year."""
    witness = create_basic_person(
        index=12,
        first_name="Young",
        surname="Witness",
        birth_date=CalendarDate(
            cal=Calendar.GREGORIAN,
            dmy=DateValue(day=1, month=1, year=2000, prec=Sure())
        )
    )

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = witness

    result = get_witness_info(12, person_repo)

    assert result['date_range'] == "2000-"


def test_get_witness_info_not_found():
    """Test witness info when witness not found."""
    person_repo = Mock()
    person_repo.get_person_by_id.side_effect = Exception("Not found")

    result = get_witness_info(999, person_repo)

    assert result == {}


# ===== Test get_sort_key =====

def test_get_sort_key_valid_date():
    """Test sort key generation with valid date."""
    date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=15, month=6, year=2000, prec=Sure())
    )
    event = {'_sort_date': date}

    result = get_sort_key(event)

    assert result == (2000, 6, 15)


def test_get_sort_key_no_date():
    """Test sort key generation with no date."""
    event = {'_sort_date': None}

    result = get_sort_key(event)

    assert result == (9999, 12, 31)


def test_get_sort_key_partial_date():
    """Test sort key generation with partial date."""
    date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=0, month=6, year=2000, prec=Sure())
    )
    event = {'_sort_date': date}

    result = get_sort_key(event)

    assert result == (2000, 6, 31)


def test_get_sort_key_year_only():
    """Test sort key generation with year only."""
    date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=0, month=0, year=1995, prec=Sure())
    )
    event = {'_sort_date': date}

    result = get_sort_key(event)

    assert result == (1995, 12, 31)


# ===== Test get_timeline_events =====

def test_get_timeline_events_birth_only():
    """Test timeline events with only birth."""
    birth_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=1, month=1, year=1990, prec=Sure())
    )

    person = create_basic_person(
        birth_date=birth_date,
        birth_place="Paris"
    )

    family_repo = Mock()
    person_repo = Mock()

    result = get_timeline_events(person, family_repo, person_repo)

    assert len(result) == 1
    assert result[0]['type'] == 'birth'
    assert result[0]['date_display'] == "1 January 1990"
    assert result[0]['place'] == "Paris"


def test_get_timeline_events_with_marriage():
    """Test timeline events with marriage."""
    birth_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=1, month=1, year=1990, prec=Sure())
    )
    marriage_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=15, month=6, year=2015, prec=Sure())
    )

    person = create_basic_person(
        index=1,
        birth_date=birth_date,
        families=[1]
    )

    spouse = create_basic_person(
        index=2,
        first_name="Jane",
        surname="Smith"
    )

    witness = create_basic_person(
        index=10,
        first_name="Witness",
        surname="One",
        birth_date=CalendarDate(
            cal=Calendar.GREGORIAN,
            dmy=DateValue(day=1, month=1, year=1980, prec=Sure())
        )
    )

    marriage_event = FamilyEvent(
        name=FamMarriage(),
        date=marriage_date,
        place="Church",
        reason="",
        note="Beautiful ceremony",
        src="",
        witnesses=[(10, "WITNESS")]
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        marriage_date=marriage_date,
        marriage_place="Church",
        family_events=[marriage_event]
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.side_effect = [spouse, witness]

    result = get_timeline_events(person, family_repo, person_repo)

    # Should have birth and marriage events
    assert len(result) == 2
    assert result[0]['type'] == 'birth'
    assert result[1]['type'] == 'marriage'
    assert result[1]['spouse_first_name'] == "Jane"
    assert result[1]['note'] == "Beautiful ceremony"
    assert len(result[1]['witnesses']) == 1
    assert result[1]['witnesses'][0]['first_name'] == "Witness"


def test_get_timeline_events_with_children():
    """Test timeline events with child births."""
    birth_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=1, month=1, year=1990, prec=Sure())
    )
    child_birth = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=10, month=5, year=2015, prec=Sure())
    )

    person = create_basic_person(
        index=1,
        birth_date=birth_date,
        families=[1]
    )

    child = create_basic_person(
        index=3,
        first_name="Child",
        surname="Doe",
        birth_date=child_birth
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        children=[3]
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = child

    result = get_timeline_events(person, family_repo, person_repo)

    # Should have birth and child_birth events
    assert len(result) == 2
    assert result[1]['type'] == 'child_birth'
    assert result[1]['child_first_name'] == "Child"
    assert result[1]['child_date_range'] == "2015-"


def test_get_timeline_events_with_divorce():
    """Test timeline events with divorce."""
    divorce_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=20, month=8, year=2020, prec=Sure())
    )

    person = create_basic_person(index=1, families=[1])

    spouse = create_basic_person(
        index=2,
        first_name="Jane",
        surname="Smith"
    )

    divorce_event = FamilyEvent(
        name=FamDivorce(),
        date=divorce_date,
        place="",
        reason="",
        note="Amicable split",
        src="",
        witnesses=[]
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        divorce_status=Divorced(divorce_date=divorce_date),
        family_events=[divorce_event]
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_timeline_events(person, family_repo, person_repo)

    assert any(e['type'] == 'divorce' for e in result)
    divorce_event_result = [e for e in result if e['type'] == 'divorce'][0]
    assert divorce_event_result['note'] == "Amicable split"


def test_get_timeline_events_with_death():
    """Test timeline events with death."""
    death_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=31, month=12, year=2050, prec=Sure())
    )

    person = create_basic_person(
        death_status=Dead(
            death_reason=DeathReason.UNSPECIFIED,
            date_of_death=death_date
        ),
        death_place="Hospital"
    )

    family_repo = Mock()
    person_repo = Mock()

    result = get_timeline_events(person, family_repo, person_repo)

    assert len(result) == 1
    assert result[0]['type'] == 'death'
    assert result[0]['place'] == "Hospital"


def test_get_timeline_events_chronological_order():
    """Test that timeline events are sorted chronologically."""
    birth_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=1, month=1, year=1990, prec=Sure())
    )
    marriage_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=15, month=6, year=2015, prec=Sure())
    )
    death_date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=31, month=12, year=2050, prec=Sure())
    )

    person = create_basic_person(
        index=1,
        birth_date=birth_date,
        death_status=Dead(
            death_reason=DeathReason.UNSPECIFIED,
            date_of_death=death_date
        ),
        families=[1]
    )

    spouse = create_basic_person(index=2)

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        marriage_date=marriage_date
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_timeline_events(person, family_repo, person_repo)

    assert result[0]['type'] == 'birth'
    assert result[1]['type'] == 'marriage'
    assert result[2]['type'] == 'death'


# ===== Test get_notes =====

def test_get_notes_no_notes():
    """Test notes extraction with no notes."""
    person = create_basic_person()

    family_repo = Mock()
    person_repo = Mock()

    result = get_notes(person, family_repo, person_repo)

    assert result['individual_notes'] == []
    assert result['marriage_notes'] == []


def test_get_notes_with_marriage_note():
    """Test notes extraction with marriage note."""
    person = create_basic_person(index=1, families=[1])

    spouse = create_basic_person(
        index=2,
        first_name="Jane",
        surname="Smith"
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        marriage_note="Met at university"
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_notes(person, family_repo, person_repo)

    assert len(result['marriage_notes']) == 1
    assert result['marriage_notes'][0]['spouse_name'] == "Jane Smith"
    assert result['marriage_notes'][0]['content'] == "Met at university"


def test_get_notes_with_comment():
    """Test notes extraction with family comment."""
    person = create_basic_person(index=1, families=[1])

    spouse = create_basic_person(
        index=2,
        first_name="Jane",
        surname="Smith"
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        comment="Happy family"
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_notes(person, family_repo, person_repo)

    assert len(result['marriage_notes']) == 1
    assert result['marriage_notes'][0]['content'] == "Happy family"


def test_get_notes_with_both():
    """Test notes extraction with both marriage note and comment."""
    person = create_basic_person(index=1, families=[1])

    spouse = create_basic_person(
        index=2,
        first_name="Jane",
        surname="Smith"
    )

    family = create_basic_family(
        index=1,
        parents=Parents.from_couple(1, 2),
        marriage_note="Met at university",
        comment="Happy family"
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    person_repo = Mock()
    person_repo.get_person_by_id.return_value = spouse

    result = get_notes(person, family_repo, person_repo)

    assert len(result['marriage_notes']) == 1
    assert "Met at university" in result['marriage_notes'][0]['content']
    assert "Happy family" in result['marriage_notes'][0]['content']


# ===== Test get_event_name =====

def test_get_event_name_fam_marriage():
    """Test event name formatting for FamMarriage."""
    event = FamMarriage()
    result = get_event_name(event)
    assert result == "Marriage"


def test_get_event_name_fam_divorce():
    """Test event name formatting for FamDivorce."""
    event = FamDivorce()
    result = get_event_name(event)
    assert result == "Divorce"


def test_get_event_name_fam_separated():
    """Test event name formatting for FamSeparated."""
    event = FamSeparated()
    result = get_event_name(event)
    assert result == "Separated"


def test_get_event_name_pers_birth():
    """Test event name formatting for PersBirth."""
    event = PersBirth()
    result = get_event_name(event)
    assert result == "Birth"


def test_get_event_name_pers_death():
    """Test event name formatting for PersDeath."""
    event = PersDeath()
    result = get_event_name(event)
    assert result == "Death"


# ===== Test get_sources =====

def test_get_sources_person_source():
    """Test sources extraction with person source."""
    person = create_basic_person(
        src="Birth certificate"
    )

    family_repo = Mock()

    result = get_sources(person, family_repo)

    assert len(result) == 1
    assert result[0]['type'] == 'individual'
    assert result[0]['content'] == "Birth certificate"


def test_get_sources_birth_and_death():
    """Test sources extraction with birth and death sources."""
    person = create_basic_person(
        birth_src="Hospital records",
        death_src="Death certificate"
    )

    family_repo = Mock()

    result = get_sources(person, family_repo)

    assert len(result) == 2
    assert any(s['type'] == 'birth' for s in result)
    assert any(s['type'] == 'death' for s in result)


def test_get_sources_family_source():
    """Test sources extraction with family source."""
    person = create_basic_person(index=1, families=[1])

    family = create_basic_family(
        index=1,
        src="Marriage certificate"
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    result = get_sources(person, family_repo)

    assert len(result) == 1
    assert result[0]['type'] == 'family'
    assert result[0]['content'] == "Marriage certificate"


def test_get_sources_event_source():
    """Test sources extraction with event source."""
    person = create_basic_person(index=1, families=[1])

    marriage_event = FamilyEvent(
        name=FamMarriage(),
        date=None,
        place="",
        reason="",
        note="",
        src="Church records",
        witnesses=[]
    )

    family = create_basic_family(
        index=1,
        family_events=[marriage_event]
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    result = get_sources(person, family_repo)

    assert len(result) == 1
    assert result[0]['type'] == 'Marriage'
    assert result[0]['content'] == "Church records"


def test_get_sources_multiple():
    """Test sources extraction with multiple sources."""
    person = create_basic_person(
        index=1,
        src="Personal records",
        birth_src="Birth certificate",
        families=[1]
    )

    family = create_basic_family(
        index=1,
        src="Marriage records"
    )

    family_repo = Mock()
    family_repo.get_family_by_id.return_value = family

    result = get_sources(person, family_repo)

    assert len(result) == 3


# ===== Test format_date =====

def test_format_date_gregorian():
    """Test formatting a Gregorian calendar date."""
    date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=25, month=12, year=2000, prec=Sure())
    )

    result = format_date(date)

    assert result == "25 December 2000"


def test_format_date_julian():
    """Test formatting a Julian calendar date."""
    date = CalendarDate(
        cal=Calendar.JULIAN,
        dmy=DateValue(day=1, month=1, year=1900, prec=Sure())
    )

    result = format_date(date)

    assert result == "1 January 1900"


def test_format_date_french():
    """Test formatting a French Revolutionary calendar date."""
    date = CalendarDate(
        cal=Calendar.FRENCH,
        dmy=DateValue(day=10, month=5, year=1793, prec=Sure())
    )

    result = format_date(date)

    assert result == "10 Pluviôse 1793"


def test_format_date_hebrew():
    """Test formatting a Hebrew calendar date."""
    date = CalendarDate(
        cal=Calendar.HEBREW,
        dmy=DateValue(day=15, month=7, year=5783, prec=Sure())
    )

    result = format_date(date)

    assert result == "15 Nisan 5783"


def test_format_date_partial():
    """Test formatting a date with missing day."""
    date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=0, month=6, year=1985, prec=Sure())
    )

    result = format_date(date)

    assert result == "June 1985"


def test_format_date_year_only():
    """Test formatting a date with only year."""
    date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=0, month=0, year=1900, prec=Sure())
    )

    result = format_date(date)

    assert result == "1900"


def test_format_date_not_calendar_date():
    """Test formatting with non-CalendarDate object."""
    result = format_date("not a date")
    assert result == ""


def test_format_date_all_zeros():
    """Test formatting with all zeros."""
    date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=0, month=0, year=0, prec=Sure())
    )

    result = format_date(date)

    assert result == ""


def test_format_date_invalid_month():
    """Test formatting with invalid month number."""
    date = CalendarDate(
        cal=Calendar.GREGORIAN,
        dmy=DateValue(day=15, month=99, year=2000, prec=Sure())
    )

    result = format_date(date)

    # Should only have day and year since month is invalid
    assert result == "15 2000"
