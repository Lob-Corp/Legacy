from __future__ import annotations
from libraries.date import (
    CompressedDate,
    Calendar,
    DateValue,
    CalendarDate,
    Sure,
    About,
    Maybe,
    Before,
    After,
    OrYear,
    YearInt,
    PrecisionBase,
)

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Any, Iterable, Iterator, Union, Sequence, Callable, Deque, cast
from collections import deque

# NOTE: We assume the following existing modules provide the Python translations of
# OCaml Def / Adef domain model. If some names differ, adjust imports
# accordingly.
from libraries.person import Person, Sex, PersonDescriptorT, PersonT
from libraries.family import (
    Family,
    Parents,
    Relation,
    RelationToParentType,
    MaritalStatus,
    NotDivorced,
    Divorced,
    Separated,
    DivorceStatusBase,
)
from libraries.title import Title, AccessRight
from libraries.death_info import DeathStatusBase, BurialInfoBase, NotDead, UnknownBurial
from libraries.events import (
    FamilyEvent,
    PersonalEvent,
    EventWitnessKind,
    FamMarriage,
    FamNoMarriage,
    FamNoMention,
    FamEngage,
    FamDivorce,
    FamSeparated,
    FamAnnulation,
    FamMarriageBann,
    FamMarriageContract,
    FamMarriageLicense,
    FamPACS,
    FamResidence,
    FamNamedEvent,
    PersBirth,
    PersBaptism,
    PersDeath,
    PersBurial,
    PersCremation,
    PersAccomplishment,
    PersAcquisition,
    PersAdhesion,
    PersDecoration,
    PersBaptismLDS,
    PersBarMitzvah,
    PersBatMitzvah,
    PersBenediction,
    PersRecensement,
    PersChangeName,
    PersCircumcision,
    PersConfirmation,
    PersConfirmationLDS,
    PersDiploma,
    PersDemobilisationMilitaire,
    PersDistinction,
    PersDotationLDS,
    PersDotation,
    PersEducation,
    PersElection,
    PersEmigration,
    PersExcommunication,
    PersFirstCommunion,
    PersFamilyLinkLDS,
    PersFuneral,
    PersGraduate,
    PersHospitalisation,
    PersIllness,
    PersImmigration,
    PersListePassenger,
    PersMilitaryDistinction,
    PersMobilisationMilitaire,
    PersMilitaryPromotion,
    PersMilitaryService,
    PersNaturalisation,
    PersOccupation,
    PersOrdination,
    PersProperty,
    PersResidence,
    PersRetired,
    PersScellentChildLDS,
    PersScellentParentLDS,
    PersScellentSpouseLDS,
    PersVenteBien,
    PersWill,
    PersNamedEvent,
)

# ---------------------------------------------------------------------------
# Child parsing helpers (port of OCaml parse_child logic)
# ---------------------------------------------------------------------------
def _parse_child_line(
    line_tokens: List[str],
    default_surname: str,
    default_sex: Sex,
    common_src: str,
    common_birth_place: str,
) -> Tuple[Person[int, int, str], str]:
    """Parse a child definition line (tokens after '-').

    Returns (person, surname_used).
    Implements surname fallback similar to OCaml parse_child.
    Minimal fields populated; life events unparsed at this stage.
    """
    toks = list(line_tokens)
    first, occ, toks = parse_first_name(toks)
    surname = default_surname
    if toks:
        head = toks[0]
        if head == '?':
            toks = toks[1:]
            if toks:
                surname, toks = parse_name(toks)
        else:
            c0 = head[0]
            # characters that indicate no explicit surname token present
            boundary = set('<>!?~-0123456789{#([')
            if c0 not in boundary:
                surname, toks = parse_name(toks)
    # Construct Person using dataclass fields order from libraries.person.Person
    person: Person[int, int, str] = Person(
        index=-1,
        first_name=first,
        surname=surname,
        occ=occ,
        image='',
        public_name='',
        qualifiers=[],
        aliases=[],
        first_names_aliases=[],
        surname_aliases=[],
        titles=[],
        non_native_parents_relation=[],
        related_persons=[],
        occupation='',
        sex=default_sex,
        access_right=AccessRight.PUBLIC,
        birth_date=None,
        birth_place=common_birth_place,
        birth_note='',
        birth_src=common_src,
        baptism_date=None,
        baptism_place='',
        baptism_note='',
        baptism_src='',
        death=NotDead(),
        death_place='',
        death_note='',
        death_src='',
        burial=UnknownBurial(),
        burial_place='',
        burial_note='',
        burial_src='',
        personal_events=[],
        notes='',
        src='',
    )
    return person, surname

magic_gwo = "GnWo000o"
create_all_keys: bool = False


@dataclass(frozen=True)
class Key:
    pk_first_name: str
    pk_surname: str
    pk_occ: int = 0


class Somebody:  # sum type wrapper
    pass


@dataclass(frozen=True)
class SomebodyUndefined(Somebody):
    key: Key


@dataclass(frozen=True)
class SomebodyDefined(Somebody):
    person: Person[int, int, str]


class GwSyntax:  # root variant marker
    pass


