"""
Implementation of the MOD_IND route - Individual modification page.
"""

from flask import render_template, request, g, redirect, url_for, jsonify
from typing import Union
from datetime import date
from typing import Optional, Dict, Any, List, Tuple
import hashlib
import json
from .db_utils import get_db_service
from database.sqlite_database_service import SQLiteDatabaseService
from repositories.person_repository import PersonRepository
import libraries.person as app_person
import libraries.date as app_date
import libraries.death_info as death_info
import libraries.burial_info as burial_info
import libraries.title as app_title
import libraries.events as app_events
import libraries.family as app_family


def find_person_by_name(
    person_repo: PersonRepository, first_name: str, surname: str, occ: int
) -> Optional[int]:
    """
    Find a person ID by their name, surname, and occurrence number.
    Returns None if not found.
    """
    try:
        all_persons = person_repo.get_all_persons()
        for person in all_persons:
            if (
                person.first_name == first_name
                and person.surname == surname
                and person.occ == occ
            ):
                return person.index
        return None
    except Exception:
        return None


def parse_calendar_date(
    form_data: Dict, prefix: str
) -> Optional[app_date.CompressedDate]:
    """
    Parse a calendar date from form data.

    Args:
        form_data: Dictionary containing form data
        prefix: Prefix for the date fields (e.g., 'birth', 'e_date0', 'e4')

    Returns:
        CalendarDate or None if no date provided
    """
    day = form_data.get(f"{prefix}_dd", "").strip()
    month = form_data.get(f"{prefix}_mm", "").strip()
    year = form_data.get(f"{prefix}_yyyy", "").strip()
    calendar = form_data.get(f"{prefix}_cal", "gregorian").strip()
    precision = form_data.get(f"{prefix}_prec", "").strip()

    # If year is empty or 0, no date
    if not year or year == "0":
        return None

    try:
        year_int = int(year)
        month_int = int(month) if month else 0
        day_int = int(day) if day else 0

        # Map calendar string to enum
        calendar_map = {
            "gregorian": app_date.Calendar.GREGORIAN,
            "julian": app_date.Calendar.JULIAN,
            "french_republican": app_date.Calendar.FRENCH,
            "hebrew": app_date.Calendar.HEBREW,
        }
        cal_enum = calendar_map.get(calendar, app_date.Calendar.GREGORIAN)

    # Map precision string to precision object
    # (default to Sure if year provided)
        prec_obj = app_date.Sure()
        if precision == "about":
            prec_obj = app_date.About()
        elif precision == "maybe":
            prec_obj = app_date.Maybe()
        elif precision == "before":
            prec_obj = app_date.Before()
        elif precision == "after":
            prec_obj = app_date.After()
        elif precision == "sure" or precision == "":
            prec_obj = app_date.Sure()

        return app_date.CalendarDate(
            dmy=app_date.DateValue(
                day=day_int if day_int > 0 else 1,
                month=month_int if month_int > 0 else 1,
                year=year_int,
                prec=prec_obj,
                delta=0,
            ),
            cal=cal_enum,
        )
    except (ValueError, AttributeError):
        return None


def parse_date_with_fallback(
    form_data: Dict, *prefixes: str
) -> Optional[app_date.CompressedDate]:
    """
    Try to parse a date using multiple prefix patterns.
    Returns the first valid date found, or None if no date is found.

    Args:
        form_data: Dictionary containing form data
        *prefixes: Variable number of prefixes to try(e.g., 'birth', 'e_date0')

    Returns:
        CalendarDate or None
    """
    for prefix in prefixes:
        result = parse_calendar_date(form_data, prefix)
        if result is not None:
            return result
    return None


def parse_witness_from_form(
    form_data: Dict,
    event_identifier: Union[str, int],
    witness_num: int,
    person_repo: PersonRepository,
) -> Optional[Tuple[int, app_events.EventWitnessKind]]:
    """
    Parse a witness from form data and return (person_id, witness_kind).

    Args:
        event_identifier: Either a number (e.g., "0") for custom events or
                         a string (e.g., "birth", "baptism", "death", "burial")
        witness_num: The witness index for this event
        person_repo: Repository to create/find persons

    If witness action is 'link', finds existing person.
    If witness action is 'create', creates new person.
    """
    # Handle both numeric and string event identifiers
    if isinstance(event_identifier, int) or event_identifier.isdigit():
        prefix = f"e{event_identifier}_witn{witness_num}"
    else:
        # For life events like 'birth', 'baptism', etc.
        prefix = f"{event_identifier}_witn{witness_num}"

    # Check if witness exists in form. Support linking by id directly
    # (e.g., ..._index or ..._id) without requiring a first name.
    first_name = form_data.get(f"{prefix}_fn", "").strip()
    id_keys = [f"{prefix}_index", f"{prefix}_id", f"{prefix}_person_id"]
    id_str = ""
    for k in id_keys:
        if k in form_data:
            id_str = form_data.get(k, "").strip()
            if id_str:
                break
    # If neither id nor first_name are present, there's no witness here
    if not first_name and not id_str:
        return None

    surname = form_data.get(f"{prefix}_sn", "").strip()
    occ_str = form_data.get(f"{prefix}_occ", "0").strip()
    occ = int(occ_str) if occ_str.isdigit() else 0

    action_raw = form_data.get(f"{prefix}_p", "create").strip().lower()
    # Normalize action values from various UIs
    if action_raw in {"link", "l", "existing", "exist", "use", "id"}:
        action = "link"
    elif action_raw in {"create", "c", "new", "add"}:
        action = "create"
    else:
        action = "create"
    kind_str = form_data.get(f"{prefix}_kind", "WITNESS").strip()
    # Map kind string from either enum name or UI short codes
    # to enum; default to WITNESS
    kind_map = {
        "": app_events.EventWitnessKind.WITNESS,
        "WITNESS": app_events.EventWitnessKind.WITNESS,
        "godp": app_events.EventWitnessKind.WITNESS_GODPARENT,
        "info": app_events.EventWitnessKind.WITNESS_INFORMANT,
        "atte": app_events.EventWitnessKind.WITNESS_ATTENDING,
        "ment": app_events.EventWitnessKind.WITNESS_MENTIONED,
        "offi": app_events.EventWitnessKind.WITNESS_CIVILOFFICER,
        "reli": app_events.EventWitnessKind.WITNESS_RELIGIOUSOFFICER,
        "othe": app_events.EventWitnessKind.WITNESS_OTHER,
    }
    witness_kind = kind_map.get(kind_str)
    if witness_kind is None:
        # Try enum name direct access, else fallback
        try:
            witness_kind = app_events.EventWitnessKind[kind_str]
        except KeyError:
            # Backwards compatibility: map generic OFFICER to CIVILOFFICER
            if kind_str == "WITNESS_OFFICER":
                witness_kind = app_events.EventWitnessKind.WITNESS_CIVILOFFICER
            else:
                witness_kind = app_events.EventWitnessKind.WITNESS

    person_id = None

    # If id is provided, use it directly
    if id_str and id_str.isdigit() and int(id_str) > 0:
        return (int(id_str), witness_kind)

    if action == "link":
        # Try to find existing person
        person_id = find_person_by_name(person_repo, first_name, surname, occ)
        if person_id is None:
            # Person not found, create new one
            action = "create"

    if action == "create" or person_id is None:
        # Create new person
        sex_str = form_data.get(f"{prefix}_sex", "U").strip()
        sex_map = {
            "M": app_person.Sex.MALE,
            "F": app_person.Sex.FEMALE,
            "U": app_person.Sex.NEUTER,
        }
        sex = sex_map.get(sex_str, app_person.Sex.NEUTER)

        occupation = form_data.get(f"{prefix}_occu", "").strip()

        # Create minimal person
        new_person = app_person.Person(
            index=None,  # Let DB autogenerate ID
            first_name=first_name,
            surname=surname,
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
            access_right=app_title.AccessRight.PUBLIC,
            birth_date=None,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_date=None,
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=death_info.DontKnowIfDead(),
            death_place="",
            death_note="",
            death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="",
            burial_note="",
            burial_src="",
            personal_events=[],
            notes="",
            src="",
            ascend=app_family.Ascendants(
                parents=None,
                consanguinity_rate=None
            ),
            families=[],
        )

        created = person_repo.add_person(new_person)
        # Prefer id from returned object when available
        if hasattr(created, "index") and created.index:
            person_id = created.index
        else:
            # Fallback: search by name/occ
            person_id = find_person_by_name(
                person_repo, first_name, surname, occ
            )

    if person_id is not None:
        return (person_id, witness_kind)

    return None


