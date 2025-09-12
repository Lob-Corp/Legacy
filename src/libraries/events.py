from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, TypeVar

from date import CompressedDate


class EventWitnessKind(Enum):
    WITNESS = "Witness"
    WITNESS_GODPARENT = "Witness_GodParent"
    WITNESS_CIVILOFFICER = "Witness_CivilOfficer"
    WITNESS_RELIGIOUSOFFICER = "Witness_ReligiousOfficer"
    WITNESS_INFORMANT = "Witness_Informant"
    WITNESS_ATTENDING = "Witness_Attending"
    WITNESS_MENTIONED = "Witness_Mentioned"
    WITNESS_OTHER = "Witness_Other"


EventDescriptorT = TypeVar('EventDescriptorT')
PersonT = TypeVar('PersonT')

# Personal events


class PersEventNameBase(Generic[EventDescriptorT]):
    def __init__(self):
        raise NotImplementedError(
            "EventNameBase is a base class and cannot be instantiated directly. Use one of its subclasses instead."
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
    def __init__(self, name: EventDescriptorT):
        self.name = name


@dataclass(frozen=True)
class PersonalEvent(Generic[PersonT, EventDescriptorT]):
    name: PersEventNameBase[EventDescriptorT]
    date: CompressedDate
    place: EventDescriptorT
    reason: EventDescriptorT
    note: EventDescriptorT
    src: EventDescriptorT
    witnesses: list[tuple[PersonT, EventWitnessKind]]

# Family events


class FamEventNameBase(Generic[EventDescriptorT]):
    def __init__(self):
        raise NotImplementedError(
            "FamEventNameBase is a base class and cannot be instantiated directly. Use one of its subclasses instead."
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
    def __init__(self, name: EventDescriptorT):
        self.name = name


@dataclass(frozen=True)
class FamilyEvent(Generic[PersonT, EventDescriptorT]):
    name: FamEventNameBase[EventDescriptorT]
    date: CompressedDate
    place: EventDescriptorT
    reason: EventDescriptorT
    note: EventDescriptorT
    src: EventDescriptorT
    witnesses: list[tuple[PersonT, EventWitnessKind]]
