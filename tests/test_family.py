from libraries.consanguinity_rate import ConsanguinityRate
import pytest
from libraries.date import Calendar
from libraries.events import EventWitnessKind, FamMarriage, FamilyEvent
from libraries.family import Ascendants, DivorceStatusBase, Divorced, Family, MaritalStatus, NotDivorced, Parents, Relation, RelationToParentType, Separated


# ---- __init__ ----
def test_init_with_list_of_ints():
    p = Parents([1, 2])
    assert p.parents == [1, 2]


def test_init_empty_list():
    with pytest.raises(AssertionError):
        _ = Parents([])


def test_init_type_check_fails():
    with pytest.raises(AssertionError):
        Parents([1, "not same type"])


# ---- from_couple ----
def test_from_couple_with_ints():
    p = Parents.from_couple(1, 2)
    assert isinstance(p, Parents)
    assert p.parents == [1, 2]


def test_from_couple_type_check_fails():
    with pytest.raises(AssertionError):
        Parents.from_couple(1, "x")


# ---- is_couple ----
def test_is_couple_true():
    p = Parents([1, 2])
    assert p.is_couple() is True


def test_is_couple_false():
    p = Parents([1])
    assert p.is_couple() is False


# ---- couple ----
def test_couple_returns_tuple():
    p = Parents([1, 2])
    assert p.couple() == (1, 2)


def test_couple_raises_if_not_two():
    p = Parents([1])
    with pytest.raises(AssertionError):
        p.couple()


# ---- father ----
def test_father_returns_first():
    p = Parents([1, 2])
    assert p.father() == 1


def test_father_with_one_parent():
    p = Parents([42])
    assert p.father() == 42


# ---- mother ----
def test_mother_returns_second():
    p = Parents([1, 2])
    assert p.mother() == 2


def test_mother_raises_if_not_enough():
    p = Parents([1])
    with pytest.raises(AssertionError):
        p.mother()


# ---- __getitem__ ----
def test_getitem_valid_index():
    p = Parents([1, 2, 3])
    assert p[0] == 1
    assert p[2] == 3


def test_getitem_out_of_range():
    p = Parents([1])
    with pytest.raises(AssertionError):
        _ = p[5]

# DivorceStatusBase hierarchy


def test_divorcestatusbase_cannot_instantiate():
    with pytest.raises(NotImplementedError):
        DivorceStatusBase()


def test_notdivorced_instantiation():
    nd = NotDivorced()
    assert isinstance(nd, NotDivorced)
    assert isinstance(nd, DivorceStatusBase)


def test_divorced_instantiation_and_date():
    date = (Calendar.GREGORIAN, 123)
    d = Divorced(date)
    assert isinstance(d, Divorced)
    assert d.divorce_date == date


def test_separated_instantiation():
    s = Separated()
    assert isinstance(s, Separated)
    assert isinstance(s, DivorceStatusBase)


# --- RelationToParentType Enum ---


def test_relation_to_parent_enum_values():
    assert RelationToParentType.ADOPTION.value == "Adoption"
    assert RelationToParentType.RECOGNITION.value == "Recognition"
    assert RelationToParentType.CANDIDATEPARENT.value == "CandidateParent"
    assert RelationToParentType.GODPARENT.value == "GodParent"
    assert RelationToParentType.FOSTERPARENT.value == "FosterParent"

# --- Relation dataclass ---


def test_relation_with_parents():
    father = "John"
    mother = "Jane"
    relation = Relation(
        type=RelationToParentType.ADOPTION,
        father=father,
        mother=mother,
        sources=["source1", "source2"]
    )
    assert relation.type == RelationToParentType.ADOPTION
    assert relation.father == "John"
    assert relation.mother == "Jane"
    assert relation.sources == ["source1", "source2"]


def test_relation_without_parents():
    relation = Relation[int, str](
        type=RelationToParentType.GODPARENT,
        father=None,
        mother=None,
        sources=[]
    )
    assert relation.type == RelationToParentType.GODPARENT
    assert relation.father is None
    assert relation.mother is None
    assert relation.sources == []

# --- Ascendants dataclass ---


def test_ascendants_with_parents():
    parents = ("Father", "Mother")
    consanguinity = ConsanguinityRate(42)  # real class tested elsewhere
    asc = Ascendants(parents=parents, consanguinity_rate=consanguinity)
    assert asc.parents == parents
    assert asc.consanguinity_rate == consanguinity


def test_ascendants_without_parents():
    consanguinity = ConsanguinityRate(0)
    asc = Ascendants[int](parents=None, consanguinity_rate=consanguinity)
    assert asc.parents is None
    assert asc.consanguinity_rate == consanguinity

# --- Family dataclass ---


def test_family_full_creation():
    date = "2025-01-01"
    events = [
        FamilyEvent[int, str | None](
            name=FamMarriage(),
            date=date,
            place="Paris",
            reason=None,
            note="note",
            src="src",
            witnesses=[]
        )
    ]

    fam = Family[int, int, str | None](
        index=1,
        marriage_date=date,
        marriage_place="Paris",
        marriage_note="note",
        marriage_src="src",
        witnesses=[1, 2],
        divorce=NotDivorced(),
        relation_kind=MaritalStatus.MARRIED,
        family_events=events,
        comment="comment",
        origin_file="file.gw",
        src="source"
    )

    assert fam.index == 1
    assert fam.marriage_date == date
    assert fam.marriage_place == "Paris"
    assert fam.marriage_note == "note"
    assert fam.marriage_src == "src"
    assert fam.witnesses == [1, 2]
    assert fam.relation_kind == MaritalStatus.MARRIED
    assert fam.family_events == events
    assert fam.comment == "comment"
    assert fam.origin_file == "file.gw"
    assert fam.src == "source"
