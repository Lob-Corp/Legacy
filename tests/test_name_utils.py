# import pytest
# from libraries.name import NameUtils


# class TestUnaccentUtf8:
#     """Tests for unaccent_utf_8 method"""

#     def test_unaccent_utf_8_with_simple_ascii_lowercase(self):
#         result, pos = NameUtils.unaccent_utf_8("hello", 0, True)
#         assert result == "h"
#         assert pos == 1

#     def test_unaccent_utf_8_with_simple_ascii_uppercase_to_lower(self):
#         result, pos = NameUtils.unaccent_utf_8("HELLO", 0, True)
#         assert result == "h"
#         assert pos == 1

#     def test_unaccent_utf_8_with_simple_ascii_uppercase_keep_case(self):
#         result, pos = NameUtils.unaccent_utf_8("HELLO", 0, False)
#         assert result == "H"
#         assert pos == 1

#     def test_unaccent_utf_8_with_accented_character_e_acute(self):
#         result, pos = NameUtils.unaccent_utf_8("é", 0, True)
#         assert result == "e"
#         assert pos == 1

#     def test_unaccent_utf_8_with_accented_character_e_grave(self):
#         result, pos = NameUtils.unaccent_utf_8("è", 0, True)
#         assert result == "e"
#         assert pos == 1

#     def test_unaccent_utf_8_with_accented_character_a_circumflex(self):
#         result, pos = NameUtils.unaccent_utf_8("â", 0, True)
#         assert result == "a"
#         assert pos == 1

#     def test_unaccent_utf_8_with_accented_character_c_cedilla(self):
#         result, pos = NameUtils.unaccent_utf_8("ç", 0, True)
#         assert result == "c"
#         assert pos == 1

#     def test_unaccent_utf_8_with_accented_character_n_tilde(self):
#         result, pos = NameUtils.unaccent_utf_8("ñ", 0, True)
#         assert result == "n"
#         assert pos == 1

#     def test_unaccent_utf_8_with_accented_uppercase_keep_case(self):
#         result, pos = NameUtils.unaccent_utf_8("É", 0, False)
#         assert result == "E"
#         assert pos == 1

#     def test_unaccent_utf_8_with_accented_uppercase_to_lower(self):
#         result, pos = NameUtils.unaccent_utf_8("É", 0, True)
#         assert result == "e"
#         assert pos == 1

#     def test_unaccent_utf_8_at_middle_position(self):
#         result, pos = NameUtils.unaccent_utf_8("café", 3, True)
#         assert result == "e"
#         assert pos == 4

#     def test_unaccent_utf_8_at_end_position(self):
#         result, pos = NameUtils.unaccent_utf_8("test", 3, True)
#         assert result == "t"
#         assert pos == 4

#     def test_unaccent_utf_8_beyond_string_length(self):
#         result, pos = NameUtils.unaccent_utf_8("test", 10, True)
#         assert result == ""
#         assert pos == 10

#     def test_unaccent_utf_8_with_empty_string(self):
#         result, pos = NameUtils.unaccent_utf_8("", 0, True)
#         assert result == ""
#         assert pos == 0

#     def test_unaccent_utf_8_with_number(self):
#         result, pos = NameUtils.unaccent_utf_8("5", 0, True)
#         assert result == "5"
#         assert pos == 1

#     def test_unaccent_utf_8_with_special_character(self):
#         result, pos = NameUtils.unaccent_utf_8("-", 0, True)
#         assert result == "-"
#         assert pos == 1


# class TestNextCharsIfEquiv:
#     """Tests for next_chars_if_equiv method"""

#     def test_next_chars_if_equiv_with_identical_ascii_chars(self):
#         result = NameUtils.next_chars_if_equiv("hello", 0, "hello", 0)
#         assert result == (1, 1)

#     def test_next_chars_if_equiv_with_different_ascii_chars(self):
#         result = NameUtils.next_chars_if_equiv("hello", 0, "world", 0)
#         assert result is None

#     def test_next_chars_if_equiv_with_case_difference(self):
#         result = NameUtils.next_chars_if_equiv("Hello", 0, "hello", 0)
#         assert result == (1, 1)

#     def test_next_chars_if_equiv_with_accented_vs_unaccented(self):
#         result = NameUtils.next_chars_if_equiv("café", 3, "cafe", 3)
#         assert result == (4, 4)

#     def test_next_chars_if_equiv_with_both_accented_same(self):
#         result = NameUtils.next_chars_if_equiv("café", 3, "café", 3)
#         assert result == (4, 4)

