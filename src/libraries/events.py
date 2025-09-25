"""
events.py
-----------
Small, strongly-typed representations for personal and family events used
throughout the codebase. This module defines:

- EventWitnessKind: enumerates kinds of witnesses/participants in events.
- Pers* and Fam* event name classes: lightweight markers for event kinds.
- PersonalEvent and FamilyEvent dataclasses: main, generic containers for
    event data (name, date, place, reason, note, source, witnesses).

These types are intentionally thin and generic so callers can store arbitrary
descriptor types (strings, structured descriptors, or IDs) as event fields.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, List, Optional, Tuple, TypeVar, Callable

from libraries.date import CompressedDate, Date


class EventWitnessKind(Enum):
    """Kinds of persons associated with an event.

    Use these enum values to tag people attached to an event (witnesses,
    informants, officiants, etc.). The underlying values are simple strings
    suitable for serialization.
    """

    WITNESS = "Witness"
    WITNESS_GODPARENT = "Witness_GodParent"
    WITNESS_CIVILOFFICER = "Witness_CivilOfficer"
    WITNESS_RELIGIOUSOFFICER = "Witness_ReligiousOfficer"
    WITNESS_INFORMANT = "Witness_Informant"
    WITNESS_ATTENDING = "Witness_Attending"
    WITNESS_MENTIONED = "Witness_Mentioned"
    WITNESS_OTHER = "Witness_Other"


EventDescriptorT = TypeVar("EventDescriptorT")
PersonT = TypeVar("PersonT")

# Personal events


class PersEventNameBase(Generic[EventDescriptorT]):
    """Base class for personal event name markers.

    Subclass this to represent a specific personal event kind. Instances of
    these marker classes are lightweight and typically used only as type
    discriminators; `PersNamedEvent` carries an actual descriptor payload.
    """

    def __init__(self):
        raise NotImplementedError(
            "EventNameBase is a base class and cannot be"
            "instantiated directly. Use one of its subclasses instead."
        )


class PersBirth(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersBaptism(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersDeath(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersBurial(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersCremation(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersAccomplishment(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersAcquisition(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersAdhesion(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersBaptismLDS(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersBarMitzvah(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersBatMitzvah(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersBenediction(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersChangeName(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersCircumcision(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersConfirmation(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersConfirmationLDS(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersDecoration(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersDemobilisationMilitaire(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersDiploma(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersDistinction(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersDotation(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersDotationLDS(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersEducation(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersElection(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersEmigration(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersExcommunication(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersFamilyLinkLDS(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersFirstCommunion(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersFuneral(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersGraduate(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersHospitalisation(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersIllness(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersImmigration(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersListePassenger(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersMilitaryDistinction(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersMilitaryPromotion(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersMilitaryService(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersMobilisationMilitaire(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersNaturalisation(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersOccupation(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersOrdination(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersProperty(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersRecensement(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersResidence(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersRetired(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersScellentChildLDS(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersScellentParentLDS(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersScellentSpouseLDS(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersVenteBien(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersWill(PersEventNameBase[Any]):
    def __init__(self):
        pass


class PersNamedEvent(PersEventNameBase[EventDescriptorT]):
    """Personal event type that carries a custom descriptor.

    Example: PersNamedEvent("HousePurchase") or PersNamedEvent(my_descriptor)
    where `my_descriptor` is an application-specific object describing the
    event.
    """

    def __init__(self, name: EventDescriptorT):
        self.name = name


@dataclass(frozen=True)
class PersonalEvent(Generic[PersonT, EventDescriptorT]):
    """Container for a personal event.

    Fields are generic so callers can use strings, structured descriptors, or
    domain-specific objects for `place`, `reason`, `note`, and `src`.

    - name: a marker or named event instance (see `PersNamedEvent`).
    - date: a `CompressedDate` (can represent compressed calendars, text, or None).
    - witnesses: list of (person, witness_kind) tuples.
    """

    name: PersEventNameBase[EventDescriptorT]
    date: CompressedDate
    place: EventDescriptorT
    reason: EventDescriptorT
    note: EventDescriptorT
    src: EventDescriptorT
    witnesses: List[Tuple[PersonT, EventWitnessKind]]

    def map_personal_event(
        self,
        date_mapper: Optional[Callable[[Date], Date]],
        string_mapper: Callable[[EventDescriptorT], EventDescriptorT],
        person_mapper: Callable[[PersonT], PersonT],
    ) -> "PersonalEvent[PersonT, EventDescriptorT]":
        event_name: PersEventNameBase[EventDescriptorT] = self.name
        if isinstance(self.name, PersNamedEvent):
            event_name = PersNamedEvent(string_mapper(self.name.name))

        return PersonalEvent(
            name=event_name,
            date=self.date.map_cdate(date_mapper),
            place=string_mapper(self.place),
            reason=string_mapper(self.reason),
            note=string_mapper(self.note),
            src=string_mapper(self.src),
            witnesses=[
                (person_mapper(personal), event_witness)
                for personal, event_witness in self.witnesses
            ],
        )


# Family events


class FamEventNameBase(Generic[EventDescriptorT]):
    """Base class for family event name markers (see PersEventNameBase).

    Subclass to provide family event kinds; use `FamNamedEvent` to attach a
    descriptor payload.
    """

    def __init__(self):
        raise NotImplementedError(
            "FamEventNameBase is a base class and cannot be"
            "instantiated directly. Use one of its subclasses instead."
        )


class FamMarriage(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamNoMarriage(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamNoMention(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamEngage(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamDivorce(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamSeparated(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamAnnulation(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamMarriageBann(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamMarriageContract(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamMarriageLicense(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamPACS(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamResidence(FamEventNameBase[Any]):
    def __init__(self):
        pass


class FamNamedEvent(FamEventNameBase[EventDescriptorT]):
    """Family event type that carries a custom descriptor (see PersNamedEvent)."""

    def __init__(self, name: EventDescriptorT):
        self.name = name


@dataclass(frozen=True)
class FamilyEvent(Generic[PersonT, EventDescriptorT]):
    """Container for a family-related event.

    Mirrors `PersonalEvent` but uses family-specific event name markers.
    """

    name: FamEventNameBase[EventDescriptorT]
    date: CompressedDate
    place: EventDescriptorT
    reason: EventDescriptorT
    note: EventDescriptorT
    src: EventDescriptorT
    witnesses: List[Tuple[PersonT, EventWitnessKind]]

    def map_family_event(
        self,
        string_mapper: Callable[[EventDescriptorT], EventDescriptorT],
        date_mapper: Callable[[Date], Date],
        witness_mapper: Callable[[PersonT], PersonT],
    ) -> "FamilyEvent[PersonT, EventDescriptorT]":
        event_name: FamEventNameBase[EventDescriptorT] = self.name
        if isinstance(self.name, FamNamedEvent):
            event_name = FamNamedEvent(string_mapper(self.name.name))

        return FamilyEvent(
            name=event_name,
            date=self.date.map_cdate(date_mapper),
            place=string_mapper(self.place),
            reason=string_mapper(self.reason),
            note=string_mapper(self.note),
            src=string_mapper(self.src),
            witnesses=[
                (witness_mapper(personal), event_witness)
                for personal, event_witness in self.witnesses
            ],
        )
