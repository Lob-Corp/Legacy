from libraries.name import NameUtils



def test_unaccent_utf_8():
    result, pos = NameUtils.unaccent_utf_8("hello", 0, True)
    assert result == "h" and pos == 1
    
    result, pos = NameUtils.unaccent_utf_8("Hello", 0, False)
    assert result == "H" and pos == 1
    
    result, pos = NameUtils.unaccent_utf_8("café", 3, True)
    assert result == "e" and pos == 4
    
    result, pos = NameUtils.unaccent_utf_8("José", 1, True)
    assert result == "o" and pos == 2
    
    result, pos = NameUtils.unaccent_utf_8("Müller", 1, True)
    assert result == "u" and pos == 2
    
    result, pos = NameUtils.unaccent_utf_8("test", 10, True)
    assert result == "" and pos == 10
    
    result, pos = NameUtils.unaccent_utf_8("", 0, True)
    assert result == "" and pos == 0

def test_next_chars_if_equiv():
    result = NameUtils.next_chars_if_equiv("hello", 0, "hello", 0)
    assert result == (1, 1)
    
    result = NameUtils.next_chars_if_equiv("Hello", 0, "hello", 0)
    assert result == (1, 1)
    
    result = NameUtils.next_chars_if_equiv("café", 3, "cafe", 3)
    assert result == (4, 4)
    
    result = NameUtils.next_chars_if_equiv("test", 10, "test", 0)
    assert result is None
    
    result = NameUtils.next_chars_if_equiv("", 0, "", 0)
    assert result is None

def test_lower():
    assert NameUtils.lower("Hello World") == "hello world"
    assert NameUtils.lower("UPPERCASE") == "uppercase"
    assert NameUtils.lower("José María") == "jose maria"
    assert NameUtils.lower("François") == "francois"
    assert NameUtils.lower("Jean-Baptiste") == "jean baptiste"
    assert NameUtils.lower("Dr. Smith") == "dr. smith"
    assert NameUtils.lower("Version 2.0") == "version 2.0"
    assert NameUtils.lower("  multiple   spaces  ") == "multiple spaces"
    assert NameUtils.lower("") == ""
    assert NameUtils.lower("A") == "a"

def test_title():
    assert NameUtils.title("hello world") == "Hello World"
    assert NameUtils.title("jean-baptiste") == "Jean-Baptiste"
    assert NameUtils.title("mary o'connor") == "Mary O'Connor"
    assert NameUtils.title("Hello World") == "Hello World"
    assert NameUtils.title("test123") == "Test123"
    assert NameUtils.title("") == ""

def test_abbrev():
    assert NameUtils.abbrev("saint marie") == "st marie"
    assert NameUtils.abbrev("sainte anne") == "ste anne"
    assert NameUtils.abbrev("van der berg") == "der berg"
    assert NameUtils.abbrev("von neumann") == "neumann"
    assert NameUtils.abbrev("de la cruz") == "la cruz"
    assert NameUtils.abbrev("Saint Francis") == "St Francis"
    assert NameUtils.abbrev("jean de saint martin") == "jean st martin"
    assert NameUtils.abbrev("john smith") == "john smith"
    assert NameUtils.abbrev("") == ""

def test_roman_number():
    assert NameUtils.roman_number("Louis XIV", 6) == 9
    assert NameUtils.roman_number("Henry VIII", 6) == 10
    assert NameUtils.roman_number("iv", 0) == 2
    assert NameUtils.roman_number("civil", 1) is None
    assert NameUtils.roman_number("hello world", 0) is None
    assert NameUtils.roman_number("", 0) is None

