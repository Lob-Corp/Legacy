from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

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


class PersBirth(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersBaptism(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersDeath(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersBurial(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersCremation(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersAccomplishment(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersAcquisition(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersAdhesion(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersBaptismLDS(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersBarMitzvah(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersBatMitzvah(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersBenediction(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersChangeName(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersCircumcision(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersConfirmation(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersConfirmationLDS(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersDecoration(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersDemobilisationMilitaire(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersDiploma(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersDistinction(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersDotation(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersDotationLDS(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersEducation(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersElection(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersEmigration(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersExcommunication(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersFamilyLinkLDS(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersFirstCommunion(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersFuneral(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersGraduate(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersHospitalisation(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersIllness(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersImmigration(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersListePassenger(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersMilitaryDistinction(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersMilitaryPromotion(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersMilitaryService(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersMobilisationMilitaire(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersNaturalisation(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersOccupation(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersOrdination(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersProperty(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersRecensement(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersResidence(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersRetired(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersScellentChildLDS(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersScellentParentLDS(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersScellentSpouseLDS(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersVenteBien(PersEventNameBase[None]):
    def __init__(self):
        pass


class PersWill(PersEventNameBase[None]):
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


class FamMarriage(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamNoMarriage(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamNoMention(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamEngage(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamDivorce(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamSeparated(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamAnnulation(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamMarriageBann(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamMarriageContract(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamMarriageLicense(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamPACS(FamEventNameBase[None]):
    def __init__(self):
        pass


class FamResidence(FamEventNameBase[None]):
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
