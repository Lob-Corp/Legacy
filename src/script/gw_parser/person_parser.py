"""Person and name parsing functions.

Handles parsing of person references, names, and full person definitions.
"""

from typing import List, Tuple, Sequence, Optional

from libraries.person import Person, Sex
from libraries.title import (
    AccessRight,
    Title,
    TitleName,
    NoTitle,
    UseMainTitle
)
from libraries.death_info import (
    BurialInfoBase,
    Burial,
    Cremated,
    DeathStatusBase,
    DontKnowIfDead,
    DeadYoung,
    OfCourseDead,
    DeadDontKnowWhen,
    Dead,
    DeathReason,
    UnknownBurial,
)

from .data_types import Key, Somebody, SomebodyDefined, SomebodyUndefined
from .utils import cut_space
from .date_parser import date_of_string_py, CompressedDate


def parse_first_name(tokens: Sequence[str]) -> Tuple[str, int, List[str]]:
    """Parse first name token, extracting occurrence number if present.

    Args:
        tokens: Token sequence starting with first name

    Returns:
        Tuple of (first_name, occurrence, remaining_tokens)
    """
    if not tokens:
        raise ValueError("Expected first name token")
    token = tokens[0]
    occ = 0
    # occurrence suffix pattern name[n]
    if '[' in token and token.endswith(']'):
        base, occ_str = token.rsplit('[', 1)
        occ_str = occ_str[:-1]
        if occ_str.isdigit():
            occ = int(occ_str)
            token = base
    return cut_space(token), occ, list(tokens[1:])


def parse_name(tokens: Sequence[str]) -> Tuple[str, List[str]]:
    """Parse surname token.

    Args:
        tokens: Token sequence

    Returns:
        Tuple of (surname, remaining_tokens)
    """
    if not tokens:
        return "", []
    t0 = tokens[0]
    if t0.startswith(('{', '#')):
        return "", list(tokens)
    return cut_space(t0), list(tokens[1:])


def parse_person_ref(tokens: Sequence[str]
                     ) -> Tuple[Somebody, str, int, List[str]]:
    """Parse a person reference (surname + first name + occurrence).

    Args:
        tokens: Token sequence

    Returns:
        Tuple of (Somebody, surname, occurrence, remaining_tokens)
    """
    surname, tokens = parse_name(tokens)
    first, occ, tokens = parse_first_name(tokens)
    if first == "?" or surname == "?":
        # unknown person placeholder
        key = Key(first, surname, occ)
        return SomebodyUndefined(key), surname, occ, tokens
    key = Key(first, surname, occ)
    return SomebodyUndefined(key), surname, occ, tokens


def parse_parent(
    tokens: Sequence[str],
    default_sex: Sex = Sex.NEUTER
) -> Tuple[Somebody, str, int, List[str]]:
    """Parse a parent in a family line (may have inline definition).

    Similar to OCaml's parse_parent function. Checks if the person is:
    - Just a reference (next token is '+' or end of line) → Undefined
    - Has inline attributes (dates, places, etc.) → Defined with full Person

    Args:
        tokens: Token sequence
        default_sex: Default sex if not specified (usually Male/Female)

    Returns:
        Tuple of (Somebody, surname, occurrence, remaining_tokens)
    """
    surname, tokens = parse_name(tokens)
    first, occ, tokens = parse_first_name(tokens)

    if first == "?" or surname == "?":
        key = Key(first, surname, occ)
        return SomebodyUndefined(key), surname, occ, tokens

    # Check if this is just a reference (not an inline definition)
    # A person is considered "defined inline" if there are more tokens
    # AND the next token doesn't start with '+' (marriage indicator)
    defined_inline = False
    if tokens:
        next_token = tokens[0]
        if next_token.startswith('+'):
            defined_inline = False
        else:
            defined_inline = True

    if not defined_inline:
        key = Key(first, surname, occ)
        return SomebodyUndefined(key), surname, occ, tokens
    else:
        person, tokens = build_person(first, surname, occ, default_sex, tokens)
        return SomebodyDefined(person), surname, occ, tokens


def _parse_first_names_aliases(
        tokens: List[str]) -> Tuple[List[str], List[str]]:
    """Parse first name aliases (tokens in {braces})."""
    aliases: List[str] = []
    while tokens and tokens[0].startswith('{') and tokens[0].endswith('}'):
        raw = tokens.pop(0)
        aliases.append(cut_space(raw[1:-1]))
    return aliases, tokens


def _parse_surname_aliases(tokens: List[str]) -> Tuple[List[str], List[str]]:
    """Parse surname aliases (#salias tokens)."""
    res: List[str] = []
    while len(tokens) >= 2 and tokens[0] == '#salias':
        res.append(cut_space(tokens[1]))
        tokens = tokens[2:]
    return res, tokens