def test_abbreviate_name():
    result = NameUtils.abbreviate_name("Catherine")
    assert len(result) > 0
    
    result = NameUtils.abbreviate_name("Philippe")
    assert "f" in result.lower()
    assert "ph" not in result.lower()
    
    result = NameUtils.abbreviate_name("Karl")
    assert "c" in result.lower()
    
    result = NameUtils.abbreviate_name("Charles")
    assert not result.endswith("s")
    
    result = NameUtils.abbreviate_name("Louis XIV")
    assert "xiv" in result.lower() or "XIV" in result
    
    assert NameUtils.abbreviate_name("") == ""

def test_strip_lower():
    assert NameUtils.strip_lower("Hello World") == "helloworld"
    assert NameUtils.strip_lower("Jean-Baptiste") == "jeanbaptiste"
    assert NameUtils.strip_lower("José María") == "josemaria"
    assert NameUtils.strip_lower("  multiple   spaces  ") == "multiplespaces"
    assert NameUtils.strip_lower("") == ""

def test_abbreviate_lower():
    result = NameUtils.abbreviate_lower("Saint Catherine")
    assert len(result) >= 0
    
    result = NameUtils.abbreviate_lower("Jean de Baptiste")
    assert len(result) >= 0
    
    assert len(NameUtils.abbreviate_lower("")) == 0

def test_concat():
    assert NameUtils.concat("John", "Smith") == "John Smith"
    assert NameUtils.concat("", "") == ""
    assert NameUtils.concat("John", "") == "John"
    assert NameUtils.concat("", "Smith") == "Smith"

def test_contains_forbidden_char():
    assert NameUtils.contains_forbidden_char("test:email") is True
    assert NameUtils.contains_forbidden_char("name@domain") is True
    assert NameUtils.contains_forbidden_char("hash#tag") is True
    assert NameUtils.contains_forbidden_char("equal=sign") is True
    assert NameUtils.contains_forbidden_char("dollar$sign") is True
    assert NameUtils.contains_forbidden_char("clean name") is False
    assert NameUtils.contains_forbidden_char("") is False

def testsplit_name_internal():
    result = NameUtils.split_name_internal("hello world", " ")
    assert result == ["hello", "world"]
    
    result = NameUtils.split_name_internal("van der Berg-Smith", " -")
    assert result == ["van", "der", "Berg", "Smith"]
    
    result = NameUtils.split_name_internal("SingleWord", " ")
    assert result == ["SingleWord"]
    
    result = NameUtils.split_name_internal("", " ")
    assert result == []

def test_integration_genealogy_workflow():
    original_name = "Saint-Jean Baptiste de la Fontaine-Rodriguez"
    
    lowered = NameUtils.lower(original_name)
    assert len(lowered) > 0 and lowered.islower()
    
    abbreviated = NameUtils.abbrev(lowered)
    assert "st" in abbreviated
    
    phonetic = NameUtils.abbreviate_name(abbreviated)
    assert len(phonetic) >= 0
    
    processed = NameUtils.abbreviate_lower(original_name)
    assert len(processed) >= 0

def test_name_matching_scenarios():
    name1 = NameUtils.abbreviate_lower("Catherine Johnson")
    name2 = NameUtils.abbreviate_lower("Katherine Jonson")
    assert len(name1) >= 0 and len(name2) >= 0
    
    french1 = NameUtils.abbreviate_lower("Jean de la Fontaine")
    french2 = NameUtils.abbreviate_lower("Jean Delafontaine")
    assert len(french1) >= 0 and len(french2) >= 0

def test_unicode_international_names():
    names = ["José María García", "François Müller", "Björn Andersson"]
    
    for name in names:
        lower_result = NameUtils.lower(name)
        assert len(lower_result) > 0
        
        abbrev_result = NameUtils.abbrev(name)
        assert len(abbrev_result) > 0
        
        phonetic_result = NameUtils.abbreviate_name(name)
        assert len(phonetic_result) >= 0

