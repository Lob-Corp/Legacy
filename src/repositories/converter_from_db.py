from datetime import date
from typing import List, Optional, Tuple
import re
import libraries.date
import database.date
import libraries.family
import database.family
import database.family_witness
import database.family_event
import database.family_event_witness
import libraries.events
import database.descend_children
import libraries.person
import database.person
import libraries.death_info
import libraries.title
import database.titles
import database.personal_event
import database.person_event_witness
import database.relation
import database.person_non_native_relations
import database.person_relations
import database.person_titles
import database.union_families
import libraries.consanguinity_rate


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
    if to_convert is None or \
            (not to_convert.iso_date or to_convert.iso_date == ''):
        return None
    try:
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
    except BaseException:
        s = to_convert.iso_date.strip()
        # mm-yyyy (month 1-2 digits, year 4 digits)
        m = re.match(r'^\s*(\d{1,2})-(\d{4})\s*$', s)
        if m:
            month = int(m.group(1))
            year = int(m.group(2))
            return libraries.date.CalendarDate(
                dmy=libraries.date.DateValue(
                    day=0,
                    month=month,
                    year=year,
                    prec=convert_precision_from_db(
                        to_convert.precision_obj),
                    delta=to_convert.delta,
                ),
                cal=to_convert.calendar,
            )
        # yyyy (4 digits)
        m = re.match(r'^\s*(\d{4})\s*$', s)
        if m:
            year = int(m.group(1))
            return libraries.date.CalendarDate(
                dmy=libraries.date.DateValue(
                    day=0,
                    month=0,
                    year=year,
                    prec=convert_precision_from_db(
                        to_convert.precision_obj),
                    delta=to_convert.delta,
                ),
                cal=to_convert.calendar,
            )
        raise


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
    events_and_witnesses: List[Tuple[
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
                       for e in events_and_witnesses],
        comment=to_convert.comment,
        origin_file=to_convert.origin_file,
        src=to_convert.src,
        parents=libraries.family.Parents([to_convert.parents.father_id,
                                          to_convert.parents.mother_id]),
        children=[c.person_id for c in children],
    )


def convert_death_status_from_db(
    to_convert: database.person.DeathStatus,
    death_reason: Optional[database.person.DeathReason],
    death_date: Optional[database.date.Date]
) -> libraries.death_info.DeathStatusBase:
    """Convert death status from database to library type."""
    match to_convert:
        case database.person.DeathStatus.NOT_DEAD:
            return libraries.death_info.NotDead()
        case database.person.DeathStatus.DEAD:
            if death_date is None:
                raise ValueError(
                    "Death date must be provided for DEAD status"
                )
            if death_reason is None:
                raise ValueError(
                    "Death reason must be provided for DEAD status"
                )
            return libraries.death_info.Dead(
                death_reason=death_reason,
                date_of_death=convert_date_from_db(death_date)
            )
        case database.person.DeathStatus.DEAD_YOUNG:
            return libraries.death_info.DeadYoung()
        case database.person.DeathStatus.DEAD_DONT_KNOW_WHEN:
            return libraries.death_info.DeadDontKnowWhen()
        case database.person.DeathStatus.DONT_KNOW_IF_DEAD:
            return libraries.death_info.DontKnowIfDead()
        case database.person.DeathStatus.OF_COURSE_DEAD:
            return libraries.death_info.OfCourseDead()


def convert_burial_status_from_db(
    to_convert: database.person.BurialStatus,
    burial_date: Optional[database.date.Date]
) -> libraries.burial_info.BurialInfoBase:
    """Convert burial status from database to library type."""
    match to_convert:
        case database.person.BurialStatus.UNKNOWN_BURIAL:
            return libraries.burial_info.UnknownBurial()
        case database.person.BurialStatus.BURIAL:
            if burial_date is None:
                raise ValueError(
                    "Burial date must be provided for BURIAL status"
                )
            return libraries.burial_info.Burial(
                burial_date=convert_date_from_db(burial_date)
            )
        case database.person.BurialStatus.CREMATED:
            if burial_date is None:
                raise ValueError(
                    "Burial date must be provided for CREMATED status"
                )
            return libraries.burial_info.Cremated(
                cremation_date=convert_date_from_db(burial_date)
            )


