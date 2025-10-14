import os
import tempfile
from typing import cast

from script.gwcomp import (
    SomebodyUndefined,
    parse_gw_file,
    FamilyGwSyntax,
    NotesGwSyntax,
    RelationsGwSyntax,
    PersonalEventsGwSyntax,
    BaseNotesGwSyntax,
    WizardNotesGwSyntax,
)

# Sample minimal .gw content for each block type
FAM_BLOCK = """fam 0 John + 0 Jane
wit m: 0 John
src test_source
fevt
#marr 2020 #p Paris #c Ceremony #s Source
end fevt
beg
- Paul
end
"""

FAM_BLOCK_NO_MARRIAGE = """fam 0 John +# 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_NOT_MARRIED = """fam 0 John +~ 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_ENGAGED = """fam 0 John +e 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_WITH_DIVORCE = """fam 0 John +2020 0 Jane
-2022
beg
- Paul
end
"""

FAM_BLOCK_SEPARATED = """fam 0 John +2020 0 Jane
#sep
beg
- Paul
end
"""

FAM_BLOCK_WITH_MULTIPLE_CHILDREN = """fam 0 John + 0 Jane
beg
- Paul
- m: Peter
- f: Patricia
end
"""

FAM_BLOCK_WITH_COMMENT = """fam 0 John + 0 Jane
comm This is a family comment
beg
- Paul
end
"""

# TODO: Future implementation - marriage contracts, licenses, PACS, residence
FAM_BLOCK_MARRIAGE_CONTRACT = """fam 0 John +#contract 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_MARRIAGE_LICENSE = """fam 0 John +#license 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_PACS = """fam 0 John +#pacs 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_RESIDENCE = """fam 0 John +#residence 0 Jane
beg
- Paul
end
"""

NOTES_BLOCK = """notes 0 John
This is a note about John.
Another line of note.
"""

REL_BLOCK = """rel 0 John
beg
- adop fath: 0 Mike
- adop moth: 0 Mary
end
"""

REL_BLOCK_DUAL_PARENT = """rel 0 John
beg
- adop: 0 Mike + 0 Mary
end
"""

REL_BLOCK_RECOGNITION = """rel 0 John
beg
- reco fath: 0 Mike
end
"""

REL_BLOCK_CANDIDATE_PARENT = """rel 0 John
beg
- cand fath: 0 Mike
end
"""

REL_BLOCK_GODPARENT = """rel 0 John
beg
- godp fath: 0 Mike
end
"""

REL_BLOCK_FOSTER_PARENT = """rel 0 John
beg
- fost fath: 0 Mike
end
"""

PEVT_BLOCK = """pevt 0 John
#birt 1990 #p Paris #c Born #s Source
end pevt
"""

PEVT_BLOCK_MULTIPLE_EVENTS = """pevt 0 John
#birt 1990 #p Paris
#bapt 1990/02/15 #p Paris
#deat 2050 #p London
end pevt
"""

PEVT_BLOCK_CUSTOM_EVENT = """pevt 0 John
#gradschool 2010 #p Boston #c Graduated from university
end pevt
"""

# TODO: Future implementation - special personal event types
PEVT_BLOCK_BAPTISM_LDS = """pevt 0 John
#brtm 1990 #p Salt Lake City
end pevt
"""

PEVT_BLOCK_BAR_MITZVAH = """pevt 0 John
#barm 2005 #p Jerusalem
end pevt
"""

NOTES_DB_BLOCK = """notes-db
This is a base note.
end notes-db
"""

WIZARD_NOTE_BLOCK = """wizard-note wiz123
This is a wizard note.
end wizard-note
"""

# TODO: Future implementation - encoding and gwplus directives
ENCODING_DIRECTIVE = """encoding: iso-8859-1
fam 0 John + 0 Jane
beg
- Paul
end
"""

GWPLUS_DIRECTIVE = """gwplus
fam 0 John + 0 Jane
beg
- Paul
end
"""


def write_temp_gw(content: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".gw")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def test_parse_family_block():
    path = write_temp_gw(FAM_BLOCK)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks, "Should parse a FamilyGwSyntax block"
    fam = fam_blocks[0]
    assert cast(SomebodyUndefined,
                fam.couple.mother()).key.pk_first_name == "Jane"
    assert cast(SomebodyUndefined,
                fam.couple.father()).key.pk_first_name == "John"
    assert fam.descend and fam.descend[0].first_name == "Paul"


def test_parse_notes_block():
    path = write_temp_gw(NOTES_BLOCK)
    result = parse_gw_file(path)
    os.remove(path)
    notes_blocks = [x for x in result if isinstance(x, NotesGwSyntax)]
    assert notes_blocks, "Should parse a NotesGwSyntax block"
    notes = notes_blocks[0]
    assert "This is a note about John." in notes.content


def test_parse_relations_block():
    path = write_temp_gw(REL_BLOCK)
    result = parse_gw_file(path)
    os.remove(path)
    rel_blocks = [x for x in result if isinstance(x, RelationsGwSyntax)]
    assert rel_blocks, "Should parse a RelationsGwSyntax block"
    rel = rel_blocks[0]
    assert rel.relations and rel.relations[0].type.name == "ADOPTION"


def test_parse_personal_events_block():
    path = write_temp_gw(PEVT_BLOCK)
    result = parse_gw_file(path)
    os.remove(path)
    pevt_blocks = [x for x in result if isinstance(x, PersonalEventsGwSyntax)]
    assert pevt_blocks, "Should parse a PersonalEventsGwSyntax block"
    evt = pevt_blocks[0]
    assert evt.events and evt.events[0].place == "Paris"


def test_parse_base_notes_block():
    path = write_temp_gw(NOTES_DB_BLOCK)
    result = parse_gw_file(path)
    os.remove(path)
    base_notes_blocks = [x for x in result if isinstance(x, BaseNotesGwSyntax)]
    assert base_notes_blocks, "Should parse a BaseNotesGwSyntax block"
    base_notes = base_notes_blocks[0]
    assert "base note" in base_notes.content


def test_parse_wizard_notes_block():
    path = write_temp_gw(WIZARD_NOTE_BLOCK)
    result = parse_gw_file(path)
    os.remove(path)
    wizard_notes_blocks = [
        x for x in result if isinstance(
            x, WizardNotesGwSyntax)]
    assert wizard_notes_blocks, "Should parse a WizardNotesGwSyntax block"
    wiz_notes = wizard_notes_blocks[0]
    assert wiz_notes.wizard_id == "wiz123"
    assert "wizard note" in wiz_notes.content


# Additional family block tests
def test_parse_family_no_marriage():
    path = write_temp_gw(FAM_BLOCK_NO_MARRIAGE)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.relation_kind.name == "NO_MENTION"


def test_parse_family_not_married():
    path = write_temp_gw(FAM_BLOCK_NOT_MARRIED)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.relation_kind.name == "NOT_MARRIED"


def test_parse_family_engaged():
    path = write_temp_gw(FAM_BLOCK_ENGAGED)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.relation_kind.name == "ENGAGED"


def test_parse_family_with_divorce():
    path = write_temp_gw(FAM_BLOCK_WITH_DIVORCE)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.relation_kind.name == "MARRIED"
    # Check divorce status exists
    assert hasattr(fam.family.divorce_status, '__class__')


def test_parse_family_separated():
    path = write_temp_gw(FAM_BLOCK_SEPARATED)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.divorce_status.__class__.__name__ == "Separated"


def test_parse_family_multiple_children():
    path = write_temp_gw(FAM_BLOCK_WITH_MULTIPLE_CHILDREN)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert len(fam.descend) == 3


def test_parse_family_with_comment():
    path = write_temp_gw(FAM_BLOCK_WITH_COMMENT)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.comment == "This is a family comment"


# Additional relations block tests
def test_parse_relations_dual_parent():
    path = write_temp_gw(REL_BLOCK_DUAL_PARENT)
    result = parse_gw_file(path)
    os.remove(path)
    rel_blocks = [x for x in result if isinstance(x, RelationsGwSyntax)]
    assert rel_blocks
    rel = rel_blocks[0]
    assert rel.relations[0].father is not None
    assert rel.relations[0].mother is not None


def test_parse_relations_recognition():
    path = write_temp_gw(REL_BLOCK_RECOGNITION)
    result = parse_gw_file(path)
    os.remove(path)
    rel_blocks = [x for x in result if isinstance(x, RelationsGwSyntax)]
    assert rel_blocks
    rel = rel_blocks[0]
    assert rel.relations[0].type.name == "RECOGNITION"


def test_parse_relations_candidate_parent():
    path = write_temp_gw(REL_BLOCK_CANDIDATE_PARENT)
    result = parse_gw_file(path)
    os.remove(path)
    rel_blocks = [x for x in result if isinstance(x, RelationsGwSyntax)]
    assert rel_blocks
    rel = rel_blocks[0]
    assert rel.relations[0].type.name == "CANDIDATEPARENT"


def test_parse_relations_godparent():
    path = write_temp_gw(REL_BLOCK_GODPARENT)
    result = parse_gw_file(path)
    os.remove(path)
    rel_blocks = [x for x in result if isinstance(x, RelationsGwSyntax)]
    assert rel_blocks
    rel = rel_blocks[0]
    assert rel.relations[0].type.name == "GODPARENT"


def test_parse_relations_foster_parent():
    path = write_temp_gw(REL_BLOCK_FOSTER_PARENT)
    result = parse_gw_file(path)
    os.remove(path)
    rel_blocks = [x for x in result if isinstance(x, RelationsGwSyntax)]
    assert rel_blocks
    rel = rel_blocks[0]
    assert rel.relations[0].type.name == "FOSTERPARENT"


# Additional personal events tests
def test_parse_personal_events_multiple():
    path = write_temp_gw(PEVT_BLOCK_MULTIPLE_EVENTS)
    result = parse_gw_file(path)
    os.remove(path)
    pevt_blocks = [x for x in result if isinstance(x, PersonalEventsGwSyntax)]
    assert pevt_blocks
    evt = pevt_blocks[0]
    assert len(evt.events) == 3


def test_parse_personal_events_custom():
    path = write_temp_gw(PEVT_BLOCK_CUSTOM_EVENT)
    result = parse_gw_file(path)
    os.remove(path)
    pevt_blocks = [x for x in result if isinstance(x, PersonalEventsGwSyntax)]
    assert pevt_blocks
    evt = pevt_blocks[0]
    # Custom events should be parsed as named events
    assert evt.events[0].name.__class__.__name__ == "PersNamedEvent"


# TODO: Future implementation - marriage contract/license/PACS/residence
def test_parse_family_marriage_contract():
    path = write_temp_gw(FAM_BLOCK_MARRIAGE_CONTRACT)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.relation_kind.name == "MARRIAGE_CONTRACT"


# TODO: Future implementation - marriage license parsing
def test_parse_family_marriage_license():
    path = write_temp_gw(FAM_BLOCK_MARRIAGE_LICENSE)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.relation_kind.name == "MARRIAGE_LICENSE"


# TODO: Future implementation - PACS parsing
def test_parse_family_pacs():
    path = write_temp_gw(FAM_BLOCK_PACS)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.relation_kind.name == "PACS"


# TODO: Future implementation - residence parsing
def test_parse_family_residence():
    path = write_temp_gw(FAM_BLOCK_RESIDENCE)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    assert fam.family.relation_kind.name == "RESIDENCE"


# TODO: Future implementation - baptism LDS parsing
def test_parse_personal_events_baptism_lds():
    path = write_temp_gw(PEVT_BLOCK_BAPTISM_LDS)
    result = parse_gw_file(path)
    os.remove(path)
    pevt_blocks = [x for x in result if isinstance(x, PersonalEventsGwSyntax)]
    assert pevt_blocks


# TODO: Future implementation - bar mitzvah parsing
def test_parse_personal_events_bar_mitzvah():
    path = write_temp_gw(PEVT_BLOCK_BAR_MITZVAH)
    result = parse_gw_file(path)
    os.remove(path)
    pevt_blocks = [x for x in result if isinstance(x, PersonalEventsGwSyntax)]
    assert pevt_blocks


# TODO: Future implementation - encoding directive parsing
def test_parse_encoding_directive():
    path = write_temp_gw(ENCODING_DIRECTIVE)
    result = parse_gw_file(path)
    os.remove(path)
    # Should handle encoding directive and parse family
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks


# TODO: Future implementation - gwplus directive parsing
def test_parse_gwplus_directive():
    path = write_temp_gw(GWPLUS_DIRECTIVE)
    result = parse_gw_file(path)
    os.remove(path)
    # Should handle gwplus directive and parse family
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