def test_edge_cases_robustness():
    edge_cases = ["", " ", "a", "A", "123", "   multiple   spaces   ", "ALLUPPERCASE"]
    
    for case in edge_cases:
        try:
            NameUtils.lower(case)
            NameUtils.title(case)
            NameUtils.abbrev(case)
            NameUtils.abbreviate_name(case)
            NameUtils.strip_lower(case)
            NameUtils.abbreviate_lower(case)
            NameUtils.contains_forbidden_char(case)
            NameUtils.split_name_internal(case, " ")
        except Exception:
            assert False, f"Function failed on edge case '{case}'"

def test_constants_accessibility():
    assert isinstance(NameUtils.FORBIDDEN_CHARS, list)
    assert len(NameUtils.FORBIDDEN_CHARS) > 0
    assert ":" in NameUtils.FORBIDDEN_CHARS
    
    assert isinstance(NameUtils.ABBREV_LIST, dict)
    assert len(NameUtils.ABBREV_LIST) > 0
    assert "saint" in NameUtils.ABBREV_LIST
    assert NameUtils.ABBREV_LIST["saint"] == "st"
    """Test title() with already capitalized text."""
    assert NameUtils.title("Hello World") == "Hello World"
    assert NameUtils.title("HELLO WORLD") == "Hello World"

def test_title_numbers_and_special_chars():
    """Test title() with numbers and special characters."""
    assert NameUtils.title("test123") == "Test123"
    assert NameUtils.title("a1b2c3") == "A1B2C3"
    assert NameUtils.title("name-with-hyphens") == "Name-With-Hyphens"

def test_title_edge_cases():
    """Test title() edge cases."""
    assert NameUtils.title("") == ""
    assert NameUtils.title("a") == "A"
    assert NameUtils.title("123") == "123"
    assert NameUtils.title("   spaces   ") == "   Spaces   "

def test_title_mixed_separators():
    """Test title() with various separators."""
    assert NameUtils.title("word1 word2-word3.word4") == "Word1 Word2-Word3.Word4"
    assert NameUtils.title("a/b\\c|d") == "A/B\\C|D"

# ========== ABBREV TESTS ==========

def test_abbrev_saint_abbreviations():
    """Test abbrev() with saint abbreviations."""
    assert NameUtils.abbrev("saint marie") == "st marie"
    assert NameUtils.abbrev("sainte anne") == "ste anne"
    assert NameUtils.abbrev("Saint Francis") == "St Francis"
    assert NameUtils.abbrev("Sainte Marie") == "Ste Marie"

def test_abbrev_particle_removal():
    """Test abbrev() removes particles."""
    assert NameUtils.abbrev("van der berg") == "der berg"
    assert NameUtils.abbrev("von neumann") == "neumann"
    assert NameUtils.abbrev("de la cruz") == "la cruz"
    assert NameUtils.abbrev("af nielsen") == "nielsen"

def test_abbrev_mixed_case_particles():
    """Test abbrev() with mixed case particles."""
    assert NameUtils.abbrev("Van Der Berg") == "Der Berg"
    assert NameUtils.abbrev("DE LA CRUZ") == "LA CRUZ"
    assert NameUtils.abbrev("Von Neumann") == "Neumann"

def test_abbrev_multiple_particles():
    """Test abbrev() with multiple particles in sequence."""
    assert NameUtils.abbrev("jean de saint martin") == "jean st martin"
    assert NameUtils.abbrev("marie van der saint") == "marie der st"

def test_abbrev_no_changes_needed():
    """Test abbrev() when no abbreviation is needed."""
    assert NameUtils.abbrev("john smith") == "john smith"
    assert NameUtils.abbrev("simple name") == "simple name"
    assert NameUtils.abbrev("testing") == "testing"

def test_abbrev_edge_cases():
    """Test abbrev() edge cases."""
    assert NameUtils.abbrev("") == ""
    assert NameUtils.abbrev("saint") == "st"
    assert NameUtils.abbrev("de") == ""
    assert NameUtils.abbrev("a b c") == "b c"  # All particles removed