def convert_title_name_from_db(
    name: str
) -> libraries.title.TitleNameBase[str]:
    """Convert title name from database string to library type."""
    if name == "":
        return libraries.title.NoTitle()
    elif name == "main":
        return libraries.title.UseMainTitle()
    else:
        return libraries.title.TitleName(title_name=name)


def convert_title_from_db(
    to_convert: database.titles.Titles
) -> libraries.title.Title[str]:
    """Convert title from database to library type."""
    return libraries.title.Title(
        title_name=convert_title_name_from_db(to_convert.name),
        ident=to_convert.ident,
        place=to_convert.place,
        date_start=convert_date_from_db(to_convert.date_start_obj),
        date_end=convert_date_from_db(to_convert.date_end_obj),
        nth=to_convert.nth
    )


def convert_relation_from_db(
    to_convert: database.relation.Relation
) -> libraries.family.Relation[int, str]:
    """Convert relation (non-native parent) from database to library type."""
    return libraries.family.Relation(
        type=to_convert.type,
        father=to_convert.father_id if to_convert.father_id else None,
        mother=to_convert.mother_id if to_convert.mother_id else None,
        sources=to_convert.sources
    )


def convert_pers_event_name_from_db(
    name: database.personal_event.PersonalEventName
) -> libraries.events.PersEventNameBase[str]:
    """Convert personal event name from database enum to library type."""
    match name:
        case database.personal_event.PersonalEventName.BIRTH:
            return libraries.events.PersBirth()
        case database.personal_event.PersonalEventName.BAPTISM:
            return libraries.events.PersBaptism()
        case database.personal_event.PersonalEventName.DEATH:
            return libraries.events.PersDeath()
        case database.personal_event.PersonalEventName.BURIAL:
            return libraries.events.PersBurial()
        case database.personal_event.PersonalEventName.CREMATION:
            return libraries.events.PersCremation()
        case database.personal_event.PersonalEventName.ACCOMPLISHMENT:
            return libraries.events.PersAccomplishment()
        case database.personal_event.PersonalEventName.ACQUISITION:
            return libraries.events.PersAcquisition()
        case database.personal_event.PersonalEventName.ADHESION:
            return libraries.events.PersAdhesion()
        case database.personal_event.PersonalEventName.BAPTISM_LDS:
            return libraries.events.PersBaptismLDS()
        case database.personal_event.PersonalEventName.BAR_MITZVAH:
            return libraries.events.PersBarMitzvah()
        case database.personal_event.PersonalEventName.BAT_MITZVAH:
            return libraries.events.PersBatMitzvah()
        case database.personal_event.PersonalEventName.BENEDICTION:
            return libraries.events.PersBenediction()
        case database.personal_event.PersonalEventName.CHANGE_NAME:
            return libraries.events.PersChangeName()
        case database.personal_event.PersonalEventName.CIRCUMCISION:
            return libraries.events.PersCircumcision()
        case database.personal_event.PersonalEventName.CONFIRMATION:
            return libraries.events.PersConfirmation()
        case database.personal_event.PersonalEventName.CONFIRMATION_LDS:
            return libraries.events.PersConfirmationLDS()
        case database.personal_event.PersonalEventName.DECORATION:
            return libraries.events.PersDecoration()
        case (database.personal_event.PersonalEventName.
              DEMOBILISATION_MILITAIRE):
            return libraries.events.PersDemobilisationMilitaire()
        case database.personal_event.PersonalEventName.DIPLOMA:
            return libraries.events.PersDiploma()
        case database.personal_event.PersonalEventName.DISTINCTION:
            return libraries.events.PersDistinction()
        case database.personal_event.PersonalEventName.DOTATION:
            return libraries.events.PersDotation()
        case database.personal_event.PersonalEventName.DOTATION_LDS:
            return libraries.events.PersDotationLDS()
        case database.personal_event.PersonalEventName.EDUCATION:
            return libraries.events.PersEducation()
        case database.personal_event.PersonalEventName.ELECTION:
            return libraries.events.PersElection()
        case database.personal_event.PersonalEventName.EMIGRATION:
            return libraries.events.PersEmigration()
        case database.personal_event.PersonalEventName.EXCOMMUNICATION:
            return libraries.events.PersExcommunication()
        case database.personal_event.PersonalEventName.FAMILY_LINK_LDS:
            return libraries.events.PersFamilyLinkLDS()
        case database.personal_event.PersonalEventName.FIRST_COMMUNION:
            return libraries.events.PersFirstCommunion()
        case database.personal_event.PersonalEventName.FUNERAL:
            return libraries.events.PersFuneral()
        case database.personal_event.PersonalEventName.GRADUATE:
            return libraries.events.PersGraduate()
        case database.personal_event.PersonalEventName.HOSPITALISATION:
            return libraries.events.PersHospitalisation()
        case database.personal_event.PersonalEventName.ILLNESS:
            return libraries.events.PersIllness()
        case database.personal_event.PersonalEventName.IMMIGRATION:
            return libraries.events.PersImmigration()
        case database.personal_event.PersonalEventName.LISTE_PASSENGER:
            return libraries.events.PersListePassenger()
        case database.personal_event.PersonalEventName.MILITARY_DISTINCTION:
            return libraries.events.PersMilitaryDistinction()
        case database.personal_event.PersonalEventName.MILITARY_PROMOTION:
            return libraries.events.PersMilitaryPromotion()
        case database.personal_event.PersonalEventName.MILITARY_SERVICE:
            return libraries.events.PersMilitaryService()
        case database.personal_event.PersonalEventName.MOBILISATION_MILITAIRE:
            return libraries.events.PersMobilisationMilitaire()
        case database.personal_event.PersonalEventName.NATURALISATION:
            return libraries.events.PersNaturalisation()
        case database.personal_event.PersonalEventName.OCCUPATION:
            return libraries.events.PersOccupation()
        case database.personal_event.PersonalEventName.ORDINATION:
            return libraries.events.PersOrdination()
        case database.personal_event.PersonalEventName.PROPERTY:
            return libraries.events.PersProperty()
        case database.personal_event.PersonalEventName.RECENSEMENT:
            return libraries.events.PersRecensement()
        case database.personal_event.PersonalEventName.RESIDENCE:
            return libraries.events.PersResidence()
        case database.personal_event.PersonalEventName.RETIRED:
            return libraries.events.PersRetired()
        case database.personal_event.PersonalEventName.SCELLENT_CHILD_LDS:
            return libraries.events.PersScellentChildLDS()
        case database.personal_event.PersonalEventName.SCELLENT_PARENT_LDS:
            return libraries.events.PersScellentParentLDS()
        case database.personal_event.PersonalEventName.SCELLENT_SPOUSE_LDS:
            return libraries.events.PersScellentSpouseLDS()
        case database.personal_event.PersonalEventName.VENTE_BIEN:
            return libraries.events.PersVenteBien()
        case database.personal_event.PersonalEventName.WILL:
            return libraries.events.PersWill()
        case database.personal_event.PersonalEventName.NAMED_EVENT:
            return libraries.events.PersNamedEvent(name=name.value)