def get_first_value(form_data: Dict, keys: List[str]) -> str:
    """Return first non-empty string among the provided keys from form_data."""
    for k in keys:
        if k in form_data:
            val = form_data.get(k, "").strip()
            if val != "":
                return val
    # If present but empty, return empty to allow presence detection
    for k in keys:
        if k in form_data:
            return ""
    return ""


def convert_person_to_template_context(
    person_obj: app_person.Person,
    person_repo: Optional[PersonRepository] = None,
) -> Dict[str, Any]:
    """Convert a Person object from the repository to
    template context format.

    """

    def date_to_dict(d: Optional[app_date.CompressedDate]) -> Dict[str, str]:
        """Convert a date to template dictionary format."""
        if d is None:
            return {
                "day": "",
                "month": "",
                "year": "",
                "calendar": "gregorian",
                "precision": "",
            }

        if isinstance(d, app_date.CalendarDate):
            calendar_map = {
                app_date.Calendar.GREGORIAN: "gregorian",
                app_date.Calendar.JULIAN: "julian",
                app_date.Calendar.FRENCH: "french_republican",
                app_date.Calendar.HEBREW: "hebrew",
            }
            # Map precision class to UI string
            prec_obj = getattr(d.dmy, "prec", None)
            prec_value = ""
            if isinstance(prec_obj, app_date.Sure):
                prec_value = "sure"
            elif isinstance(prec_obj, app_date.About):
                prec_value = "about"
            elif isinstance(prec_obj, app_date.Maybe):
                prec_value = "maybe"
            elif isinstance(prec_obj, app_date.Before):
                prec_value = "before"
            elif isinstance(prec_obj, app_date.After):
                prec_value = "after"
            return {
                "day": str(d.dmy.day) if d.dmy.day > 0 else "",
                "month": str(d.dmy.month) if d.dmy.month > 0 else "",
                "year": str(d.dmy.year) if d.dmy.year > 0 else "",
                "calendar": calendar_map.get(d.cal, "gregorian"),
                "precision": prec_value,
            }
        return {
            "day": "",
            "month": "",
            "year": "",
            "calendar": "gregorian",
            "precision": "",
        }

    # Determine death status
    death_status = "alive"
    if isinstance(person_obj.death_status, death_info.Dead):
        # Preserve detailed death reason when available
        reason = getattr(person_obj.death_status, "death_reason", None)
        reason_map = {
            getattr(death_info.DeathReason, "KILLED", None): "killed",
            getattr(death_info.DeathReason, "MURDERED", None): "murdered",
            getattr(death_info.DeathReason, "EXECUTED", None): "executed",
            getattr(death_info.DeathReason, "DISAPPEARED", None):
            "disappeared",
            getattr(death_info.DeathReason, "UNSPECIFIED", None): "dead",
        }
        death_status = reason_map.get(reason, "dead")
    elif isinstance(person_obj.death_status, death_info.DeadYoung):
        death_status = "killed"
    elif isinstance(person_obj.death_status, death_info.DeadDontKnowWhen):
        death_status = "obviously_dead"
    elif isinstance(person_obj.death_status, death_info.DontKnowIfDead):
        death_status = "dont_know"
    elif isinstance(person_obj.death_status, death_info.OfCourseDead):
        death_status = "obviously_dead"

    # Extract death date
    death_date = None
    if isinstance(person_obj.death_status, death_info.Dead):
        death_date = person_obj.death_status.date_of_death

    # Determine burial type
    burial_type = "burial"
    burial_date = None
    if isinstance(person_obj.burial, burial_info.Burial):
        burial_type = "burial"
        burial_date = person_obj.burial.burial_date
    elif isinstance(person_obj.burial, burial_info.Cremated):
        burial_type = "cremated"
        burial_date = person_obj.burial.cremation_date

    sex_map = {
        app_person.Sex.MALE: "M",
        app_person.Sex.FEMALE: "F",
        app_person.Sex.NEUTER: "U",
    }

    access_map = {
        app_title.AccessRight.PUBLIC: "public",
        app_title.AccessRight.PRIVATE: "private",
        app_title.AccessRight.IFTITLES: "if_titles",
    }

    # Extract witnesses from personal events for life events and custom events
    def _witness_kind_to_slug(k: app_events.EventWitnessKind) -> str:
        mapping = {
            app_events.EventWitnessKind.WITNESS_GODPARENT: "godp",
            app_events.EventWitnessKind.WITNESS_INFORMANT: "info",
            app_events.EventWitnessKind.WITNESS_ATTENDING: "atte",
            app_events.EventWitnessKind.WITNESS_MENTIONED: "ment",
            app_events.EventWitnessKind.WITNESS_CIVILOFFICER: "offi",
            app_events.EventWitnessKind.WITNESS_RELIGIOUSOFFICER: "reli",
            app_events.EventWitnessKind.WITNESS_OTHER: "othe",
            app_events.EventWitnessKind.WITNESS: "",
        }
        return mapping.get(k, "")

    def build_witness_ctx(
        witness_id: int, kind: app_events.EventWitnessKind
    ) -> Dict[str, Any]:
        ctx: Dict[str, Any] = {
            "index": witness_id,
            "first_name": "",
            "surname": "",
            "occ": 0,
            "sex": "U",
            "occupation": "",
            "public": False,
            "kind": _witness_kind_to_slug(kind),
        }
        if person_repo is not None and witness_id:
            try:
                wp = person_repo.get_person_by_id(witness_id)
                ctx["first_name"] = wp.first_name or ""
                ctx["surname"] = wp.surname or ""
                ctx["occ"] = (
                    wp.occ if getattr(wp, "occ", None) is not None else 0
                )
                # optional enrichments
                ctx["sex"] = sex_map.get(
                    getattr(wp, "sex", app_person.Sex.NEUTER), "U"
                )
                ctx["occupation"] = getattr(wp, "occupation", "") or ""
            except Exception:
                pass
        return ctx

    birth_witnesses = []
    baptism_witnesses = []
    death_witnesses = []
    burial_witnesses = []
    custom_events = []

    for event in person_obj.personal_events:
        if isinstance(event.name, app_events.PersBirth):
            birth_witnesses = [
                build_witness_ctx(w[0], w[1]) for w in event.witnesses
            ]
        elif isinstance(event.name, app_events.PersBaptism):
            baptism_witnesses = [
                build_witness_ctx(w[0], w[1]) for w in event.witnesses
            ]
        elif isinstance(event.name, app_events.PersDeath):
            death_witnesses = [
                build_witness_ctx(w[0], w[1]) for w in event.witnesses
            ]
        elif isinstance(
            event.name, (app_events.PersBurial, app_events.PersCremation)
        ):
            burial_witnesses = [
                build_witness_ctx(w[0], w[1]) for w in event.witnesses
            ]
        else:
            # Custom event
            # Map event classes to template type codes
            if isinstance(event.name, app_events.PersResidence):
                event_type_code = "#resi"
            else:
                event_type_code = "#other"
            custom_events.append(
                {
                    "type": event_type_code,
                    "date": date_to_dict(event.date),
                    "place": event.place,
                    "note": event.note,
                    "source": event.src,
                    "witnesses": [
                        build_witness_ctx(w[0], w[1]) for w in event.witnesses
                    ],
                }
            )

    # Helper to build relation parent dict expected by template
    def build_relation_parent(parent_id: Optional[int]) -> Dict[str, Any]:
        # Default structure expected by the template UI
        parent_ctx: Dict[str, Any] = {
            "index": None,
            "first_name": "",
            "surname": "",
            # Use string '0' so Jinja conditionals treat it as truthy
            # and display 0
            "occ": "0",
            "action": "create",
            "occupation": "",
            "dead": False,
            "public": False,
        }
        if parent_id and isinstance(parent_id, int) and parent_id > 0:
            parent_ctx["index"] = parent_id
            parent_ctx["action"] = "link"
            # Enrich with data if repository available
            if person_repo is not None:
                try:
                    p = person_repo.get_person_by_id(parent_id)
                    parent_ctx["first_name"] = p.first_name or ""
                    parent_ctx["surname"] = p.surname or ""
                    # Always serialize occ as string; default to '0'
                    parent_ctx["occ"] = (
                        str(p.occ)
                        if getattr(p, "occ", None) is not None
                        else "0"
                    )
                    parent_ctx["occupation"] = p.occupation or ""
                except Exception:
                    # Ignore fetching errors; keep minimal context
                    pass
        return parent_ctx

    return {
        "id": person_obj.index,
        "index": person_obj.index,
        "first_name": person_obj.first_name,
        "surname": person_obj.surname,
        "number": str(person_obj.occ),
        "sex": sex_map.get(person_obj.sex, "U"),
        "public_name": person_obj.public_name,
        "image": person_obj.image,
        "access": access_map.get(person_obj.access_right, "public"),
        "nickname": person_obj.qualifiers[0] if person_obj.qualifiers else "",
        "sobriquets": person_obj.qualifiers,
        "alias": person_obj.aliases,
        "alt_first_names": person_obj.first_names_aliases,
        "surnames": person_obj.surname_aliases,
        "occupations":
        [person_obj.occupation] if person_obj.occupation else [],
        "source": person_obj.src,
        "death_status": death_status,
        "birth": {
            "date": date_to_dict(person_obj.birth_date),
            "place": person_obj.birth_place,
            "source": person_obj.birth_src,
            "note": person_obj.birth_note,
            "witnesses": birth_witnesses,
        },
        "baptism": {
            "date": date_to_dict(person_obj.baptism_date),
            "place": person_obj.baptism_place,
            "source": person_obj.baptism_src,
            "note": person_obj.baptism_note,
            "witnesses": baptism_witnesses,
        },
        "death": (
            {
                "date": date_to_dict(death_date),
                "place": person_obj.death_place,
                "source": person_obj.death_src,
                "note": person_obj.death_note,
                "age": "",
                "witnesses": death_witnesses,
            }
            if death_date
            else None
        ),
        "burial": (
            {
                "date": date_to_dict(burial_date),
                "place": person_obj.burial_place,
                "source": person_obj.burial_src,
                "note": person_obj.burial_note,
                "type": burial_type,
                "witnesses": burial_witnesses,
            }
            if burial_date
            else None
        ),
        "events": custom_events,
        "relations": [
            {
                # Ensure relation type is a string label the template expects
                "type": (
                    rel.type.value
                    if hasattr(rel.type, "value")
                    else str(rel.type)
                ),
                "father": build_relation_parent(
                    rel.father
                    if isinstance(rel.father, int) or rel.father is None
                    else None
                ),
                "mother": build_relation_parent(
                    rel.mother
                    if isinstance(rel.mother, int) or rel.mother is None
                    else None
                ),
                "sources": getattr(rel, "sources", ""),
            }
            for rel in (person_obj.non_native_parents_relation or [])
        ],
        "parents": {
            "father": (
                person_obj.ascend.parents.father
                if person_obj.ascend.parents
                else None
            ),
            "mother": (
                person_obj.ascend.parents.mother
                if person_obj.ascend.parents
                else None
            ),
        },
        "families": person_obj.families if person_obj.families else [],
        "titles": [
            {
                "name": (
                    title.title_name.title_name
                    if hasattr(title.title_name, "title_name")
                    else str(title.title_name)
                ),
                "ident": title.ident,
                "place": title.place,
                "date_start": date_to_dict(title.date_start),
                "date_end": date_to_dict(title.date_end),
                "nth": title.nth,
            }
            for title in person_obj.titles
        ],
        "notes": person_obj.notes,
    }