@dataclass(frozen=True)
class FamilyGwSyntax(GwSyntax):
    couple: Parents[Somebody]
    father_sex: Sex
    mother_sex: Sex
    witnesses: List[Tuple[Somebody, Sex]]
    events: List[Tuple[FamilyEvent[Somebody, str], List[Sex]]]
    family: Family[int, Person[int, int, str], str]
    descend: List[Person[int, int, str]]


@dataclass(frozen=True)
class NotesGwSyntax(GwSyntax):
    key: Key
    content: str


@dataclass(frozen=True)
class RelationsGwSyntax(GwSyntax):
    person: Somebody
    sex: Sex
    relations: List[Relation[Somebody, str]]  # descriptor type assumed str


@dataclass(frozen=True)
class PersonalEventsGwSyntax(GwSyntax):
    person: Somebody
    sex: Sex
    events: List[PersonalEvent[Somebody, str]]


@dataclass(frozen=True)
class BaseNotesGwSyntax(GwSyntax):
    page: str  # "" = base notes
    content: str


@dataclass(frozen=True)
class WizardNotesGwSyntax(GwSyntax):
    wizard_id: str
    content: str


# ---------------- Parsing Helpers (Translation of selected OCaml helpers) ---------------- #


def copy_decode(s: str, i1: int, i2: int) -> str:
    """Decode word slice, translating '\\x' (escaped) and '_' -> ' '.
    In the OCaml code: replaces "\\" sequences and underscores. Here we simplify:
    - backslash followed by any char copies that char
    - '_' becomes space
    """
    out: List[str] = []
    i = i1
    while i < i2:
        c = s[i]
        if c == '\\' and i + 1 < i2:
            out.append(s[i + 1])
            i += 2
            continue
        if c == '_':
            out.append(' ')
        else:
            out.append(c)
        i += 1
    return ''.join(out)


def fields(line: str) -> List[str]:
    tokens: List[str] = []
    n = len(line)
    i = 0
    while i < n:
        while i < n and line[i] in (' ', '\t'):
            i += 1
        if i >= n:
            break
        start = i
        while i < n and line[i] not in (' ', '\t'):
            i += 1
        tokens.append(copy_decode(line, start, i))
    return tokens


def cut_space(x: str) -> str:
    return x.strip()


def get_field(label: str, tokens: Sequence[str]) -> Tuple[str, List[str]]:
    if len(tokens) >= 2 and tokens[0] == label:
        return cut_space(tokens[1]), list(tokens[2:])
    return "", list(tokens)


def _strip_trailing_spaces(text: str) -> str:
    # Approximate Mutil.strip_all_trailing_spaces
    lines = text.split('\n')
    cleaned = [ln.rstrip(' \t') for ln in lines]
    # Remove trailing empty lines
    while cleaned and cleaned[-1] == '':
        cleaned.pop()
    return '\n'.join(cleaned)