def _parse_listed(
        label: str, tokens: List[str]) -> Tuple[List[str], List[str]]:
    """Parse list of labeled values (e.g., #nick, #alias)."""
    res: List[str] = []
    while len(tokens) >= 2 and tokens[0] == label:
        res.append(cut_space(tokens[1]))
        tokens = tokens[2:]
    return res, tokens


def _parse_titles(tokens: List[str]) -> Tuple[List[Title[str]], List[str]]:
    """Parse title tokens ([title:ident:place:start:end:nth])."""
    titles: List[Title[str]] = []
    while tokens and tokens[0].startswith('[') and tokens[0].endswith(']'):
        body = tokens.pop(0)[1:-1]
        # scan_title replicate: name:title:place:date_start:date_end:nth
        parts: List[str] = []
        cur = ''
        esc = False
        for ch in body:
            if esc:
                cur += ch
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == ':':
                parts.append(cur)
                cur = ''
            else:
                cur += ch
        parts.append(cur)
        while len(parts) < 6:
            parts.append('')
        raw_name, ident, place, d_start, d_end, nth = parts[:6]

        tname: TitleName[str] | NoTitle | UseMainTitle
        if raw_name == '':
            tname = NoTitle()
        elif raw_name == '*':
            tname = UseMainTitle()
        else:
            tname = TitleName(raw_name)

        try:
            ds = date_of_string_py(d_start, 0) if d_start else None
        except Exception:
            ds = None
        try:
            de = date_of_string_py(d_end, 0) if d_end else None
        except Exception:
            de = None
        try:
            nth_i = int(nth) if nth else 0
        except ValueError:
            nth_i = 0

        titles.append(
            Title(
                title_name=tname,
                ident=ident,
                place=place,
                date_start=ds,
                date_end=de,
                nth=nth_i))
    return titles, tokens


def _parse_access(tokens: List[str]) -> Tuple[AccessRight, List[str]]:
    """Parse access right tokens (#apubl, #apriv)."""
    if tokens and tokens[0] in ('#apubl', '#apriv'):
        tag = tokens.pop(0)
        if tag == '#apubl':
            return AccessRight.PUBLIC, tokens
        return AccessRight.PRIVATE, tokens
    return AccessRight.IFTITLES, tokens


def _parse_optional_date_prefixed(
        tokens: List[str],
        bang_means_none: bool = True) -> Tuple[CompressedDate, List[str]]:
    """Parse optional date from tokens with optional ! prefix."""
    if not tokens:
        return None, tokens
    head = tokens[0]
    if bang_means_none and head.startswith('!'):
        return None, tokens
    if head and (head[0] in '~?<>-' or head[0].isdigit()):
        try:
            dt = date_of_string_py(head, 0)
            return dt, tokens[1:]
        except Exception:
            return None, tokens
    return None, tokens