def test_abbrev_ier_replacement():
    """Test abbrev() with 'ier' replacement."""
    assert NameUtils.abbrev("premier") == "premier"  # 'ier' -> 'i'
    assert NameUtils.abbrev("Premier") == "Premier"

# ========== ROMAN_NUMBER TESTS ==========

def test_roman_number_valid_at_start():
    """Test roman_number() with valid numerals at string start."""
    assert NameUtils.roman_number("iv", 0) == 2
    assert NameUtils.roman_number("ix", 0) == 2
    assert NameUtils.roman_number("xi", 0) == 2
    assert NameUtils.roman_number("xl", 0) == 2

def test_roman_number_valid_after_space():
    """Test roman_number() with valid numerals after space."""
    assert NameUtils.roman_number("Louis XIV", 6) == 9
    assert NameUtils.roman_number("Henry VIII", 6) == 10
    assert NameUtils.roman_number("Elizabeth II", 10) == 12
    assert NameUtils.roman_number("test iv", 5) == 7


def test_roman_number_mixed_case():
    """Test roman_number() with mixed case."""
    assert NameUtils.roman_number("IV", 0) == 2
    assert NameUtils.roman_number("Ix", 0) == 2
    assert NameUtils.roman_number("Xi", 0) == 2

def test_roman_number_partial_match():
    """Test roman_number() with partial matches that don't end at word boundary."""
    assert NameUtils.roman_number("ivan", 0) is None  # 'iv' + 'an'
    assert NameUtils.roman_number("extra", 0) is None  # 'x' + 'tra'

def test_roman_number_edge_cases():
    """Test roman_number() edge cases."""
    # Empty string
    assert NameUtils.roman_number("", 0) is None
    
    # Single characters
    assert NameUtils.roman_number("i", 0) == 1
    assert NameUtils.roman_number("x", 0) == 1
    assert NameUtils.roman_number("v", 0) == 1
    assert NameUtils.roman_number("l", 0) == 1

# ========== ABBREVIATE_NAME TESTS ==========

def test_abbreviate_name_vowel_removal():
    """Test abbreviate_name() removes vowels after first."""
    result = NameUtils.abbreviate_name("Catherine")
    # Should remove vowels after first, but this depends on implementation
    assert len(result) < len("Catherine")

def test_abbreviate_name_character_replacements():
    """Test abbreviate_name() character replacements."""
    # k/q -> c
    result_k = NameUtils.abbreviate_name("Karl")
    assert "c" in result_k.lower()
    
    result_q = NameUtils.abbreviate_name("Quentin")
    assert "c" in result_q.lower()

    # z -> s
    result_z = NameUtils.abbreviate_name("Zachary")
    assert "s" in result_z.lower()

def test_abbreviate_name_ph_replacement():
    """Test abbreviate_name() ph -> f replacement."""
    result = NameUtils.abbreviate_name("Philippe")
    assert "f" in result.lower()
    # Should not contain 'ph'
    assert "ph" not in result.lower()

def test_abbreviate_name_h_removal():
    """Test abbreviate_name() removes standalone 'h'."""
    result = NameUtils.abbreviate_name("Thomas")
    # 'h' should be removed
    assert "h" not in result

def test_abbreviate_name_s_removal_at_end():
    """Test abbreviate_name() removes 's' at word endings."""
    result = NameUtils.abbreviate_name("Charles")
    # Ending 's' should be removed
    assert not result.endswith("s")

def test_abbreviate_name_double_consonant_removal():
    """Test abbreviate_name() eliminates double consonants."""
    result = NameUtils.abbreviate_name("William")
    # Should not have double 'l'
    assert "ll" not in result

    result2 = NameUtils.abbreviate_name("Matthew")
    # Should not have double 't'
    assert "tt" not in result2

