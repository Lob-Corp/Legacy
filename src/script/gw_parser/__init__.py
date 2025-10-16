"""GeneWeb .gw file parser.

This package provides functionality to parse GeneWeb genealogical data files
(.gw format) into structured Python objects.
"""

from .parser import parse_gw_file
from .gw_converter import convert_gw_file, GwConverter
from .data_types import (
    Key,
    Somebody,
    SomebodyUndefined,
    SomebodyDefined,
    GwSyntax,
    FamilyGwSyntax,
    NotesGwSyntax,
    RelationsGwSyntax,
    PersonalEventsGwSyntax,
    BaseNotesGwSyntax,
    WizardNotesGwSyntax,
    PageExtGwSyntax,
)

__all__ = [
    'parse_gw_file',
    'convert_gw_file',
    'GwConverter',
    'Key',
    'Somebody',
    'SomebodyUndefined',
    'SomebodyDefined',
    'GwSyntax',
    'FamilyGwSyntax',
    'NotesGwSyntax',
    'RelationsGwSyntax',
    'PersonalEventsGwSyntax',
    'BaseNotesGwSyntax',
    'WizardNotesGwSyntax',
    'PageExtGwSyntax',
]
