import os
import tempfile
from typing import cast

from script.gw_parser import (
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
    # Complex scenarios
    COMPLEX_FAMILY_WITH_EVERYTHING,
    PERSON_WITH_COMPLEX_DATES,
    PERSON_WITH_ALL_FIELDS,
    MULTIPLE_RELATIONS_SAME_PERSON,
    MULTIPLE_EVENTS_WITH_WITNESSES,
    FAMILY_WITH_COMPLEX_MARRIAGE_HISTORY,
    NESTED_SURNAMES_AND_OCCURRENCES,
    MIXED_CONTENT_FILE,
    PERSON_WITH_DEATH_VARIATIONS,
    DATES_WITH_CALENDARS,
    FAMILY_WITH_SEX_OVERRIDES,
    COMPLEX_TITLES_AND_ALIASES,
    EVENTS_WITH_ALL_WITNESS_TYPES,
    EMPTY_AND_EDGE_CASES,
    # Family event tests
    FAMILY_EVENTS_ALL_TYPES,
    FAMILY_EVENTS_WITH_WITNESSES,
    FAMILY_EVENTS_NO_MARRIAGE,
    FAMILY_EVENTS_ENGAGEMENT_ONLY,
    FAMILY_EVENTS_PACS,
    FAMILY_EVENTS_ANNULMENT,
    FAMILY_EVENTS_MULTIPLE_RESIDENCES,
    FAMILY_EVENTS_COMPLEX_DATES,
    FAMILY_EVENTS_WITH_NOTES_AND_SOURCES,
    FAMILY_EVENTS_NAMED_CUSTOM,
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


# Complex scenario tests

def test_complex_family_with_everything():
    """Test family with witnesses, events, sources, and multiple children."""
    path = write_temp_gw(COMPLEX_FAMILY_WITH_EVERYTHING)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Verify witnesses
    assert len(fam.witnesses) == 2
    # Verify events
    assert len(fam.events) >= 1
    # Verify children with birth info
    assert len(fam.descend) == 3
    assert fam.descend[0].first_name == "Robert"
    assert fam.descend[1].first_name == "Susan"
    assert fam.descend[2].first_name == "Michael"
    # Verify family comment
    assert "ceremony" in fam.family.comment.lower()


def test_person_with_complex_dates():
    """Test various date precision markers and ranges."""
    path = write_temp_gw(PERSON_WITH_COMPLEX_DATES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    # Should parse children with different date formats
    assert len(fam_blocks[0].descend) == 6


def test_person_with_all_fields():
    """Test person with all possible fields populated."""
    path = write_temp_gw(PERSON_WITH_ALL_FIELDS)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    # Should parse person with extensive details
    assert len(fam_blocks[0].descend) == 1
    child = fam_blocks[0].descend[0]
    assert child.first_name == "Robert"
    # Verify public name (parentheses) - cut_space converts _ to spaces
    assert child.public_name == "Robert the Great"
    # Verify titles exist
    assert len(child.titles) >= 2
    # Verify occupation
    assert child.occupation == "Engineer"
    # Verify image
    assert child.image == "photo.jpg"
    # Verify first name aliases from {braces}
    assert len(child.first_names_aliases) >= 2  # Bob, Robbie
    # Verify surname aliases from #salias
    assert len(child.surname_aliases) >= 2  # Roberts, Robertson


def test_multiple_relations_same_person():
    """Test person with multiple different relation types."""
    path = write_temp_gw(MULTIPLE_RELATIONS_SAME_PERSON)
    result = parse_gw_file(path)
    os.remove(path)
    rel_blocks = [x for x in result if isinstance(x, RelationsGwSyntax)]
    assert rel_blocks
    rel = rel_blocks[0]
    # Should have multiple relations
    assert len(rel.relations) >= 4
    # Check different relation types are present
    rel_types = [r.type.name for r in rel.relations]
    assert 'ADOPTION' in rel_types
    assert 'GODPARENT' in rel_types
    assert 'FOSTERPARENT' in rel_types


def test_multiple_events_with_witnesses():
    """Test personal events with various witnesses and notes."""
    path = write_temp_gw(MULTIPLE_EVENTS_WITH_WITNESSES)
    result = parse_gw_file(path)
    os.remove(path)
    pevt_blocks = [x for x in result if isinstance(x, PersonalEventsGwSyntax)]
    assert pevt_blocks
    pevt = pevt_blocks[0]
    # Should have multiple events
    assert len(pevt.events) >= 3
    # Events should have witnesses
    for event in pevt.events:
        if event.name.__class__.__name__ in ['PersBirth', 'PersBaptism']:
            # These events should have witnesses in the test data
            pass


def test_family_with_complex_marriage_history():
    """Test multiple marriages for same person."""
    path = write_temp_gw(FAMILY_WITH_COMPLEX_MARRIAGE_HISTORY)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    # Should parse both marriages
    assert len(fam_blocks) >= 2


def test_nested_surnames_and_occurrences():
    """Test handling of name occurrences and surname inheritance."""
    path = write_temp_gw(NESTED_SURNAMES_AND_OCCURRENCES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    # Should parse all three families
    assert len(fam_blocks) == 3
    # Verify children names and occurrences
    assert len(fam_blocks[0].descend) >= 1
    assert len(fam_blocks[1].descend) >= 3
    assert len(fam_blocks[2].descend) >= 1


def test_mixed_content_file():
    """Test file with multiple different block types."""
    path = write_temp_gw(MIXED_CONTENT_FILE)
    result = parse_gw_file(path)
    os.remove(path)
    # Should have different block types
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    notes_blocks = [x for x in result if isinstance(x, NotesGwSyntax)]
    rel_blocks = [x for x in result if isinstance(x, RelationsGwSyntax)]
    pevt_blocks = [x for x in result if isinstance(x, PersonalEventsGwSyntax)]
    base_notes = [x for x in result if isinstance(x, BaseNotesGwSyntax)]
    wiz_notes = [x for x in result if isinstance(x, WizardNotesGwSyntax)]
    page_ext = [x for x in result if isinstance(x, PageExtGwSyntax)]

    assert len(fam_blocks) >= 2
    assert len(notes_blocks) >= 1
    assert len(rel_blocks) >= 1
    assert len(pevt_blocks) >= 1
    assert len(base_notes) >= 1
    assert len(wiz_notes) >= 1
    assert len(page_ext) >= 1


def test_person_with_death_variations():
    """Test different death status codes."""
    path = write_temp_gw(PERSON_WITH_DEATH_VARIATIONS)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    # Should parse all children with different death statuses
    assert len(fam_blocks[0].descend) >= 6


def test_dates_with_calendars():
    """Test dates with different calendar suffixes."""
    path = write_temp_gw(DATES_WITH_CALENDARS)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    # Should parse children with different calendar types
    assert len(fam_blocks[0].descend) >= 4


def test_family_with_sex_overrides():
    """Test relation types with sex overrides."""
    path = write_temp_gw(FAMILY_WITH_SEX_OVERRIDES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    # Should parse families with different relation types and sex overrides
    assert len(fam_blocks) >= 3
    # Verify sex overrides were applied
    for fam in fam_blocks:
        # Sex values should be set based on overrides
        assert fam.father_sex is not None
        assert fam.mother_sex is not None


def test_complex_titles_and_aliases():
    """Test person with multiple titles and aliases."""
    path = write_temp_gw(COMPLEX_TITLES_AND_ALIASES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    child = fam_blocks[0].descend[0]
    assert child.first_name == "Robert"
    # Should have multiple surname aliases
    assert len(child.surname_aliases) >= 3  # Roberts, Robertson, Robertsen
    # Should have multiple titles
    assert len(child.titles) >= 4  # King, Duke, Baron, and one more
    # Should have some form of aliases
    assert len(child.aliases) >= 1  # Bob_the_Builder


def test_events_with_all_witness_types():
    """Test event with all different witness types."""
    path = write_temp_gw(EVENTS_WITH_ALL_WITNESS_TYPES)
    result = parse_gw_file(path)
    os.remove(path)
    pevt_blocks = [x for x in result if isinstance(x, PersonalEventsGwSyntax)]
    assert pevt_blocks
    # Should parse event with multiple witnesses of different types
    assert len(pevt_blocks[0].events) >= 1


def test_empty_and_edge_cases():
    """Test edge cases like empty families, missing names, etc."""
    path = write_temp_gw(EMPTY_AND_EDGE_CASES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    # Should handle edge cases gracefully
    assert len(fam_blocks) >= 2


# Family event tests

def test_family_events_all_types():
    """Test family block with all different event types."""
    path = write_temp_gw(FAMILY_EVENTS_ALL_TYPES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have multiple different event types
    assert len(fam.events) >= 8
    # Check for specific event types
    event_tags = [str(type(evt[0].name).__name__) for evt in fam.events]
    assert 'FamMarriage' in event_tags
    assert 'FamMarriageBann' in event_tags
    assert 'FamMarriageContract' in event_tags
    assert 'FamMarriageLicense' in event_tags
    assert 'FamResidence' in event_tags
    assert 'FamSeparated' in event_tags
    assert 'FamDivorce' in event_tags


def test_family_events_with_witnesses():
    """Test family events with multiple witnesses."""
    path = write_temp_gw(FAMILY_EVENTS_WITH_WITNESSES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have events
    assert len(fam.events) >= 2
    # Marriage event should have witnesses
    marriage_event = fam.events[0]
    assert len(marriage_event[1]) >= 5  # 5 witnesses for marriage


def test_family_events_no_marriage():
    """Test family events for unmarried couple."""
    path = write_temp_gw(FAMILY_EVENTS_NO_MARRIAGE)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have residence and no marriage events
    assert len(fam.events) >= 2
    event_tags = [str(type(evt[0].name).__name__) for evt in fam.events]
    assert 'FamResidence' in event_tags
    assert 'FamNoMarriage' in event_tags


def test_family_events_engagement_only():
    """Test family with engagement but no marriage."""
    path = write_temp_gw(FAMILY_EVENTS_ENGAGEMENT_ONLY)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have engagement event
    assert len(fam.events) >= 1
    event_tags = [str(type(evt[0].name).__name__) for evt in fam.events]
    assert 'FamEngage' in event_tags


def test_family_events_pacs():
    """Test family with PACS (French civil union)."""
    path = write_temp_gw(FAMILY_EVENTS_PACS)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have PACS and residence events
    assert len(fam.events) >= 2
    event_tags = [str(type(evt[0].name).__name__) for evt in fam.events]
    assert 'FamPACS' in event_tags
    assert 'FamResidence' in event_tags


def test_family_events_annulment():
    """Test family with marriage annulment."""
    path = write_temp_gw(FAMILY_EVENTS_ANNULMENT)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have marriage and annulment events
    assert len(fam.events) >= 2
    event_tags = [str(type(evt[0].name).__name__) for evt in fam.events]
    assert 'FamMarriage' in event_tags
    assert 'FamAnnulation' in event_tags


def test_family_events_multiple_residences():
    """Test family with multiple residence changes."""
    path = write_temp_gw(FAMILY_EVENTS_MULTIPLE_RESIDENCES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have marriage and 5 residence events
    assert len(fam.events) >= 6
    residence_events = [
        evt for evt in fam.events
        if type(evt[0].name).__name__ == 'FamResidence'
    ]
    assert len(residence_events) >= 5


def test_family_events_complex_dates():
    """Test family events with various date formats."""
    path = write_temp_gw(FAMILY_EVENTS_COMPLEX_DATES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should parse all events with different date formats
    assert len(fam.events) >= 5


def test_family_events_with_notes_and_sources():
    """Test family events with detailed notes and sources."""
    path = write_temp_gw(FAMILY_EVENTS_WITH_NOTES_AND_SOURCES)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have events with sources and notes
    assert len(fam.events) >= 3
    # Check that events have sources
    for evt, _ in fam.events:
        if evt.src:  # Some events should have sources
            assert len(evt.src) > 0


def test_family_events_named_custom():
    """Test family with custom named events."""
    path = write_temp_gw(FAMILY_EVENTS_NAMED_CUSTOM)
    result = parse_gw_file(path)
    os.remove(path)
    fam_blocks = [x for x in result if isinstance(x, FamilyGwSyntax)]
    assert fam_blocks
    fam = fam_blocks[0]
    # Should have marriage plus custom events
    assert len(fam.events) >= 3
    event_tags = [str(type(evt[0].name).__name__) for evt in fam.events]
    assert 'FamMarriage' in event_tags
    # Custom events should be parsed as FamNamedEvent
    assert 'FamNamedEvent' in event_tags