#     def test_next_chars_if_equiv_with_both_accented_different(self):
#         result = NameUtils.next_chars_if_equiv("café", 3, "cafè", 3)
#         assert result == (4, 4)  # Both normalize to 'e'

#     def test_next_chars_if_equiv_when_first_string_index_out_of_bounds(self):
#         result = NameUtils.next_chars_if_equiv("hi", 10, "hello", 0)
#         assert result is None

#     def test_next_chars_if_equiv_when_second_string_index_out_of_bounds(self):
#         result = NameUtils.next_chars_if_equiv("hello", 0, "hi", 10)
#         assert result is None

#     def test_next_chars_if_equiv_when_both_indices_out_of_bounds(self):
#         result = NameUtils.next_chars_if_equiv("hi", 10, "bye", 10)
#         assert result is None

#     def test_next_chars_if_equiv_at_end_of_both_strings(self):
#         result = NameUtils.next_chars_if_equiv("test", 3, "best", 3)
#         assert result == (4, 4)


# class TestLower:
#     """Tests for lower method"""

#     def test_lower_with_simple_lowercase_string(self):
#         assert NameUtils.lower("hello") == "hello"

#     def test_lower_with_simple_uppercase_string(self):
#         assert NameUtils.lower("HELLO") == "hello"

#     def test_lower_with_mixed_case_string(self):
#         assert NameUtils.lower("HeLLo") == "hello"

#     def test_lower_with_accented_characters(self):
#         assert NameUtils.lower("café") == "cafe"

#     def test_lower_with_multiple_accented_characters(self):
#         assert NameUtils.lower("José María") == "jose maria"

#     def test_lower_with_hyphens_converted_to_spaces(self):
#         assert NameUtils.lower("Jean-Baptiste") == "jean baptiste"

#     def test_lower_with_underscores_converted_to_spaces(self):
#         assert NameUtils.lower("first_name") == "first name"

#     def test_lower_with_numbers_preserved(self):
#         assert NameUtils.lower("Louis14") == "louis14"

#     def test_lower_with_dots_preserved(self):
#         assert NameUtils.lower("J.R.R.") == "j.r.r."

#     def test_lower_with_multiple_spaces_normalized(self):
#         assert NameUtils.lower("hello    world") == "hello world"

#     def test_lower_with_leading_spaces_stripped(self):
#         assert NameUtils.lower("  hello") == "hello"

#     def test_lower_with_trailing_spaces_stripped(self):
#         assert NameUtils.lower("hello  ") == "hello"

#     def test_lower_with_special_characters_converted_to_spaces(self):
#         assert NameUtils.lower("hello@world") == "hello world"

#     def test_lower_with_parentheses_converted_to_spaces(self):
#         assert NameUtils.lower("(Jean)") == "jean"

#     def test_lower_with_empty_string(self):
#         assert NameUtils.lower("") == ""

#     def test_lower_with_only_special_characters(self):
#         assert NameUtils.lower("@#$%") == ""

#     def test_lower_with_mixed_special_and_alphanumeric(self):
#         assert NameUtils.lower("Hello@World#2024") == "hello world 2024"

#     def test_lower_with_apostrophes_converted_to_spaces(self):
#         assert NameUtils.lower("O'Brien") == "o brien"

#     def test_lower_with_multiple_consecutive_special_chars(self):
#         assert NameUtils.lower("hello---world") == "hello world"

#     def test_lower_with_cedilla(self):
#         assert NameUtils.lower("François") == "francois"


# class TestTitle:
#     """Tests for title method"""

#     def test_title_with_lowercase_words(self):
#         assert NameUtils.title("hello world") == "Hello World"

#     def test_title_with_uppercase_words(self):
#         assert NameUtils.title("HELLO WORLD") == "Hello World"

#     def test_title_with_mixed_case(self):
#         assert NameUtils.title("hELLo WoRLd") == "Hello World"

#     def test_title_with_single_word(self):
#         assert NameUtils.title("hello") == "Hello"

#     def test_title_with_hyphenated_words(self):
#         assert NameUtils.title("jean-baptiste") == "Jean-Baptiste"

#     def test_title_with_apostrophes(self):
#         assert NameUtils.title("o'brien") == "O'Brien"

#     def test_title_with_numbers(self):
#         assert NameUtils.title("louis 14") == "Louis 14"

#     def test_title_with_empty_string(self):
#         assert NameUtils.title("") == ""

#     def test_title_with_only_spaces(self):
#         assert NameUtils.title("   ") == "   "

