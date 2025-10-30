import unicodedata
import re
from typing import List, Optional, Tuple


class NameUtils:
    """
    Comprehensive name processing and normalization utilities
    for genealogy applications.

    This class provides a sophisticated set of tools for handling
    names in genealogical
    databases, addressing the complexities of:
    - International character sets and Unicode normalization
    - Historical naming conventions and variations
    - Phonetic similarity matching for family tree research
    - Multi-language name particle handling (French, German, Dutch, etc.)
    - Database indexing optimization for efficient name searches

    Note: Converted from OCaml genealogy library, preserving semantic meaning
    while leveraging Python's strengths for string processing and
    Unicode handling.
    """

    # Characters prohibited in names within the genealogy system
    FORBIDDEN_CHARS = [":", "@", "#", "=", "$"]

    # List of abbreviations and particles
    ABBREV_LIST = {
        "a": "",
        "af": "",
        "d": "",
        "de": "",
        "di": "",
        "ier": "i",
        "of": "",
        "saint": "st",
        "sainte": "ste",
        "van": "",
        "von": "",
        "zu": "",
        "zur": "",
    }

    @staticmethod
    def unaccent_utf_8(
        s: str, start_pos: int = 0, to_lower: bool = True
    ) -> Tuple[str, int]:
        """
        Remove accents from UTF-8 characters and optionally
        convert to lowercase.

        Args:
            s: String to process
            start_pos: Starting position in string
            to_lower: Whether to convert to lowercase

        Returns:
            Tuple of (processed_string, next_position)
        """
        if start_pos >= len(s):
            return ("", start_pos)

        # Get the character at start_pos
        char = s[start_pos]

        # Remove accents using Unicode normalization
        normalized = unicodedata.normalize("NFD", char)
        unaccented = "".join(
            c for c in normalized if unicodedata.category(c) != "Mn"
        )

        if to_lower:
            unaccented = unaccented.lower()

        return (unaccented, start_pos + 1)

    @staticmethod
    def next_chars_if_equiv(
        s: str, i: int, t: str, j: int
    ) -> Optional[Tuple[int, int]]:
        """
        Compare characters at positions, ignoring accents and case.

        Returns:
            Some (next_i, next_j) if equivalent, None otherwise
        """
        if i >= len(s) or j >= len(t):
            return None

        s1, i1 = NameUtils.unaccent_utf_8(s, i, True)
        t1, j1 = NameUtils.unaccent_utf_8(t, j, True)

        if s1 == t1:
            return (i1, j1)
        return None

    @staticmethod
    def lower(s: str) -> str:
        """
        Primary normalization function for name comparison.

        Transformations:
        - Converts to lowercase
        - Removes accents
        - Keeps only letters, numbers, and dots
        - Converts non-alphanumeric chars to spaces
        - Strips leading/trailing spaces
        """
        if not s:
            return ""

        # Remove accents using Unicode normalization
        normalized = unicodedata.normalize("NFD", s)
        unaccented = "".join(
            c for c in normalized if unicodedata.category(c) != "Mn"
        )

        # Convert to lowercase
        lowered = unaccented.lower()

        # Replace non-alphanumeric chars (except dots) with spaces
        cleaned = re.sub(r"[^a-z0-9.]+", " ", lowered)

        # Strip leading/trailing spaces, normalize multiple spaces into one
        return re.sub(r"\s+", " ", cleaned).strip()

    @staticmethod
    def title(s: str) -> str:
        """
        Convert string to title case (first letter of each word capitalized).
        """
        if not s:
            return ""

        result = []
        capitalize_next = True

        for char in s:
            if char.isalpha():
                result.append(
                    char.upper() if capitalize_next else char.lower()
                )
                capitalize_next = False
            else:
                result.append(char)
                capitalize_next = True

        return "".join(result)

    @staticmethod
    def abbrev(s: str) -> str:
        """
        Apply abbreviation rules to entire string.

        Process word by word, replacing or removing based on ABBREV_LIST.
        """
        if not s:
            return ""

        words: List[str] = s.split(" ")

        for i, word in enumerate(words):
            abbreviation_word = NameUtils.ABBREV_LIST.get(word.lower(), word)
            if abbreviation_word and word[0].isupper():
                abbreviation_word = (
                    abbreviation_word[0].upper() + abbreviation_word[1:]
                )
            words[i] = abbreviation_word
        return " ".join(filter(None, words))

    @staticmethod
    def roman_number(s: str, pos: int) -> Optional[int]:
        """
        Detect Roman numerals in string starting at position.

        Args:
            s: String to search
            pos: Starting position

        Returns:
            Next position after Roman numeral if found, None otherwise
        """
        if pos != 0 and s[pos - 1] != " " or not s:
            return None

        i = pos
        while i < len(s) and s[i].lower() in "ivxl":
            i += 1

        if i == len(s) or s[i] == " ":
            return i

        return None

    @staticmethod
    def abbreviate_name(s: str) -> str:
        """
        Advanced phonetic normalization (custom Soundex-like algorithm).

        Algorithm:
        1. Preserves Roman numerals
        2. Vowel handling: Removes vowels except first vowel of words (→ 'e')
        3. Character replacements: k/q→c, y→i, z→s
        4. Special rules: ph→f, removes standalone 'h',
        removes 's' at word endings
        5. Eliminates double consonants
        """
        if not s:
            return ""

        result = []

        def _replace_match_case(regex: str, char: str, s: str) -> str:
            def rep(match: re.Match):
                return (
                    char.capitalize() if match.group(0)[0].isupper() else char
                )

            return re.sub(
                rf"{regex}",
                rep,
                s,
                flags=re.IGNORECASE,
            )

        words = s.split(" ")

        for word in words:
            if not word:
                continue
            if NameUtils.roman_number(word, 0) is not None:
                result.append(word)
                continue
            if word and word[0].lower() in "aeiouy":
                word = ("e" if word[0].islower() else "E") + word[1:]
            word = word[0] + _replace_match_case(
                r"[aeiouyAEIOUY]", "", word[1:]
            )
            word = _replace_match_case(r"(ph|Ph)", "f", word)
            word = _replace_match_case(r"[kqKQ]", "c", word)
            word = _replace_match_case(r"[yY]", "i", word)
            word = _replace_match_case(r"[zZ]", "s", word)
            word = word.replace("h", "")
            word = re.sub(r"s\b", "", word)
            word = re.sub(
                r"([bcdfghjklmnpqrtvwxyz])\1+",
                r"\1",
                word,
                flags=re.IGNORECASE,
            )
            result.append(word)

        return "".join(result)

    @staticmethod
    def strip_lower(s: str) -> str:
        """
        Combined normalization: strip(lower(s)).

        Primary name comparison in genealogy system.
        """
        return NameUtils.lower(s).replace(" ", "")

    @staticmethod
    def abbreviate_lower(s: str) -> str:
        """
        Advanced normalization: crush(abbrev(lower(s))).

        Secondary name comparison for fuzzy matching.
        Used for name indexing in database.
        """
        return NameUtils.abbreviate_name(NameUtils.abbrev(NameUtils.lower(s)))

    @staticmethod
    def concat(first_name: str, surname: str) -> str:
        """
        Efficiently concatenate first name and surname with space.

        Args:
            first_name: First name
            surname: Surname

        Returns:
            Concatenated name with space separator
        """
        return f"{first_name.strip()} {surname.strip()}".strip()

    @staticmethod
    def contains_forbidden_char(s: str) -> bool:
        """
        Check if string contains any forbidden characters.

        Args:
            s: String to check

        Returns:
            True if any forbidden character is found
        """
        return any(char in s for char in NameUtils.FORBIDDEN_CHARS)