def convert_personal_event_from_db(
    to_convert: database.personal_event.PersonalEvent,
    witnesses: List[database.person_event_witness.PersonEventWitness]
) -> libraries.events.PersonalEvent[int, str]:
    """Convert personal event from database to library type."""
    return libraries.events.PersonalEvent(
        name=convert_pers_event_name_from_db(to_convert.name),
        date=convert_date_from_db(to_convert.date_obj),
        place=to_convert.place,
        reason=to_convert.reason,
        note=to_convert.note,
        src=to_convert.src,
        witnesses=[(w.person_id, w.kind) for w in witnesses]
    )


def convert_person_from_db(
    to_convert: database.person.Person,
    titles: List[database.titles.Titles],
    non_native_relations: List[database.relation.Relation],
    related_persons: List[database.person_relations.PersonRelations],
    personal_events_and_witnesses: List[Tuple[
        database.personal_event.PersonalEvent,
        List[database.person_event_witness.PersonEventWitness]
    ]],
    family_ids: List[int]
) -> libraries.person.Person[int, int, str, int]:
    """Convert person from database to library type.

    Args:
        to_convert: The database person to convert
        titles: List of titles associated with the person
        non_native_relations: List of non-native parent relations
        related_persons: List of related person relations
        personal_events_and_witnesses: List of tuples containing events
            and their witnesses
        family_ids: List of family IDs the person belongs to

    Returns:
        A Person object with int indexes, int person references,
        str descriptors, and int family references
    """
    # Parse comma-separated lists from database string fields
    qualifiers = [
        q.strip() for q in to_convert.qualifiers.split(',') if q.strip()
    ]
    aliases = [
        a.strip() for a in to_convert.aliases.split(',') if a.strip()
    ]
    first_names_aliases = [
        fn.strip()
        for fn in to_convert.first_names_aliases.split(',')
        if fn.strip()
    ]
    surname_aliases = [
        sn.strip()
        for sn in to_convert.surname_aliases.split(',')
        if sn.strip()
    ]

    # Determine ascendants - if person has ascend, get family ID
    if to_convert.ascend:
        ascend_family = to_convert.ascend.parents
        consanguinity_rate = libraries.consanguinity_rate.ConsanguinityRate(
            to_convert.ascend.consang
        )
    else:
        ascend_family = None
        consanguinity_rate = libraries.consanguinity_rate.ConsanguinityRate(0)

    print("BIRTH DATE OBJECT")
    print(to_convert.birth_date)
    print(to_convert.first_name)
    print(to_convert.surname)
    print(to_convert.birth_date_obj)
    print((
        convert_date_from_db(to_convert.birth_date_obj)
        if to_convert.birth_date_obj else None
    ))

    return libraries.person.Person(
        index=to_convert.id,
        first_name=to_convert.first_name,
        surname=to_convert.surname,
        occ=to_convert.occ,
        image=to_convert.image,
        public_name=to_convert.public_name,
        qualifiers=qualifiers,
        aliases=aliases,
        first_names_aliases=first_names_aliases,
        surname_aliases=surname_aliases,
        titles=[convert_title_from_db(t) for t in titles],
        non_native_parents_relation=[
            convert_relation_from_db(r) for r in non_native_relations
        ],
        related_persons=[rp.related_person_id for rp in related_persons],
        occupation=to_convert.occupation,
        sex=to_convert.sex,
        access_right=to_convert.access_right,
        birth_date=(
            convert_date_from_db(to_convert.birth_date_obj)
            if to_convert.birth_date_obj else None
        ),
        birth_place=to_convert.birth_place,
        birth_note=to_convert.birth_note,
        birth_src=to_convert.birth_src,
        baptism_date=(
            convert_date_from_db(to_convert.baptism_date_obj)
            if to_convert.baptism_date_obj else None
        ),
        baptism_place=to_convert.baptism_place,
        baptism_note=to_convert.baptism_note,
        baptism_src=to_convert.baptism_src,
        death_status=convert_death_status_from_db(
            to_convert.death_status,
            to_convert.death_reason,
            to_convert.death_date_obj
        ),
        death_place=to_convert.death_place,
        death_note=to_convert.death_note,
        death_src=to_convert.death_src,
        burial=convert_burial_status_from_db(
            to_convert.burial_status,
            to_convert.burial_date_obj
        ),
        burial_place=to_convert.burial_place,
        burial_note=to_convert.burial_note,
        burial_src=to_convert.burial_src,
        personal_events=[
            convert_personal_event_from_db(e[0], e[1])
            for e in personal_events_and_witnesses
        ],
        notes=to_convert.notes,
        src=to_convert.src,
        ascend=libraries.family.Ascendants(
            parents=ascend_family,
            consanguinity_rate=consanguinity_rate
        ),
        families=family_ids
    )
