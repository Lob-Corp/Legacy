"""Conversion layer from GwSyntax (parsed GeneWeb) to application types.

This module converts the parsed GeneWeb syntax into the proper application
types defined in the libraries/ module.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import replace

from script.gw_parser.data_types import (
    FamilyGwSyntax,
    GwSyntax,
    Key,
    NotesGwSyntax,
    PersonalEventsGwSyntax,
    RelationsGwSyntax,
    BaseNotesGwSyntax,
    WizardNotesGwSyntax,
    PageExtGwSyntax,
    Somebody,
    SomebodyDefined,
    SomebodyUndefined,
)
from libraries.person import Person, Sex, AccessRight
from libraries.family import Family, Relation, Ascendants, Parents
from libraries.events import FamilyEvent, PersonalEvent, PersDeath
from libraries.burial_info import UnknownBurial
from libraries.death_info import NotDead, Dead, DeathReason
from libraries.consanguinity_rate import ConsanguinityRate


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
            Person[int, int, str, int]
        ] = {}
        self.dummy_persons: set[Tuple[str, str, int]] = set()
        self.families: Dict[
            int, Family[int, Person[int, int, str, int], str]
        ] = {}
        # Notes storage: Key -> content
        self.notes: Dict[Tuple[str, str, int], str] = {}
        # Relations storage: Key -> relations
        self.relations: Dict[
            Tuple[str, str, int],
            List[Relation[Person[int, int, str, int], str]]
        ] = {}
        # Personal events storage: Key -> events
        self.personal_events: Dict[
            Tuple[str, str, int],
            List[PersonalEvent[Person[int, int, str, int], str]]
        ] = {}
        self.base_notes: List[Tuple[str, str]] = []
        self.wizard_notes: Dict[str, str] = {}
        self.page_extensions: Dict[str, str] = {}

    def key_tuple(self, key: Key) -> Tuple[str, str, int]:
        """Convert a Key to a hashable tuple."""
        return (key.pk_first_name, key.pk_surname, key.pk_occ)

    def _create_dummy_person(self, key: Key) -> Person[int, int, str, int]:
        """Create a minimal dummy person for an undefined reference.

        Mimics OCaml gwc's behavior of creating placeholder persons
        ('U' marker) that can be overridden later with full definition.

        Args:
            key: The person key (name and occurrence)

        Returns:
            A minimal Person object with just basic identification
        """

        index = self.person_index_counter
        self.person_index_counter += 1
        dummy = Person(
            index=index,
            first_name=key.pk_first_name,
            surname=key.pk_surname,
            occ=key.pk_occ,
            image="",
            public_name="",
            qualifiers=[],
            aliases=[],
            first_names_aliases=[],
            surname_aliases=[],
            titles=[],
            non_native_parents_relation=[],
            related_persons=[],
            occupation="",
            sex=Sex.NEUTER,
            access_right=AccessRight.PUBLIC,
            birth_date=None,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_date=None,
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=NotDead(),
            death_place="",
            death_note="",
            death_src="",
            burial=UnknownBurial(),
            burial_place="",
            burial_note="",
            burial_src="",
            personal_events=[],
            notes="",
            src="",
            ascend=Ascendants(
                parents=None,
                consanguinity_rate=ConsanguinityRate.from_integer(-1)
            ),
            families=[],
        )
        return dummy

    def resolve_somebody(
        self,
        somebody: Somebody
    ) -> Person[int, int, str, int]:
        """Resolve a Somebody reference to an actual Person.

        Creates dummy persons for undefined references (like OCaml's 'U').
        Overrides dummies when full definition found (like OCaml's 'D').

        Args:
            somebody: The Somebody reference (defined or undefined)

        Returns:
            The resolved Person object
        """
        if isinstance(somebody, SomebodyDefined):
            key_tuple = (
                somebody.person.first_name,
                somebody.person.surname,
                somebody.person.occ
            )
            if key_tuple in self.dummy_persons:
                self.dummy_persons.remove(key_tuple)
                old_person = self.person_by_key[key_tuple]
                person = replace(somebody.person, index=old_person.index)
            elif key_tuple not in self.person_by_key:
                person = replace(
                    somebody.person,
                    index=self.person_index_counter
                )
                self.person_index_counter += 1
            else:
                person = somebody.person

            self.person_by_key[key_tuple] = person
            return person

        elif isinstance(somebody, SomebodyUndefined):
            key_tuple = self.key_tuple(somebody.key)

            if key_tuple in self.person_by_key:
                return self.person_by_key[key_tuple]
            else:
                dummy = self._create_dummy_person(somebody.key)
                self.person_by_key[key_tuple] = dummy
                self.dummy_persons.add(key_tuple)
                return dummy
        else:
            raise TypeError(f"Unknown Somebody type: {type(somebody)}")

    def resolve_somebody_list(
        self,
        somebodies: List[Somebody]
    ) -> List[Person[int, int, str, int]]:
        """Resolve a list of Somebody references."""
        return [self.resolve_somebody(s) for s in somebodies]

    def convert_family(
        self,
        gw_family: FamilyGwSyntax
    ) -> Tuple[
        Family[int, Person[int, int, str, int], str],
        List[Person[int, int, str, int]]
    ]:
        """Convert a FamilyGwSyntax to a Family and register persons.

        Args:
            gw_family: The parsed family block

        Returns:
            Tuple of (converted Family, list of children)
        """
        # Resolve the couple (father and mother) - this creates dummies
        # if needed and registers them in person_by_key
        resolved_parents: List[Person[int, int, str, int]] = []
        if len(gw_family.couple.parents) >= 1:
            father = self.resolve_somebody(gw_family.couple.parents[0])
            resolved_parents.append(father)
        if len(gw_family.couple.parents) >= 2:
            mother = self.resolve_somebody(gw_family.couple.parents[1])
            resolved_parents.append(mother)

        if resolved_parents:
            family_parents = Parents(resolved_parents)
        else:
            # This shouldn't happen in well-formed data
            raise ValueError("Family has no parents")

        # Register inline-defined children into person_by_key, assigning
        # indices if needed so subsequent updates (ascend/families) persist.
        for person in gw_family.descend:
            key_tuple = (person.first_name, person.surname, person.occ)
            if key_tuple in self.person_by_key:
                # Already present (dummy or defined earlier), keep existing
                continue
            # If the person has an unassigned index (-1), assign a new one
            if person.index == -1:
                person = replace(person, index=self.person_index_counter)
                self.person_index_counter += 1
            self.person_by_key[key_tuple] = person

        witness_persons = []
        for witness_somebody, sex in gw_family.witnesses:
            witness = self.resolve_somebody(witness_somebody)
            witness_persons.append(witness)

        converted_events: List[
            FamilyEvent[Person[int, int, str, int], str]
        ] = []
        for event, witness_sexes in gw_family.events:
            resolved_witnesses = []
            for witness_somebody, witness_kind in event.witnesses:
                resolved_witness = self.resolve_somebody(witness_somebody)
                resolved_witnesses.append((resolved_witness, witness_kind))
            converted_event = replace(event, witnesses=resolved_witnesses)
            converted_events.append(converted_event)

        family = gw_family.family

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
            parents=family_parents,
            children=gw_family.descend,
        )

        self.families[self.family_index_counter] = converted_family

        updated_parents = []
        for parent in resolved_parents:
            parent_key = (parent.first_name, parent.surname, parent.occ)
            if parent_key in self.person_by_key:
                existing_parent = self.person_by_key[parent_key]
                # Add this family to parent's families list (marriages/unions)
                updated_parent = replace(
                    existing_parent,
                    families=existing_parent.families + [
                        self.family_index_counter
                    ]
                )
                self.person_by_key[parent_key] = updated_parent
                updated_parents.append(updated_parent)
            else:
                # Parent not yet in person_by_key, use original
                updated_parents.append(parent)

        updated_family_parents = Parents(updated_parents)
        converted_family = replace(
            converted_family,
            parents=updated_family_parents
        )

        updated_children = []
        for child in gw_family.descend:
            child_key = (child.first_name, child.surname, child.occ)
            if child_key in self.person_by_key:
                existing_child = self.person_by_key[child_key]
                # Update child's ascend to point to this family
                updated_ascend = replace(
                    existing_child.ascend,
                    parents=self.family_index_counter
                )
                updated_child = replace(
                    existing_child,
                    ascend=updated_ascend
                )
                self.person_by_key[child_key] = updated_child
                updated_children.append(updated_child)
            else:
                # Child not yet in person_by_key, use original
                updated_children.append(child)

        converted_family = replace(
            converted_family,
            children=updated_children
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

        converted_relations: List[
            Relation[Person[int, int, str, int], str]
        ] = []
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

        converted_events: List[
            PersonalEvent[Person[int, int, str, int], str]
        ] = []
        for event in gw_events.events:
            resolved_witnesses = []
            for witness_somebody, witness_kind in event.witnesses:
                resolved_witness = self.resolve_somebody(witness_somebody)
                resolved_witnesses.append((resolved_witness, witness_kind))
            converted_event = replace(event, witnesses=resolved_witnesses)
            converted_events.append(converted_event)

        self.personal_events[key_tuple] = converted_events

        # If this person was a dummy, mark them as defined now
        # since we have substantial data (events) for them
        if key_tuple in self.dummy_persons:
            self.dummy_persons.remove(key_tuple)

    def convert_base_notes(self, gw_base_notes: BaseNotesGwSyntax) -> None:
        """Store base notes (database-wide notes).

        Args:
            gw_base_notes: The parsed base notes block
        """
        self.base_notes.append((gw_base_notes.page, gw_base_notes.content))

    def convert_wizard_notes(
        self,
        gw_wizard_notes: WizardNotesGwSyntax
    ) -> None:
        """Store wizard notes.

        Args:
            gw_wizard_notes: The parsed wizard notes block
        """
        self.wizard_notes[gw_wizard_notes.wizard_id] = \
            gw_wizard_notes.content

    def convert_page_ext(self, gw_page_ext: PageExtGwSyntax) -> None:
        """Store page extension content.

        Args:
            gw_page_ext: The parsed page extension block
        """
        self.page_extensions[gw_page_ext.page_name] = gw_page_ext.content

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
        elif isinstance(gw_syntax, BaseNotesGwSyntax):
            self.convert_base_notes(gw_syntax)
        elif isinstance(gw_syntax, WizardNotesGwSyntax):
            self.convert_wizard_notes(gw_syntax)
        elif isinstance(gw_syntax, PageExtGwSyntax):
            self.convert_page_ext(gw_syntax)
        else:
            raise TypeError(f"Unknown GwSyntax type: {type(gw_syntax)}")

    def convert_all(self, gw_blocks: List[GwSyntax]) -> None:
        """Convert multiple GwSyntax blocks in sequence.

        Args:
            gw_blocks: List of parsed GeneWeb blocks
        """
        for block in gw_blocks:
            self.convert(block)

    def get_all_persons(self) -> List[Person[int, int, str, int]]:
        """Get all registered persons."""
        return list(self.person_by_key.values())

    def get_all_families(
        self
    ) -> List[Family[int, Person[int, int, str, int], str]]:
        """Get all registered families."""
        return list(self.families.values())

    def get_person_by_key(
        self,
        first_name: str,
        surname: str,
        occ: int = 0
    ) -> Optional[Person[int, int, str, int]]:
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
        person: Person[int, int, str, int]
    ) -> Person[int, int, str, int]:
        """Enrich a person with notes, relations, and personal events.

        Args:
            person: The base person object

        Returns:
            A new Person with additional data merged in
        """
        from dataclasses import replace

        key_tuple = (person.first_name, person.surname, person.occ)

        notes = self.notes.get(key_tuple, person.notes)
        relations = self.relations.get(
            key_tuple,
            person.non_native_parents_relation
        )
        events = self.personal_events.get(
            key_tuple,
            person.personal_events
        )

        # Extract death information from personal events if present
        death_status = person.death_status
        death_place = person.death_place
        death_note = person.death_note
        death_src = person.death_src

        for event in events:
            if isinstance(event.name, PersDeath):
                # Found a death event - update death status
                if event.date:
                    death_status = Dead(DeathReason.UNSPECIFIED, event.date)
                if event.place:
                    death_place = event.place
                if event.note:
                    death_note = event.note
                if event.src:
                    death_src = event.src
                break  # Only process the first death event

        return replace(
            person,
            notes=notes,
            non_native_parents_relation=relations,
            personal_events=events,
            death_status=death_status,
            death_place=death_place,
            death_note=death_note,
            death_src=death_src,
        )

    def get_enriched_persons(self) -> List[Person[int, int, str, int]]:
        """Get all persons with notes, relations, events merged in."""
        return [
            self.enrich_person_with_additional_data(person)
            for person in self.get_all_persons()
        ]

    def get_dummy_persons(self) -> List[Person[int, int, str, int]]:
        """Get all persons that remain as dummies (undefined references).

        These are persons that were referenced but never fully defined,
        similar to OCaml entries with 'U' marker.

        Returns:
            List of persons that were referenced but never defined
        """
        return [
            self.person_by_key[key_tuple]
            for key_tuple in self.dummy_persons
        ]

    def get_base_notes(self) -> List[Tuple[str, str]]:
        """Get all database-wide notes.

        Returns:
            List of (page, content) tuples for base notes
        """
        return self.base_notes

    def get_wizard_notes(self) -> Dict[str, str]:
        """Get all wizard notes.

        Returns:
            Dictionary mapping wizard_id to content
        """
        return self.wizard_notes

    def get_page_extensions(self) -> Dict[str, str]:
        """Get all page extensions.

        Returns:
            Dictionary mapping page_name to content
        """
        return self.page_extensions

    def get_statistics(self) -> Dict[str, int]:
        """Get conversion statistics.

        Returns:
            Dictionary with counts of persons, families, dummies, and
            database-level data
        """
        defined_count = len(self.person_by_key) - len(self.dummy_persons)
        return {
            'total_persons': len(self.person_by_key),
            'defined_persons': defined_count,
            'dummy_persons': len(self.dummy_persons),
            'families': len(self.families),
            'base_notes': len(self.base_notes),
            'wizard_notes': len(self.wizard_notes),
            'page_extensions': len(self.page_extensions),
        }


def convert_gw_file(gw_blocks: List[GwSyntax]) -> Tuple[
    List[Person[int, int, str, int]],
    List[Family[int, Person[int, int, str, int], str]]
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