def date_of_string_py(s: str, start: int = 0) -> Optional[CompressedDate]:
    """Faithful port of OCaml date_of_string (minus calendar conversions for non-gregorian).
    Returns CalendarDate or textual date (str) or None.
    """
    i_ref = start

    def champ(i: int) -> tuple[int, int]:
        neg = False
        if i < len(s) and s[i] == '-':
            neg = True
            i += 1
        n = 0
        found = False
        while i < len(s) and s[i].isdigit():
            found = True
            n = 10 * n + (ord(s[i]) - 48)
            i += 1
        return (-n if neg else n, i)

    def skip_slash(i: int) -> Optional[int]:
        if i < len(s) and s[i] == '/':
            return i + 1
        return None

    if i_ref >= len(s):
        return None
    # precision
    c = s[i_ref]
    if c == '~':
        precision: PrecisionBase = About()
        i_ref += 1
    elif c == '?':
        precision = Maybe()
        i_ref += 1
    elif c == '>':
        precision = After()
        i_ref += 1
    elif c == '<':
        precision = Before()
        i_ref += 1
    else:
        precision = Sure()

    undefined = False
    year, i_ref2 = champ(i_ref)
    if i_ref2 == i_ref + 1 and s[i_ref] == '0':
        undefined = True
    i_ref = i_ref2

    def error(n: int) -> None:
        raise ValueError(f'date_of_string{n} {s}')

    def dmy2(year2: int, i: int) -> tuple[tuple[int, int, int], int]:
        maybe = skip_slash(i)
        if maybe is not None:
            i = maybe
            month2 = year2
            year2, i = champ(i)
            maybe2 = skip_slash(i)
            if maybe2 is not None:
                i = maybe2
                day2 = month2
                month2 = year2
                year2, i = champ(i)
                if month2 < 1 or month2 > 13:
                    error(2)
                if day2 < 1 or day2 > 31:
                    error(3)
                return (day2, month2, year2), i
            if month2 < 1 or month2 > 13:
                error(4)
            return (0, month2, year2), i
        return (0, 0, year2), i

    date: Optional[tuple[Any, int]]
    maybe = skip_slash(i_ref)
    if maybe is not None:
        i_ref = maybe
        month = year
        year, i_ref = champ(i_ref)
        maybe2 = skip_slash(i_ref)
        if maybe2 is not None:
            i_ref = maybe2
            day = month
            month = year
            year, i_ref = champ(i_ref)
            if month < 1 or month > 13:
                error(2)
            if day < 1 or day > 31:
                error(3)
            dv = DateValue(
                day=day,
                month=month,
                year=year,
                prec=precision,
                delta=0)
            date = (CalendarDate(dv, Calendar.GREGORIAN), i_ref)
        else:
            if year == 0:
                date = None
            elif month < 1 or month > 13:
                error(4)
            else:
                dv = DateValue(
                    day=0,
                    month=month,
                    year=year,
                    prec=precision,
                    delta=0)
                date = (CalendarDate(dv, Calendar.GREGORIAN), i_ref)
    else:
        if undefined:
            if i_ref == len(s):
                date = None
            elif s[i_ref] == '(' and s[-1] == ')':
                inner = s[i_ref + 1: len(s) - 1].strip()
                inner = inner.replace('_', ' ')
                date = (inner, len(s))
            else:
                raise ValueError(f'date_of_string {s}')
        else:
            dv = DateValue(day=0, month=0, year=year, prec=precision, delta=0)
            date = (CalendarDate(dv, Calendar.GREGORIAN), i_ref)

    # OrYear / YearInt
    if date is not None and isinstance(date[0], CalendarDate):
        caldate, idx = date
        if idx < len(s) and s[idx] == '|':
            year2, j = champ(idx + 1)
            (d2, m2, y2), j = dmy2(year2, j)
            dv2 = DateValue(day=d2, month=m2, year=y2, prec=None, delta=0)
            caldate.dmy.prec = OrYear(dv2)  # type: ignore[attr-defined]
            date = (caldate, j)
        elif idx + 1 < len(s) and s[idx:idx + 2] == '..':
            year2, j = champ(idx + 2)
            (d2, m2, y2), j = dmy2(year2, j)
            dv2 = DateValue(day=d2, month=m2, year=y2, prec=None, delta=0)
            caldate.dmy.prec = YearInt(dv2)  # type: ignore[attr-defined]
            date = (caldate, j)

    # Calendar suffix
    if date is not None and isinstance(date[0], CalendarDate):
        caldate, idx = date
        if idx < len(s):
            suf = s[idx]
            if suf == 'G':
                caldate.cal = Calendar.GREGORIAN
                idx += 1
            elif suf == 'J':
                caldate.cal = Calendar.JULIAN
                idx += 1
            elif suf == 'F':
                caldate.cal = Calendar.FRENCH
                idx += 1
            elif suf == 'H':
                caldate.cal = Calendar.HEBREW
                idx += 1
            date = (caldate, idx)
    if date is None:
        return None
    dt, idx = date
    if idx != len(s):
        raise ValueError(f'date_of_string5 {s}')
    return dt


def get_optional_date(
        tokens: Sequence[str]) -> Tuple[Optional[CompressedDate], List[str]]:
    if not tokens:
        return None, []
    t0 = tokens[0]
    if not t0:
        return None, list(tokens)
    if t0[0] in ('~', '?', '<', '>', '-', '0', '1', '2',
                 '3', '4', '5', '6', '7', '8', '9'):
        try:
            dt = date_of_string_py(t0, 0)
            if dt is not None:
                return dt, list(tokens[1:])
        except Exception:
            pass  # fall through if parsing fails
    if t0.startswith('!'):
        # explicit absence retains token (mirrors OCaml returning original
        # list?)
        return None, list(tokens)
    return None, list(tokens)


def parse_first_name(tokens: Sequence[str]) -> Tuple[str, int, List[str]]:
    if not tokens:
        raise ValueError("Expected first name token")
    token = tokens[0]
    occ = 0
    # occurrence suffix pattern name[n]
    if '[' in token and token.endswith(']'):
        base, occ_str = token.rsplit('[', 1)
        occ_str = occ_str[:-1]
        if occ_str.isdigit():  # rely on Python int parsing
            occ = int(occ_str)
            token = base
    return cut_space(token), occ, list(tokens[1:])


def parse_name(tokens: Sequence[str]) -> Tuple[str, List[str]]:
    if not tokens:
        return "", []
    t0 = tokens[0]
    if t0.startswith(('{', '#')):
        return "", list(tokens)
    return cut_space(t0), list(tokens[1:])


def parse_person_ref(tokens: Sequence[str]
                     ) -> Tuple[Somebody, str, int, List[str]]:
    surname, tokens = parse_name(tokens)
    first, occ, tokens = parse_first_name(tokens)
    if first == "?" or surname == "?":
        # unknown person placeholder (treated as definition here)
        key = Key(first, surname, occ)
        return SomebodyUndefined(key), surname, occ, tokens
    # For initial translation we return Undefined (real def requires further
    # parsing)
    key = Key(first, surname, occ)
    return SomebodyUndefined(key), surname, occ, tokens


# ---------------- Person Parsing (full fidelity WIP) ---------------- #

def _parse_first_names_aliases(
        tokens: List[str]) -> Tuple[List[str], List[str]]:
    aliases: List[str] = []
    while tokens and tokens[0].startswith('{') and tokens[0].endswith('}'):
        raw = tokens.pop(0)
        aliases.append(cut_space(raw[1:-1]))
    return aliases, tokens


