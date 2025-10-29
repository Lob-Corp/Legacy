"""
Route and helpers for the add_family page in Geneweb Flask app.
All helper functions are at module level for clarity and testability.
"""
from flask import (
    render_template, request, current_app, jsonify, redirect, url_for, g, abort
)
from pprint import pformat
from .db_utils import get_db_service
from typing import Optional, List


# --- Helper functions for add_family route ---
def get_first(form_data, single_key: str, default: str = "") -> str:
    """Get the first value for a form field, or default if missing."""
    vals = form_data.get(single_key)
    return vals[0] if vals and len(vals) > 0 else default


def parse_int(value: str, default: int = 0) -> int:
    """Parse an integer from a string, or return default on failure."""
    try:
        return int(value)
    except Exception:
        return default


def parse_calendar_date(form_data, prefix: str):
    """
    Build a CalendarDate from fields like <prefix>_dd/mm/yyyy.
    Returns None if year is empty or 0.
    """
    from libraries.date import Calendar, DateValue, Sure, CalendarDate
    dd = get_first(form_data, f"{prefix}_dd").strip()
    mm = get_first(form_data, f"{prefix}_mm").strip()
    yyyy = get_first(form_data, f"{prefix}_yyyy").strip()
    if not yyyy:
        return None
    day = parse_int(dd, 0) if dd else 0
    month = parse_int(mm, 0) if mm else 0
    year = parse_int(yyyy, 0)
    if year == 0:
        return None
    dv = DateValue(day=day, month=month, year=year, prec=Sure(), delta=0)
    return CalendarDate(dmy=dv, cal=Calendar.GREGORIAN)


def parse_sex(sex_str: str):
    """Parse sex from form value (M/F/N)."""
    from libraries.person import Sex
    sex_str = sex_str.strip().upper()
    if sex_str == 'M':
        return Sex.MALE
    elif sex_str == 'F':
        return Sex.FEMALE
    return Sex.NEUTER


def ensure_person(form_data, db_service, person_repo, pa_idx: int) -> int:
    """
    Create or link a parent person and return its database id.
    pa_idx is 1 or 2.
    """
    from libraries.person import Sex, Person as LibPerson
    from libraries.title import AccessRight
    from libraries.consanguinity_rate import ConsanguinityRate
    from libraries.family import Ascendants
    from libraries.death_info import NotDead, Dead, DeathReason, UnknownBurial
    sel = get_first(form_data, f"pa{pa_idx}_p", "create")
    fn = get_first(form_data, f"pa{pa_idx}_fn").strip()
    sn = get_first(form_data, f"pa{pa_idx}_sn").strip()
    occ = parse_int(get_first(form_data, f"pa{pa_idx}_occ", "0"), 0)
    occ = 0 if occ is None else occ
    if sel == 'link':
        from database.person import Person as DBPerson
        session = db_service.get_session()
        try:
            match = db_service.get(session, DBPerson, {
                'first_name': fn,
                'surname': sn,
                'occ': occ,
            })
            if not match:
                raise ValueError(
                    f"No existing person found to link: {fn} {sn} (occ={occ})")
            return match.id
        finally:
            session.close()
    sex = Sex.MALE if pa_idx == 1 else Sex.FEMALE
    birth_date = parse_calendar_date(form_data, f"pa{pa_idx}b")
    birth_place = get_first(form_data, f"pa{pa_idx}b_pl")
    death_date = parse_calendar_date(form_data, f"pa{pa_idx}d")
    death_place = get_first(form_data, f"pa{pa_idx}d_pl")
    occupation = get_first(form_data, f"pa{pa_idx}_occu")
    if death_date:
        death_status = Dead(
            death_reason=DeathReason.UNSPECIFIED, date_of_death=death_date)
    else:
        death_status = NotDead()
    lib_person = LibPerson[
        int, int, str, int
    ](
        index=0,
        first_name=fn,
        surname=sn,
        occ=occ,
        image="",
        public_name="",
        qualifiers=[],
        aliases=[],
        first_names_aliases=[],
        surname_aliases=[],
        titles=[],
        non_native_parents_relation=[],
        related_persons=[],
        occupation=occupation,
        sex=sex,
        access_right=AccessRight.PUBLIC,
        birth_date=birth_date,
        birth_place=birth_place,
        birth_note="",
        birth_src="",
        baptism_date=None,
        baptism_place="",
        baptism_note="",
        baptism_src="",
        death_status=death_status,
        death_place=death_place,
        death_note="",
        death_src="",
        burial=UnknownBurial(),
        burial_place="",
        burial_note="",
        burial_src="",
        personal_events=[],
        notes="",
        src="",
        ascend=Ascendants[int](
            parents=None,
            consanguinity_rate=ConsanguinityRate.from_integer(0)
        ),
        families=[]
    )
    person_repo.add_person(lib_person)
    from database.person import Person as DBPerson
    session = db_service.get_session()
    try:
        created = db_service.get(session, DBPerson, {
            'first_name': fn,
            'surname': sn,
            'occ': occ,
        })
        if not created:
            raise RuntimeError("Failed to create person in database")
        return created.id
    finally:
        session.close()


