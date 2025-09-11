from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from date import CompressedDate
from death_info import BurialInfoBase, DeathStatusBase
from events import PersonalEvent
from family import Relation
from title import AccessRight, Title


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

IndexType = TypeVar('IndexType')
PersonType = TypeVar('PersonType')
PersonDescriptorType = TypeVar('PersonDescriptorType')

@dataclass(frozen=True)
class Person(Generic[IndexType, PersonType, PersonDescriptorType]):
    index: IndexType
    first_name: PersonDescriptorType
    surname: PersonDescriptorType
    occ: int
    image: str
    public_name: PersonDescriptorType
    qualifiers: list[PersonDescriptorType]
    aliases: list[PersonDescriptorType]
    first_names_aliases: list[PersonDescriptorType]
    surname_aliases: list[PersonDescriptorType]
    titles: list[Title[PersonDescriptorType]]
    NonNativeParentsRelation: list[Relation[PersonType, PersonDescriptorType]]
    RelatedPersons: list[PersonType]
    occupation: PersonDescriptorType
    sex: Sex
    access_right: AccessRight
    birth_date: CompressedDate
    birth_place: PersonDescriptorType
    birth_note: PersonDescriptorType
    birth_src: PersonDescriptorType
    baptism_date: CompressedDate
    baptism_place: PersonDescriptorType
    baptism_note: PersonDescriptorType
    baptism_src: PersonDescriptorType
    death_date: DeathStatusBase
    death_place: PersonDescriptorType
    death_note: PersonDescriptorType
    death_src: PersonDescriptorType
    burial_date: BurialInfoBase
    burial_place: PersonDescriptorType
    burial_note: PersonDescriptorType
    burial_src: PersonDescriptorType
    personal_events: list[PersonalEvent[PersonType, PersonDescriptorType]]
    notes: PersonDescriptorType
    src: PersonDescriptorType