def _parse_surname_aliases(tokens: List[str]) -> Tuple[List[str], List[str]]:
    res: List[str] = []
    while len(tokens) >= 2 and tokens[0] == '#salias':
        res.append(cut_space(tokens[1]))
        tokens = tokens[2:]
    return res, tokens


def _parse_listed(
        label: str, tokens: List[str]) -> Tuple[List[str], List[str]]:
    # For #nick and #alias (single value each occurrence)
    res: List[str] = []
    while len(tokens) >= 2 and tokens[0] == label:
        res.append(cut_space(tokens[1]))
        tokens = tokens[2:]
    return res, tokens


def _parse_titles(tokens: List[str]) -> Tuple[List[Title[str]], List[str]]:
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
        # title name mapping
        from libraries.title import NoTitle, UseMainTitle, TitleName
        # type: ignore[name-defined]
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
    if tokens and tokens[0] in ('#apubl', '#apriv'):
        tag = tokens.pop(0)
        if tag == '#apubl':
            return AccessRight.PUBLIC, tokens
        return AccessRight.PRIVATE, tokens
    return AccessRight.IFTITLES, tokens


def _parse_optional_date_prefixed(
        tokens: List[str], bang_means_none: bool = True) -> Tuple[Optional[CompressedDate], List[str]]:
    if not tokens:
        return None, tokens
    head = tokens[0]
    if bang_means_none and head.startswith('!'):
        return None, tokens  # keep token per OCaml semantics
    if head and (head[0] in '~?<>-' or head[0].isdigit()):
        try:
            dt = date_of_string_py(head, 0)
            return dt, tokens[1:]
        except Exception:
            return None, tokens
    return None, tokens


def build_person(first: str, surname: str, occ: int, sex: Sex,
                 tokens: List[str]) -> Tuple[Person[int, int, str], List[str]]:
    # Parse sequential fields per OCaml order
    first_aliases, tokens = _parse_first_names_aliases(tokens)
    surname_aliases, tokens = _parse_surname_aliases(tokens)
    # public name ( (xxx) )
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
    if baptism_date is None:
        # may still have '!<date>' pattern handled above
        pass
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
    # death parsing simplified: codes mapping
    from libraries.death_info import (
        DeathStatusBase,
        DeadYoung,
        OfCourseDead,
        DontKnowIfDead,
        DeadDontKnowWhen,
        NotDead,
        Dead,
        DeathReason,
    )
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
    # burial info
    from libraries.death_info import Burial, Cremated, UnknownBurial
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
    # Create person (notes, personal_events left empty; related lists empty
    # for now)
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


# ---------------- Parsing of Blocks ---------------- #


class Encoding(str):
    UTF8 = 'utf-8'
    ISO_8859_1 = 'iso-8859-1'


def iter_non_comment_lines(lines: Iterable[str]) -> Iterator[str]:
    for raw in lines:
        line = raw.rstrip('\r\n')
        if not line or line.startswith('#'):
            continue
        yield line


class LineStream:
    """Lookahead + pushback capable line stream over already pre-filtered lines."""

    def __init__(self, source: Iterator[str]):
        self._src = source
        self._buf: Deque[str] = deque()

    def peek(self) -> Optional[str]:
        if not self._buf:
            try:
                nxt = next(self._src)
            except StopIteration:
                return None
            self._buf.appendleft(nxt)
        return self._buf[0]

    def pop(self) -> Optional[str]:
        if self._buf:
            return self._buf.popleft()
        try:
            return next(self._src)
        except StopIteration:
            return None

    def push_back(self, line: str) -> None:
        self._buf.appendleft(line)

    def __iter__(self) -> 'LineStream':  # pragma: no cover - convenience
        return self

    def __next__(self) -> str:  # pragma: no cover - convenience
        nxt = self.pop()
        if nxt is None:
            raise StopIteration
        return nxt


# ---------------- Event / Relation Name Mappings ---------------- #

_fam_event_map = {
    '#marr': FamMarriage,
    '#nmar': FamNoMarriage,
    '#nmen': FamNoMention,
    '#enga': FamEngage,
    '#div': FamDivorce,
    '#sep': FamSeparated,
    '#anul': FamAnnulation,
    '#marb': FamMarriageBann,
    '#marc': FamMarriageContract,
    '#marl': FamMarriageLicense,
    '#pacs': FamPACS,
    '#resi': FamResidence,
}


def parse_family_event_name(tag: str):
    if tag.startswith('#') and tag not in _fam_event_map:
        # named custom event
        return FamNamedEvent(tag[1:])
    cls = _fam_event_map.get(tag)
    if cls is None:
        raise ValueError(f'Unknown family event tag {tag}')
    return cls()


