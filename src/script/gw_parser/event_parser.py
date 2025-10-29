"""Event parsing functions for GeneWeb files.

Handles parsing of family events and personal events with witnesses and notes.
"""

from typing import List, Tuple, Optional

from libraries.person import Sex
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

from .data_types import Somebody
from .utils import fields, get_field
from .date_parser import get_optional_date
from .person_parser import parse_person_ref
from .stream import LineStream


# Event name mappings

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
    """Parse family event name from tag."""
    if tag.startswith('#') and tag not in _fam_event_map:
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
    """Parse personal event name from tag."""
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
        tokens: List[str]) -> Tuple[EventWitnessKind, List[str]]:
    """Parse witness kind from tokens."""
    if tokens and tokens[0] in _witness_kind_map:
        return _witness_kind_map[tokens[0]], tokens[1:]
    return EventWitnessKind.WITNESS, tokens


def parse_event_witness_lines(
        stream: LineStream) -> Tuple[
            List[Tuple[Somebody, Sex, EventWitnessKind]], Optional[str]]:
    """Parse witness lines for an event."""
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


def parse_event_notes(stream: LineStream) -> Tuple[str, Optional[str]]:
    """Parse note lines for an event."""
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


def parse_family_events(
        stream: LineStream) -> List[
            Tuple[FamilyEvent[Somebody, str], List[Sex]]]:
    """Parse family events block (after 'fevt' header)."""
    events: List[Tuple[FamilyEvent[Somebody, str], List[Sex]]] = []
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
        witnesses, _next_start = parse_event_witness_lines(stream)
        notes, _ = parse_event_notes(stream)
        sexes = [w[1] for w in witnesses]
        evt = FamilyEvent(
            name=name,
            date=date_opt or '',
            place=place,
            reason=reason,
            note=notes,
            src=src,
            witnesses=[(w[0], w[2]) for w in witnesses],
        )
        events.append((evt, sexes))
    return events


def parse_personal_events(
        stream: LineStream) -> List[PersonalEvent[Somebody, str]]:
    """Parse personal events block (after 'pevt' header)."""
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
        witnesses, _ = parse_event_witness_lines(stream)
        notes, _ = parse_event_notes(stream)
        if toks:
            raise ValueError(f"Unparsed tokens in personal event line: {toks}")
        evt = PersonalEvent(
            name=name,
            date=date_opt or '',
            place=place,
            reason=reason,
            note=notes,
            src=src,
            witnesses=[(w[0], w[2]) for w in witnesses],
        )
        events.append(evt)
    return events
