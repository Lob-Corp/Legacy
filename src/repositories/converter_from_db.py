from datetime import date
from typing import List, Optional, Tuple
import libraries.date
import database.date
import libraries.family
import database.family
import database.family_witness
import database.family_event
import database.family_event_witness
import libraries.events
import database.descend_children


def convert_precision_from_db(
        to_convert: database.date.Precision) -> libraries.date.PrecisionBase:
    def date_value() -> libraries.date.DateValue:
        dateTime = date.fromisoformat(to_convert.iso_date)
        return libraries.date.DateValue(day=dateTime.day,
                                        month=dateTime.month,
                                        year=dateTime.year,
                                        prec=None,
                                        delta=to_convert.delta,)

    match to_convert.precision_level:
        case database.date.DatePrecision.SURE:
            return libraries.date.Sure()
        case database.date.DatePrecision.ABOUT:
            return libraries.date.About()
        case database.date.DatePrecision.MAYBE:
            return libraries.date.Maybe()
        case database.date.DatePrecision.BEFORE:
            return libraries.date.Before()
        case database.date.DatePrecision.AFTER:
            return libraries.date.After()
        case database.date.DatePrecision.ORYEAR:
            return libraries.date.OrYear(date_value=date_value())
        case database.date.DatePrecision.YEARINT:
            return libraries.date.YearInt(date_value=date_value())
        case _:
            raise ValueError(
                f"Unknown precision level: {to_convert.precision_level}"
            )


def convert_date_from_db(
        to_convert: database.date.Date) -> libraries.date.CompressedDate:
    dateTime = date.fromisoformat(to_convert.iso_date)

    return libraries.date.CalendarDate(
        dmy=libraries.date.DateValue(dateTime.day,
                                     dateTime.month,
                                     dateTime.year,
                                     prec=convert_precision_from_db(
                                         to_convert.precision_obj),
                                     delta=to_convert.delta,),
        cal=to_convert.calendar,
    )


def convert_divorce_status_from_db(to_convert: database.family.DivorceStatus,
                                   divorce_date: Optional[database.date.Date]
                                   ) -> libraries.family.DivorceStatusBase:
    match to_convert:
        case database.family.DivorceStatus.NOT_DIVORCED:
            return libraries.family.NotDivorced()
        case database.family.DivorceStatus.SEPARATED:
            return libraries.family.Separated()
        case database.family.DivorceStatus.DIVORCED:
            if divorce_date is None:
                raise ValueError(
                    "Divorce date must be provided for divorced status"
                )
            return libraries.family.Divorced(divorce_date=convert_date_from_db(
                divorce_date))


def convert_fam_event_from_db(
    to_convert: database.family_event.FamilyEvent,
    witnesses: List[database.family_event_witness.FamilyEventWitness]
) -> libraries.family.FamilyEvent[int, str]:
    famEventName: libraries.events.FamEventNameBase
    match to_convert.name:
        case database.family_event.FamilyEventName.MARRIAGE:
            famEventName = libraries.events.FamMarriage()
        case database.family_event.FamilyEventName.NO_MARRIAGE:
            famEventName = libraries.events.FamNoMarriage()
        case database.family_event.FamilyEventName.NO_MENTION:
            famEventName = libraries.events.FamNoMention()
        case database.family_event.FamilyEventName.DIVORCE:
            famEventName = libraries.events.FamDivorce()
        case database.family_event.FamilyEventName.ENGAGE:
            famEventName = libraries.events.FamEngage()
        case database.family_event.FamilyEventName.SEPARATED:
            famEventName = libraries.events.FamSeparated()
        case database.family_event.FamilyEventName.ANNULATION:
            famEventName = libraries.events.FamAnnulation()
        case database.family_event.FamilyEventName.MARRIAGE_BANN:
            famEventName = libraries.events.FamMarriageBann()
        case database.family_event.FamilyEventName.MARRIAGE_CONTRACT:
            famEventName = libraries.events.FamMarriageContract()
        case database.family_event.FamilyEventName.MARRIAGE_LICENSE:
            famEventName = libraries.events.FamMarriageLicense()
        case database.family_event.FamilyEventName.PACS:
            famEventName = libraries.events.FamPACS()
        case database.family_event.FamilyEventName.RESIDENCE:
            famEventName = libraries.events.FamResidence()
        case database.family_event.FamilyEventName.NAMED_EVENT:
            famEventName = libraries.events.FamNamedEvent(
                name=to_convert.name.value)
    return libraries.family.FamilyEvent(
        name=famEventName,
        date=convert_date_from_db(to_convert.date_obj),
        place=to_convert.place,
        reason=to_convert.reason,
        note=to_convert.note,
        src=to_convert.src,
        witnesses=[(w.person_id, w.kind) for w in witnesses],
    )


def convert_family_from_db(
    to_convert: database.family.Family,
    witnesses: List[database.family_witness.FamilyWitness],
    eventsAndWitnesses: List[Tuple[
        database.family_event.FamilyEvent,
        List[database.family_event_witness.FamilyEventWitness]
    ]],
    children: List[database.descend_children.DescendChildren]
) -> libraries.family.Family[int, int, str]:
    return libraries.family.Family(
        index=to_convert.id,
        marriage_date=convert_date_from_db(to_convert.marriage_date_obj),
        marriage_place=to_convert.marriage_place,
        marriage_note=to_convert.marriage_note,
        marriage_src=to_convert.marriage_src,
        witnesses=[w.person_id for w in witnesses],
        relation_kind=to_convert.relation_kind,
        divorce_status=convert_divorce_status_from_db(
            to_convert.divorce_status, to_convert.divorce_date_obj
        ),
        family_events=[convert_fam_event_from_db(e[0], e[1])
                       for e in eventsAndWitnesses],
        comment=to_convert.comment,
        origin_file=to_convert.origin_file,
        src=to_convert.src,
        parents=libraries.family.Parents([to_convert.parents.father_id,
                                          to_convert.parents.mother_id]),
        children=[c.person_id for c in children],
    )