_pers_event_map = {
    '#birt': PersBirth,
    '#bapt': PersBaptism,
    '#deat': PersDeath,
    '#buri': PersBurial,
    '#crem': PersCremation,
    '#acco': PersAccomplishment,
    '#acqu': PersAcquisition,
    '#adhe': PersAdhesion,
    '#awar': PersDecoration,
    '#bapl': PersBaptismLDS,
    '#barm': PersBarMitzvah,
    '#basm': PersBatMitzvah,
    '#bles': PersBenediction,
    '#cens': PersRecensement,
    '#chgn': PersChangeName,
    '#circ': PersCircumcision,
    '#conf': PersConfirmation,
    '#conl': PersConfirmationLDS,
    '#degr': PersDiploma,
    '#demm': PersDemobilisationMilitaire,
    '#dist': PersDistinction,
    '#dotl': PersDotationLDS,
    '#endl': PersDotation,
    '#educ': PersEducation,
    '#elec': PersElection,
    '#emig': PersEmigration,
    '#exco': PersExcommunication,
    '#fcom': PersFirstCommunion,
    '#flkl': PersFamilyLinkLDS,
    '#fune': PersFuneral,
    '#grad': PersGraduate,
    '#hosp': PersHospitalisation,
    '#illn': PersIllness,
    '#immi': PersImmigration,
    '#lpas': PersListePassenger,
    '#mdis': PersMilitaryDistinction,
    '#mobm': PersMobilisationMilitaire,
    '#mpro': PersMilitaryPromotion,
    '#mser': PersMilitaryService,
    '#natu': PersNaturalisation,
    '#occu': PersOccupation,
    '#ordn': PersOrdination,
    '#prop': PersProperty,
    '#resi': PersResidence,
    '#reti': PersRetired,
    '#slgc': PersScellentChildLDS,
    '#slgp': PersScellentParentLDS,
    '#slgs': PersScellentSpouseLDS,
    '#vteb': PersVenteBien,
    '#will': PersWill,
}


def parse_personal_event_name(tag: str):
    if tag.startswith('#') and tag not in _pers_event_map:
        return PersNamedEvent(tag[1:])
    cls = _pers_event_map.get(tag)
    if cls is None:
        raise ValueError(f'Unknown personal event tag {tag}')
    return cls()


_witness_kind_map = {
    '#godp': EventWitnessKind.WITNESS_GODPARENT,
    '#offi': EventWitnessKind.WITNESS_CIVILOFFICER,
    '#reli': EventWitnessKind.WITNESS_RELIGIOUSOFFICER,
    '#info': EventWitnessKind.WITNESS_INFORMANT,
    '#atte': EventWitnessKind.WITNESS_ATTENDING,
    '#ment': EventWitnessKind.WITNESS_MENTIONED,
    '#othe': EventWitnessKind.WITNESS_OTHER,
}


def parse_witness_kind(
        tokens: Sequence[str]) -> Tuple[EventWitnessKind, List[str]]:
    if tokens and tokens[0] in _witness_kind_map:
        return _witness_kind_map[tokens[0]], list(tokens[1:])
    return EventWitnessKind.WITNESS, list(tokens)


def _parse_marriage_and_relation(
    tokens: List[str],
) -> Tuple[
    MaritalStatus,
    Sex,
    Sex,
    Optional[CompressedDate],
    str,
    str,
    str,
    DivorceStatusBase,
    List[str],
]:
    """Full-fidelity port of OCaml get_mar_date.

    Returns (relation_kind, father_sex, mother_sex, marriage_date, place, note, src, divorce_status, rest_tokens).
    """
    rest = list(tokens)

    marriage_date: Optional[CompressedDate] = None
    relation_kind: MaritalStatus = MaritalStatus.MARRIED
    father_sex: Sex = Sex.MALE
    mother_sex: Sex = Sex.FEMALE
    place = note = src = ""
    divorce_status: DivorceStatusBase = NotDivorced()

    # Marriage indicator '+' possibly followed immediately by date.
    if rest and rest[0].startswith('+'):
        plus_tok = rest.pop(0)
        if len(plus_tok) > 1:
            try:
                marriage_date = date_of_string_py(plus_tok[1:])
            except Exception:
                marriage_date = None

    def decode_override_sexes(candidate: str) -> Tuple[Sex, Sex] | None:
        if len(candidate) != 2:
            return None

        def decode(c: str) -> Sex:
            if c == 'm':
                return Sex.MALE
            if c == 'f':
                return Sex.FEMALE
            if c == '?':
                return Sex.NEUTER
            raise ValueError
        try:
            return decode(candidate[0]), decode(candidate[1])
        except Exception:
            return None

    # Relation tag and optional sex overrides for several tags.
    if rest and rest[0].startswith('#'):
        tag = rest[0]
        tag_map: dict[str, MaritalStatus] = {
            '#nm': MaritalStatus.NOT_MARRIED,
            '#eng': MaritalStatus.ENGAGED,
            '#noment': MaritalStatus.NO_MENTION,
            '#nsck': MaritalStatus.NO_SEXES_CHECK_NOT_MARRIED,
            '#nsckm': MaritalStatus.NO_SEXES_CHECK_MARRIED,
            '#banns': MaritalStatus.MARRIAGE_BANN,
            '#contract': MaritalStatus.MARRIAGE_CONTRACT,
            '#license': MaritalStatus.MARRIAGE_LICENSE,
            '#pacs': MaritalStatus.PACS,
            '#residence': MaritalStatus.RESIDENCE,
        }
        if tag in tag_map:
            relation_kind = tag_map[tag]
            rest.pop(0)
            # Only certain tags allow an immediate two-char sex override token.
            if relation_kind in (
                MaritalStatus.NO_MENTION,
                MaritalStatus.NO_SEXES_CHECK_NOT_MARRIED,
                MaritalStatus.NO_SEXES_CHECK_MARRIED,
                MaritalStatus.MARRIAGE_BANN,
                MaritalStatus.MARRIAGE_CONTRACT,
                MaritalStatus.MARRIAGE_LICENSE,
                MaritalStatus.PACS,
                MaritalStatus.RESIDENCE,
            ) and rest:
                sexes_override = decode_override_sexes(rest[0])
                if sexes_override is not None:
                    father_sex, mother_sex = sexes_override
                    rest.pop(0)

    # Fields (#mp, #mn, #ms)
    def take_field(label: str) -> str:
        nonlocal rest
        if len(rest) >= 2 and rest[0] == label:
            val = rest[1]
            rest = rest[2:]
            return val
        return ""

    place = take_field('#mp')
    note = take_field('#mn')
    src = take_field('#ms')

    # Divorce / separation indicators
    if rest:
        head = rest[0]
        if head.startswith('-'):
            tok = rest.pop(0)
            div_date: Optional[CompressedDate] = None
            if len(tok) > 1:
                try:
                    div_date = date_of_string_py(tok[1:])
                except Exception:
                    div_date = None
            # If date absent, pass None (represents cdate_None)
            divorce_status = Divorced(div_date)
        elif head == '#sep':
            rest.pop(0)
            divorce_status = Separated()

    return (
        relation_kind,
        father_sex,
        mother_sex,
        marriage_date,
        place,
        note,
        src,
        divorce_status,
        rest,
    )


