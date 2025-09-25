# test_database_info.py
from libraries.database import *
import pytest
from libraries.date import DateValue
from libraries.death_info import NotDead, UnknownBurial
from libraries.person import Person, Sex
from libraries.family import Family, MaritalStatus, NotDivorced
from libraries.title import AccessRight, Title, UseMainTitle


@pytest.fixture
def date_fixture() -> DateValue:
    return DateValue(1, 1, 2000, None, 0)


@pytest.fixture
def person_fixture(date_fixture) -> Person[int, str, str]:
    return Person(
        index=1,
        first_name="John",
        surname="Doe",
        occ=0,
        image="",
        public_name="John Doe",
        qualifiers=[],
        aliases=[],
        first_names_aliases=[],
        surname_aliases=[],
        titles=[],
        non_native_parents_relation=[],
        related_persons=[],
        occupation="Worker",
        sex=Sex.MALE,
        access_right=AccessRight.PUBLIC,
        birth_date=date_fixture,
        birth_place="Paris",
        birth_note="",
        birth_src="",
        baptism_date=date_fixture,
        baptism_place="",
        baptism_note="",
        baptism_src="",
        death=NotDead(),  # replace with DeathStatusBase if needed
        death_place="",
        death_note="",
        death_src="",
        burial=UnknownBurial(),
        burial_place="",
        burial_note="",
        burial_src="",
        personal_events=[],
        notes="",
        src=""
    )


@pytest.fixture
def family_fixture(date_fixture, person_fixture) -> Family[int, str, str]:
    return Family(
        index=1,
        marriage_date=date_fixture,
        marriage_place="Paris",
        marriage_note="",
        marriage_src="",
        witnesses=[person_fixture],
        relation_kind=MaritalStatus.MARRIED,
        divorce_status=NotDivorced(),
        family_events=[],
        comment="",
        origin_file="origin.gw",
        src=""
    )


@pytest.fixture
def title_fixture(date_fixture) -> Title[None]:
    return Title(title_name=UseMainTitle(), ident="T1", place="Paris", date_start=date_fixture, date_end=date_fixture, nth=1)
# ---- Tests for Database errors ----


def test_person_already_exists_error(person_fixture):
    err = PersonAlreadyExistsError(person=person_fixture)
    assert err.person == person_fixture


def test_person_is_own_ancestor_error(person_fixture):
    err = PersonIsOwnAncestorError(person=person_fixture)
    assert err.person == person_fixture


def test_bad_sex_of_married_person_error(person_fixture):
    err = BadSexOfMarriedPersonError(person=person_fixture)
    assert err.person == person_fixture


# ---- Base classes tests ----

def test_database_warning_base_raises():
    with pytest.raises(NotImplementedError):
        DatabaseWarningBase()


def test_database_misc_info_base_raises():
    with pytest.raises(NotImplementedError):
        DatabaseMiscInfoBase()


def test_database_updated_info_base_raises():
    with pytest.raises(NotImplementedError):
        DatabaseUpdatedInfoBase()


# ---- Warnings tests ----

def test_big_age_between_spouses_warning(person_fixture, date_fixture):
    warning = BigAgeBetweenSpousesWarning(
        husband=person_fixture, wife=person_fixture, date=date_fixture)
    assert warning.husband == person_fixture
    assert warning.wife == person_fixture
    assert warning.date == date_fixture


def test_birth_after_death_warning(person_fixture):
    warning = BirthAfterDeathWarning(person=person_fixture)
    assert warning.person == person_fixture


def test_incoherent_sex_warning(person_fixture):
    warning = IncoherentSexWarning(person=person_fixture, expected=1, actual=2)
    assert warning.expected == 1
    assert warning.actual == 2
    assert warning.person == person_fixture


def test_changed_order_of_children_warning(family_fixture, person_fixture):
    warning = ChangedOrderOfChildrenWarning(
        family=family_fixture,
        descendence=[person_fixture],
        old_order=[0],
        new_order=[0]
    )
    assert warning.family == family_fixture
    assert warning.descendence == [person_fixture]
    assert warning.old_order == [0]
    assert warning.new_order == [0]


def test_changed_order_of_marriages_warning(person_fixture, family_fixture):
    warning = ChangedOrderOfMarriagesWarning(
        person=person_fixture,
        old_order=[family_fixture],
        new_order=[family_fixture]
    )
    assert warning.person == person_fixture
    assert warning.old_order == [family_fixture]
    assert warning.new_order == [family_fixture]


def test_changed_order_of_family_events_warning(family_fixture):
    warning = ChangedOrderOfFamilyEventsWarning[Family[str, int, str], None](
        family=family_fixture,
        old_order=[],
        new_order=[]
    )
    assert warning.family == family_fixture
    assert warning.old_order == []
    assert warning.new_order == []


