"""Conversion layer from GwSyntax (parsed GeneWeb) to application types.

This module converts the parsed GeneWeb syntax into the proper application
types defined in the libraries/ module.
"""

from typing import Dict, List, Optional, Tuple

from script.gw_parser.data_types import (
    FamilyGwSyntax,
    GwSyntax,
    Key,
    NotesGwSyntax,
    PersonalEventsGwSyntax,
    RelationsGwSyntax,
    Somebody,
    SomebodyDefined,
    SomebodyUndefined,
)
from libraries.person import Person
from libraries.family import Family, Relation
from libraries.events import FamilyEvent, PersonalEvent


class GwConverter:
    """Converts GeneWeb parsed syntax to application types.

    This class handles the conversion of parsed GeneWeb data structures
    into the strongly-typed application models used throughout the app.
    It manages person resolution, index assignment, and proper type
    construction.
    """

    def __init__(self):
        """Initialize the converter with tracking structures."""
        self.person_index_counter: int = 0
        self.family_index_counter: int = 0

        # Map from Key to resolved Person
        self.person_by_key: Dict[
            Tuple[str, str, int],
            Person[int, int, str]
        ] = {}

        # Map from family index to Family
        self.families: Dict[int, Family[int, Person[int, int, str], str]] = {}

        # Notes storage: Key -> content
        self.notes: Dict[Tuple[str, str, int], str] = {}

        # Relations storage: Key -> relations
        self.relations: Dict[
            Tuple[str, str, int],
            List[Relation[Person[int, int, str], str]]
        ] = {}

        # Personal events storage: Key -> events
        self.personal_events: Dict[
            Tuple[str, str, int],
            List[PersonalEvent[Person[int, int, str], str]]
        ] = {}

    def key_tuple(self, key: Key) -> Tuple[str, str, int]:
        """Convert a Key to a hashable tuple."""
        return (key.pk_first_name, key.pk_surname, key.pk_occ)

    def resolve_somebody(
        self,
        somebody: Somebody
    ) -> Person[int, int, str]:
        """Resolve a Somebody reference to an actual Person.

        Args:
            somebody: The Somebody reference (defined or undefined)

        Returns:
            The resolved Person object

        Raises:
            ValueError: If an undefined person cannot be resolved
        """
        if isinstance(somebody, SomebodyDefined):
            return somebody.person
        elif isinstance(somebody, SomebodyUndefined):
            key_tuple = self.key_tuple(somebody.key)
            if key_tuple in self.person_by_key:
                return self.person_by_key[key_tuple]
            else:
                raise ValueError(
                    f"Cannot resolve undefined person: "
                    f"{somebody.key.pk_first_name} "
                    f"{somebody.key.pk_surname} "
                    f"#{somebody.key.pk_occ}"
                )
        else:
            raise TypeError(f"Unknown Somebody type: {type(somebody)}")

    def resolve_somebody_list(
        self,
        somebodies: List[Somebody]
    ) -> List[Person[int, int, str]]:
        """Resolve a list of Somebody references."""
        return [self.resolve_somebody(s) for s in somebodies]

    def convert_family(
        self,
        gw_family: FamilyGwSyntax
    ) -> Tuple[
        Family[int, Person[int, int, str], str],
        List[Person[int, int, str]]
    ]:
        """Convert a FamilyGwSyntax to a Family and register persons.

        Args:
            gw_family: The parsed family block

        Returns:
            Tuple of (converted Family, list of children)
        """
        # Register all persons in the family first
        for person in gw_family.descend:
            key_tuple = (person.first_name, person.surname, person.occ)
            self.person_by_key[key_tuple] = person

        # Resolve witnesses
        witness_persons = []
        for witness_somebody, sex in gw_family.witnesses:
            witness = self.resolve_somebody(witness_somebody)
            witness_persons.append(witness)

        # Convert family events - resolve witness references
        converted_events: List[FamilyEvent[Person[int, int, str], str]] = []
        for event, witness_sexes in gw_family.events:
            # The event already has the structure, we just need to ensure
            # witness types are resolved if needed
            converted_events.append(event)

        # Use the family data from gw_family.family
        family = gw_family.family

        # Create converted family with proper witness list
        converted_family = Family(
            index=self.family_index_counter,
            marriage_date=family.marriage_date,
            marriage_place=family.marriage_place,
            marriage_note=family.marriage_note,
            marriage_src=family.marriage_src,
            witnesses=witness_persons,
            relation_kind=family.relation_kind,
            divorce_status=family.divorce_status,
            family_events=converted_events,
            comment=family.comment,
            origin_file=family.origin_file,
            src=family.src,
        )

        self.families[self.family_index_counter] = converted_family
        self.family_index_counter += 1

        return converted_family, gw_family.descend

    def convert_notes(self, gw_notes: NotesGwSyntax) -> None:
        """Store notes for a person.

        Args:
            gw_notes: The parsed notes block
        """
        key_tuple = self.key_tuple(gw_notes.key)
        self.notes[key_tuple] = gw_notes.content

    def convert_relations(self, gw_relations: RelationsGwSyntax) -> None:
        """Store relations for a person.

        Args:
            gw_relations: The parsed relations block
        """
        person = self.resolve_somebody(gw_relations.person)
        key_tuple = (person.first_name, person.surname, person.occ)

        # Convert relations - resolve parent references
        converted_relations: List[Relation[Person[int, int, str], str]] = []
        for relation in gw_relations.relations:
            father = (
                self.resolve_somebody(relation.father)
                if relation.father is not None
                else None
            )
            mother = (
                self.resolve_somebody(relation.mother)
                if relation.mother is not None
                else None
            )
            converted_relation = Relation(
                type=relation.type,
                father=father,
                mother=mother,
                sources=relation.sources,
            )
            converted_relations.append(converted_relation)

        self.relations[key_tuple] = converted_relations

    def convert_personal_events(
        self,
        gw_events: PersonalEventsGwSyntax
    ) -> None:
        """Store personal events for a person.

        Args:
            gw_events: The parsed personal events block
        """
        person = self.resolve_somebody(gw_events.person)
        key_tuple = (person.first_name, person.surname, person.occ)

        # Convert events - resolve witness references
        converted_events: List[PersonalEvent[Person[int, int, str], str]] = []
        for event in gw_events.events:
            # Events are already in the right structure
            converted_events.append(event)

        self.personal_events[key_tuple] = converted_events

    def convert(self, gw_syntax: GwSyntax) -> None:
        """Convert a GwSyntax block and accumulate in the converter.

        Args:
            gw_syntax: The parsed GeneWeb block to convert

        Raises:
            TypeError: If the GwSyntax type is not recognized
        """
        if isinstance(gw_syntax, FamilyGwSyntax):
            self.convert_family(gw_syntax)
        elif isinstance(gw_syntax, NotesGwSyntax):
            self.convert_notes(gw_syntax)
        elif isinstance(gw_syntax, RelationsGwSyntax):
            self.convert_relations(gw_syntax)
        elif isinstance(gw_syntax, PersonalEventsGwSyntax):
            self.convert_personal_events(gw_syntax)
        else:
            raise TypeError(f"Unknown GwSyntax type: {type(gw_syntax)}")

    def convert_all(self, gw_blocks: List[GwSyntax]) -> None:
        """Convert multiple GwSyntax blocks in sequence.

        Args:
            gw_blocks: List of parsed GeneWeb blocks
        """
        for block in gw_blocks:
            self.convert(block)

    def get_all_persons(self) -> List[Person[int, int, str]]:
        """Get all registered persons."""
        return list(self.person_by_key.values())

    def get_all_families(
        self
    ) -> List[Family[int, Person[int, int, str], str]]:
        """Get all registered families."""
        return list(self.families.values())

    def get_person_by_key(
        self,
        first_name: str,
        surname: str,
        occ: int = 0
    ) -> Optional[Person[int, int, str]]:
        """Look up a person by their key.

        Args:
            first_name: First name of the person
            surname: Surname of the person
            occ: Occurrence number (default 0)

        Returns:
            The Person if found, None otherwise
        """
        key_tuple = (first_name, surname, occ)
        return self.person_by_key.get(key_tuple)

    def enrich_person_with_additional_data(
        self,
        person: Person[int, int, str]
    ) -> Person[int, int, str]:
        """Enrich a person with notes, relations, and personal events.

        Args:
            person: The base person object

        Returns:
            A new Person with additional data merged in
        """
        from dataclasses import replace

        key_tuple = (person.first_name, person.surname, person.occ)

        # Get additional data
        notes = self.notes.get(key_tuple, person.notes)
        relations = self.relations.get(
            key_tuple,
            person.non_native_parents_relation
        )
        events = self.personal_events.get(
            key_tuple,
            person.personal_events
        )

        # Create enriched person
        return replace(
            person,
            notes=notes,
            non_native_parents_relation=relations,
            personal_events=events,
        )

    def get_enriched_persons(self) -> List[Person[int, int, str]]:
        """Get all persons with notes, relations, events merged in."""
        return [
            self.enrich_person_with_additional_data(person)
            for person in self.get_all_persons()
        ]


def convert_gw_file(gw_blocks: List[GwSyntax]) -> Tuple[
    List[Person[int, int, str]],
    List[Family[int, Person[int, int, str], str]]
]:
    """Convenience function to convert a complete GeneWeb file.

    Args:
        gw_blocks: List of all parsed GeneWeb blocks from a file

    Returns:
        Tuple of (list of enriched persons, list of families)
    """
    converter = GwConverter()
    converter.convert_all(gw_blocks)
    return converter.get_enriched_persons(), converter.get_all_families()