def _parse_event_witness_lines(
        stream: LineStream) -> Tuple[List[Tuple[Somebody, Sex, EventWitnessKind]], Optional[str]]:
    witnesses: List[Tuple[Somebody, Sex, EventWitnessKind]] = []
    while True:
        nxt = stream.peek()
        if nxt is None:
            return witnesses, None
        f = fields(nxt)
        if not f or f[0] not in ('wit', 'wit:'):
            return witnesses, nxt
        # consume line
        stream.pop()
        toks = f[1:]
        sex = Sex.NEUTER
        if toks and toks[0] in ('m:', 'f:'):
            sex = Sex.MALE if toks[0] == 'm:' else Sex.FEMALE
            toks = toks[1:]
        wk, toks = parse_witness_kind(toks)
        somebody, _, _, _ = parse_person_ref(toks)
        witnesses.append((somebody, sex, wk))
    # unreachable


def _parse_event_notes(stream: LineStream) -> Tuple[str, Optional[str]]:
    notes_parts: List[str] = []
    while True:
        nxt = stream.peek()
        if nxt is None:
            break
        f = fields(nxt)
        if not f or f[0] != 'note':
            break
        # consume
        line = stream.pop()
        assert line is not None
        if len(line) > len('note '):
            notes_parts.append(line[len('note '):])
    return '\n'.join(notes_parts), stream.peek()


def _parse_family_events(
        stream: LineStream) -> List[Tuple[FamilyEvent[Somebody, str], List[Sex]]]:
    events: List[Tuple[FamilyEvent[Somebody, str], List[Sex]]] = []
    # first line already consumed: 'fevt' header; events follow until 'end
    # fevt'
    while True:
        nxt = stream.pop()
        if nxt is None:
            break
        if nxt.strip() == 'end fevt':
            break
        f = fields(nxt)
        if not f:
            continue
        name_token = f[0]
        name = parse_family_event_name(name_token)
        toks = f[1:]
        date_opt, toks = get_optional_date(toks)
        place, toks = get_field('#p', toks)
        reason, toks = get_field('#c', toks)
        src, toks = get_field('#s', toks)
        if toks:
            raise ValueError(f"Unparsed tokens in family event line: {toks}")
        witnesses, _next_start = _parse_event_witness_lines(stream)
        notes, _ = _parse_event_notes(stream)
        sexes = [w[1] for w in witnesses]
        evt = FamilyEvent(
            name=name,
            date=date_opt or '',  # empty placeholder
            place=place,
            reason=reason,
            note=notes,
            src=src,
            witnesses=[(w[0], w[2]) for w in witnesses],
        )
        events.append((evt, sexes))
    return events


def _parse_personal_events(
        stream: LineStream) -> List[PersonalEvent[Somebody, str]]:
    events: List[PersonalEvent[Somebody, str]] = []
    while True:
        nxt = stream.pop()
        if nxt is None:
            break
        if nxt.strip() == 'end pevt':
            break
        f = fields(nxt)
        if not f:
            continue
        name_token = f[0]
        name = parse_personal_event_name(name_token)
        toks = f[1:]
        date_opt, toks = get_optional_date(toks)
        place, toks = get_field('#p', toks)
        reason, toks = get_field('#c', toks)
        src, toks = get_field('#s', toks)
        witnesses, _ = _parse_event_witness_lines(stream)
        notes, _ = _parse_event_notes(stream)
        if toks:
            raise ValueError(f"Unparsed tokens in personal event line: {toks}")
        evt = PersonalEvent(
            name=name,
            date=date_opt or '',  # empty placeholder
            place=place,
            reason=reason,
            note=notes,
            src=src,
            witnesses=[(w[0], w[2]) for w in witnesses],
        )
        events.append(evt)
    return events


