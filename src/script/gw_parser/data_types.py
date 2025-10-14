"""Data types for GeneWeb parser.

Defines the core data structures used to represent parsed GeneWeb blocks.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

from libraries.person import Person, Sex
from libraries.family import Family, Parents, Relation
from libraries.events import FamilyEvent, PersonalEvent


magic_gwo = "GnWo000o"
create_all_keys: bool = False
gwplus_mode: bool = False
no_fail_mode: bool = False


@dataclass(frozen=True)
class Key:
    """Represents a person key (first name, surname, occurrence)."""
    pk_first_name: str
    pk_surname: str
    pk_occ: int = 0


class Somebody:
    """Sum type wrapper for person references (defined or undefined)."""
    pass


@dataclass(frozen=True)
class SomebodyUndefined(Somebody):
    """Person reference that hasn't been fully parsed yet."""
    key: Key


@dataclass(frozen=True)
class SomebodyDefined(Somebody):
    """Person reference with full person data."""
    person: Person[int, int, str]


class GwSyntax:
    """Root variant marker for all GeneWeb syntax blocks."""
    pass


@dataclass(frozen=True)
class FamilyGwSyntax(GwSyntax):
    """Represents a family block (fam)."""
    couple: Parents[Somebody]
    father_sex: Sex
    mother_sex: Sex
    witnesses: List[Tuple[Somebody, Sex]]
    events: List[Tuple[FamilyEvent[Somebody, str], List[Sex]]]
    family: Family[int, Person[int, int, str], str]
    descend: List[Person[int, int, str]]


@dataclass(frozen=True)
class NotesGwSyntax(GwSyntax):
    """Represents a notes block for a person."""
    key: Key
    content: str


@dataclass(frozen=True)
class RelationsGwSyntax(GwSyntax):
    """Represents a relations block (rel)."""
    person: Somebody
    sex: Sex
    relations: List[Relation[Somebody, str]]


@dataclass(frozen=True)
class PersonalEventsGwSyntax(GwSyntax):
    """Represents a personal events block (pevt)."""
    person: Somebody
    sex: Sex
    events: List[PersonalEvent[Somebody, str]]


@dataclass(frozen=True)
class BaseNotesGwSyntax(GwSyntax):
    """Represents database notes (notes-db)."""
    page: str  # "" = base notes
    content: str


@dataclass(frozen=True)
class WizardNotesGwSyntax(GwSyntax):
    """Represents wizard notes."""
    wizard_id: str
    content: str


@dataclass(frozen=True)
class PageExtGwSyntax(GwSyntax):
    """Represents a page extension block (page-ext)."""
    page_name: str
    content: str


class Encoding(str):
    """Encoding types supported by GeneWeb."""
    UTF8 = 'utf-8'
    ISO_8859_1 = 'iso-8859-1'
