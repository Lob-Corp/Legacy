from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, List, TypeVar

from libraries.date import CompressedDate, Date
from libraries.death_info import DeathStatusBase
from libraries.burial_info import BurialInfoBase
from libraries.events import PersonalEvent
from libraries.family import Ascendants, Relation
from libraries.title import AccessRight, Title


class Sex(Enum):
    """Biological sex classification for genealogical records."""

    MALE = "MALE"
    FEMALE = "FEMALE"
    NEUTER = "NEUTER"


@dataclass(frozen=True)
class Place:
    """Represents a hierarchical geographic location.

    Follows the typical administrative divisions from smallest (town)
    to largest (country) with an 'other' field for additional details.
    """

    town: str
    township: str
    canton: str
    district: str
    county: str
    region: str
    country: str
    other: str


# Type variables for genealogical data structures
IdxT = TypeVar("IdxT")
IdxT2 = TypeVar("IdxT2")

# Person reference type (e.g., Person or PersonId)
PersonT = TypeVar("PersonT")
PersonT2 = TypeVar("PersonT2")

# Family reference type
FamilyT = TypeVar("FamilyT")
FamilyT2 = TypeVar("FamilyT2")

# String descriptors (names, notes, etc.)
PersonDescriptorT = TypeVar("PersonDescriptorT")
PersonDescriptorT2 = TypeVar("PersonDescriptorT2")


@dataclass(frozen=True)
class Person(Generic[IdxT, PersonT, PersonDescriptorT, FamilyT]):
    """Complete genealogical record for an individual person.

    Contains all biographical information typically tracked in genealogy:
    names, dates, places, relationships, and sources. Uses generic types
    to support different storage backends and identifier systems.
    """

    index: IdxT
    first_name: PersonDescriptorT
    surname: PersonDescriptorT
    occ: int
    image: PersonDescriptorT
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

    # Birth information
    birth_date: CompressedDate
    birth_place: PersonDescriptorT
    birth_note: PersonDescriptorT
    birth_src: PersonDescriptorT

    # Baptism/christening information
    baptism_date: CompressedDate
    baptism_place: PersonDescriptorT
    baptism_note: PersonDescriptorT
    baptism_src: PersonDescriptorT
    death_status: DeathStatusBase
    death_place: PersonDescriptorT
    death_note: PersonDescriptorT
    death_src: PersonDescriptorT

    # Burial information
    burial: BurialInfoBase
    burial_place: PersonDescriptorT
    burial_note: PersonDescriptorT
    burial_src: PersonDescriptorT
    personal_events: List[PersonalEvent[PersonT, PersonDescriptorT]]
    notes: PersonDescriptorT
    src: PersonDescriptorT

    ascend: Ascendants[FamilyT]
    families: List[FamilyT]

    def map_person(
        self,
        string_mapper: Callable[[PersonDescriptorT], PersonDescriptorT2],
        person_mapper: Callable[[PersonT], PersonT2],
        date_mapper: Callable[[Date], Date],
        index_mapper: Callable[[IdxT], IdxT2],
        family_mapper: Callable[[FamilyT], FamilyT2],
    ) -> "Person[IdxT2, PersonT2, PersonDescriptorT2, FamilyT2]":
        """Transform all fields using provided mapper functions.

        This creates a new Person instance with all string descriptors,
        person references, and dates transformed using the respective
        mapper functions. Useful for data migration, format conversion,
        or applying systematic transformations.

        Args:
            string_mapper: Function to transform string descriptors
            person_mapper: Function to transform person references
            date_mapper: Function to transform dates
            index_mapper: Function to transform the person index
            family_mapper: Function to transform family references

        Returns:
            New Person instance with all fields transformed
        """
        return Person(
            index=index_mapper(self.index),
            first_name=string_mapper(self.first_name),
            surname=string_mapper(self.surname),
            occ=self.occ,
            image=string_mapper(self.image),
            public_name=string_mapper(self.public_name),
            qualifiers=[string_mapper(q) for q in self.qualifiers],
            aliases=[string_mapper(a) for a in self.aliases],
            first_names_aliases=[
                string_mapper(fna) for fna in self.first_names_aliases
            ],
            surname_aliases=[string_mapper(sa) for sa in self.surname_aliases],
            titles=[
                title.map_title(string_mapper, date_mapper)
                for title in self.titles
            ],
            non_native_parents_relation=[
                r.map_relation_strings(string_mapper, person_mapper)
                for r in self.non_native_parents_relation
            ],
            related_persons=[person_mapper(rp) for rp in self.related_persons],
            occupation=string_mapper(self.occupation),
            sex=self.sex,
            access_right=self.access_right,
            birth_date=self.birth_date.map_cdate(date_mapper),
            birth_place=string_mapper(self.birth_place),
            birth_note=string_mapper(self.birth_note),
            birth_src=string_mapper(self.birth_src),
            baptism_date=self.baptism_date.map_cdate(date_mapper),
            baptism_place=string_mapper(self.baptism_place),
            baptism_note=string_mapper(self.baptism_note),
            baptism_src=string_mapper(self.baptism_src),
            death_status=self.death_status.map_death(date_mapper),
            death_place=string_mapper(self.death_place),
            death_note=string_mapper(self.death_note),
            death_src=string_mapper(self.death_src),
            burial=self.burial.map_burial(date_mapper),
            burial_place=string_mapper(self.burial_place),
            burial_note=string_mapper(self.burial_note),
            burial_src=string_mapper(self.burial_src),
            personal_events=[
                personal_event.map_personal_event(
                    date_mapper, string_mapper, person_mapper
                )
                for personal_event in self.personal_events
            ],
            notes=string_mapper(self.notes),
            src=string_mapper(self.src),
            ascend=self.ascend.map_ascendants(family_mapper),
            families=[family_mapper(f) for f in self.families],
        )