def parse_family_block(
        first_line_fields: List[str],
        stream: LineStream) -> FamilyGwSyntax:
    tokens = first_line_fields[1:]  # drop 'fam'
    father, _, _, tokens = parse_person_ref(tokens)
    relation_kind, fath_sex, moth_sex, marriage_date, marr_place, marr_note, marr_src, divorce_status, tokens = _parse_marriage_and_relation(
        tokens)
    mother, _, _, tokens = parse_person_ref(tokens)
    # any residue tokens currently ignored
    parents: Parents[Somebody] = Parents.from_couple(
        father, mother)  # type: ignore
    # After header, parse optional witness lines (block-level witnesses before
    # events)
    witnesses: List[Tuple[Somebody, Sex]] = []
    while True:
        nxt = stream.peek()
        if nxt is None:
            break
        f = fields(nxt)
        if not f or f[0] not in ('wit', 'wit:'):
            break
        line = stream.pop()
        if line is None:
            break
        fline = fields(line)
        toks = fline[1:]
        sex = Sex.NEUTER
        if toks and toks[0] in ('m:', 'f:'):
            sex = Sex.MALE if toks[0] == 'm:' else Sex.FEMALE
            toks = toks[1:]
        somebody, _, _, _ = parse_person_ref(toks)
        witnesses.append((somebody, sex))
    # family source 'src <text>' line
    fam_src = ''
    nxt = stream.peek()
    if nxt:
        f = fields(nxt)
        if f and f[0] == 'src' and len(f) == 2:
            fam_src = f[1]
            stream.pop()
    # common children source 'csrc' and birth place 'cbp'
    common_child_src = ''
    common_child_bp = ''
    for tag in ('csrc', 'cbp'):
        nxt = stream.peek()
        if nxt:
            f = fields(nxt)
            if f and f[0] == tag and len(f) == 2:
                if tag == 'csrc':
                    common_child_src = f[1]
                else:
                    common_child_bp = f[1]
                stream.pop()
    # comment line 'comm <text>'
    comment = ''
    nxt = stream.peek()
    if nxt and nxt.startswith('comm '):
        comment = nxt[5:]
        stream.pop()
    # family events block
    events: List[Tuple[FamilyEvent[Somebody, str], List[Sex]]] = []
    nxt = stream.peek()
    if nxt and nxt.startswith('fevt'):
        # consume header line then parse events until end fevt
        stream.pop()
        events = _parse_family_events(stream)
    # children block parsing
    descend: List[Person[int, int, str]] = []
    nxt = stream.peek()
    if nxt and nxt.strip() == 'beg':
        stream.pop()
        while True:
            line = stream.pop()
            if line is None:
                break
            if line.strip() == 'end':
                break
            f = fields(line)
            if not f or f[0] != '-':
                raise ValueError(f'Invalid child line: {line}')
            toks = f[1:]
            child_sex = Sex.NEUTER
            if toks and toks[0] in ('m:', 'f:'):
                child_sex = Sex.MALE if toks[0] == 'm:' else Sex.FEMALE
                toks = toks[1:]
            # Determine father's surname from Somebody variants if defined
            father_person = None
            first_parent = parents.parents[0]
            if isinstance(first_parent, SomebodyDefined):
                father_person = first_parent.person
            father_surname = father_person.surname if father_person else ''
            child, _ = _parse_child_line(
                toks,
                default_surname=father_surname,
                default_sex=child_sex,
                common_src=common_child_src,
                common_birth_place=common_child_bp,
            )
            descend.append(child)
    family: Family[int, Person[int, int, str], str] = Family(  # type: ignore
        index=-1,
    marriage_date=marriage_date or '',  # empty placeholder
        marriage_place=marr_place,
        marriage_note=marr_note,
        marriage_src=marr_src,
        witnesses=[],  # top-level family witnesses unresolved -> list of Somebody not Person
        relation_kind=relation_kind,
        divorce_status=divorce_status,
        family_events=cast(List[FamilyEvent[Person[int, int, str], str]], [
                           evt for (evt, _) in events]),
        comment=comment,
        origin_file='',
        src=fam_src,
    )
    return FamilyGwSyntax(
        couple=parents,
    father_sex=fath_sex,
    mother_sex=moth_sex,
        witnesses=witnesses,
        events=events,
        family=family,
        descend=descend,
    )


def parse_notes_block(
        fields_line: List[str],
        stream: LineStream) -> NotesGwSyntax:
    # notes FIRST OCC SURNAME ... -> simplified extraction
    tokens = fields_line[1:]
    surname, tokens = parse_name(tokens)
    first, occ, tokens = parse_first_name(tokens)
    key = Key(first, surname, occ)
    # subsequent lines until blank or new block start are concatenated
    # (placeholder)
    content_lines: List[str] = []
    while True:
        nxt = stream.peek()
        if nxt is None:
            break
        if nxt.startswith(('fam ', 'notes', 'rel ', 'pevt ',
                          'notes-db', 'wizard-note', 'page-ext')):
            break
        content_lines.append(stream.pop() or '')
    return NotesGwSyntax(key=key, content='\n'.join(content_lines))