def test_changed_order_of_person_events_warning(person_fixture):
    warning = ChangedOrderOfPersonEventsWarning[Person[int, str, str], None](
        person=person_fixture,
        old_order=[],
        new_order=[]
    )
    assert warning.person == person_fixture
    assert warning.old_order == []
    assert warning.new_order == []


def test_children_not_in_order_warning(family_fixture, person_fixture):
    warning = ChildrenNotInOrderWarning(
        family=family_fixture,
        descendence=[person_fixture],
        first_child=person_fixture,
        second_child=person_fixture
    )
    assert warning.first_child == person_fixture
    assert warning.second_child == person_fixture


def test_close_children_warning(family_fixture, person_fixture):
    warning = CloseChildrenWarning(
        family=family_fixture, child1=person_fixture, child2=person_fixture)
    assert warning.child1 == person_fixture
    assert warning.child2 == person_fixture


def test_dead_old_warning(person_fixture, date_fixture):
    warning = DeadOldWarning(person=person_fixture, date=date_fixture)
    assert warning.person == person_fixture
    assert warning.date == date_fixture


def test_dead_too_early_to_be_father_warning(person_fixture):
    warning = DeadTooEarlyToBeFatherWarning(
        child=person_fixture, father=person_fixture)
    assert warning.child == person_fixture
    assert warning.father == person_fixture


def test_distant_children_warning(family_fixture, person_fixture):
    warning = DistantChildrenWarning(
        family=family_fixture, child1=person_fixture, child2=person_fixture)
    assert warning.child1 == person_fixture
    assert warning.child2 == person_fixture
    assert warning.family == family_fixture


def test_f_event_order_warning(person_fixture):
    warning = FEventOrderWarning(
        person=person_fixture, event1=None, event2=None)
    assert warning.person == person_fixture
    assert warning.event1 is None
    assert warning.event2 is None


def test_f_witness_event_after_death_warning(person_fixture, family_fixture):
    warning = FWitnessEventAfterDeathWarning(
        person=person_fixture, event=None, family=family_fixture)
    assert warning.person == person_fixture
    assert warning.family == family_fixture
    assert warning.event is None


def test_f_witness_event_before_birth_warning(person_fixture, family_fixture):
    warning = FWitnessEventBeforeBirthWarning(
        person=person_fixture, event=None, family=family_fixture)
    assert warning.person == person_fixture
    assert warning.family == family_fixture
    assert warning.event is None


def test_incoherent_ancestor_date_warning(person_fixture):
    warning = IncoherentAncestorDateWarning(
        ancestor=person_fixture, person=person_fixture)
    assert warning.ancestor == person_fixture
    assert warning.person == person_fixture


def test_marriage_date_after_death_warning(person_fixture):
    warning = MarriageDateAfterDeathWarning(person=person_fixture)
    assert warning.person == person_fixture


def test_marriage_date_before_birth_warning(person_fixture):
    warning = MarriageDateBeforeBirthWarning(person=person_fixture)
    assert warning.person == person_fixture


def test_mother_dead_before_child_birth_warning(person_fixture):
    warning = MotherDeadBeforeChildBirthWarning(
        mother=person_fixture, child=person_fixture)
    assert warning.mother == person_fixture
    assert warning.child == person_fixture


def test_parent_born_after_child_warning(person_fixture):
    warning = ParentBornAfterChildWarning(
        parent=person_fixture, child=person_fixture)
    assert warning.parent == person_fixture
    assert warning.child == person_fixture


def test_parent_too_old_warning(person_fixture, date_fixture):
    warning = ParentTooOldWarning(
        parent=person_fixture, date=date_fixture, child=person_fixture)
    assert warning.parent == person_fixture
    assert warning.date == date_fixture
    assert warning.child == person_fixture


def test_parent_too_young_warning(person_fixture, date_fixture):
    warning = ParentTooYoungWarning(
        parent=person_fixture, date=date_fixture, child=person_fixture)
    assert warning.parent == person_fixture
    assert warning.date == date_fixture
    assert warning.child == person_fixture


def test_p_event_order_warning(person_fixture):
    warning = PEventOrderWarning(
        person=person_fixture, event1=None, event2=None)
    assert warning.person == person_fixture
    assert warning.event1 is None
    assert warning.event2 is None


def test_possible_duplicate_fam_warning(family_fixture):
    warning = PossibleDuplicateFamWarning(
        family1=family_fixture, family2=family_fixture)
    assert warning.family1 == family_fixture
    assert warning.family2 == family_fixture


def test_possible_duplicate_fam_homonymous_warning(person_fixture, family_fixture):
    warning = PossibleDuplicateFamHomonymousWarning(
        family1=family_fixture, family2=family_fixture, spouse=person_fixture)
    assert warning.family1 == family_fixture
    assert warning.family2 == family_fixture
    assert warning.spouse == person_fixture