#     def test_title_with_leading_space(self):
#         assert NameUtils.title(" hello") == " Hello"

#     def test_title_with_trailing_space(self):
#         assert NameUtils.title("hello ") == "Hello "

#     def test_title_with_multiple_spaces(self):
#         assert NameUtils.title("hello  world") == "Hello  World"

#     def test_title_with_dots(self):
#         assert NameUtils.title("j.r.r. tolkien") == "J.R.R. Tolkien"

#     def test_title_with_special_characters(self):
#         assert NameUtils.title("hello@world") == "Hello@World"

#     def test_title_with_single_letter(self):
#         assert NameUtils.title("a") == "A"


# class TestAbbrev:
#     """Tests for abbrev method"""

#     def test_abbrev_with_no_abbreviations(self):
#         assert NameUtils.abbrev("john smith") == "john smith"

#     def test_abbrev_removes_de(self):
#         assert NameUtils.abbrev("pierre de paris") == "pierre paris"

#     def test_abbrev_removes_van(self):
#         assert NameUtils.abbrev("vincent van gogh") == "vincent gogh"

#     def test_abbrev_removes_von(self):
#         assert NameUtils.abbrev("ludwig von beethoven") == "ludwig beethoven"

#     def test_abbrev_removes_multiple_particles(self):
#         assert NameUtils.abbrev("charles de la fontaine") == "charles la fontaine"

#     def test_abbrev_replaces_saint_with_st(self):
#         assert NameUtils.abbrev("saint pierre") == "st pierre"

#     def test_abbrev_replaces_sainte_with_ste(self):
#         assert NameUtils.abbrev("sainte marie") == "ste marie"

#     def test_abbrev_replaces_ier_with_i(self):
#         assert NameUtils.abbrev("premier") == "premier"

#     def test_abbrev_removes_of(self):
#         assert NameUtils.abbrev("john of england") == "john england"

#     def test_abbrev_removes_zu(self):
#         assert NameUtils.abbrev("otto zu hamburg") == "otto hamburg"

#     def test_abbrev_removes_zur(self):
#         assert NameUtils.abbrev("heinrich zur linde") == "heinrich linde"

#     def test_abbrev_removes_di(self):
#         assert NameUtils.abbrev("leonardo di caprio") == "leonardo caprio"
  
#     def test_abbrev_removes_af(self):
#         assert NameUtils.abbrev("anders af sweden") == "anders sweden"

#     def test_abbrev_removes_a(self):
#         assert NameUtils.abbrev("maria a castile") == "maria castile"

#     def test_abbrev_removes_d(self):
#         assert NameUtils.abbrev("jean d arc") == "jean arc"

#     def test_abbrev_preserves_case_for_saint(self):
#         assert NameUtils.abbrev("Saint Pierre") == "St Pierre"

#     def test_abbrev_preserves_case_for_sainte(self):
#         assert NameUtils.abbrev("Sainte Marie") == "Ste Marie"

#     def test_abbrev_with_empty_string(self):
#         assert NameUtils.abbrev("") == ""

#     def test_abbrev_with_multiple_spaces(self):
#         assert NameUtils.abbrev("jean  de  paris") == "jean paris"

#     def test_abbrev_case_insensitive_matching(self):
#         assert NameUtils.abbrev("Jean DE Paris") == "Jean Paris"

#     def test_abbrev_with_mixed_case_particles(self):
#         assert NameUtils.abbrev("Charles De La Fontaine") == "Charles La Fontaine"


# class TestRomanNumber:
#     """Tests for roman_number method"""

#     def test_roman_number_at_start_with_valid_numeral(self):
#         assert NameUtils.roman_number("XIV century", 0) == 3

#     def test_roman_number_at_start_with_lowercase(self):
#         assert NameUtils.roman_number("xiv century", 0) == 3

#     def test_roman_number_after_space(self):
#         assert NameUtils.roman_number("Louis XIV", 6) == 9

#     def test_roman_number_not_after_space(self):
#         assert NameUtils.roman_number("testiv", 4) is None

#     def test_roman_number_at_end_of_string(self):
#         assert NameUtils.roman_number("Louis XIV", 6) == 9

#     def test_roman_number_followed_by_space(self):
#         assert NameUtils.roman_number("IX century", 0) == 2

#     def test_roman_number_single_character(self):
#         assert NameUtils.roman_number("I am", 0) == 1

#     def test_roman_number_with_no_roman_chars(self):
#         assert NameUtils.roman_number("hello world", 0) is None

