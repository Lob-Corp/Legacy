from dataclasses import dataclass
from enum import Enum
from typing import Generic, List, TypeVar

from libraries.date import CompressedDate
from libraries.death_info import BurialInfoBase, DeathStatusBase
from libraries.events import PersonalEvent
from libraries.family import Relation
from libraries.title import AccessRight, Title


class Sex(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTER = "NEUTER"


@dataclass(frozen=True)
class Place:
    town: str
    township: str
    canton: str
    district: str
    county: str
    region: str
    country: str
    other: str


IdxT = TypeVar('IdxT')
PersonT = TypeVar('PersonT')
PersonDescriptorT = TypeVar('PersonDescriptorT')


@dataclass(frozen=True)
class Person(Generic[IdxT, PersonT, PersonDescriptorT]):
    index: IdxT
    first_name: PersonDescriptorT
    surname: PersonDescriptorT
    occ: int
    image: str
    public_name: PersonDescriptorT
    qualifiers: List[PersonDescriptorT]
    aliases: List[PersonDescriptorT]
    first_names_aliases: List[PersonDescriptorT]
    surname_aliases: List[PersonDescriptorT]
    titles: List[Title[PersonDescriptorT]]
    non_native_parents_relation: List[Relation[PersonT, PersonDescriptorT]]
    related_persons: List[PersonT]
    occupation: PersonDescriptorT
    sex: Sex
    access_right: AccessRight
    birth_date: CompressedDate
    birth_place: PersonDescriptorT
    birth_note: PersonDescriptorT
    birth_src: PersonDescriptorT
    baptism_date: CompressedDate
    baptism_place: PersonDescriptorT
    baptism_note: PersonDescriptorT
    baptism_src: PersonDescriptorT
    death_status: DeathStatusBase
    death_place: PersonDescriptorT
    death_note: PersonDescriptorT
    death_src: PersonDescriptorT
    burial: BurialInfoBase
    burial_place: PersonDescriptorT
    burial_note: PersonDescriptorT
    burial_src: PersonDescriptorT
    personal_events: List[PersonalEvent[PersonT, PersonDescriptorT]]
    notes: PersonDescriptorT
    src: PersonDescriptorT