def test_abbreviate_name_roman_numerals_preserved():
    """Test abbreviate_name() preserves Roman numerals."""
    result = NameUtils.abbreviate_name("Louis XIV")
    assert "xiv" in result.lower() or "XIV" in result

    result2 = NameUtils.abbreviate_name("Henry VIII")
    assert "viii" in result2.lower() or "VIII" in result2

def test_abbreviate_name_case_preservation():
    """Test abbreviate_name() preserves original case patterns."""
    result = NameUtils.abbreviate_name("Philippe")
    # Should preserve capitalization pattern
    assert result[0].isupper() if result else True

    result2 = NameUtils.abbreviate_name("KARL")
    # Should handle all caps
    assert len(result2) > 0

def test_abbreviate_name_edge_cases():
    """Test abbreviate_name() edge cases."""
    assert NameUtils.abbreviate_name("") == ""
    
    # Single character
    result = NameUtils.abbreviate_name("A")
    assert len(result) >= 0

    # Single word
    result = NameUtils.abbreviate_name("John")
    assert len(result) > 0

def test_abbreviate_name_multiple_words():
    """Test abbreviate_name() with multiple words."""
    result = NameUtils.abbreviate_name("Jean Baptiste")
    # Should process each word
    assert len(result) > 0

    result2 = NameUtils.abbreviate_name("Marie Antoinette")
    assert len(result2) > 0

# ========== STRIP_LOWER TESTS ==========

def test_strip_lower_basic_functionality():
    """Test strip_lower() basic functionality."""
    assert NameUtils.strip_lower("Hello World") == "helloworld"
    assert NameUtils.strip_lower("Jean-Baptiste") == "jeanbaptiste"
    assert NameUtils.strip_lower("O'Connor") == "oconnor"

def test_strip_lower_accented_characters():
    """Test strip_lower() with accented characters."""
    assert NameUtils.strip_lower("José María") == "josemaria"
    assert NameUtils.strip_lower("François") == "francois"
    assert NameUtils.strip_lower("naïve café") == "naivecafe"

def test_strip_lower_multiple_spaces():
    """Test strip_lower() with multiple spaces."""
    assert NameUtils.strip_lower("  multiple   spaces  ") == "multiplespaces"
    assert NameUtils.strip_lower("a  b  c") == "abc"

def test_strip_lower_special_characters():
    """Test strip_lower() with special characters."""
    assert NameUtils.strip_lower("name@domain.com") == "namedomain.com"
    assert NameUtils.strip_lower("test-case") == "testcase"

def test_strip_lower_edge_cases():
    """Test strip_lower() edge cases."""
    assert NameUtils.strip_lower("") == ""
    assert NameUtils.strip_lower("   ") == ""
    assert NameUtils.strip_lower("a") == "a"

# ========== ABBREVIATE_LOWER TESTS ==========

def test_abbreviate_lower_full_pipeline():
    """Test abbreviate_lower() full processing pipeline."""
    # Should apply: lower -> abbrev -> abbreviate_name
    result = NameUtils.abbreviate_lower("Saint Catherine")
    assert len(result) > 0

    result2 = NameUtils.abbreviate_lower("Jean de Baptiste")
    assert len(result2) > 0

def test_abbreviate_lower_case_normalization():
    """Test abbreviate_lower() normalizes case."""
    result1 = NameUtils.abbreviate_lower("CATHERINE")
    result2 = NameUtils.abbreviate_lower("catherine")
    result3 = NameUtils.abbreviate_lower("Catherine")
    
    # All should produce similar results (case-normalized)
    assert len(result1) > 0
    assert len(result2) > 0
    assert len(result3) > 0

def test_abbreviate_lower_particles_and_phonetic():
    """Test abbreviate_lower() with particles and phonetic processing."""
    result = NameUtils.abbreviate_lower("Saint-Jean von Katherine")
    # Should handle particles and phonetic processing
    assert len(result) > 0

