"""Converter functions from library types to database models.

This module provides functions to convert from immutable library types
back to SQLAlchemy database models for persistence.
"""
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


def convert_precision_to_db(
    to_convert: libraries.date.PrecisionBase,
    calendar: Optional[libraries.date.Calendar] = None
) -> database.date.Precision:
    """Convert precision from library type to database model."""
    db_precision = database.date.Precision()

    match to_convert:
        case libraries.date.Sure():
            db_precision.precision_level = database.date.DatePrecision.SURE
            db_precision.iso_date = None
            db_precision.delta = None
        case libraries.date.About():
            db_precision.precision_level = database.date.DatePrecision.ABOUT
            db_precision.iso_date = None
            db_precision.delta = None
        case libraries.date.Maybe():
            db_precision.precision_level = database.date.DatePrecision.MAYBE
            db_precision.iso_date = None
            db_precision.delta = None
        case libraries.date.Before():
            db_precision.precision_level = database.date.DatePrecision.BEFORE
            db_precision.iso_date = None
            db_precision.delta = None
        case libraries.date.After():
            db_precision.precision_level = database.date.DatePrecision.AFTER
            db_precision.iso_date = None
            db_precision.delta = None
        case libraries.date.OrYear(date_value=dv):
            db_precision.precision_level = database.date.DatePrecision.ORYEAR
            db_precision.iso_date = date(
                dv.year, dv.month, dv.day
            ).isoformat()
            db_precision.delta = dv.delta
        case libraries.date.YearInt(date_value=dv):
            db_precision.precision_level = database.date.DatePrecision.YEARINT
            db_precision.iso_date = date(
                dv.year, dv.month, dv.day
            ).isoformat()
            db_precision.delta = dv.delta
        case _:
            raise ValueError(f"Unknown precision type: {type(to_convert)}")

    db_precision.calendar = calendar
    return db_precision


def convert_date_to_db(
    to_convert: libraries.date.CompressedDate
) -> Optional[database.date.Date]:
    """Convert date from library type to database model."""

    def default_precision(
        calendar: Optional[libraries.date.Calendar]
    ) -> database.date.Precision:
        if not calendar:
            calendar = libraries.date.Calendar.GREGORIAN
        db_precision = database.date.Precision()
        db_precision.precision_level = database.date.DatePrecision.SURE
        db_precision.iso_date = None
        db_precision.delta = None
        db_precision.calendar = calendar
        return db_precision

    if to_convert is None:
        return None

    if isinstance(to_convert, str):
        if to_convert == "":
            db_date = database.date.Date()
            db_date.iso_date = ""
            db_date.calendar = libraries.date.Calendar.GREGORIAN
            db_date.delta = 0
            db_date.precision_obj = default_precision(None)
            return db_date
        raise ValueError(
            "Cannot convert non empty free-form string date to database model"
        )

    if isinstance(to_convert, tuple):
        raise ValueError(
            "Cannot convert tuple date format to database model"
        )

    if isinstance(to_convert, libraries.date.CalendarDate):
        if to_convert.dmy.year == 0:
            return None
        db_date = database.date.Date()
        db_date.iso_date = date(
            to_convert.dmy.year,
            to_convert.dmy.month,
            to_convert.dmy.day
        ).isoformat()
        db_date.calendar = to_convert.cal
        db_date.delta = to_convert.dmy.delta

        if to_convert.dmy.prec:
            db_date.precision_obj = convert_precision_to_db(
                to_convert.dmy.prec,
                to_convert.cal
            )
        else:
            db_date.precision_obj = default_precision(None)
        return db_date

    raise ValueError(f"Unknown date type: {type(to_convert)}")


def convert_divorce_status_to_db(
    to_convert: libraries.family.DivorceStatusBase
) -> Tuple[database.family.DivorceStatus, Optional[database.date.Date]]:
    """Convert divorce status from library type to database model.

    Returns:
        Tuple of (DivorceStatus enum, optional divorce Date)
    """
    match to_convert:
        case libraries.family.NotDivorced():
            return (database.family.DivorceStatus.NOT_DIVORCED, None)
        case libraries.family.Separated():
            return (database.family.DivorceStatus.SEPARATED, None)
        case libraries.family.Divorced(divorce_date=divorce_date):
            return (
                database.family.DivorceStatus.DIVORCED,
                convert_date_to_db(divorce_date)
            )
        case _:
            raise ValueError(
                f"Unknown divorce status type: {type(to_convert)}"
            )