#     def test_roman_number_with_invalid_continuation(self):
#         assert NameUtils.roman_number("IXZ", 0) is None

#     def test_roman_number_with_mixed_case(self):
#         assert NameUtils.roman_number("IxV", 0) == 3

#     def test_roman_number_empty_at_position(self):
#         result = NameUtils.roman_number("", 0)
#         assert result is None


# class TestAbbreviateName:
#     """Tests for abbreviate_name method (phonetic crushing)"""

#     def test_abbreviate_name_with_simple_name(self):
#         result = NameUtils.abbreviate_name("john")
#         assert result == "jn"

#     def test_abbreviate_name_removes_vowels_except_first(self):
#         result = NameUtils.abbreviate_name("alexander")
#         assert result == "elxndr"

#     def test_abbreviate_name_preserves_first_vowel_as_e(self):
#         result = NameUtils.abbreviate_name("oliver")
#         assert result == "elvr"

#     def test_abbreviate_name_replaces_ph_with_f(self):
#         result = NameUtils.abbreviate_name("philip")
#         assert result == "flp"

#     def test_abbreviate_name_replaces_k_with_c(self):
#         result = NameUtils.abbreviate_name("karl")
#         assert result == "crl"

#     def test_abbreviate_name_replaces_q_with_c(self):
#         result = NameUtils.abbreviate_name("quentin")
#         assert result == "cntn"

#     def test_abbreviate_name_replaces_y_with_i(self):
#         result = NameUtils.abbreviate_name("yves")
#         assert result == "ev"

#     def test_abbreviate_name_replaces_z_with_s(self):
#         result = NameUtils.abbreviate_name("zeus")
#         assert result == "s"

#     def test_abbreviate_name_removes_h(self):
#         result = NameUtils.abbreviate_name("thomas")
#         assert result == "tm"

#     def test_abbreviate_name_removes_trailing_s(self):
#         result = NameUtils.abbreviate_name("charles")
#         assert result == "crl"

#     def test_abbreviate_name_removes_double_consonants(self):
#         result = NameUtils.abbreviate_name("william")
#         assert result == "wlm"

#     def test_abbreviate_name_with_multiple_words(self):
#         result = NameUtils.abbreviate_name("jean pierre")
#         assert result == "jnpr"

#     def test_abbreviate_name_preserves_roman_numerals(self):
#         result = NameUtils.abbreviate_name("louis xiv")
#         assert result == "lxiv"

#     def test_abbreviate_name_with_uppercase(self):
#         result = NameUtils.abbreviate_name("JOHN")
#         assert result == "JHN"

#     def test_abbreviate_name_with_mixed_case(self):
#         result = NameUtils.abbreviate_name("JoHn")
#         assert result == "JHn"

#     def test_abbreviate_name_with_empty_string(self):
#         assert NameUtils.abbreviate_name("") == ""

#     def test_abbreviate_name_with_catherine_and_katherine_same_result(self):
#         cat = NameUtils.abbreviate_name("catherine")
#         kat = NameUtils.abbreviate_name("katherine")
#         assert cat == kat  # Both should normalize similarly

#     def test_abbreviate_name_preserves_case_for_ph(self):
#         result = NameUtils.abbreviate_name("Philip")
#         assert result == "Flp"

#     def test_abbreviate_name_starting_with_vowel_uppercase(self):
#         result = NameUtils.abbreviate_name("Andrew")
#         assert result == "Endrw"


# class TestStripLower:
#     """Tests for strip_lower method"""

#     def test_strip_lower_with_simple_name(self):
#         assert NameUtils.strip_lower("John Smith") == "johnsmith"

#     def test_strip_lower_removes_all_spaces(self):
#         assert NameUtils.strip_lower("Jean Baptiste de La Fontaine") == "jeanbaptistedelafontaine"

#     def test_strip_lower_with_accented_characters(self):
#         assert NameUtils.strip_lower("José María") == "josemaria"

#     def test_strip_lower_with_hyphens(self):
#         assert NameUtils.strip_lower("Jean-Baptiste") == "jeanbaptiste"

#     def test_strip_lower_with_uppercase(self):
#         assert NameUtils.strip_lower("JOHN SMITH") == "johnsmith"

#     def test_strip_lower_with_empty_string(self):
#         assert NameUtils.strip_lower("") == ""

#     def test_strip_lower_with_numbers(self):
#         assert NameUtils.strip_lower("Louis XIV") == "louisxiv"