def test_p_witness_event_after_death_warning(person_fixture):
    warning = PWitnessEventAfterDeathWarning(
        person=person_fixture, event="Event1", witness=person_fixture)
    assert warning.person == person_fixture
    assert warning.event == "Event1"
    assert warning.witness == person_fixture


def test_p_witness_event_before_birth_warning(person_fixture):
    warning = PWitnessEventBeforeBirthWarning(
        person=person_fixture, event="Event1", witness=person_fixture)
    assert warning.person == person_fixture
    assert warning.event == "Event1"
    assert warning.witness == person_fixture


def test_title_dates_error_warning(person_fixture, title_fixture):
    warning = TitleDatesErrorWarning(
        person=person_fixture, title=title_fixture)
    assert warning.person == person_fixture
    assert warning.title == title_fixture


def test_undefined_sex_warning(person_fixture):
    warning = UndefinedSexWarning(person=person_fixture)
    assert warning.person == person_fixture


def test_young_for_marriage_warning(person_fixture, date_fixture, family_fixture):
    warning = YoungForMarriageWarning(
        person=person_fixture, date=date_fixture, family=family_fixture)
    assert warning.person == person_fixture
    assert warning.date == date_fixture
    assert warning.family == family_fixture


def test_old_for_marriage_warning(person_fixture, date_fixture, family_fixture):
    warning = OldForMarriageWarning(
        person=person_fixture, date=date_fixture, family=family_fixture)
    assert warning.person == person_fixture
    assert warning.date == date_fixture
    assert warning.family == family_fixture

# ---- Tests for DatabaseUpdatedInfo subclasses ----


def test_person_added_info(person_fixture):
    info = PersonAddedInfo(person=person_fixture)
    assert info.person == person_fixture


def test_person_modified_info(person_fixture):
    old_person = person_fixture
    new_person = person_fixture
    info = PersonModifiedInfo(old_person=old_person, new_person=new_person)
    assert info.old_person == old_person
    assert info.new_person == new_person


def test_person_deleted_info(person_fixture):
    info = PersonDeletedInfo(person=person_fixture)
    assert info.person == person_fixture


def test_person_merged_info(person_fixture):
    info = PersonMergedInfo(result_person=person_fixture,
                            person1=person_fixture, person2=person_fixture)
    assert info.result_person == person_fixture


def test_send_image_info(person_fixture):
    info = SendImageInfo(person=person_fixture)
    assert info.person == person_fixture


def test_delete_image_info(person_fixture):
    info = DeleteImageInfo(person=person_fixture)
    assert info.person == person_fixture


def test_family_added_info(person_fixture, family_fixture):
    info = FamilyAddedInfo(person=person_fixture, family=family_fixture)
    assert info.person == person_fixture
    assert info.family == family_fixture


def test_family_deleted_info(person_fixture, family_fixture):
    info = FamilyDeletedInfo(person=person_fixture, family=family_fixture)
    assert info.person == person_fixture
    assert info.family == family_fixture


def test_family_modified_info(person_fixture, family_fixture):
    old_family = family_fixture
    new_family = family_fixture
    info = FamilyModifiedInfo(person=person_fixture,
                              old_family=old_family, new_family=new_family)
    assert info.old_family == old_family
    assert info.new_family == new_family


def test_family_merged_info(person_fixture, family_fixture):
    info = FamilyMergedInfo(person=person_fixture, result_family=family_fixture,
                            family1=family_fixture, family2=family_fixture)
    assert info.result_family == family_fixture


def test_family_inverted_info(person_fixture, family_fixture):
    info = FamilyInvertedInfo(person=person_fixture,
                              iverted_family=family_fixture)
    assert info.iverted_family == family_fixture


def test_children_names_changed_info(person_fixture):
    change_tuple = ("old_first", "old_last", 1, person_fixture)
    info = ChildrenNamesChangedInfo[int, Person[int, str, str], str](person=person_fixture, changes=[
        (change_tuple, change_tuple)])
    assert info.person == person_fixture
    assert info.changes[0] == (change_tuple, change_tuple)


def test_parent_added_info(person_fixture, family_fixture):
    info = ParentAddedInfo(person=person_fixture, family=family_fixture)
    assert info.person == person_fixture
    assert info.family == family_fixture


def test_ancestors_killed_info(person_fixture):
    info = AncestorsKilledInfo(person=person_fixture)
    assert info.person == person_fixture


def test_multi_person_modified(person_fixture):
    info = MultiPersonModified(
        old_person=person_fixture, new_person=person_fixture, multi=True)
    assert info.multi is True


def test_notes_updated_info():
    note_info = NotesUpdatedInfo(note=5, description="Some note")
    assert note_info.note == 5
    assert note_info.description == "Some note"

    note_info_none = NotesUpdatedInfo(note=None, description="No note")
    assert note_info_none.note is None
    assert note_info_none.description == "No note"
