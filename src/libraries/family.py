from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, Tuple, TypeVar

from libraries.consanguinity_rate import ConsanguinityRate
from libraries.date import CompressedDate
from libraries.events import FamilyEvent


class MaritalStatus(Enum):
    MARRIED = "MARRIED"
    NOT_MARRIED = "NOT_MARRIED"
    ENGAGED = "ENGAGED"
    NO_SEXES_CHECK_NOT_MARRIED = "NO_SEXES_CHECK_NOT_MARRIED"
    NO_MENTION = "NO_MENTION"
    NO_SEXES_CHECK_MARRIED = "NO_SEXES_CHECK_MARRIED"
    MARRIAGE_BANN = "MARRIAGE_BANN"
    MARRIAGE_CONTRACT = "MARRIAGE_CONTRACT"
    MARRIAGE_LICENSE = "MARRIAGE_LICENSE"
    PACS = "PACS"
    RESIDENCE = "RESIDENCE"


PersonT = TypeVar('PersonT')


class Parents(Generic[PersonT]):
    def __init__(self, parents: List[PersonT]):
        assert len(parents) != 0, "Parents List cannot be empty"
        assert all(isinstance(p, type(parents[0]))
                   for p in parents), "All parents must be of the same type"
        self.parents = parents

    @staticmethod
    def from_couple(a: PersonT, b: PersonT) -> 'Parents[PersonT]':
        return Parents([a, b])

    def is_couple(self) -> bool:
        return len(self.parents) == 2

    def couple(self) -> Tuple[PersonT, PersonT]:
        assert len(self.parents) == 2, "Is not a couple"
        return (self.parents[0], self.parents[1])

    def father(self) -> PersonT:
        """
        Get first parent.
        Warning: homophobic and heteronormative
        assumption, use with caution"""
        assert len(self.parents) >= 1
        return self.parents[0]

    def mother(self) -> PersonT:
        """
        Get second parent.
        Warning: homophobic and heteronormative
        assumption, use with caution"""
        assert len(self.parents) >= 2
        return self.parents[1]

    def __getitem__(self, index: int) -> PersonT:
        assert 0 <= index < len(self.parents), "Index out of range"
        return self.parents[index]


class DivorceStatusBase:
    def __init__(self):
        raise NotImplementedError(
            "DivorceStatusBase is a base class and cannot be"
            "instantiated directly. Use one of its subclasses instead.")


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


RelationDescriptorT = TypeVar('RelationDescriptorT')


@dataclass(frozen=True)
class Relation(Generic[PersonT, RelationDescriptorT]):
    type: RelationToParentType
    father: PersonT | None
    mother: PersonT | None
    sources: RelationDescriptorT


FamilyT = TypeVar('FamilyT')


@dataclass(frozen=True)
class Ascendants(Generic[FamilyT]):
    parents: FamilyT | None
    consanguinity_rate: ConsanguinityRate


IdxT = TypeVar('IdxT')
FamilyDescriptorT = TypeVar('FamilyDescriptorT')


@dataclass(frozen=True)
class Family(Generic[IdxT, PersonT, FamilyDescriptorT]):
    index: IdxT
    marriage_date: CompressedDate
    marriage_place: FamilyDescriptorT
    marriage_note: FamilyDescriptorT
    marriage_src: FamilyDescriptorT
    witnesses: List[PersonT]
    relation_kind: MaritalStatus
    divorce_status: DivorceStatusBase
    family_events: List[FamilyEvent[PersonT, FamilyDescriptorT]]
    comment: FamilyDescriptorT
    origin_file: FamilyDescriptorT  # .gw filename
    src: FamilyDescriptorT