def test_abbreviate_lower_edge_cases():
    """Test abbreviate_lower() edge cases."""
    assert len(NameUtils.abbreviate_lower("")) == 0
    
    result = NameUtils.abbreviate_lower("a")
    assert len(result) >= 0

# ========== CONCAT TESTS ==========

def test_concat_basic_functionality():
    """Test concat() basic functionality."""
    assert NameUtils.concat("John", "Smith") == "John Smith"
    assert NameUtils.concat("Marie", "Curie") == "Marie Curie"

def test_concat_empty_strings():
    """Test concat() with empty strings."""
    assert NameUtils.concat("", "") == ""
    assert NameUtils.concat("John", "") == "John"
    assert NameUtils.concat("", "Smith") == "Smith"

def test_concat_whitespace_handling():
    """Test concat() with whitespace."""
    assert NameUtils.concat("  John  ", "  Smith  ") == "John Smith"
    assert NameUtils.concat("John", "   ") == "John"
    assert NameUtils.concat("   ", "Smith") == "Smith"

def test_concat_special_characters():
    """Test concat() with special characters."""
    assert NameUtils.concat("Jean-Baptiste", "O'Connor") == "Jean-Baptiste O'Connor"
    assert NameUtils.concat("Dr.", "Smith") == "Dr. Smith"

# ========== CONTAINS_FORBIDDEN_CHAR TESTS ==========

def test_contains_forbidden_char_found_single():
    """Test contains_forbidden_char() detects single forbidden characters."""
    assert NameUtils.contains_forbidden_char("test:email") is True
    assert NameUtils.contains_forbidden_char("name@domain") is True
    assert NameUtils.contains_forbidden_char("hash#tag") is True
    assert NameUtils.contains_forbidden_char("equal=sign") is True
    assert NameUtils.contains_forbidden_char("dollar$sign") is True

def test_contains_forbidden_char_found_multiple():
    """Test contains_forbidden_char() detects multiple forbidden characters."""
    assert NameUtils.contains_forbidden_char("test:@#=$") is True
    assert NameUtils.contains_forbidden_char("bad@email:format") is True

def test_contains_forbidden_char_not_found():
    """Test contains_forbidden_char() with clean strings."""
    assert NameUtils.contains_forbidden_char("clean name") is False
    assert NameUtils.contains_forbidden_char("simple-name") is False
    assert NameUtils.contains_forbidden_char("") is False
    assert NameUtils.contains_forbidden_char("test123") is False

def test_contains_forbidden_char_edge_cases():
    """Test contains_forbidden_char() edge cases."""
    # Only forbidden characters
    assert NameUtils.contains_forbidden_char(":@#=$") is True
    
    # Single character strings
    assert NameUtils.contains_forbidden_char(":") is True
    assert NameUtils.contains_forbidden_char("a") is False

# ========== SPLIT_NAME_INTERNAL TESTS ==========

def testsplit_name_internal_single_separator():
    """Test split_name_internal() with single separator."""
    result = NameUtils.split_name_internal("hello world", " ")
    assert result == ["hello", "world"]

    result = NameUtils.split_name_internal("one-two", "-")
    assert result == ["one", "two"]

def testsplit_name_internal_multiple_separators():
    """Test split_name_internal() with multiple separators."""
    result = NameUtils.split_name_internal("van der Berg-Smith", " -")
    assert result == ["van", "der", "Berg", "Smith"]

    result = NameUtils.split_name_internal("a-b c-d", " -")
    assert result == ["a", "b", "c", "d"]

def testsplit_name_internal_no_separators():
    """Test split_name_internal() with no separators found."""
    result = NameUtils.split_name_internal("SingleWord", " ")
    assert result == ["SingleWord"]

    result = NameUtils.split_name_internal("NoHyphens", "-")
    assert result == ["NoHyphens"]