#     def test_strip_lower_with_special_characters(self):
#         assert NameUtils.strip_lower("O'Brien") == "obrien"

#     def test_strip_lower_with_dots(self):
#         assert NameUtils.strip_lower("J.R.R. Tolkien") == "j.r.r.tolkien"


# class TestAbbreviateLower:
#     """Tests for abbreviate_lower method"""

#     def test_abbreviate_lower_with_simple_name(self):
#         result = NameUtils.abbreviate_lower("John Smith")
#         assert "ejn" in result
#         assert "smt" in result

#     def test_abbreviate_lower_with_particles_removed(self):
#         result = NameUtils.abbreviate_lower("Pierre de Paris")
#         assert "de" not in result.lower()

#     def test_abbreviate_lower_with_van(self):
#         result = NameUtils.abbreviate_lower("Vincent van Gogh")
#         assert "van" not in result.lower()

#     def test_abbreviate_lower_full_pipeline(self):
#         # Test that it applies lower -> abbrev -> abbreviate_name
#         result = NameUtils.abbreviate_lower("Jean-Baptiste de La Fontaine")
#         # Should be lowercased, abbreviated (de removed), and phonetically crushed
#         assert "de" not in result

#     def test_abbreviate_lower_with_empty_string(self):
#         assert NameUtils.abbreviate_lower("") == ""

#     def test_abbreviate_lower_with_accented_characters(self):
#         result = NameUtils.abbreviate_lower("José")
#         assert "jose" in result or " jos" in result  # Accents removed

#     def test_abbreviate_lower_with_saint(self):
#         result = NameUtils.abbreviate_lower("Saint Pierre")
#         assert "st" in result.lower()


# class TestConcat:
#     """Tests for concat method"""

#     def test_concat_with_both_names_present(self):
#         assert NameUtils.concat("John", "Smith") == "John Smith"

#     def test_concat_with_empty_first_name(self):
#         assert NameUtils.concat("", "Smith") == "Smith"

#     def test_concat_with_empty_surname(self):
#         assert NameUtils.concat("John", "") == "John"

#     def test_concat_with_both_empty(self):
#         assert NameUtils.concat("", "") == ""

#     def test_concat_with_spaces_in_names(self):
#         assert NameUtils.concat("Jean Baptiste", "de La Fontaine") == "Jean Baptiste de La Fontaine"

#     def test_concat_with_leading_space_in_first_name(self):
#         assert NameUtils.concat(" John", "Smith") == "John Smith"

#     def test_concat_with_trailing_space_in_surname(self):
#         assert NameUtils.concat("John", "Smith ") == "John Smith"

#     def test_concat_with_spaces_in_both(self):
#         assert NameUtils.concat(" John ", " Smith ") == "John   Smith"


# class TestContainsForbiddenChar:
#     """Tests for contains_forbidden_char method"""

#     def test_contains_forbidden_char_with_colon(self):
#         assert NameUtils.contains_forbidden_char("John:Smith") is True

#     def test_contains_forbidden_char_with_at_sign(self):
#         assert NameUtils.contains_forbidden_char("John@Smith") is True

#     def test_contains_forbidden_char_with_hash(self):
#         assert NameUtils.contains_forbidden_char("John#Smith") is True

#     def test_contains_forbidden_char_with_equals(self):
#         assert NameUtils.contains_forbidden_char("John=Smith") is True

#     def test_contains_forbidden_char_with_dollar(self):
#         assert NameUtils.contains_forbidden_char("John$Smith") is True

#     def test_contains_forbidden_char_with_no_forbidden_chars(self):
#         assert NameUtils.contains_forbidden_char("John Smith") is False

#     def test_contains_forbidden_char_with_empty_string(self):
#         assert NameUtils.contains_forbidden_char("") is False

#     def test_contains_forbidden_char_with_hyphen_allowed(self):
#         assert NameUtils.contains_forbidden_char("Jean-Baptiste") is False

#     def test_contains_forbidden_char_with_apostrophe_allowed(self):
#         assert NameUtils.contains_forbidden_char("O'Brien") is False

#     def test_contains_forbidden_char_with_multiple_forbidden(self):
#         assert NameUtils.contains_forbidden_char("John:@#=$Smith") is True


# class TestSplitNameInternal:
#     """Tests for _split_name_internal method"""

#     def test_split_name_internal_on_spaces(self):
#         result = NameUtils._split_name_internal("John Paul Smith", " ")
#         assert result == ["John", "Paul", "Smith"]