def convert_fam_event_name_to_db(
    to_convert: libraries.events.FamEventNameBase[str]
) -> Tuple[database.family_event.FamilyEventName, Optional[str]]:
    """Convert family event name from library type to database enum.

    Returns:
        Tuple of (FamilyEventName enum, optional custom name string)
    """
    match to_convert:
        case libraries.events.FamMarriage():
            return (database.family_event.FamilyEventName.MARRIAGE, None)
        case libraries.events.FamNoMarriage():
            return (database.family_event.FamilyEventName.NO_MARRIAGE, None)
        case libraries.events.FamNoMention():
            return (database.family_event.FamilyEventName.NO_MENTION, None)
        case libraries.events.FamDivorce():
            return (database.family_event.FamilyEventName.DIVORCE, None)
        case libraries.events.FamEngage():
            return (database.family_event.FamilyEventName.ENGAGE, None)
        case libraries.events.FamSeparated():
            return (database.family_event.FamilyEventName.SEPARATED, None)
        case libraries.events.FamAnnulation():
            return (database.family_event.FamilyEventName.ANNULATION, None)
        case libraries.events.FamMarriageBann():
            return (
                database.family_event.FamilyEventName.MARRIAGE_BANN, None
            )
        case libraries.events.FamMarriageContract():
            return (
                database.family_event.FamilyEventName.MARRIAGE_CONTRACT, None
            )
        case libraries.events.FamMarriageLicense():
            return (
                database.family_event.FamilyEventName.MARRIAGE_LICENSE, None
            )
        case libraries.events.FamPACS():
            return (database.family_event.FamilyEventName.PACS, None)
        case libraries.events.FamResidence():
            return (database.family_event.FamilyEventName.RESIDENCE, None)
        case libraries.events.FamNamedEvent(name=name):
            return (database.family_event.FamilyEventName.NAMED_EVENT, name)
        case _:
            raise ValueError(
                f"Unknown family event name type: {type(to_convert)}"
            )


def convert_fam_event_to_db(
    to_convert: libraries.family.FamilyEvent[int, str]
) -> Tuple[
    database.family_event.FamilyEvent,
    List[database.family_event_witness.FamilyEventWitness]
]:
    """Convert family event from library type to database model.

    Returns:
        Tuple of (FamilyEvent, list of FamilyEventWitness)
    """
    db_event = database.family_event.FamilyEvent()

    event_name, custom_name = convert_fam_event_name_to_db(to_convert.name)
    db_event.name = event_name

    db_event.date_obj = convert_date_to_db(to_convert.date)

    db_event.place = to_convert.place
    db_event.reason = to_convert.reason
    db_event.note = to_convert.note
    db_event.src = to_convert.src

    witnesses = []
    for person_id, witness_kind in to_convert.witnesses:
        db_witness = database.family_event_witness.FamilyEventWitness()
        db_witness.person_id = person_id
        db_witness.kind = witness_kind
        witnesses.append(db_witness)

    return (db_event, witnesses)


