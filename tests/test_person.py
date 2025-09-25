from libraries.person import Person, Place, Sex
import pytest
from libraries.burial_info import UnknownBurial
from libraries.death_info import DontKnowIfDead, NotDead
from libraries.events import EventWitnessKind, PersBirth, PersonalEvent
from libraries.family import Relation, RelationToParentType
from libraries.title import AccessRight, Title, TitleName
from libraries.date import CompressedDate


@pytest.fixture
def compressed_date_fixture() -> CompressedDate:
    return "2025-01-01"


@pytest.fixture
def title_fixture(compressed_date_fixture) -> Title[str]:
    return Title[str](
        title_name=TitleName[str]("name"),
        ident="t1",
        place="Paris",
        date_start=compressed_date_fixture,
        date_end=compressed_date_fixture,
        nth=1,
    )


@pytest.fixture
def pers_event_fixture(compressed_date_fixture) -> PersonalEvent[int, str]:
    name = PersBirth()
    place = "Paris"
    reason = "Test"
    note = "Note"
    src = "Source"
    witnesses = [(5, EventWitnessKind.WITNESS)]

    return PersonalEvent[int, str](
        name=name,
        date=compressed_date_fixture,
        place=place,
        reason=reason,
        note=note,
        src=src,
        witnesses=witnesses,
    )


def test_place_full_creation():
    place = Place(
        town="Paris",
        township="Township",
        canton="Canton",
        district="District",
        county="County",
        region="Île-de-France",
        country="France",
        other="Extra info",
    )
    assert place.town == "Paris"
    assert place.region == "Île-de-France"
    assert place.country == "France"
    assert place.other == "Extra info"


# --- Person dataclass ---


def test_person_minimal_stubs(
    compressed_date_fixture, title_fixture, pers_event_fixture
):
    fake_relation = Relation[int, str](
        type=RelationToParentType.ADOPTION, father=None, mother=None, sources=[]
    )
    person = Person(
        index=1,
        first_name="Jean",
        surname="Dupont",
        occ=1,
        image="jean.png",
        public_name="Jean D.",
        qualifiers=["qual1"],
        aliases=["alias1"],
        first_names_aliases=["J"],
        surname_aliases=["Du."],
        titles=[title_fixture],
        non_native_parents_relation=[fake_relation],
        related_persons=[],
        occupation="Farmer",
        sex=Sex.MALE,
        access_right=AccessRight.PUBLIC,
        birth_date=compressed_date_fixture,
        birth_place="Paris",
        birth_note="note",
        birth_src="src",
        baptism_date=compressed_date_fixture,
        baptism_place="Church",
        baptism_note="bap note",
        baptism_src="bap src",
        death=DontKnowIfDead(),
        death_place="Paris",
        death_note="death note",
        death_src="death src",
        burial=UnknownBurial(),
        burial_place="Cemetery",
        burial_note="burial note",
        burial_src="burial src",
        personal_events=[pers_event_fixture],
        notes="general note",
        src="src file",
    )

    # Check key fields
    assert person.index == 1
    assert person.first_name == "Jean"
    assert person.surname == "Dupont"
    assert person.occupation == "Farmer"
    assert person.sex is Sex.MALE
    assert person.access_right == AccessRight.PUBLIC
    assert person.birth_place == "Paris"
    assert person.burial_place == "Cemetery"
    assert person.notes == "general note"


def test_person_with_empty_lists(compressed_date_fixture):
    person = Person[int, str, str](
        index=2,
        first_name="Alice",
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
        occupation="",
        sex=Sex.FEMALE,
        access_right=AccessRight.PRIVATE,
        birth_date=compressed_date_fixture,
        birth_place="",
        birth_note="",
        birth_src="",
        baptism_date=compressed_date_fixture,
        baptism_place="",
        baptism_note="",
        baptism_src="",
        death=NotDead(),
        death_place="",
        death_note="",
        death_src="",
        burial=UnknownBurial(),
        burial_place="",
        burial_note="",
        burial_src="",
        personal_events=[],
        notes="",
        src="",
    )

    assert person.index == 2
    assert person.sex is Sex.FEMALE
    assert person.access_right == AccessRight.PRIVATE
    assert person.titles == []
    assert person.personal_events == []