#     def test_split_name_internal_on_hyphens(self):
#         result = NameUtils._split_name_internal("Jean-Baptiste", "-")
#         assert result == ["Jean", "Baptiste"]

#     def test_split_name_internal_on_spaces_and_hyphens(self):
#         result = NameUtils._split_name_internal("Jean-Baptiste de Paris", " -")
#         assert result == ["Jean", "Baptiste", "de", "Paris"]

#     def test_split_name_internal_with_single_word(self):
#         result = NameUtils._split_name_internal("John", " ")
#         assert result == ["John"]

#     def test_split_name_internal_with_empty_string(self):
#         result = NameUtils._split_name_internal("", " ")
#         assert result == []

#     def test_split_name_internal_with_leading_separator(self):
#         result = NameUtils._split_name_internal(" John", " ")
#         assert result == ["", "John"]

#     def test_split_name_internal_with_trailing_separator(self):
#         result = NameUtils._split_name_internal("John ", " ")
#         assert result == ["John", ""]

#     def test_split_name_internal_with_multiple_consecutive_separators(self):
#         result = NameUtils._split_name_internal("John  Smith", " ")
#         assert result == ["John", "", "Smith"]

#     def test_split_name_internal_with_callback(self):
#         positions = []
        
#         def callback(pos, length):
#             positions.append((pos, length))
        
#         NameUtils._split_name_internal("John Smith", " ", callback)
#         assert len(positions) == 2
#         assert positions[0] == (0, 4)  # "John"
#         assert positions[1] == (5, 5)  # "Smith"

#     def test_split_name_internal_with_callback_on_hyphens(self):
#         positions = []
        
#         def callback(pos, length):
#             positions.append((pos, length))
        
#         NameUtils._split_name_internal("Jean-Baptiste", "-", callback)
#         assert len(positions) == 2
#         assert positions[0] == (0, 4)  # "Jean"
#         assert positions[1] == (5, 8)  # "Baptiste"

#     def test_split_name_internal_complex_case(self):
#         result = NameUtils._split_name_internal("van-der Berg-Smith", " -")
#         assert result == ["van", "der", "Berg", "Smith"]

#     def test_split_name_internal_with_only_separators(self):
#         result = NameUtils._split_name_internal("---", "-")
#         assert result == ["", "", "", ""]


# class TestEdgeCases:
#     """Tests for edge cases and integration scenarios"""

#     def test_full_pipeline_complex_name(self):
#         """Test the full normalization pipeline"""
#         original = "Jean-Baptiste de La Fontaine"
#         lowered = NameUtils.lower(original)
#         abbreviated = NameUtils.abbrev(lowered)
#         crushed = NameUtils.abbreviate_name(abbreviated)
        
#         assert isinstance(crushed, str)
#         assert len(crushed) > 0

#     def test_unicode_handling_comprehensive(self):
#         """Test various Unicode characters"""
#         names = ["José", "François", "Müller", "Søren", "Łukasz"]
#         for name in names:
#             result = NameUtils.lower(name)
#             assert isinstance(result, str)
#             assert result.isascii() or result.replace(" ", "").isalnum()

#     def test_empty_string_handling_all_methods(self):
#         """Ensure all methods handle empty strings gracefully"""
#         assert NameUtils.lower("") == ""
#         assert NameUtils.title("") == ""
#         assert NameUtils.abbrev("") == ""
#         assert NameUtils.abbreviate_name("") == ""
#         assert NameUtils.strip_lower("") == ""
#         assert NameUtils.abbreviate_lower("") == ""
#         assert NameUtils.concat("", "") == ""
#         assert NameUtils.contains_forbidden_char("") is False

#     def test_very_long_name(self):
#         """Test with unusually long input"""
#         long_name = "Jean " * 100
#         result = NameUtils.lower(long_name)
#         assert isinstance(result, str)

#     def test_numbers_in_names(self):
#         """Test handling of numbers in various contexts"""
#         assert "14" in NameUtils.lower("Louis XIV")
#         assert "3" in NameUtils.lower("Henry 3")

#     def test_case_preservation_in_title(self):
#         """Test that title case works correctly"""
#         assert NameUtils.title("the lord of the rings") == "The Lord Of The Rings"

#     def test_multiple_particles_abbreviation(self):
#         """Test multiple particles in one name"""
#         result = NameUtils.abbrev("charles de van von zu paris")
#         assert "de" not in result
#         assert "van" not in result
#         assert "von" not in result
#         assert "zu" not in result
#         assert "charles" in result
#         assert "paris" in result