def ensure_child(form_data,
                 db_service,
                 person_repo,
                 ch_idx: int) -> Optional[int]:
    """
    Create or link a child person and return its database id.
    Returns None if no name provided.
    """
    from libraries.person import Sex, Person as LibPerson
    from libraries.title import AccessRight
    from libraries.consanguinity_rate import ConsanguinityRate
    from libraries.family import Ascendants
    from libraries.death_info import NotDead, UnknownBurial
    sel = get_first(form_data, f"ch{ch_idx}_p", "create")
    fn = get_first(form_data, f"ch{ch_idx}_fn").strip()
    sn = get_first(form_data, f"ch{ch_idx}_sn").strip()
    if not fn and not sn:
        return None
    occ = parse_int(get_first(form_data, f"ch{ch_idx}_occ", "0"), 0)
    sex_str = get_first(form_data, f"ch{ch_idx}_sex", "N")
    sex = parse_sex(sex_str)
    if sel == 'link':
        from database.person import Person as DBPerson
        session = db_service.get_session()
        try:
            match = db_service.get(session, DBPerson, {
                'first_name': fn,
                'surname': sn,
                'occ': occ,
            })
            if match:
                return match.id
        finally:
            session.close()
    birth_date = parse_calendar_date(form_data, f"ch{ch_idx}b")
    birth_place = get_first(form_data, f"ch{ch_idx}b_pl")
    lib_person = LibPerson[int, int, str, int](
        index=0,
        first_name=fn,
        surname=sn,
        occ=occ,
        image="",
        public_name="",
        qualifiers=[],
        aliases=[],
        first_names_aliases=[],
        surname_aliases=[],
        titles=[],
        non_native_parents_relation=[],
        related_persons=[],
        occupation="",
        sex=sex,
        access_right=AccessRight.PUBLIC,
        birth_date=birth_date,
        birth_place=birth_place,
        birth_note="",
        birth_src="",
        baptism_date=None,
        baptism_place="",
        baptism_note="",
        baptism_src="",
        death_status=NotDead(),
        death_place="",
        death_note="",
        death_src="",
        burial=UnknownBurial(),
        burial_place="",
        burial_note="",
        burial_src="",
        personal_events=[],
        notes="",
        src="",
        ascend=Ascendants[int](
            parents=None,
            consanguinity_rate=ConsanguinityRate.from_integer(0)
        ),
        families=[]
    )
    person_repo.add_person(lib_person)
    from database.person import Person as DBPerson
    session = db_service.get_session()
    try:
        created = db_service.get(session, DBPerson, {
            'first_name': fn,
            'surname': sn,
            'occ': occ,
        })
        if not created:
            raise RuntimeError(f"Failed to create child person: {fn} {sn}")
        return created.id
    finally:
        session.close()


