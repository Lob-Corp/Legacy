from database.person import Person
from database.family import Family
from database.place import Place
from database.family_event import FamilyEvent
from database.date_value import DateValue
from database.ascends import Ascends
from database.couple import Couple
from database.couple_parents import CoupleParents
from database.descend_children import DescendChildren
from database.descends import Descends
from database.family_event_witness import FamilyEventWitness
from database.family_events import FamilyEvents
from database.family_witness import FamilyWitness
from database.person_event_witness import PersonEventWitness
from database.person_events import PersonEvents
from database.person_non_native_relations import PersonNonNativeRelations
from database.person_relations import PersonRelations
from database.person_titles import PersonTitles
from database.personal_event import PersonalEvent
from database.relation import Relation
from database.titles import Titles
from database.union_families import UnionFamilies
from database.unions import Unions


def test_person_instantiation():
    p = Person()
    assert isinstance(p, Person)


def test_family_instantiation():
    f = Family()
    assert isinstance(f, Family)


def test_place_instantiation():
    pl = Place()
    assert isinstance(pl, Place)


def test_family_event_instantiation():
    fe = FamilyEvent()
    assert isinstance(fe, FamilyEvent)


def test_date_value_instantiation():
    dv = DateValue()
    assert isinstance(dv, DateValue)


def test_ascends_instantiation():
    a = Ascends()
    assert isinstance(a, Ascends)


def test_couple_instantiation():
    c = Couple()
    assert isinstance(c, Couple)


def test_couple_parents_instantiation():
    cp = CoupleParents()
    assert isinstance(cp, CoupleParents)


def test_descend_children_instantiation():
    dc = DescendChildren()
    assert isinstance(dc, DescendChildren)


def test_descends_instantiation():
    d = Descends()
    assert isinstance(d, Descends)


def test_family_event_witness_instantiation():
    few = FamilyEventWitness()
    assert isinstance(few, FamilyEventWitness)


def test_family_events_instantiation():
    fev = FamilyEvents()
    assert isinstance(fev, FamilyEvents)


def test_family_witness_instantiation():
    fw = FamilyWitness()
    assert isinstance(fw, FamilyWitness)


def test_person_event_witness_instantiation():
    pew = PersonEventWitness()
    assert isinstance(pew, PersonEventWitness)


def test_person_events_instantiation():
    pev = PersonEvents()
    assert isinstance(pev, PersonEvents)


def test_person_non_native_relations_instantiation():
    pnnr = PersonNonNativeRelations()
    assert isinstance(pnnr, PersonNonNativeRelations)


def test_person_relations_instantiation():
    pr = PersonRelations()
    assert isinstance(pr, PersonRelations)


def test_person_titles_instantiation():
    pt = PersonTitles()
    assert isinstance(pt, PersonTitles)


def test_personal_event_instantiation():
    pe = PersonalEvent()
    assert isinstance(pe, PersonalEvent)


def test_relation_instantiation():
    r = Relation()
    assert isinstance(r, Relation)


def test_titles_instantiation():
    t = Titles()
    assert isinstance(t, Titles)


def test_union_families_instantiation():
    uf = UnionFamilies()
    assert isinstance(uf, UnionFamilies)


def test_unions_instantiation():
    u = Unions()
    assert isinstance(u, Unions)
