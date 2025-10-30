"""Block parsing functions for GeneWeb files.

Handles parsing of different block types: family, notes, relations,
personal events, etc.
"""

from dataclasses import replace
from typing import List, Tuple, Optional, cast

from libraries.person import Person, Sex
from libraries.title import AccessRight
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
    Ascendants,
)
from libraries.events import FamilyEvent
from libraries.burial_info import UnknownBurial
from libraries.death_info import NotDead
from libraries.consanguinity_rate import ConsanguinityRate

from .person_parser import build_person
from .data_types import (
    Key,
    Somebody,
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
from .utils import fields
from .date_parser import date_of_string_py, CompressedDate
from .person_parser import (
    parse_person_ref,
    parse_parent,
    parse_first_name,
    parse_name,
)
from .event_parser import (
    parse_family_events,
    parse_personal_events,
)
from .stream import LineStream


def _parse_child_line(
    line_tokens: List[str],
    default_surname: str,
    default_sex: Sex,
    common_src: str,
    common_birth_place: str,
) -> Tuple[Person[int, int, str, int], str]:
    """Parse a child definition line (tokens after '-').

    Returns (person, surname_used).
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
            boundary = set('<>!?~-0123456789{#([')
            if c0 not in boundary:
                surname, toks = parse_name(toks)

    person, _ = build_person(first, surname, occ, default_sex, toks)

    # Apply defaults
    if not person.birth_place:
        person = replace(person, birth_place=common_birth_place)
    if not person.birth_src:
        person = replace(person, birth_src=common_src)

    return person, surname


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
    """Parse marriage indicator and relation type.

    Returns (relation_kind, father_sex, mother_sex, marriage_date, place,
    note, src, divorce_status, rest_tokens).
    """
    rest = list(tokens)

    marriage_date: Optional[CompressedDate] = None
    relation_kind: MaritalStatus = MaritalStatus.MARRIED
    father_sex: Sex = Sex.MALE
    mother_sex: Sex = Sex.FEMALE
    place = note = src = ""
    divorce_status: DivorceStatusBase = NotDivorced()

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


def parse_family_block(
        first_line_fields: List[str],
        stream: LineStream) -> FamilyGwSyntax:
    """Parse a family block (fam)."""
    tokens = first_line_fields[1:]  # drop 'fam'
    father, _, _, tokens = parse_parent(tokens, Sex.MALE)
    relation_kind, fath_sex, moth_sex, marriage_date, marr_place, \
        marr_note, marr_src, divorce_status, tokens = \
        _parse_marriage_and_relation(tokens)
    mother, _, _, tokens = parse_parent(tokens, Sex.FEMALE)

    parents: Parents[Somebody] = Parents.from_couple(
        father, mother)  # type: ignore

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

    fam_src = ''
    nxt = stream.peek()
    if nxt:
        f = fields(nxt)
        if f and f[0] == 'src' and len(f) == 2:
            fam_src = f[1]
            stream.pop()

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

    comment = ''
    nxt = stream.peek()
    if nxt and nxt.startswith('comm '):
        comment = nxt[5:]
        stream.pop()

    events: List[Tuple[FamilyEvent[Somebody, str], List[Sex]]] = []
    nxt = stream.peek()
    if nxt and nxt.startswith('fevt'):
        stream.pop()
        events = parse_family_events(stream)

    descend: List[Person[int, int, str, int]] = []
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
            if toks:
                tok0 = toks[0]
                match tok0:
                    case 'm:' | 'h' | 'm':
                        child_sex = Sex.MALE
                        toks = toks[1:]
                    case 'f' | 'f:':
                        child_sex = Sex.FEMALE
                        toks = toks[1:]

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

    # Extract Person objects from Somebody references for template Family
    # The converter will replace this with properly resolved persons
    template_parents: List[Person[int, int, str, int]] = []
    for somebody in parents.parents:
        if isinstance(somebody, SomebodyDefined):
            template_parents.append(somebody.person)

    # Parents must have at least one element
    if not template_parents:
        # Create a minimal placeholder if no defined parents
        # This shouldn't happen in well-formed data
        placeholder = Person(
            index=-1, first_name="", surname="", occ=0,
            image="", public_name="", qualifiers=[], aliases=[],
            first_names_aliases=[], surname_aliases=[], titles=[],
            non_native_parents_relation=[], related_persons=[],
            occupation="", sex=Sex.NEUTER, access_right=AccessRight.PUBLIC,
            birth_date=None, birth_place="", birth_note="", birth_src="",
            baptism_date=None, baptism_place="", baptism_note="",
            baptism_src="", death_status=NotDead(), death_place="",
            death_note="", death_src="", burial=UnknownBurial(),
            burial_place="", burial_note="", burial_src="",
            personal_events=[], notes="", src="",
            ascend=Ascendants(
                parents=None,
                consanguinity_rate=ConsanguinityRate.from_integer(-1)
            ),
            families=[]
        )
        template_parents.append(placeholder)

    family: Family[int, Person[int, int, str, int], str] = Family(
        index=-1,
        marriage_date=marriage_date or '',
        marriage_place=marr_place,
        marriage_note=marr_note,
        marriage_src=marr_src,
        witnesses=[],
        relation_kind=relation_kind,
        divorce_status=divorce_status,
        family_events=cast(
            List[FamilyEvent[Person[int, int, str, int], str]],
            [evt for (evt, _) in events]
        ),
        comment=comment,
        origin_file='',
        src=fam_src,
        parents=Parents(template_parents),
        children=descend,
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
    """Parse a notes block."""
    tokens = fields_line[1:]
    surname, tokens = parse_name(tokens)
    first, occ, tokens = parse_first_name(tokens)
    key = Key(first, surname, occ)

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


def parse_relations_block(
        first_line_fields: List[str],
        stream: LineStream) -> RelationsGwSyntax:
    """Parse a relations block (rel)."""
    tokens = first_line_fields[1:]
    person, _, _, tokens = parse_person_ref(tokens)
    sex = Sex.NEUTER
    if tokens and tokens[0] in ('#h', '#f'):
        sex = Sex.MALE if tokens[0] == '#h' else Sex.FEMALE
        tokens = tokens[1:]

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
            # dual parent form
            father_ref, _, _, toks = parse_person_ref(toks)
            if not toks or toks[0] != '+':
                raise ValueError(
                    'Expected + between father and mother in '
                    'dual-parent relation')
            toks = toks[1:]
            mother_ref, _, _, toks = parse_person_ref(toks)
            if toks:
                raise ValueError(
                    f'Unexpected tokens after dual-parent relation: {toks}')
        else:
            # single parent form
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


def parse_personal_events_block(
        first_line_fields: List[str],
        stream: LineStream) -> PersonalEventsGwSyntax:
    """Parse a personal events block (pevt)."""
    tokens = first_line_fields[1:]
    person, _, _, tokens = parse_person_ref(tokens)
    events = parse_personal_events(stream)
    return PersonalEventsGwSyntax(person=person, sex=Sex.NEUTER, events=events)


def parse_block(line: str, stream: LineStream) -> Optional[GwSyntax]:
    """Parse a block based on its tag."""
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
        return parse_personal_events_block(f, stream)
    if tag == 'rel':
        return parse_relations_block(f, stream)
    if tag == 'page-ext':
        page_name = line[len('page-ext'):].strip()
        content = []
        while True:
            ln = stream.pop()
            if ln is None:
                break
            if ln.strip() == 'end page-ext':
                break
            content.append(ln)
        return PageExtGwSyntax(page_name=page_name, content='\n'.join(content))

    return None
