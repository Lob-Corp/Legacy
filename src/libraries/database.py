from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, List, Tuple, TypeAlias, TypeVar

from libraries.date import DateValue
from libraries.family import Family
from libraries.person import Person


PersonT = TypeVar('PersonT')
PersonIndexT = TypeVar('PersonIndexT')
FamilyT = TypeVar('FamilyT')
DescendenceT = TypeVar('DescendenceT')
TitleT = TypeVar('TitleT')
PersEventT = TypeVar('PersEventT')
FamEventT = TypeVar('FamEventT')
DatabaseDescriptorT = TypeVar('DatabaseDescriptorT')


@dataclass(frozen=True)
class PersonDatabaseError(Exception, Generic[PersonT]):
    person: PersonT


class PersonAlreadyExistsError(PersonDatabaseError[PersonT]):
    pass


class PersonIsOwnAncestorError(PersonDatabaseError[PersonT]):
    pass


class BadSexOfMarriedPersonError(PersonDatabaseError[PersonT]):
    pass


class DatabaseWarningBase(
    Generic
    [PersonIndexT, PersonT, FamilyT, DescendenceT, TitleT, PersEventT,
     FamEventT]):
    def __init__(self):
        raise NotImplementedError(
            "DatabaseWarningBase is a base class and cannot be"
            "instantiated directly. Use one of its subclasses instead.")


@dataclass(frozen=True)
class BigAgeBetweenSpousesWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, None, None]):
    husband: PersonT
    wife: PersonT
    date: DateValue


@dataclass(frozen=True)
class BirthAfterDeathWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, None, None, None]):
    person: PersonT


@dataclass(frozen=True)
class IncoherentSexWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, None, None, None]):
    person: PersonT
    expected: int
    actual: int


@dataclass(frozen=True)
class ChangedOrderOfChildrenWarning(
        DatabaseWarningBase
        [PersonIndexT, None, FamilyT, DescendenceT, None, None, None]):
    family: FamilyT
    descendence: DescendenceT
    old_order: List[PersonIndexT]
    new_order: List[PersonIndexT]


@dataclass(frozen=True)
class ChangedOrderOfMarriagesWarning(
        DatabaseWarningBase[None, PersonT, FamilyT, None, None, None, None]):
    person: PersonT
    old_order: List[FamilyT]
    new_order: List[FamilyT]


@dataclass(frozen=True)
class ChangedOrderOfFamilyEventsWarning(
        DatabaseWarningBase[None, None, FamilyT, None, None, None, FamEventT]):
    family: FamilyT
    old_order: List[FamEventT]
    new_order: List[FamEventT]


@dataclass(frozen=True)
class ChangedOrderOfPersonEventsWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, PersEventT, None]
):
    person: PersonT
    old_order: List[PersEventT]
    new_order: List[PersEventT]


@dataclass(frozen=True)
class ChildrenNotInOrderWarning(
        DatabaseWarningBase
        [None, PersonT, FamilyT, DescendenceT, None, None, None]):
    family: FamilyT
    descendence: DescendenceT
    first_child: PersonT
    second_child: PersonT


@dataclass(frozen=True)
class CloseChildrenWarning(
        DatabaseWarningBase
        [None, PersonT, FamilyT, None, None, None, None]):
    family: FamilyT
    child1: PersonT
    child2: PersonT


@dataclass(frozen=True)
class DeadOldWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, None, None, None]):
    person: PersonT
    date: DateValue


@dataclass(frozen=True)
class DeadTooEarlyToBeFatherWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, None, None]):
    child: PersonT
    father: PersonT


@dataclass(frozen=True)
class DistantChildrenWarning(
        DatabaseWarningBase
        [None, PersonT, FamilyT, None, None, None, None]):
    family: FamilyT
    child1: PersonT
    child2: PersonT


@dataclass(frozen=True)
class FEventOrderWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, None, None, FamEventT]):
    person: PersonT
    event1: FamEventT
    event2: FamEventT


@dataclass(frozen=True)
class FWitnessEventAfterDeathWarning(
    DatabaseWarningBase[None, PersonT, FamilyT, None, None, None, FamEventT]
):
    person: PersonT
    event: FamEventT
    family: FamilyT


@dataclass(frozen=True)
class FWitnessEventBeforeBirthWarning(
        DatabaseWarningBase[None, PersonT, FamilyT, None, None, None, FamEventT
                            ]):
    person: PersonT
    event: FamEventT
    family: FamilyT


@dataclass(frozen=True)
class IncoherentAncestorDateWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, None, None]):
    ancestor: PersonT
    person: PersonT


@dataclass(frozen=True)
class MarriageDateAfterDeathWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, None, None]):
    person: PersonT


@dataclass(frozen=True)
class MarriageDateBeforeBirthWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, None, None]):
    person: PersonT


@dataclass(frozen=True)
class MotherDeadBeforeChildBirthWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, None, None]):
    mother: PersonT
    child: PersonT


@dataclass(frozen=True)
class ParentBornAfterChildWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, None, None]):
    parent: PersonT
    child: PersonT


@dataclass(frozen=True)
class ParentTooOldWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, None, None, None]):
    parent: PersonT
    date: DateValue
    child: PersonT


@dataclass(frozen=True)
class ParentTooYoungWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, None, None, None]):
    parent: PersonT
    date: DateValue
    child: PersonT