def convert_family_to_db(
    to_convert: libraries.family.Family[int, int, str],
    couple_id: int
) -> Tuple[
    database.family.Family,
    List[database.family_witness.FamilyWitness],
    List[Tuple[
        database.family_event.FamilyEvent,
        List[database.family_event_witness.FamilyEventWitness]
    ]],
    List[database.descend_children.DescendChildren]
]:
    """Convert family from library type to database model.

    Args:
        to_convert: The library Family to convert
        couple_id: The database ID of the associated Couple record

    Returns:
        Tuple of (Family, witnesses, events with their witnesses, children)
    """
    db_family = database.family.Family()

    db_family.id = to_convert.index
    db_family.marriage_date_obj = convert_date_to_db(to_convert.marriage_date)
    db_family.marriage_place = to_convert.marriage_place
    db_family.marriage_note = to_convert.marriage_note
    db_family.marriage_src = to_convert.marriage_src
    db_family.relation_kind = to_convert.relation_kind
    db_family.comment = to_convert.comment
    db_family.origin_file = to_convert.origin_file
    db_family.src = to_convert.src
    db_family.parents_id = couple_id

    divorce_status, divorce_date = convert_divorce_status_to_db(
        to_convert.divorce_status
    )
    db_family.divorce_status = divorce_status
    db_family.divorce_date_obj = divorce_date

    witnesses = []
    for person_id in to_convert.witnesses:
        db_witness = database.family_witness.FamilyWitness()
        db_witness.person_id = person_id
        witnesses.append(db_witness)

    events_and_witnesses = []
    for event in to_convert.family_events:
        db_event, db_witnesses = convert_fam_event_to_db(event)
        events_and_witnesses.append((db_event, db_witnesses))

    children = []
    for person_id in to_convert.children:
        db_child = database.descend_children.DescendChildren()
        db_child.person_id = person_id
        children.append(db_child)

    return (db_family, witnesses, events_and_witnesses, children)


def convert_death_status_to_db(
    to_convert: libraries.death_info.DeathStatusBase
) -> Tuple[
    database.person.DeathStatus,
    Optional[database.person.DeathReason],
    Optional[database.date.Date]
]:
    """Convert death status from library type to database model.

    Returns:
        Tuple of (DeathStatus enum, optional DeathReason, optional Date)
    """
    match to_convert:
        case libraries.death_info.NotDead():
            return (database.person.DeathStatus.NOT_DEAD, None, None)
        case libraries.death_info.Dead(
            death_reason=reason, date_of_death=death_date
        ):
            return (
                database.person.DeathStatus.DEAD,
                reason,
                convert_date_to_db(death_date)
            )
        case libraries.death_info.DeadYoung():
            return (database.person.DeathStatus.DEAD_YOUNG, None, None)
        case libraries.death_info.DeadDontKnowWhen():
            return (
                database.person.DeathStatus.DEAD_DONT_KNOW_WHEN, None, None
            )
        case libraries.death_info.DontKnowIfDead():
            return (
                database.person.DeathStatus.DONT_KNOW_IF_DEAD, None, None
            )
        case libraries.death_info.OfCourseDead():
            return (database.person.DeathStatus.OF_COURSE_DEAD, None, None)
        case _:
            raise ValueError(
                f"Unknown death status type: {type(to_convert)}"
            )


def convert_burial_status_to_db(
    to_convert: libraries.burial_info.BurialInfoBase
) -> Tuple[database.person.BurialStatus, Optional[database.date.Date]]:
    """Convert burial status from library type to database model.

    Returns:
        Tuple of (BurialStatus enum, optional burial Date)
    """
    match to_convert:
        case libraries.burial_info.UnknownBurial():
            return (database.person.BurialStatus.UNKNOWN_BURIAL, None)
        case libraries.burial_info.Burial(burial_date=burial_date):
            return (
                database.person.BurialStatus.BURIAL,
                convert_date_to_db(burial_date)
            )
        case libraries.burial_info.Cremated(cremation_date=cremation_date):
            return (
                database.person.BurialStatus.CREMATED,
                convert_date_to_db(cremation_date)
            )
        case _:
            raise ValueError(
                f"Unknown burial status type: {type(to_convert)}"
            )


def convert_title_name_to_db(
    to_convert: libraries.title.TitleNameBase[str]
) -> str:
    """Convert title name from library type to database string."""
    match to_convert:
        case libraries.title.NoTitle():
            return ""
        case libraries.title.UseMainTitle():
            return "main"
        case libraries.title.TitleName(title_name=name):
            return name
        case _:
            raise ValueError(
                f"Unknown title name type: {type(to_convert)}"
            )


