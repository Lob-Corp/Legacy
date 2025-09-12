import pytest
from events import *

# --- Personal Events ---


def test_personal_singleton_event_instantiation():
    with pytest.raises(NotImplementedError):
        PersEventNameBase()

    e = PersBirth()
    assert isinstance(e, PersEventNameBase)
    assert isinstance(e, PersBirth)


def test_personal_named_event():
    name = "Graduation"
    e = PersNamedEvent(name)
    assert e.name == name
    assert isinstance(e, PersNamedEvent)
    assert isinstance(e, PersEventNameBase)


def test_personal_event_dataclass():
    class DummyPerson:
        pass

    name = PersBirth()
    date = "2025-01-01"
    place = "Paris"
    reason = "Test"
    note = "Note"
    src = "Source"
    witnesses = [(5, EventWitnessKind.WITNESS)]

    event = PersonalEvent[int, str](
        name=name,
        date=date,
        place=place,
        reason=reason,
        note=note,
        src=src,
        witnesses=witnesses,
    )

    assert event.name == name
    assert event.date == date
    assert event.place == place
    assert event.reason == reason
    assert event.note == note
    assert event.src == src
    assert event.witnesses == witnesses


def test_personal_event_match():
    event_singleton = PersBirth()
    event_named = PersNamedEvent("Graduation")

    matched_singleton = None
    matched_named = None

    match event_singleton:
        case PersBirth():
            matched_singleton = True
        case _:
            matched_singleton = False

    match event_named:
        case PersNamedEvent(name=name):
            matched_named = name
        case _:
            matched_named = None

    assert matched_singleton is True
    assert matched_named == "Graduation"


# --- Family Events ---

def test_family_singleton_event_instantiation():
    with pytest.raises(NotImplementedError):
        FamEventNameBase()

    e = FamMarriage()
    assert isinstance(e, FamEventNameBase)
    assert isinstance(e, FamMarriage)


def test_family_named_event():
    name = "CustomMarriage"
    e = FamNamedEvent(name)
    assert e.name == name
    assert isinstance(e, FamNamedEvent)
    assert isinstance(e, FamEventNameBase)


def test_family_event_dataclass():
    class DummyPerson:
        pass

    name = FamMarriage()
    date = "2025-01-01"
    place = "Berlin"
    reason = "Test"
    note = "Note"
    src = "Source"
    witnesses = [(DummyPerson(), EventWitnessKind.WITNESS)]

    event = FamilyEvent(
        name=name,
        date=date,
        place=place,
        reason=reason,
        note=note,
        src=src,
        witnesses=witnesses,
    )

    assert event.name == name
    assert event.date == date
    assert event.place == place
    assert event.reason == reason
    assert event.note == note
    assert event.src == src
    assert event.witnesses == witnesses


def test_family_event_match():
    event_singleton = FamMarriage()
    event_named = FamNamedEvent("CustomMarriage")

    matched_singleton = None
    matched_named = None

    match event_singleton:
        case FamMarriage():
            matched_singleton = True
        case _:
            matched_singleton = False

    match event_named:
        case FamNamedEvent(name=name):
            matched_named = name
        case _:
            matched_named = None

    assert matched_singleton is True
    assert matched_named == "CustomMarriage"