def handle_mod_individual_post(
    base: str,
    person_id: int,
    lang: str,
    person_repo: PersonRepository,
    db_service: SQLiteDatabaseService,
) -> Any:
    """
    Handle POST request for modifying an individual.

    Parses form data and updates the person in the database.
    """
    form_data = request.form.to_dict()

    # Handle delete action early
    action = form_data.get("action", "").strip().lower()
    if action == "delete" or form_data.get("delete", "").strip() in (
        "1",
        "true",
        "yes",
    ):
        try:
            person_repo.delete_person(person_id)
        except Exception as e:
            if (
                request.accept_mimetypes.accept_json
                and not request.accept_mimetypes.accept_html
            ):
                return jsonify({"ok": False, "error": str(e)}), 400
            return f"Error deleting person: {str(e)}", 400

        if (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            return jsonify(
                {"ok": True, "deleted": True, "person_id": person_id}
            )
        # No index route yet; return a simple confirmation page
        return f"Person {person_id} deleted from base '{base}'."

    # Print POST data for debugging
    print("=" * 80)
    print("POST DATA RECEIVED:")
    print("=" * 80)
    for key, value in sorted(form_data.items()):
        print(f"{key}: {value}")
    print("=" * 80)

    # Get existing person
    try:
        existing_person = person_repo.get_person_by_id(person_id)
    except ValueError:
        if (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            return (
                jsonify(
                    {
                        "ok": False,
                        "error": f"Person with id {person_id} not found",
                    }
                ),
                404,
            )
        return f"Person with id {person_id} not found", 404

    # Parse basic fields
    first_name = form_data.get("first_name", "").strip()
    surname = form_data.get("surname", "").strip()
    occ = int(form_data.get("number", "0") or "0")

    sex_map = {
        "M": app_person.Sex.MALE,
        "F": app_person.Sex.FEMALE,
        "U": app_person.Sex.NEUTER,
    }
    sex = sex_map.get(form_data.get("sex", "U"), app_person.Sex.NEUTER)

    access_map = {
        "public": app_title.AccessRight.PUBLIC,
        "private": app_title.AccessRight.PRIVATE,
        "if_titles": app_title.AccessRight.IFTITLES,
    }
    access_right = access_map.get(
        form_data.get("access", "public"), app_title.AccessRight.PUBLIC
    )

    # Parse lists
    sobriquets = []
    i = 0
    while f"sobriquet_{i}" in form_data:
        val = form_data.get(f"sobriquet_{i}", "").strip()
        if val:
            sobriquets.append(val)
        i += 1

    aliases = []
    i = 0
    while f"alias_{i}" in form_data:
        val = form_data.get(f"alias_{i}", "").strip()
        if val:
            aliases.append(val)
        i += 1

    alt_first_names = []
    i = 0
    while f"alt_first_name_{i}" in form_data:
        val = form_data.get(f"alt_first_name_{i}", "").strip()
        if val:
            alt_first_names.append(val)
        i += 1

    alt_surnames = []
    i = 0
    while f"surname_alias_{i}" in form_data:
        val = form_data.get(f"surname_alias_{i}", "").strip()
        if val:
            alt_surnames.append(val)
        i += 1

    occupations = []
    i = 0
    while f"occupation_{i}" in form_data:
        val = form_data.get(f"occupation_{i}", "").strip()
        if val:
            occupations.append(val)
        i += 1
    occupation = occupations[0] if occupations else ""

    # Parse titles (support title_{i}_*, title{i}_*, and _t_* patterns)
    titles = []
    for i in range(0, 50):
        title_name_str = get_first_value(
            form_data,
            [f"title_{i}_name", f"title{i}_name", f"t_name{i}", f"_t_name{i}"]
        )
        ident = get_first_value(
            form_data,
            [
                f"title_{i}_ident",
                f"title{i}_ident",
                f"t_ident{i}",
                f"_t_ident{i}"
            ]
        )
        place = get_first_value(
            form_data,
            [
                f"title_{i}_place",
                f"title{i}_place",
                f"t_place{i}",
                f"_t_place{i}"
            ]
        )
        date_start = parse_date_with_fallback(
            form_data,
            f"title_{i}_start",
            f"title{i}_start",
            f"t_date_start{i}",
            f"_t_date_start{i}",
        )
        date_end = parse_date_with_fallback(
            form_data,
            f"title_{i}_end",
            f"title{i}_end",
            f"t_date_end{i}",
            f"_t_date_end{i}"
        )
        nth_str = get_first_value(
            form_data,
            [f"title_{i}_nth", f"title{i}_nth", f"t_nth{i}", f"_t_nth{i}"]
        )

        has_any_title_data = any(
            [title_name_str, ident, place, date_start, date_end, nth_str]
        )
        if not has_any_title_data:
            continue

        if title_name_str == "main":
            title_name = app_title.UseMainTitle()
        elif title_name_str:
            title_name = app_title.TitleName(title_name=title_name_str)
        else:
            title_name = app_title.NoTitle()

        try:
            nth = int(nth_str) if nth_str else 0
        except ValueError:
            nth = 0

        # Ensure date_start is not None for database constraints
        # If date_start is None, create an empty/minimal date (year 1)
        # Note: year 0 is treated as None by convert_date_to_db
        if date_start is None:
            from libraries.precision import Sure
            from libraries.calendar_date import Calendar

            date_start = app_date.CalendarDate(
                dmy=app_date.DateValue(
                    day=0, month=0, year=1, prec=Sure(), delta=0
                ),
                cal=Calendar.GREGORIAN,
            )
        # date_end can remain None if not specified (title still current)

        title = app_title.Title(
            title_name=title_name,
            ident=ident,
            place=place,
            date_start=date_start,
            date_end=date_end,
            nth=nth,
        )
        titles.append(title)

    # Parse relations (non-native parents).
    # Support both relation_{i}_* and r{i}_* patterns
    relations = []

    def parse_relation_parent(idx: int, role: str) -> Optional[int]:
        """Parse a relation parent (father/mother) either by direct id
        or by create/link fields.

        """
        # Direct ID if provided
        id_key_variants = (
            [f"relation_{idx}_father", f"relation_{idx}_mother"]
            if role == "fath"
            else [f"relation_{idx}_mother", f"relation_{idx}_father"]
        )
        for key in id_key_variants:
            pid = form_data.get(key, "").strip()
            if pid and pid.isdigit() and int(pid) > 0:
                return int(pid)

        # Create/Link via r{idx}_{role}_*
        action = form_data.get(f"r{idx}_{role}_p", "").strip() or "create"
        fn = form_data.get(f"r{idx}_{role}_fn", "").strip()
        sn = form_data.get(f"r{idx}_{role}_sn", "").strip()
        occ_str = form_data.get(f"r{idx}_{role}_occ", "0").strip()
        occ = int(occ_str) if occ_str.isdigit() else 0

        if not fn:  # no data
            return None

        if action == "link":
            pid = find_person_by_name(person_repo, fn, sn, occ)
            if pid is not None:
                return pid
            # fallback to create

        # Create new minimal person
        default_sex = "M" if role == "fath" else "F"
        sex_str = (
            form_data.get(f"r{idx}_{role}_sex", default_sex).strip()
            or default_sex
        )
        sex_map = {
            "M": app_person.Sex.MALE,
            "F": app_person.Sex.FEMALE,
            "U": app_person.Sex.NEUTER,
        }
        sex_val = sex_map.get(
            sex_str,
            app_person.Sex.MALE if role == "fath" else app_person.Sex.FEMALE,
        )
        occupation = form_data.get(f"r{idx}_{role}_occu", "").strip()

        new_parent = app_person.Person(
            index=None,
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
            sex=sex_val,
            access_right=app_title.AccessRight.PUBLIC,
            birth_date=None,
            birth_place="",
            birth_note="",
            birth_src="",
            baptism_date=None,
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=death_info.DontKnowIfDead(),
            death_place="",
            death_note="",
            death_src="",
            burial=burial_info.UnknownBurial(),
            burial_place="",
            burial_note="",
            burial_src="",
            personal_events=[],
            notes="",
            src="",
            ascend=app_family.Ascendants(
                parents=None, consanguinity_rate=None
            ),
            families=[],
        )
        person_repo.add_person(new_parent)
        return find_person_by_name(person_repo, fn, sn, occ)

    for i in range(0, 50):
        rel_type_str = get_first_value(
            form_data, [f"relation_{i}_type", f"r{i}_type"]
        )
        father_id_str = get_first_value(
            form_data, [f"relation_{i}_father", f"r{i}_father"]
        )
        mother_id_str = get_first_value(
            form_data, [f"relation_{i}_mother", f"r{i}_mother"]
        )
        sources = get_first_value(
            form_data, [f"relation_{i}_sources", f"r{i}_sources"]
        )

        # detect presence if any fields exist for this relation index
        has_any_rel_data = any(
            [
                rel_type_str,
                father_id_str,
                mother_id_str,
                form_data.get(f"r{i}_fath_fn"),
                form_data.get(f"r{i}_moth_fn"),
            ]
        )
        if not has_any_rel_data:
            continue

    # Map string to enum (support a few aliases;
    # unknown -> candidate parent)
        rel_type_map = {
            "adoption": app_family.RelationToParentType.ADOPTION,
            "adoptive_parents": app_family.RelationToParentType.ADOPTION,
            "recognition": app_family.RelationToParentType.RECOGNITION,
            "recognized_parents": app_family.RelationToParentType.RECOGNITION,
            "candidate": app_family.RelationToParentType.CANDIDATEPARENT,
            "candidateparent": app_family.RelationToParentType.CANDIDATEPARENT,
            "possible_parents":
            app_family.RelationToParentType.CANDIDATEPARENT,
            "godparent": app_family.RelationToParentType.GODPARENT,
            "godparents": app_family.RelationToParentType.GODPARENT,
            "foster": app_family.RelationToParentType.FOSTERPARENT,
            "fosterparent": app_family.RelationToParentType.FOSTERPARENT,
            "foster_parents": app_family.RelationToParentType.FOSTERPARENT,
            "undef": app_family.RelationToParentType.CANDIDATEPARENT,
            "undefined": app_family.RelationToParentType.CANDIDATEPARENT,
            "": app_family.RelationToParentType.CANDIDATEPARENT,
        }
        rel_type = rel_type_map.get(
            rel_type_str.lower(),
            app_family.RelationToParentType.CANDIDATEPARENT,
        )

        # Determine father/mother IDs
        father_id = None
        if father_id_str and father_id_str.isdigit() \
                and int(father_id_str) > 0:
            father_id = int(father_id_str)
        else:
            father_id = parse_relation_parent(i, "fath")

        mother_id = None
        if mother_id_str and mother_id_str.isdigit() \
                and int(mother_id_str) > 0:
            mother_id = int(mother_id_str)
        else:
            mother_id = parse_relation_parent(i, "moth")

        relation = app_family.Relation(
            type=rel_type, father=father_id, mother=mother_id, sources=sources
        )
        relations.append(relation)

    # Parse dates and witnesses for life events
    # Support multiple field naming conventions: birth_dd/e_date0_dd/e0_dd
    birth_date = parse_date_with_fallback(form_data, "birth", "e_date0", "e0")
    birth_place = form_data.get(
        "e_place0", form_data.get("birth_place", "")
    ).strip()
    birth_note = form_data.get(
        "e_note0", form_data.get("birth_note", "")
    ).strip()
    birth_src = form_data.get("e_src0", form_data.get("birth_src", "")).strip()

    # Parse birth witnesses (support direct id-only linking)
    # Try both birth_witn* and e0_witn* patterns
    birth_witnesses = []
    for event_pattern in ["birth", 0]:
        witness_num = 0
        while True:
            if isinstance(event_pattern, int):
                prefix = f"e{event_pattern}_witn{witness_num}"
            else:
                prefix = f"{event_pattern}_witn{witness_num}"
            witness_fn = form_data.get(f"{prefix}_fn", "").strip()
            id_present = False
            for k in (f"{prefix}_index", f"{prefix}_id",
                      f"{prefix}_person_id"):
                if form_data.get(k, "").strip():
                    id_present = True
                    break
            if not witness_fn and not id_present:
                break
            witness = parse_witness_from_form(
                form_data, event_pattern, witness_num, person_repo
            )
            if witness:
                birth_witnesses.append(witness)
            witness_num += 1

    # Support multiple field naming conventions: baptism_dd/e_date1_dd/e1_dd
    baptism_date = parse_date_with_fallback(
        form_data, "baptism", "e_date1", "e1"
    )
    baptism_place = form_data.get(
        "e_place1", form_data.get("baptism_place", "")
    ).strip()
    baptism_note = form_data.get(
        "e_note1", form_data.get("baptism_note", "")
    ).strip()
    baptism_src = form_data.get(
        "e_src1", form_data.get("baptism_src", "")
    ).strip()

    # Parse baptism witnesses (support direct id-only linking)
    # Try both baptism_witn* and e1_witn* patterns
    baptism_witnesses = []
    for event_pattern in ["baptism", 1]:
        witness_num = 0
        while True:
            if isinstance(event_pattern, int):
                prefix = f"e{event_pattern}_witn{witness_num}"
            else:
                prefix = f"{event_pattern}_witn{witness_num}"
            witness_fn = form_data.get(f"{prefix}_fn", "").strip()
            id_present = False
            for k in (f"{prefix}_index", f"{prefix}_id",
                      f"{prefix}_person_id"):
                if form_data.get(k, "").strip():
                    id_present = True
                    break
            if not witness_fn and not id_present:
                break
            witness = parse_witness_from_form(
                form_data, event_pattern, witness_num, person_repo
            )
            if witness:
                baptism_witnesses.append(witness)
            witness_num += 1

    # Parse death status
    death_status_str = form_data.get("death_status", "alive")
    death_status: death_info.DeathStatusBase
    death_place = form_data.get(
        "e_place2", form_data.get("death_place", "")
    ).strip()
    death_note = form_data.get(
        "e_note2", form_data.get("death_note", "")
    ).strip()
    death_src = form_data.get("e_src2", form_data.get("death_src", "")).strip()

    # Parse death witnesses (support direct id-only linking)
    # Try both death_witn* and e2_witn* patterns
    death_witnesses = []
    for event_pattern in ["death", 2]:
        witness_num = 0
        while True:
            if isinstance(event_pattern, int):
                prefix = f"e{event_pattern}_witn{witness_num}"
            else:
                prefix = f"{event_pattern}_witn{witness_num}"
            witness_fn = form_data.get(f"{prefix}_fn", "").strip()
            id_present = False
            for k in (f"{prefix}_index", f"{prefix}_id",
                      f"{prefix}_person_id"):
                if form_data.get(k, "").strip():
                    id_present = True
                    break
            if not witness_fn and not id_present:
                break
            witness = parse_witness_from_form(
                form_data, event_pattern, witness_num, person_repo
            )
            if witness:
                death_witnesses.append(witness)
            witness_num += 1

    if death_status_str == "alive":
        death_status = death_info.NotDead()
    elif death_status_str == "dont_know":
        death_status = death_info.DontKnowIfDead()
    elif death_status_str == "obviously_dead":
        death_status = death_info.OfCourseDead()
    else:  # dead, killed, murdered, executed, disappeared
        # Support multiple field naming conventions: death_dd/e_date2_dd/e2_dd
        death_date = parse_date_with_fallback(
            form_data, "death", "e_date2", "e2"
        )
        # Map specific reasons; default to UNSPECIFIED for plain 'dead'
        reason_map = {
            "killed": death_info.DeathReason.KILLED,
            "murdered": death_info.DeathReason.MURDERED,
            "executed": death_info.DeathReason.EXECUTED,
            "disappeared": death_info.DeathReason.DISAPPEARED,
            "dead": death_info.DeathReason.UNSPECIFIED,
        }
        death_reason = reason_map.get(
            death_status_str.lower(), death_info.DeathReason.UNSPECIFIED
        )
        death_status = death_info.Dead(
            death_reason=death_reason, date_of_death=death_date
        )

    # Parse burial
    burial_type = form_data.get("burial_type", "burial")
    # Support multiple field naming conventions: burial_dd/e_date3_dd/e3_dd
    burial_date = parse_date_with_fallback(
        form_data, "burial", "e_date3", "e3"
    )
    burial_place = form_data.get(
        "e_place3", form_data.get("burial_place", "")
    ).strip()
    burial_note = form_data.get(
        "e_note3", form_data.get("burial_note", "")
    ).strip()
    burial_src = form_data.get(
        "e_src3", form_data.get("burial_src", "")
    ).strip()

    # Parse burial witnesses (support direct id-only linking)
    # Try both burial_witn* and e3_witn* patterns
    burial_witnesses = []
    for event_pattern in ["burial", 3]:
        witness_num = 0
        while True:
            if isinstance(event_pattern, int):
                prefix = f"e{event_pattern}_witn{witness_num}"
            else:
                prefix = f"{event_pattern}_witn{witness_num}"
            witness_fn = form_data.get(f"{prefix}_fn", "").strip()
            id_present = False
            for k in (f"{prefix}_index", f"{prefix}_id",
                      f"{prefix}_person_id"):
                if form_data.get(k, "").strip():
                    id_present = True
                    break
            if not witness_fn and not id_present:
                break
            witness = parse_witness_from_form(
                form_data, event_pattern, witness_num, person_repo
            )
            if witness:
                burial_witnesses.append(witness)
            witness_num += 1

    burial: burial_info.BurialInfoBase
    if burial_type == "cremated" and burial_date:
        burial = burial_info.Cremated(cremation_date=burial_date)
    elif burial_date:
        burial = burial_info.Burial(burial_date=burial_date)
    else:
        burial = burial_info.UnknownBurial()

    # Parse personal events; we'll populate after integrating any
    # witnesses from custom life-event markers
    personal_events = []

    # Parse custom personal events (sparse indices like e_name4 are allowed)
    event_indices = []

    for key in form_data.keys():
        if key.startswith("e_name"):
            try:
                idx = int(key.replace("e_name", ""))
                event_indices.append(idx)
            except ValueError:
                continue

    for event_num in sorted(set(event_indices)):
        event_name = form_data.get(f"e_name{event_num}", "").strip()
        event_name_norm = event_name.lower()

    # Support multiple field naming conventions:
    # e_date{num}_dd/e{num}_dd
        event_date = parse_date_with_fallback(
            form_data, f"e_date{event_num}", f"e{event_num}"
        )
        event_place = form_data.get(f"e_place{event_num}", "").strip()
        event_note = form_data.get(f"e_note{event_num}", "").strip()
        event_src = form_data.get(f"e_src{event_num}", "").strip()

        # Parse witnesses for this event
        witnesses = []
        witness_num = 0
        while True:
            witness = parse_witness_from_form(
                form_data, event_num, witness_num, person_repo
            )
            if witness is None:
                break
            witnesses.append(witness)
            witness_num += 1

    # If this is a core life event marker (support several aliases),
    # merge witnesses
        birth_markers = {"#birt", "#birth", "birt", "birth"}
        bapt_markers = {"#bapt", "#baptism", "bapt", "baptism"}
        death_markers = {"#deat", "#death", "deat", "death"}
        burial_markers = {"#buri", "#burial", "buri", "burial", "buried"}
        cremation_markers = {
            "#crem",
            "#cremation",
            "crem",
            "cremation",
            "cremated",
        }

        if event_name_norm in birth_markers:
            # Replace or extend birth_witnesses with those captured via
            # e{event_num}_witn*
            if witnesses:
                birth_witnesses = witnesses
            # Skip creating a separate personal event for life-event markers
            continue
        if event_name_norm in bapt_markers:
            if witnesses:
                baptism_witnesses = witnesses
            continue
        if event_name_norm in death_markers:
            if witnesses:
                death_witnesses = witnesses
            continue
        if (
            event_name_norm in burial_markers
            or event_name_norm in cremation_markers
        ):
            if witnesses:
                burial_witnesses = witnesses
            continue

        # For indices 0..3 with blank names, skip creating custom events
        if event_num in [0, 1, 2, 3] and not event_name:
            continue

        # Determine if there's meaningful data for a custom event
        has_any_data = bool(
            event_date or event_place or event_note or event_src or witnesses
        )

        # Skip life-event markers (handled by vitals and optional
        # personal events for witnesses)
        # This is a safety check in case new markers are added above
        all_life_markers = (
            birth_markers
            | bapt_markers
            | death_markers
            | burial_markers
            | cremation_markers
        )
        if event_name_norm in all_life_markers:
            continue

    # Only create custom event if there's actual data
    # (not just an index with no content)
        if has_any_data:
            # Map event type code to event class; default to residence
            # when missing/unknown
            if (
                event_name_norm == "#residence"
                or event_name_norm == "#resi"
                or not event_name
            ):
                event_name_obj = app_events.PersResidence()
            else:
                # Fallback generic custom event -> currently model uses
                # PersResidence as default
                event_name_obj = app_events.PersResidence()

            personal_event = app_events.PersonalEvent(
                name=event_name_obj,
                date=event_date,
                place=event_place,
                reason="",
                note=event_note,
                src=event_src,
                witnesses=witnesses,
            )
            personal_events.append(personal_event)

    # After merging life-event witnesses from custom markers, add personal
    # events for life events if they have witnesses
    if birth_witnesses and birth_date:
        birth_event = app_events.PersonalEvent(
            name=app_events.PersBirth(),
            date=birth_date,
            place=birth_place,
            reason="",
            note=birth_note,
            src=birth_src,
            witnesses=birth_witnesses,
        )
        personal_events.append(birth_event)

    if baptism_witnesses and baptism_date:
        baptism_event = app_events.PersonalEvent(
            name=app_events.PersBaptism(),
            date=baptism_date,
            place=baptism_place,
            reason="",
            note=baptism_note,
            src=baptism_src,
            witnesses=baptism_witnesses,
        )
        personal_events.append(baptism_event)

    if (
        death_witnesses
        and isinstance(death_status, death_info.Dead)
        and death_status.date_of_death
    ):
        death_event = app_events.PersonalEvent(
            name=app_events.PersDeath(),
            date=death_status.date_of_death,
            place=death_place,
            reason="",
            note=death_note,
            src=death_src,
            witnesses=death_witnesses,
        )
        personal_events.append(death_event)

    if burial_witnesses:
        if isinstance(burial, burial_info.Burial) and burial.burial_date:
            burial_event = app_events.PersonalEvent(
                name=app_events.PersBurial(),
                date=burial.burial_date,
                place=burial_place,
                reason="",
                note=burial_note,
                src=burial_src,
                witnesses=burial_witnesses,
            )
            personal_events.append(burial_event)
        elif (
            isinstance(burial, burial_info.Cremated)
            and burial.cremation_date
        ):
            cremation_event = app_events.PersonalEvent(
                name=app_events.PersCremation(),
                date=burial.cremation_date,
                place=burial_place,
                reason="",
                note=burial_note,
                src=burial_src,
                witnesses=burial_witnesses,
            )
            personal_events.append(cremation_event)

    # Create updated person object
    updated_person = app_person.Person(
        index=person_id,
        first_name=first_name,
        surname=surname,
        occ=occ,
        image=form_data.get("image", "").strip(),
        public_name=form_data.get("public_name", "").strip(),
        qualifiers=sobriquets,
        aliases=aliases,
        first_names_aliases=alt_first_names,
        surname_aliases=alt_surnames,
        titles=titles if titles else existing_person.titles,
        non_native_parents_relation=(
            relations
            if relations
            else existing_person.non_native_parents_relation
        ),
        related_persons=existing_person.related_persons,
        occupation=occupation,
        sex=sex,
        access_right=access_right,
        birth_date=birth_date,
        birth_place=birth_place,
        birth_note=birth_note,
        birth_src=birth_src,
        baptism_date=baptism_date,
        baptism_place=baptism_place,
        baptism_note=baptism_note,
        baptism_src=baptism_src,
        death_status=death_status,
        death_place=death_place,
        death_note=death_note,
        death_src=death_src,
        burial=burial,
        burial_place=burial_place,
        burial_note=burial_note,
        burial_src=burial_src,
        personal_events=personal_events,
        notes=form_data.get("notes", "").strip(),
        src=form_data.get("person_source", "").strip(),
        ascend=existing_person.ascend,
        families=existing_person.families,
    )

    # Update person in database
    try:
        # First, avoid single-parent conflicts by clearing date-bearing fields
        # for the core edit, then set them via a dedicated repository method.
        core_person = app_person.Person(
            index=updated_person.index,
            first_name=updated_person.first_name,
            surname=updated_person.surname,
            occ=updated_person.occ,
            image=updated_person.image,
            public_name=updated_person.public_name,
            qualifiers=updated_person.qualifiers,
            aliases=updated_person.aliases,
            first_names_aliases=updated_person.first_names_aliases,
            surname_aliases=updated_person.surname_aliases,
            titles=updated_person.titles,
            non_native_parents_relation=(
                updated_person.non_native_parents_relation
            ),
            related_persons=updated_person.related_persons,
            occupation=updated_person.occupation,
            sex=updated_person.sex,
            access_right=updated_person.access_right,
            birth_date=None,
            birth_place=updated_person.birth_place,
            birth_note=updated_person.birth_note,
            birth_src=updated_person.birth_src,
            baptism_date=None,
            baptism_place=updated_person.baptism_place,
            baptism_note=updated_person.baptism_note,
            baptism_src=updated_person.baptism_src,
            death_status=(
                death_info.Dead(
                    death_reason=updated_person.death_status.death_reason,
                    date_of_death=None,
                )
                if isinstance(updated_person.death_status, death_info.Dead)
                else updated_person.death_status
            ),
            death_place=updated_person.death_place,
            death_note=updated_person.death_note,
            death_src=updated_person.death_src,
            burial=burial_info.UnknownBurial(),
            burial_place=updated_person.burial_place,
            burial_note=updated_person.burial_note,
            burial_src=updated_person.burial_src,
            personal_events=updated_person.personal_events,
            notes=updated_person.notes,
            src=updated_person.src,
            ascend=updated_person.ascend,
            families=updated_person.families,
        )

        person_repo.edit_person(core_person)
        # Now safely update vital dates and statuses
        person_repo.update_person_vitals(updated_person)
    except Exception as e:
        if (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            return jsonify({"ok": False, "error": str(e)}), 500
        return f"Error updating person: {str(e)}", 500

    # Return success
    if (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ):
        return jsonify({"ok": True, "person_id": person_id})

    # Redirect to person view (or back to form)
    return redirect(
        url_for("gwd.route_MOD_IND", base=base, id=person_id, lang=lang)
    )


def implem_route_MOD_IND(base, id, lang="en"):
    """
    Implementation of the MOD_IND route - Individual modification page.

    Args:
        base: The database base name
        id: The person ID to modify
        lang: Language code (default: 'en')

    Returns:
        Rendered template with person data or redirect after update
    """
    g.locale = lang

    # Get database service
    try:
        db_service = get_db_service(base)
    except FileNotFoundError:
        if (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            return (
                jsonify({"ok": False, "error": f"Database not found: {base}"}),
                404,
            )
        return f"Database '{base}' not found", 404
    # When tests mock get_db_service to return None, treat as not found
    if db_service is None:
        if (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            return (
                jsonify({"ok": False, "error": f"Database not found: {base}"}),
                404,
            )
        return f"Database '{base}' not found", 404

    try:
        person_repo = PersonRepository(db_service)

        # Handle POST request (form submission)
        if request.method == "POST":
            return handle_mod_individual_post(
                base, id, lang, person_repo, db_service
            )

        # Handle GET request (display form)
        try:
            person_obj = person_repo.get_person_by_id(id)
        except ValueError:
            if (
                request.accept_mimetypes.accept_json
                and not request.accept_mimetypes.accept_html
            ):
                return (
                    jsonify(
                        {
                            "ok": False,
                            "error": f"Person with id {id} not found"
                        }
                    ),
                    404,
                )
            return f"Person with id {id} not found", 404

    # Convert person object to template context
    # (with repository for relation enrichment)
        person = convert_person_to_template_context(person_obj, person_repo)

        # Calculate digest for data integrity (MD5 hash of person data)
        person_data_str = json.dumps(person, sort_keys=True, default=str)
        digest = hashlib.md5(person_data_str.encode()).hexdigest()
    finally:
        if db_service:
            db_service.disconnect()

    # Prepare data for the template
    context = {
        "base": base,
        "db_name": base,  # Template uses db_name
        "id": id,
        "lang": lang,
        "person": person,
        "digest": digest,
        "wizard_message": None,  # Optional message from wizard
        "max_aliases": 10,  # Maximum number of alias fields to show
        # Calendar types for dropdown
        "calendar_types": [
            {"value": "gregorian", "label": "Gregorian"},
            {"value": "julian", "label": "Julian"},
            {"value": "french_republican", "label": "French Republican"},
            {"value": "hebrew", "label": "Hebrew"},
        ],
        # Months for each calendar (will be populated by JavaScript)
        "gregorian_months": [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
        "french_republican_months": [
            "Vendémiaire",
            "Brumaire",
            "Frimaire",
            "Nivôse",
            "Pluviôse",
            "Ventôse",
            "Germinal",
            "Floréal",
            "Prairial",
            "Messidor",
            "Thermidor",
            "Fructidor",
            "Complémentaire",
        ],
        "hebrew_months": [
            "Tichri",
            "Marhechvan",
            "Kislev",
            "Tevet",
            "Chevat",
            "Adar 1",
            "Adar 2",
            "Nissan",
            "Iyar",
            "Sivan",
            "Tamouz",
            "Av",
            "Eloul",
        ],
        # Sex options
        "sex_options": [
            {"value": "M", "label": "Male"},
            {"value": "F", "label": "Female"},
            {"value": "U", "label": "Unspecified/Unknown"},
        ],
        # Access levels
        "access_levels": [
            {"value": "public", "label": "Public"},
            {"value": "private", "label": "Private"},
            {"value": "if_titles", "label": "If titles"},
        ],
        # Death status options
        "death_statuses": [
            {"value": "alive", "label": "Alive"},
            {"value": "dead", "label": "Dead"},
            {"value": "dont_know", "label": "Don't know"},
            {"value": "obviously_dead", "label": "Obviously dead"},
            {"value": "killed", "label": "Killed"},
            {"value": "murdered", "label": "Murdered"},
            {"value": "executed", "label": "Executed"},
            {"value": "disappeared", "label": "Disappeared"},
        ],
        # Event types
        "event_types": [
            "birth",
            "baptism",
            "death",
            "burial",
            "residence",
            "occupation",
            "military_service",
            "census",
            "graduation",
            "award",
            "other",
        ],
        # Relation types
        "relation_types": [
            {"value": "adoptive_parents", "label": "Adoptive parents"},
            {"value": "recognized_parents", "label": "Parents who recognized"},
            {"value": "possible_parents", "label": "Possible parents"},
            {"value": "godparents", "label": "Godparents"},
            {"value": "foster_parents", "label": "Foster parents"},
        ],
        # Languages for footer selector
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "fr", "name": "Français"},
            {"code": "de", "name": "Deutsch"},
            {"code": "es", "name": "Español"},
            {"code": "it", "name": "Italiano"},
            {"code": "pt", "name": "Português"},
            {"code": "nl", "name": "Nederlands"},
            {"code": "sv", "name": "Svenska"},
            {"code": "da", "name": "Dansk"},
            {"code": "no", "name": "Norsk"},
            {"code": "fi", "name": "Suomi"},
            {"code": "pl", "name": "Polski"},
            {"code": "cs", "name": "Čeština"},
            {"code": "ru", "name": "Русский"},
            {"code": "zh", "name": "中文"},
        ],
        # Current year for form validation
        "current_year": date.today().year,
    }

    return render_template("gwd/mod_individual.html", **context)