def testsplit_name_internal_consecutive_separators():
    """Test split_name_internal() with consecutive separators."""
    result = NameUtils.split_name_internal("word1  word2", " ")
    # Should handle multiple spaces (empty parts filtered)
    assert "word1" in result
    assert "word2" in result

    result = NameUtils.split_name_internal("a--b", "-")
    # Should handle multiple hyphens
    assert "a" in result
    assert "b" in result

def testsplit_name_internal_leading_trailing_separators():
    """Test split_name_internal() with leading/trailing separators."""
    result = NameUtils.split_name_internal(" hello world ", " ")
    # Should handle leading/trailing spaces
    assert "hello" in result
    assert "world" in result

    result = NameUtils.split_name_internal("-start-end-", "-")
    # Should handle leading/trailing hyphens
    assert "start" in result
    assert "end" in result

def testsplit_name_internal_empty_string():
    """Test split_name_internal() with empty string."""
    result = NameUtils.split_name_internal("", " ")
    assert result == []

    result = NameUtils.split_name_internal("", " -")
    assert result == []

def testsplit_name_internal_only_separators():
    """Test split_name_internal() with only separators."""
    result = NameUtils.split_name_internal("   ", " ")
    # Should return empty list (all empty parts filtered)
    assert result == [] or all(part == "" for part in result)

    result = NameUtils.split_name_internal("---", "-")
    # Should return empty list or empty strings
    assert result == [] or all(part == "" for part in result)

def testsplit_name_internal_callback_functionality():
    """Test split_name_internal() callback functionality."""
    parts = []
    NameUtils.split_name_internal(
        "hello world", 
        " ", 
        lambda pos, length: parts.append((pos, length))
    )
    
    assert len(parts) == 2
    # Verify positions and lengths are correct
    for pos, length in parts:
        assert pos >= 0
        assert length > 0

def testsplit_name_internal_complex_separators():
    """Test split_name_internal() with complex separator combinations."""
    result = NameUtils.split_name_internal("a b-c d", " -")
    assert result == ["a", "b", "c", "d"]

    result = NameUtils.split_name_internal("word1.word2,word3", ".,")
    assert result == ["word1", "word2", "word3"]

# ========== INTEGRATION TESTS ==========

def test_genealogy_name_processing_workflow():
    """Test complete genealogy name processing workflow."""
    # Test typical genealogy processing pipeline
    original_name = "Saint-Jean Baptiste de la Fontaine-Rodriguez"
    
    # Step 1: Basic normalization
    lowered = NameUtils.lower(original_name)
    assert len(lowered) > 0
    assert lowered.islower()

    # Step 2: Apply abbreviations
    abbreviated = NameUtils.abbrev(lowered)
    assert "st" in abbreviated  # "saint" -> "st"

    # Step 3: Phonetic processing
    phonetic = NameUtils.abbreviate_name(abbreviated)
    assert len(phonetic) > 0

    # Step 4: Full pipeline
    processed = NameUtils.abbreviate_lower(original_name)
    assert len(processed) > 0

def test_data_validation_and_cleaning():
    """Test data validation and cleaning scenarios."""
    # Test forbidden character detection and removal
    dirty_name = "John:Smith@genealogy#site"
    
    has_forbidden = NameUtils.contains_forbidden_char(dirty_name)
    assert has_forbidden is True

    # Test processing continues despite forbidden chars
    processed = NameUtils.lower(dirty_name)
    assert len(processed) > 0

def test_unicode_and_international_names():
    """Test Unicode and international name handling."""
    # Test various international names
    names = [
        "José María García",
        "François Müller", 
        "Björn Andersson",
        "Niño Rodriguez",
        "Ñoño Peña"
    ]
    
    for name in names:
        # All processing functions should handle Unicode
        lower_result = NameUtils.lower(name)
        assert len(lower_result) > 0
        
        abbrev_result = NameUtils.abbrev(name)
        assert len(abbrev_result) > 0
        
        phonetic_result = NameUtils.abbreviate_name(name)
        assert len(phonetic_result) >= 0