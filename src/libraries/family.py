from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, List, Tuple, TypeVar, override

from libraries.consanguinity_rate import ConsanguinityRate
from libraries.date import CompressedDate, Date
from libraries.events import FamilyEvent


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


PersonT = TypeVar("PersonT")


class Parents(Generic[PersonT]):
    def __init__(self, parents: List[PersonT]):
        assert len(parents) != 0, "Parents List cannot be empty"
        assert all(
            isinstance(p, type(parents[0])) for p in parents
        ), "All parents must be of the same type"
        self.parents = parents

    @staticmethod
    def from_couple(a: PersonT, b: PersonT) -> "Parents[PersonT]":
        return Parents([a, b])

    def is_couple(self) -> bool:
        return len(self.parents) == 2

    def couple(self) -> Tuple[PersonT, PersonT]:
        assert len(self.parents) == 2, "Is not a couple"
        return (self.parents[0], self.parents[1])

    def father(self) -> PersonT:
        assert len(self.parents) >= 1
        return self.parents[0]

    def mother(self) -> PersonT:
        assert len(self.parents) >= 2
        return self.parents[1]

    def __getitem__(self, index: int) -> PersonT:
        assert 0 <= index < len(self.parents), "Index out of range"
        return self.parents[index]


class DivorceStatusBase:
    def __init__(self):
        raise NotImplementedError(
            "DivorceStatusBase is a base class and cannot be"
            "instantiated directly. Use one of its subclasses instead."
        )

    def map_divorce(self, _: Callable[[Date], Date]):
        return self


class NotDivorced(DivorceStatusBase):
    def __init__(self):
        pass


class Divorced(DivorceStatusBase):
    def __init__(self, divorce_date: CompressedDate):
        self.divorce_date = divorce_date

    @override
    def map_divorce(self, date_mapper: Callable[[Date], Date]):
        return Divorced(divorce_date=self.divorce_date.map_cdate(date_mapper))


class Separated(DivorceStatusBase):
    def __init__(self):
        pass


class RelationToParentType(Enum):
    ADOPTION = "Adoption"
    RECOGNITION = "Recognition"
    CANDIDATEPARENT = "CandidateParent"
    GODPARENT = "GodParent"
    FOSTERPARENT = "FosterParent"


RelationDescriptorT = TypeVar("RelationDescriptorT")


@dataclass(frozen=True)
class Relation(Generic[PersonT, RelationDescriptorT]):
    type: RelationToParentType
    father: PersonT | None
    mother: PersonT | None
    sources: List[RelationDescriptorT]

    def map_relation_strings(
        self,
        string_mapper: Callable[[RelationDescriptorT], RelationDescriptorT],
        person_mapper: Callable[[PersonT], PersonT],
    ) -> "Relation[PersonT, RelationDescriptorT]":
        return Relation(
            type=self.type,
            father=person_mapper(self.father) if self.father else None,
            mother=person_mapper(self.mother) if self.mother else None,
            sources=[string_mapper(s) for s in self.sources],
        )


FamilyT = TypeVar("FamilyT")


@dataclass(frozen=True)
class Ascendants(Generic[FamilyT]):
    parents: FamilyT | None
    consanguinity_rate: ConsanguinityRate

    def map_ascendants(
        self, family_mapper: Callable[[FamilyT], FamilyT]
    ) -> "Ascendants[FamilyT]":
        return Ascendants(
            parents=family_mapper(self.parents) if self.parents else None,
            consanguinity_rate=self.consanguinity_rate,
        )


@dataclass(frozen=True)
class Descendants(Generic[PersonT]):
    children: List[PersonT]

    def map_descendants(
        self, family_mapper: Callable[[PersonT], PersonT]
    ) -> "Descendants[PersonT]":
        return Descendants(
            children=[family_mapper(child) for child in self.children]
        )


IdxT = TypeVar("IdxT")
FamilyDescriptorT = TypeVar("FamilyDescriptorT")


@dataclass(frozen=True)
class Family(Generic[IdxT, PersonT, FamilyDescriptorT]):
    index: IdxT
    marriage_date: CompressedDate
    marriage_place: FamilyDescriptorT
    marriage_note: FamilyDescriptorT
    marriage_src: FamilyDescriptorT
    witnesses: List[PersonT]
    divorce: DivorceStatusBase
    relation_kind: MaritalStatus
    family_events: List[FamilyEvent[PersonT, FamilyDescriptorT]]
    comment: FamilyDescriptorT
    origin_file: FamilyDescriptorT  # .gw filename
    src: FamilyDescriptorT

    def map_family(
        self,
        string_mapper: Callable[[FamilyDescriptorT], FamilyDescriptorT],
        person_mapper: Callable[[PersonT], PersonT],
        date_mapper: Callable[[Date], Date],
        index_mapper: Callable[[IdxT], IdxT],
    ) -> "Family[IdxT, PersonT, FamilyDescriptorT]":
        return Family(
            index=index_mapper(self.index),
            marriage_date=self.marriage_date.map_cdate(date_mapper),
            marriage_place=string_mapper(self.marriage_place),
            marriage_note=string_mapper(self.marriage_note),
            marriage_src=string_mapper(self.marriage_src),
            witnesses=[person_mapper(witness) for witness in self.witnesses],
            relation_kind=self.relation_kind,
            divorce=self.divorce.map_divorce(date_mapper),
            family_events=[
                family_event.map_family_event(
                    string_mapper, date_mapper, person_mapper
                )
                for family_event in self.family_events
            ],
            comment=string_mapper(self.comment),
            origin_file=string_mapper(self.origin_file),
            src=string_mapper(self.src),
        )
