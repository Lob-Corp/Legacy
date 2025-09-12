from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from libraries.date import CompressedDate
from libraries.death_info import BurialInfoBase, DeathStatusBase
from libraries.events import PersonalEvent
from libraries.family import Relation
from libraries.title import AccessRight, Title


class Sex(Enum):
    MALE = "Male"
    FEMALE = "Female"
    NEUTER = "Neuter"

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
    qualifiers: list[PersonDescriptorT]
    aliases: list[PersonDescriptorT]
    first_names_aliases: list[PersonDescriptorT]
    surname_aliases: list[PersonDescriptorT]
    titles: list[Title[PersonDescriptorT]]
    NonNativeParentsRelation: list[Relation[PersonT, PersonDescriptorT]]
    RelatedPersons: list[PersonT]
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
    death: DeathStatusBase
    death_place: PersonDescriptorT
    death_note: PersonDescriptorT
    death_src: PersonDescriptorT
    burial: BurialInfoBase
    burial_place: PersonDescriptorT
    burial_note: PersonDescriptorT
    burial_src: PersonDescriptorT
    personal_events: list[PersonalEvent[PersonT, PersonDescriptorT]]
    notes: PersonDescriptorT
    src: PersonDescriptorT