def parse_witness(form_data,
                  db_service,
                  person_repo,
                  event_idx: int,
                  witness_idx: int):
    """
    Parse a witness from form fields e{event_idx}_witn{witness_idx}_*.
    Returns (person_id, witness_kind) or None.
    """
    from libraries.person import Person as LibPerson
    from libraries.title import AccessRight
    from libraries.consanguinity_rate import ConsanguinityRate
    from libraries.family import Ascendants
    from libraries.death_info import NotDead, UnknownBurial
    from libraries.events import EventWitnessKind
    fn = get_first(form_data, f"e{event_idx}_witn{witness_idx}_fn").strip()
    sn = get_first(form_data, f"e{event_idx}_witn{witness_idx}_sn").strip()
    if not fn and not sn:
        return None
    occ = parse_int(
        get_first(form_data, f"e{event_idx}_witn{witness_idx}_occ", "0"), 0)
    sex_str = get_first(form_data, f"e{event_idx}_witn{witness_idx}_sex", "N")
    sex = parse_sex(sex_str)
    kind_str = get_first(
        form_data,
        f"e{event_idx}_witn{witness_idx}_kind", "witness"
    ).strip().upper()
    kind_map = {
        'WITNESS': EventWitnessKind.WITNESS,
        'WITNESS_GODPARENT': EventWitnessKind.WITNESS_GODPARENT,
        'WITNESS_CIVILOFFICER': EventWitnessKind.WITNESS_CIVILOFFICER,
        'WITNESS_RELIGIOUSOFFICER': EventWitnessKind.WITNESS_RELIGIOUSOFFICER,
        'WITNESS_INFORMANT': EventWitnessKind.WITNESS_INFORMANT,
        'WITNESS_ATTENDING': EventWitnessKind.WITNESS_ATTENDING,
        'WITNESS_MENTIONED': EventWitnessKind.WITNESS_MENTIONED,
        'WITNESS_OTHER': EventWitnessKind.WITNESS_OTHER,
    }
    witness_kind = kind_map.get(kind_str, EventWitnessKind.WITNESS)
    from database.person import Person as DBPerson
    session = db_service.get_session()
    try:
        match = db_service.get(session, DBPerson, {
            'first_name': fn,
            'surname': sn,
            'occ': occ,
        })
        if match:
            return (match.id, witness_kind)
    finally:
        session.close()
    lib_person = LibPerson[int, int, str, int](
        index=0,
        first_name=fn,
        surname=sn,
        occ=occ,
        image="",
        public_name="",
        qualifiers=[],
        aliases=[],
        first_names_aliases=[],
        surname_aliases=[],
        titles=[],
        non_native_parents_relation=[],
        related_persons=[],
        occupation="",
        sex=sex,
        access_right=AccessRight.PUBLIC,
        birth_date=None,
        birth_place="",
        birth_note="",
        birth_src="",
        baptism_date=None,
        baptism_place="",
        baptism_note="",
        baptism_src="",
        death_status=NotDead(),
        death_place="",
        death_note="",
        death_src="",
        burial=UnknownBurial(),
        burial_place="",
        burial_note="",
        burial_src="",
        personal_events=[],
        notes="",
        src="",
        ascend=Ascendants[int](
            parents=None,
            consanguinity_rate=ConsanguinityRate.from_integer(0)
        ),
        families=[]
    )
    person_repo.add_person(lib_person)
    session = db_service.get_session()
    try:
        created = db_service.get(session, DBPerson, {
            'first_name': fn,
            'surname': sn,
            'occ': occ,
        })
        if not created:
            raise RuntimeError(f"Failed to create witness: {fn} {sn}")
        return (created.id, witness_kind)
    finally:
        session.close()


