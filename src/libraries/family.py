from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from consanguinity_rate import ConsanguinityRate
from date import CompressedDate
from events import FamilyEvent

class MaritalStatus(Enum):
    MARRIED = "Married"
    NOT_MARRIED = "NotMarried"
    ENGAGED = "Engaged"
    NO_SEXES_CHECK_NOT_MARRIED = "NoSexesCheckNotMarried"
    NO_MENTION = "NoMention"
    NO_SEXES_CHECK_MARRIED = "NoSexesCheckMarried"
    MARRIAGE_BANN = "MarriageBann"
    MARRIAGE_CONTRACT = "MarriageContract"
    MARRIAGE_LICENSE = "MarriageLicense"
    PACS = "Pacs"
    RESIDENCE = "Residence"

Person = TypeVar('Person')

class Parents(Generic[Person]):
    def __init__(self, parents: list[Person]):
        assert len(parents) != 0, "Parents list cannot be empty"
        assert all(isinstance(p, type(parents[0])) for p in parents), "All parents must be of the same type"
        self.parents = parents

    @staticmethod
    def from_couple(a: Person, b: Person) -> 'Parents[Person]':
        return Parents([a, b])

    def is_couple(self) -> bool:
        return len(self.parents) == 2

    def couple(self) -> tuple[Person, Person]:
        assert len(self.parents) == 2, "Is not a couple"
        return (self.parents[0], self.parents[1])

    def father(self) -> Person:
        assert len(self.parents) >= 1
        return self.parents[0]

    def mother(self) -> Person:
        assert len(self.parents) >= 2
        return self.parents[1]

    def __getitem__(self, index: int) -> Person:
        assert 0 <= index < len(self.parents), "Index out of range"
        return self.parents[index]

class DivorceStatusBase:
    def __init__(self):
        raise NotImplementedError(
            "DivorceStatusBase is a base class and cannot be instantiated directly. Use one of its subclasses instead.")

class NotDivorced(DivorceStatusBase):
    def __init__(self):
        pass

class Divorced(DivorceStatusBase):
    def __init__(self, divorce_date: CompressedDate):
        self.divorce_date = divorce_date

class Separated(DivorceStatusBase):
    def __init__(self):
        pass

class RelationToParentType(Enum):
    ADOPTION = "Adoption"
    RECOGNITION = "Recognition"
    CANDIDATEPARENT = "CandidateParent"
    GODPARENT = "GodParent"
    FOSTERPARENT = "FosterParent"

RelationDescriptorType = TypeVar('RelationDescriptorType')

@dataclass(frozen=True)
class Relation(Generic[Person, RelationDescriptorType]):
    type: RelationToParentType
    father: Person | None
    mother: Person | None
    sources: list[RelationDescriptorType]

FamilyType = TypeVar('FamilyType')

@dataclass(frozen=True)
class Ascendants(Generic[FamilyType]):
    parents: FamilyType | None
    consanguinity_rate: ConsanguinityRate

IndexType = TypeVar('IndexType')
FamilyDescriptorType = TypeVar('FamilyDescriptorType')

@dataclass(frozen=True)
class Family(Generic[Person, IndexType, FamilyDescriptorType]):
    index: IndexType
    marriage_date: CompressedDate
    marriage_place: FamilyDescriptorType
    marriage_note: FamilyDescriptorType
    marriage_src: FamilyDescriptorType
    witnesses: list[Person]
    relation_kind: MaritalStatus
    family_events: list[FamilyEvent[Person, FamilyDescriptorType]]
    comment: FamilyDescriptorType
    origin_file: FamilyDescriptorType #.gw filename
    src: FamilyDescriptorType