def convert_title_to_db(
    to_convert: libraries.title.Title[str]
) -> database.titles.Titles:
    """Convert title from library type to database model."""
    db_title = database.titles.Titles()

    db_title.name = convert_title_name_to_db(to_convert.title_name)
    db_title.ident = to_convert.ident
    db_title.place = to_convert.place
    db_title.date_start_obj = convert_date_to_db(to_convert.date_start)
    db_title.date_end_obj = convert_date_to_db(to_convert.date_end)
    db_title.nth = to_convert.nth

    return db_title


def convert_relation_to_db(
    to_convert: libraries.family.Relation[int, str]
) -> database.relation.Relation:
    """Convert relation (non-native parent) from library to database."""
    db_relation = database.relation.Relation()

    db_relation.type = to_convert.type
    db_relation.father_id = to_convert.father if to_convert.father else 0
    db_relation.mother_id = to_convert.mother if to_convert.mother else 0
    db_relation.sources = to_convert.sources

    return db_relation


def convert_pers_event_name_to_db(
    to_convert: libraries.events.PersEventNameBase[str]
) -> Tuple[database.personal_event.PersonalEventName, Optional[str]]:
    """Convert personal event name from library type to database enum.

    Returns:
        Tuple of (PersonalEventName enum, optional custom name string)
    """
    match to_convert:
        case libraries.events.PersBirth():
            return (database.personal_event.PersonalEventName.BIRTH, None)
        case libraries.events.PersBaptism():
            return (database.personal_event.PersonalEventName.BAPTISM, None)
        case libraries.events.PersDeath():
            return (database.personal_event.PersonalEventName.DEATH, None)
        case libraries.events.PersBurial():
            return (database.personal_event.PersonalEventName.BURIAL, None)
        case libraries.events.PersCremation():
            return (database.personal_event.PersonalEventName.CREMATION, None)
        case libraries.events.PersAccomplishment():
            return (
                database.personal_event.PersonalEventName.ACCOMPLISHMENT, None
            )
        case libraries.events.PersAcquisition():
            return (
                database.personal_event.PersonalEventName.ACQUISITION, None
            )
        case libraries.events.PersAdhesion():
            return (database.personal_event.PersonalEventName.ADHESION, None)
        case libraries.events.PersBaptismLDS():
            return (
                database.personal_event.PersonalEventName.BAPTISM_LDS, None
            )
        case libraries.events.PersBarMitzvah():
            return (
                database.personal_event.PersonalEventName.BAR_MITZVAH, None
            )
        case libraries.events.PersBatMitzvah():
            return (
                database.personal_event.PersonalEventName.BAT_MITZVAH, None
            )
        case libraries.events.PersBenediction():
            return (
                database.personal_event.PersonalEventName.BENEDICTION, None
            )
        case libraries.events.PersChangeName():
            return (
                database.personal_event.PersonalEventName.CHANGE_NAME, None
            )
        case libraries.events.PersCircumcision():
            return (
                database.personal_event.PersonalEventName.CIRCUMCISION, None
            )
        case libraries.events.PersConfirmation():
            return (
                database.personal_event.PersonalEventName.CONFIRMATION, None
            )
        case libraries.events.PersConfirmationLDS():
            return (
                database.personal_event.PersonalEventName.CONFIRMATION_LDS,
                None
            )
        case libraries.events.PersDecoration():
            return (
                database.personal_event.PersonalEventName.DECORATION, None
            )
        case libraries.events.PersDemobilisationMilitaire():
            return (
                database.personal_event.PersonalEventName.
                DEMOBILISATION_MILITAIRE,
                None
            )
        case libraries.events.PersDiploma():
            return (database.personal_event.PersonalEventName.DIPLOMA, None)
        case libraries.events.PersDistinction():
            return (
                database.personal_event.PersonalEventName.DISTINCTION, None
            )
        case libraries.events.PersDotation():
            return (database.personal_event.PersonalEventName.DOTATION, None)
        case libraries.events.PersDotationLDS():
            return (
                database.personal_event.PersonalEventName.DOTATION_LDS, None
            )
        case libraries.events.PersEducation():
            return (database.personal_event.PersonalEventName.EDUCATION, None)
        case libraries.events.PersElection():
            return (database.personal_event.PersonalEventName.ELECTION, None)
        case libraries.events.PersEmigration():
            return (
                database.personal_event.PersonalEventName.EMIGRATION, None
            )
        case libraries.events.PersExcommunication():
            return (
                database.personal_event.PersonalEventName.EXCOMMUNICATION,
                None
            )
        case libraries.events.PersFamilyLinkLDS():
            return (
                database.personal_event.PersonalEventName.FAMILY_LINK_LDS,
                None
            )
        case libraries.events.PersFirstCommunion():
            return (
                database.personal_event.PersonalEventName.FIRST_COMMUNION,
                None
            )
        case libraries.events.PersFuneral():
            return (database.personal_event.PersonalEventName.FUNERAL, None)
        case libraries.events.PersGraduate():
            return (database.personal_event.PersonalEventName.GRADUATE, None)
        case libraries.events.PersHospitalisation():
            return (
                database.personal_event.PersonalEventName.HOSPITALISATION,
                None
            )
        case libraries.events.PersIllness():
            return (database.personal_event.PersonalEventName.ILLNESS, None)
        case libraries.events.PersImmigration():
            return (
                database.personal_event.PersonalEventName.IMMIGRATION, None
            )
        case libraries.events.PersListePassenger():
            return (
                database.personal_event.PersonalEventName.LISTE_PASSENGER,
                None
            )
        case libraries.events.PersMilitaryDistinction():
            return (
                database.personal_event.PersonalEventName.
                MILITARY_DISTINCTION,
                None
            )
        case libraries.events.PersMilitaryPromotion():
            return (
                database.personal_event.PersonalEventName.MILITARY_PROMOTION,
                None
            )
        case libraries.events.PersMilitaryService():
            return (
                database.personal_event.PersonalEventName.MILITARY_SERVICE,
                None
            )
        case libraries.events.PersMobilisationMilitaire():
            return (
                database.personal_event.PersonalEventName.
                MOBILISATION_MILITAIRE,
                None
            )
        case libraries.events.PersNaturalisation():
            return (
                database.personal_event.PersonalEventName.NATURALISATION,
                None
            )
        case libraries.events.PersOccupation():
            return (
                database.personal_event.PersonalEventName.OCCUPATION, None
            )
        case libraries.events.PersOrdination():
            return (
                database.personal_event.PersonalEventName.ORDINATION, None
            )
        case libraries.events.PersProperty():
            return (database.personal_event.PersonalEventName.PROPERTY, None)
        case libraries.events.PersRecensement():
            return (
                database.personal_event.PersonalEventName.RECENSEMENT, None
            )
        case libraries.events.PersResidence():
            return (database.personal_event.PersonalEventName.RESIDENCE, None)
        case libraries.events.PersRetired():
            return (database.personal_event.PersonalEventName.RETIRED, None)
        case libraries.events.PersScellentChildLDS():
            return (
                database.personal_event.PersonalEventName.SCELLENT_CHILD_LDS,
                None
            )
        case libraries.events.PersScellentParentLDS():
            return (
                database.personal_event.PersonalEventName.SCELLENT_PARENT_LDS,
                None
            )
        case libraries.events.PersScellentSpouseLDS():
            return (
                database.personal_event.PersonalEventName.SCELLENT_SPOUSE_LDS,
                None
            )
        case libraries.events.PersVenteBien():
            return (
                database.personal_event.PersonalEventName.VENTE_BIEN, None
            )
        case libraries.events.PersWill():
            return (database.personal_event.PersonalEventName.WILL, None)
        case libraries.events.PersNamedEvent(name=name):
            return (
                database.personal_event.PersonalEventName.NAMED_EVENT, name
            )
        case _:
            raise ValueError(
                f"Unknown personal event name type: {type(to_convert)}"
            )


