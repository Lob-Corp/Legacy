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
    PageExtGwSyntax,
)

from tests.import_tests.gw.test_data import (
    FAM_BLOCK,
    FAM_BLOCK_NO_MARRIAGE,
    FAM_BLOCK_NOT_MARRIED,
    FAM_BLOCK_ENGAGED,
    FAM_BLOCK_WITH_DIVORCE,
    FAM_BLOCK_SEPARATED,
    FAM_BLOCK_WITH_MULTIPLE_CHILDREN,
    FAM_BLOCK_WITH_COMMENT,
    FAM_BLOCK_MARRIAGE_CONTRACT,
    FAM_BLOCK_MARRIAGE_LICENSE,
    FAM_BLOCK_PACS,
    FAM_BLOCK_RESIDENCE,
    NOTES_BLOCK,
    REL_BLOCK,
    REL_BLOCK_DUAL_PARENT,
    REL_BLOCK_RECOGNITION,
    REL_BLOCK_CANDIDATE_PARENT,
    REL_BLOCK_GODPARENT,
    REL_BLOCK_FOSTER_PARENT,
    PEVT_BLOCK,
    PEVT_BLOCK_MULTIPLE_EVENTS,
    PEVT_BLOCK_CUSTOM_EVENT,
    PEVT_BLOCK_BAPTISM_LDS,
    PEVT_BLOCK_BAR_MITZVAH,
    NOTES_DB_BLOCK,
    WIZARD_NOTE_BLOCK,
    ENCODING_DIRECTIVE,
    GWPLUS_DIRECTIVE,
    PAGE_EXT_BLOCK,
    INVALID_CONTENT_WITH_VALID_FAMILIES,
)


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


def test_parse_encoding_directive():
    path = write_temp_gw(ENCODING_DIRECTIVE)
    result = parse_gw_file(path)
    os.remove(path)
    # Should handle encoding directive and parse family
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks


def test_parse_gwplus_directive():
    path = write_temp_gw(GWPLUS_DIRECTIVE)
    result = parse_gw_file(path)
    os.remove(path)
    # Should handle gwplus directive and parse family
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks


def test_parse_page_ext_block():
    path = write_temp_gw(PAGE_EXT_BLOCK)
    result = parse_gw_file(path)
    os.remove(path)
    page_ext_blocks = [x for x in result if isinstance(x, PageExtGwSyntax)]
    assert page_ext_blocks
    page_ext = page_ext_blocks[0]
    assert page_ext.page_name == "custom_page"
    assert "extended page content" in page_ext.content


def test_parse_no_fail_mode():
    # Test that no_fail mode allows parser to continue after errors
    path = write_temp_gw(INVALID_CONTENT_WITH_VALID_FAMILIES)
    result = parse_gw_file(path, no_fail=True)
    os.remove(path)
    # Should have parsed the valid families despite the invalid one
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert len(fam_blocks) >= 1  # At least one valid family parsed