def build_person(first: str, surname: str, occ: int, sex: Sex,
                 tokens: List[str]) -> Tuple[Person[int, int, str], List[str]]:
    """Build a complete Person object from tokens.

    Parses all person fields in sequence: aliases, titles, access rights,
    occupation, sources, birth info, baptism info, death info, burial info.

    Args:
        first: First name
        surname: Surname
        occ: Occurrence number
        sex: Sex
        tokens: Remaining tokens to parse

    Returns:
        Tuple of (Person, remaining_tokens)
    """
    first_aliases, tokens = _parse_first_names_aliases(tokens)
    surname_aliases, tokens = _parse_surname_aliases(tokens)

    public_name = ''
    if tokens and tokens[0].startswith('(') and tokens[0].endswith(')'):
        public_name = cut_space(tokens[0][1:-1])
        tokens = tokens[1:]

    image = ''
    if len(tokens) >= 2 and tokens[0] in ('#image', '#photo'):
        image = cut_space(tokens[1])
        tokens = tokens[2:]

    qualifiers, tokens = _parse_listed('#nick', tokens)
    aliases, tokens = _parse_listed('#alias', tokens)
    titles, tokens = _parse_titles(tokens)
    access, tokens = _parse_access(tokens)

    occupation = ''
    if len(tokens) >= 2 and tokens[0] == '#occu':
        occupation = cut_space(tokens[1])
        tokens = tokens[2:]

    person_sources = ''
    if len(tokens) >= 2 and tokens[0] == '#src':
        person_sources = cut_space(tokens[1])
        tokens = tokens[2:]

    birth_date, tokens = _parse_optional_date_prefixed(tokens)
    birth_place = ''
    if len(tokens) >= 2 and tokens[0] == '#bp':
        birth_place = cut_space(tokens[1])
        tokens = tokens[2:]
    birth_note = ''
    if len(tokens) >= 2 and tokens[0] == '#bn':
        birth_note = cut_space(tokens[1])
        tokens = tokens[2:]
    birth_src = ''
    if len(tokens) >= 2 and tokens[0] == '#bs':
        birth_src = cut_space(tokens[1])
        tokens = tokens[2:]

    baptism_date, tokens = _parse_optional_date_prefixed(
        tokens, bang_means_none=False)
    baptism_place = ''
    if len(tokens) >= 2 and tokens[0] == '#pp':
        baptism_place = cut_space(tokens[1])
        tokens = tokens[2:]
    baptism_note = ''
    if len(tokens) >= 2 and tokens[0] == '#pn':
        baptism_note = cut_space(tokens[1])
        tokens = tokens[2:]
    baptism_src = ''
    if len(tokens) >= 2 and tokens[0] == '#ps':
        baptism_src = cut_space(tokens[1])
        tokens = tokens[2:]

    death: DeathStatusBase = DontKnowIfDead()
    if tokens:
        code = tokens[0]
        if code in ('?', 'mj', 'od') or code and code[0] in 'kmes':
            tok = tokens.pop(0)
            if tok == '?':
                death = DontKnowIfDead()
            elif tok == 'mj':
                death = DeadYoung()
            elif tok == 'od':
                death = OfCourseDead()
            else:
                reason_map = {
                    'k': DeathReason.KILLED,
                    'm': DeathReason.MURDERED,
                    'e': DeathReason.EXECUTED,
                    's': DeathReason.DISAPPEARED}
                reason = reason_map.get(tok[0], DeathReason.UNSPECIFIED)
                if len(tok) > 1:
                    try:
                        ddt = date_of_string_py(tok[1:])
                        death = Dead(reason, ddt)
                    except Exception:
                        death = DeadDontKnowWhen()
                else:
                    death = DeadDontKnowWhen()

    death_place = ''
    if len(tokens) >= 2 and tokens[0] == '#dp':
        death_place = cut_space(tokens[1])
        tokens = tokens[2:]
    death_note = ''
    if len(tokens) >= 2 and tokens[0] == '#dn':
        death_note = cut_space(tokens[1])
        tokens = tokens[2:]
    death_src = ''
    if len(tokens) >= 2 and tokens[0] == '#ds':
        death_src = cut_space(tokens[1])
        tokens = tokens[2:]

    burial: BurialInfoBase = UnknownBurial()
    if tokens and tokens[0] in ('#buri', '#crem'):
        tag = tokens.pop(0)
        maybe_date: Optional[CompressedDate] = None
        if tokens and (tokens[0][0] in '~?<>-' or tokens[0][0].isdigit()):
            try:
                maybe_date = date_of_string_py(tokens[0])
                tokens = tokens[1:]
            except Exception:
                maybe_date = None
        if tag == '#buri':
            burial = Burial(maybe_date)
        else:
            burial = Cremated(maybe_date)

    burial_place = ''
    if len(tokens) >= 2 and tokens[0] == '#rp':
        burial_place = cut_space(tokens[1])
        tokens = tokens[2:]
    burial_note = ''
    if len(tokens) >= 2 and tokens[0] == '#rn':
        burial_note = cut_space(tokens[1])
        tokens = tokens[2:]
    burial_src = ''
    if len(tokens) >= 2 and tokens[0] == '#rs':
        burial_src = cut_space(tokens[1])
        tokens = tokens[2:]

    person: Person[int, int, str] = Person(
        index=-1,
        first_name=first,
        surname=surname,
        occ=occ,
        image=image,
        public_name=public_name,
        qualifiers=qualifiers,
        aliases=aliases,
        first_names_aliases=first_aliases,
        surname_aliases=surname_aliases,
        titles=titles,
        non_native_parents_relation=[],
        related_persons=[],
        occupation=occupation,
        sex=sex,
        access_right=access,
        birth_date=birth_date,
        birth_place=birth_place,
        birth_note=birth_note,
        birth_src=birth_src,
        baptism_date=baptism_date,
        baptism_place=baptism_place,
        baptism_note=baptism_note,
        baptism_src=baptism_src,
        death=death,
        death_place=death_place,
        death_note=death_note,
        death_src=death_src,
        burial=burial,
        burial_place=burial_place,
        burial_note=burial_note,
        burial_src=burial_src,
        personal_events=[],
        notes=person_sources,
        src=person_sources,
    )
    return person, tokens