def _parse_relations_block(
        first_line_fields: List[str],
        stream: LineStream) -> RelationsGwSyntax:
    # format: rel <person> [#h|#f]
    tokens = first_line_fields[1:]
    person, _, _, tokens = parse_person_ref(tokens)
    sex = Sex.NEUTER
    if tokens and tokens[0] in ('#h', '#f'):
        sex = Sex.MALE if tokens[0] == '#h' else Sex.FEMALE
        tokens = tokens[1:]
    # expect begin block
    nxt = stream.pop()
    relations: List[Relation[Somebody, str]] = []
    if not nxt or nxt.strip() != 'beg':
        return RelationsGwSyntax(person=person, sex=sex, relations=relations)
    while True:
        line = stream.pop()
        if line is None:
            break
        if line.strip() == 'end':
            break
        f = fields(line)
        if not f or f[0] != '-':
            continue
        toks = f[1:]
        if not toks:
            raise ValueError('Relation line missing relation code')
        rel_code = toks.pop(0)
        base_code = rel_code.rstrip(':')
        type_map = {
            'adop': RelationToParentType.ADOPTION,
            'reco': RelationToParentType.RECOGNITION,
            'cand': RelationToParentType.CANDIDATEPARENT,
            'godp': RelationToParentType.GODPARENT,
            'fost': RelationToParentType.FOSTERPARENT,
        }
        if base_code not in type_map:
            raise ValueError(f'Unknown relation code {rel_code}')
        rel_type = type_map[base_code]
        father_ref: Optional[Somebody] = None
        mother_ref: Optional[Somebody] = None
        if rel_code.endswith(':'):
            # dual parent form: expect father + '+' + mother strictly, no
            # leftovers.
            father_ref, _, _, toks = parse_person_ref(toks)
            if not toks or toks[0] != '+':
                raise ValueError(
                    'Expected + between father and mother in dual-parent relation')
            toks = toks[1:]
            mother_ref, _, _, toks = parse_person_ref(toks)
            if toks:
                raise ValueError(
                    f'Unexpected tokens after dual-parent relation: {toks}')
        else:
            # single parent form must start with fath: or moth:
            if not toks:
                raise ValueError(
                    'Single-parent relation missing parent designator')
            role = toks.pop(0)
            if role == 'fath:':
                father_ref, _, _, toks = parse_person_ref(toks)
                if toks:
                    raise ValueError(
                        f'Unexpected tokens after father relation: {toks}')
            elif role == 'moth:':
                mother_ref, _, _, toks = parse_person_ref(toks)
                if toks:
                    raise ValueError(
                        f'Unexpected tokens after mother relation: {toks}')
            else:
                raise ValueError(f'Unknown single-parent role token {role}')
        relations.append(
            Relation(
                type=rel_type,
                father=father_ref,
                mother=mother_ref,
                sources=''))
    return RelationsGwSyntax(person=person, sex=sex, relations=relations)


def _parse_personal_events_block(
        first_line_fields: List[str],
        stream: LineStream) -> PersonalEventsGwSyntax:
    tokens = first_line_fields[1:]
    person, _, _, tokens = parse_person_ref(tokens)
    events = _parse_personal_events(stream)
    return PersonalEventsGwSyntax(person=person, sex=Sex.NEUTER, events=events)


def parse_block(line: str, stream: LineStream) -> Optional[GwSyntax]:
    f = fields(line)
    if not f:
        return None
    tag = f[0]
    if tag == 'fam':
        return parse_family_block(f, stream)
    if tag == 'notes':
        return parse_notes_block(f, stream)
    if tag == 'notes-db':
        content = []
        while True:
            ln = stream.pop()
            if ln is None:
                break
            if ln.strip() == 'end notes-db':
                break
            content.append(ln)
        return BaseNotesGwSyntax(page="", content='\n'.join(content))
    if tag == 'wizard-note':
        # wizard-note <id>
        wizid = line[len('wizard-note'):].strip()
        content = []
        while True:
            ln = stream.pop()
            if ln is None:
                break
            if ln.strip() == 'end wizard-note':
                break
            content.append(ln)
        return WizardNotesGwSyntax(wizard_id=wizid, content='\n'.join(content))
    if tag == 'pevt':
        return _parse_personal_events_block(f, stream)
    if tag == 'rel':
        return _parse_relations_block(f, stream)
    return None


def parse_gw_file(path: str) -> List[GwSyntax]:
    """Parse a .gw file producing a list of GwSyntax variant objects.
    Translation note: This is an incremental port. Many detailed features (events, full
    date semantics, witnesses kinds, relations outside families) are TODO.
    """
    with open(path, 'r', encoding='utf-8') as fh:
        syntaxes: List[GwSyntax] = []
        stream = LineStream(iter_non_comment_lines(fh))
        while True:
            first = stream.pop()
            if first is None:
                break
            block = parse_block(first, stream)
            if block is not None:
                syntaxes.append(block)
        return syntaxes


__all__ = [
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
    'parse_gw_file']