def parse_family_event(form_data, db_service, person_repo, event_idx: int):
    """
    Parse a family event from form fields e{event_idx}_*.
    Returns FamilyEvent or None.
    """
    from libraries.events import (
        FamilyEvent, FamMarriage, FamNoMarriage, FamEngage,
        FamDivorce, FamSeparated, FamAnnulation,
        FamMarriageBann, FamMarriageContract, FamMarriageLicense,
        FamPACS, FamResidence, FamNamedEvent
    )
    event_name_str = get_first(form_data, f"e_name{event_idx}").strip()
    if not event_name_str:
        return None
    event_date = parse_calendar_date(form_data, f"e{event_idx}")
    if event_date is None:
        return None
    event_map = {
        '#marr': FamMarriage(),
        'marriage': FamMarriage(),
        'not married': FamNoMarriage(),
        'no sexes check (no married)': FamNoMarriage(),
        'engaged': FamEngage(),
        'divorce': FamDivorce(),
        'separated': FamSeparated(),
        'annulation': FamAnnulation(),
        'marriage bann': FamMarriageBann(),
        'marriage contract': FamMarriageContract(),
        'marriage license': FamMarriageLicense(),
        'civil union': FamPACS(),
        'pacs': FamPACS(),
        'residence': FamResidence(),
    }
    event_name_lower = event_name_str.lower()
    event_name = event_map.get(event_name_lower, FamNamedEvent(event_name_str))
    event_place = get_first(form_data, f"e{event_idx}_pl")
    event_note = get_first(form_data, f"e{event_idx}_note")
    event_src = get_first(form_data, f"e{event_idx}_src")
    witnesses = []
    for wit_idx in range(1, 11):
        witness = parse_witness(form_data, db_service,
                                person_repo, event_idx, wit_idx)
        if witness:
            witnesses.append(witness)
    return FamilyEvent[int, str](
        name=event_name,
        date=event_date,
        place=event_place,
        reason="",
        note=event_note,
        src=event_src,
        witnesses=witnesses
    )