@dataclass(frozen=True)
class PEventOrderWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, None, PersEventT, None]):
    person: PersonT
    event1: PersEventT
    event2: PersEventT


@dataclass(frozen=True)
class PossibleDuplicateFamWarning(
        DatabaseWarningBase[None, None, FamilyT, None, None, None, None]):
    family1: FamilyT
    family2: FamilyT


@dataclass(frozen=True)
class PossibleDuplicateFamHomonymousWarning(
        DatabaseWarningBase[None, PersonT, FamilyT, None, None, None, None]):
    family1: FamilyT
    family2: FamilyT
    spouse: PersonT


@dataclass(frozen=True)
class PWitnessEventAfterDeathWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, PersEventT, None]
):
    person: PersonT
    event: PersEventT
    witness: PersonT


@dataclass(frozen=True)
class PWitnessEventBeforeBirthWarning(
        DatabaseWarningBase[None, PersonT, None, None, None, PersEventT, None]
):
    person: PersonT
    event: PersEventT
    witness: PersonT


@dataclass(frozen=True)
class TitleDatesErrorWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, TitleT, None, None]):
    person: PersonT
    title: TitleT


@dataclass(frozen=True)
class UndefinedSexWarning(
        DatabaseWarningBase
        [None, PersonT, None, None, None, None, None]):
    person: PersonT


@dataclass(frozen=True)
class YoungForMarriageWarning(
        DatabaseWarningBase[None, PersonT, FamilyT, None, None, None, None]):
    person: PersonT
    date: DateValue
    family: FamilyT


@dataclass(frozen=True)
class OldForMarriageWarning(
        DatabaseWarningBase
        [None, PersonT, FamilyT, None, None, None, None]):
    person: PersonT
    date: DateValue
    family: FamilyT


class DatabaseMiscInfoBase(Generic[PersonT, DescendenceT, TitleT]):
    def __init__(self):
        raise NotImplementedError(
            "DatabaseMiscInfoBase is a base class and cannot be"
            "instantiated directly. Use one of its subclasses instead.")


@dataclass(frozen=True)
class MissingSourceInfo(DatabaseMiscInfoBase[PersonT, DescendenceT, TitleT]):
    person: PersonT
    descendence: DescendenceT
    title: TitleT


class DatabaseReadingMode(Enum):
    ALL = "All"
    FIRST_LINE = "FirstLine"
    DEG = "Deg"


@dataclass(frozen=True)
class DatabaseNote:
    read: Callable[[str, DatabaseReadingMode], str]
    origin_file: str
    files: List[str]


class DatabaseUpdatedInfoBase(
        Generic[PersonIndexT, PersonT, FamilyT, DatabaseDescriptorT]):
    def __init__(self):
        raise NotImplementedError(
            "DatabaseUpdatedInfoBase is a base class and cannot be"
            "instantiated directly. Use one of its subclasses instead.")


@dataclass(frozen=True)
class PersonAddedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]


@dataclass(frozen=True)
class PersonModifiedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    old_person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    new_person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]


@dataclass(frozen=True)
class PersonDeletedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]


@dataclass(frozen=True)
class PersonMergedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    result_person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    person1: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    person2: Person[PersonIndexT, PersonT, DatabaseDescriptorT]


@dataclass(frozen=True)
class SendImageInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]


@dataclass(frozen=True)
class DeleteImageInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]


@dataclass(frozen=True)
class FamilyAddedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, FamilyT, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    family: Family[PersonT, FamilyT, DatabaseDescriptorT]


@dataclass(frozen=True)
class FamilyDeletedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, FamilyT, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    family: Family[PersonT, FamilyT, DatabaseDescriptorT]


@dataclass(frozen=True)
class FamilyModifiedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, FamilyT, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    old_family: Family[PersonT, FamilyT, DatabaseDescriptorT]
    new_family: Family[PersonT, FamilyT, DatabaseDescriptorT]


@dataclass(frozen=True)
class FamilyMergedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, FamilyT, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    result_family: Family[PersonT, FamilyT, DatabaseDescriptorT]
    family1: Family[PersonT, FamilyT, DatabaseDescriptorT]
    family2: Family[PersonT, FamilyT, DatabaseDescriptorT]


@dataclass(frozen=True)
class FamilyInvertedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, FamilyT, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    iverted_family: FamilyT


ChildrenNamesChangedInfoChanges: TypeAlias = Tuple[str, str, int, PersonT]


@dataclass(frozen=True)
class ChildrenNamesChangedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    changes: List[Tuple[ChildrenNamesChangedInfoChanges,
                        ChildrenNamesChangedInfoChanges]]


@dataclass(frozen=True)
class ParentAddedInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, FamilyT, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    family: Family[PersonT, FamilyT, DatabaseDescriptorT]


@dataclass(frozen=True)
class AncestorsKilledInfo(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]


@dataclass(frozen=True)
class MultiPersonModified(
        DatabaseUpdatedInfoBase
        [PersonIndexT, PersonT, None, DatabaseDescriptorT]):
    old_person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    new_person: Person[PersonIndexT, PersonT, DatabaseDescriptorT]
    multi: bool


@dataclass(frozen=True)
class NotesUpdatedInfo(DatabaseUpdatedInfoBase[None, None, None, None]):
    note: int | None
    description: str
