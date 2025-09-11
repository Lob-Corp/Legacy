from events import PersonalEvent
from family import Relation
from person import *
from title import Title


def test_place_full_creation():
    place = Place(
        town="Paris",
        township="Township",
        canton="Canton",
        district="District",
        county="County",
        region="Île-de-France",
        country="France",
        other="Extra info"
    )
    assert place.town == "Paris"
    assert place.region == "Île-de-France"
    assert place.country == "France"
    assert place.other == "Extra info"

# --- Person dataclass ---

def test_person_minimal_stubs():
    # placeholders for external types
    fake_date = "2025-01-01"  # CompressedDate stub
    fake_death = "dead"       # DeathStatusBase stub
    fake_burial = "buried"    # BurialInfoBase stub
    fake_title = Title(title_name="Duke", ident="t1", place="Paris", date_start=fake_date, date_end=fake_date, nth=1)
    fake_relation = Relation(type="Adoption", father=None, mother=None, sources=[])
    fake_event = PersonalEvent(name="Birth", date=fake_date, place="Paris", reason=None, note="note", src="src", witnesses=[])

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
        titles=[fake_title],
        NonNativeParentsRelation=[fake_relation],
        RelatedPersons=[],
        occupation="Farmer",
        sex=Sex.MALE,
        access_right=AccessRight.PUBLIC,
        birth_date=fake_date,
        birth_place="Paris",
        birth_note="note",
        birth_src="src",
        baptism_date=fake_date,
        baptism_place="Church",
        baptism_note="bap note",
        baptism_src="bap src",
        death=fake_death,
        death_place="Paris",
        death_note="death note",
        death_src="death src",
        burial=fake_burial,
        burial_place="Cemetery",
        burial_note="burial note",
        burial_src="burial src",
        personal_events=[fake_event],
        notes="general note",
        src="src file"
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

def test_person_with_empty_lists():
    fake_date = "today"
    fake_death = "dead"
    fake_burial = "buried"

    person = Person(
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
        NonNativeParentsRelation=[],
        RelatedPersons=[],
        occupation="",
        sex=Sex.FEMALE,
        access_right=AccessRight.PRIVATE,
        birth_date=fake_date,
        birth_place="",
        birth_note="",
        birth_src="",
        baptism_date=fake_date,
        baptism_place="",
        baptism_note="",
        baptism_src="",
        death=fake_death,
        death_place="",
        death_note="",
        death_src="",
        burial=fake_burial,
        burial_place="",
        burial_note="",
        burial_src="",
        personal_events=[],
        notes="",
        src=""
    )

    assert person.index == 2
    assert person.sex is Sex.FEMALE
    assert person.access_right == AccessRight.PRIVATE
    assert person.titles == []
    assert person.personal_events == []