def implem_route_ADD_FAM(base, lang='en'):
    """
    Handle GET and POST requests for the add_family page.
    On POST, parses form data and stores a new family in the database.
    """
    g.locale = lang
    num_children = 1
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=False)
        files_info = {k: v.filename for k, v in request.files.items()}
        try:
            db_service = get_db_service(base)
        except FileNotFoundError as e:
            msg = str(e)
            if request.accept_mimetypes.best == 'application/json':
                return jsonify({'ok': False, 'error': msg}), 404
            abort(404, description=msg)
        from repositories.person_repository import PersonRepository
        from repositories.family_repository import FamilyRepository
        from libraries.family import (
            Family as LibFamily, Parents
            as LibParents, MaritalStatus, NotDivorced
        )
        from libraries.events import FamilyEvent
        person_repo = PersonRepository(db_service)
        family_repo = FamilyRepository(db_service)
        # Build or link both parents
        try:
            father_id = ensure_person(form_data, db_service, person_repo, 1)
            mother_id = ensure_person(form_data, db_service, person_repo, 2)
        except Exception as e:
            if request.accept_mimetypes.best == 'application/json':
                return jsonify({'ok': False, 'error': str(e)}), 400
            abort(400, description=str(e))
        # Parse children - extract child indices from form data dynamically
        children_ids: List[int] = []
        child_indices = set()
        for key in form_data.keys():
            if key.startswith('ch') and '_' in key:
                try:
                    idx_str = key[2:key.index('_')]
                    child_indices.add(int(idx_str))
                except (ValueError, IndexError):
                    continue
        for ch_idx in sorted(child_indices):
            try:
                child_id = ensure_child(
                    form_data, db_service, person_repo, ch_idx)
                if child_id:
                    children_ids.append(child_id)
            except Exception as e:
                current_app.logger.warning(
                    f"Failed to create child {ch_idx}: {e}")
                continue

        family_events: List[FamilyEvent] = []
        event_indices = set()
        for key in form_data.keys():
            if key.startswith('e_name') \
                    or (key.startswith('e')
                        and '_' in key and not key.startswith('e_')):
                try:
                    if key.startswith('e_name'):
                        idx_str = key[6:]
                    else:
                        idx_str = key[1:key.index('_')]
                    event_indices.add(int(idx_str))
                except (ValueError, IndexError):
                    continue
        for evt_idx in sorted(event_indices):
            try:
                event = parse_family_event(
                    form_data, db_service, person_repo, evt_idx)
                if event:
                    family_events.append(event)
            except Exception as e:
                current_app.logger.warning(
                    f"Failed to parse event {evt_idx}: {e}")
                continue

        # Determine family relation kind from event selector if available
        rel_kind = MaritalStatus.NO_MENTION
        raw_event = get_first(form_data, 'e_name1') or ''
        raw_event = raw_event.strip().lower()
        if raw_event in ('#marr', 'marriage'):
            rel_kind = MaritalStatus.MARRIED
        elif raw_event in ('not married', 'no sexes check (no married)'):
            rel_kind = MaritalStatus.NOT_MARRIED
        elif raw_event == 'engaged':
            rel_kind = MaritalStatus.ENGAGED
        elif raw_event == 'civil union':
            rel_kind = MaritalStatus.PACS
        elif raw_event == 'residence':
            rel_kind = MaritalStatus.RESIDENCE

        # Compute a new family index (next id) by querying max existing id
        from database.family import Family as DBFamily
        session = db_service.get_session()
        try:
            max_id = 0
            q = session.query(DBFamily).order_by(DBFamily.id.desc()).first()
            if q is not None and q.id is not None:
                max_id = int(q.id)
        finally:
            session.close()
        new_family_id = max_id + 1

        # Parse marriage date and place (from first event if it's a marriage)
        marriage_date = None
        marriage_place = ""
        if family_events and hasattr(family_events[0].name, '__class__') \
                and family_events[0].name.__class__.__name__ == 'FamMarriage':
            marriage_date = family_events[0].date
            marriage_place = family_events[0].place

        # Build library Family object with children and events
        lib_family = LibFamily[
            int, int, str
        ](
            index=new_family_id,
            marriage_date=marriage_date,
            marriage_place=marriage_place,
            marriage_note="",
            marriage_src="",
            witnesses=[],
            relation_kind=rel_kind,
            divorce_status=NotDivorced(),
            family_events=family_events,
            comment="",
            origin_file="",
            src="",
            parents=LibParents.from_couple(father_id, mother_id),
            children=children_ids,
        )

        # Persist family
        try:
            family_repo.add_family(lib_family)
        except Exception as e:
            if request.accept_mimetypes.best == 'application/json':
                return jsonify({'ok': False, 'error': str(e)}), 400
            abort(400, description=str(e))

        # Logging and response
        try:
            current_app.logger.info(
                "ADD_FAM submitted for base=%s lang=%s: %d fields, %d files",
                base, lang, len(form_data), len(files_info)
            )
            current_app.logger.debug("Fields: %s", sorted(form_data.keys()))
            current_app.logger.info(
                "ADD_FAM form fields:\n%s", pformat(form_data))
            current_app.logger.info("ADD_FAM files:\n%s", pformat(files_info))
        except Exception:
            print("[ADD_FAM] form submitted:")
            try:
                print(pformat(form_data))
                print("Files:", pformat(files_info))
            except Exception:
                print(list(form_data.keys()), files_info)

        if request.accept_mimetypes.best == 'application/json':
            return jsonify({
                'ok': True,
                'base': base,
                'lang': lang,
                'fields': form_data,
                'files': files_info,
                'family_id': new_family_id,
            })

        return redirect(
            url_for('gwd.route_ADD_FAM', base=base, lang=lang,
                    submitted=1, count=len(form_data))
        )

    # GET: render the form. If redirected after a POST, read the query
    # parameters to show a submission confirmation if needed.
    submitted = request.args.get('submitted') is not None
    submitted_count = request.args.get('count', default=0, type=int)
    return render_template(
        'gwd/add_family.html',
        base=base,
        lang=lang,
        submitted=submitted,
        submitted_count=submitted_count,
        num_children=num_children,
    )