def convert_personal_event_to_db(
    to_convert: libraries.events.PersonalEvent[int, str]
) -> Tuple[
    database.personal_event.PersonalEvent,
    List[database.person_event_witness.PersonEventWitness]
]:
    """Convert personal event from library type to database model.

    Returns:
        Tuple of (PersonalEvent, list of PersonEventWitness)
    """
    db_event = database.personal_event.PersonalEvent()

    event_name, custom_name = convert_pers_event_name_to_db(to_convert.name)
    db_event.name = event_name

    db_event.date_obj = convert_date_to_db(to_convert.date)

    db_event.place = to_convert.place
    db_event.reason = to_convert.reason
    db_event.note = to_convert.note
    db_event.src = to_convert.src

    witnesses = []
    for person_id, witness_kind in to_convert.witnesses:
        db_witness = database.person_event_witness.PersonEventWitness()
        db_witness.person_id = person_id
        db_witness.kind = witness_kind
        witnesses.append(db_witness)

    return (db_event, witnesses)


def convert_person_to_db(
    to_convert: libraries.person.Person[int, int, str, int],
    ascend_id: Optional[int] = None,
    families_id: Optional[int] = None
) -> Tuple[
    database.person.Person,
    List[database.titles.Titles],
    List[database.relation.Relation],
    List[database.person_relations.PersonRelations],
    List[Tuple[
        database.personal_event.PersonalEvent,
        List[database.person_event_witness.PersonEventWitness]
    ]]
]:
    """Convert person from library type to database model.

    Args:
        to_convert: The library Person to convert
        ascend_id: Optional database ID of the associated Ascends record
        families_id: Optional database ID of the associated Unions record

    Returns:
        Tuple of (Person, titles, non_native_relations,
                  related_persons, personal_events_and_witnesses)
    """
    db_person = database.person.Person()

    db_person.id = to_convert.index
    db_person.first_name = to_convert.first_name
    db_person.surname = to_convert.surname
    db_person.occ = to_convert.occ
    db_person.image = to_convert.image
    db_person.public_name = to_convert.public_name
    db_person.occupation = to_convert.occupation
    db_person.sex = to_convert.sex
    db_person.access_right = to_convert.access_right
    db_person.notes = to_convert.notes
    db_person.src = to_convert.src

    db_person.qualifiers = ','.join(to_convert.qualifiers)
    db_person.aliases = ','.join(to_convert.aliases)
    db_person.first_names_aliases = ','.join(to_convert.first_names_aliases)
    db_person.surname_aliases = ','.join(to_convert.surname_aliases)

    db_person.birth_date_obj = convert_date_to_db(to_convert.birth_date)
    db_person.birth_place = to_convert.birth_place
    db_person.birth_note = to_convert.birth_note
    db_person.birth_src = to_convert.birth_src

    db_person.baptism_date_obj = convert_date_to_db(to_convert.baptism_date)
    db_person.baptism_place = to_convert.baptism_place
    db_person.baptism_note = to_convert.baptism_note
    db_person.baptism_src = to_convert.baptism_src

    death_status, death_reason, death_date = convert_death_status_to_db(
        to_convert.death_status
    )
    db_person.death_status = death_status
    db_person.death_reason = death_reason
    db_person.death_date_obj = death_date
    db_person.death_place = to_convert.death_place
    db_person.death_note = to_convert.death_note
    db_person.death_src = to_convert.death_src

    burial_status, burial_date = convert_burial_status_to_db(
        to_convert.burial
    )
    db_person.burial_status = burial_status
    db_person.burial_date_obj = burial_date
    db_person.burial_place = to_convert.burial_place
    db_person.burial_note = to_convert.burial_note
    db_person.burial_src = to_convert.burial_src

    db_person.ascend_id = ascend_id
    db_person.families_id = families_id

    titles = [convert_title_to_db(t) for t in to_convert.titles]

    non_native_relations = [
        convert_relation_to_db(r)
        for r in to_convert.non_native_parents_relation
    ]

    related_persons = []
    for person_id in to_convert.related_persons:
        db_relation = database.person_relations.PersonRelations()
        db_relation.related_person_id = person_id
        related_persons.append(db_relation)

    personal_events_and_witnesses = []
    for event in to_convert.personal_events:
        db_event, db_witnesses = convert_personal_event_to_db(event)
        personal_events_and_witnesses.append((db_event, db_witnesses))

    return (
        db_person,
        titles,
        non_native_relations,
        related_persons,
        personal_events_and_witnesses
    )
