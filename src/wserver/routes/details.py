from flask import render_template, request
from repositories.person_repository import PersonRepository
from repositories.family_repository import FamilyRepository
from wserver.routes.db_utils import get_db_service
from libraries.date import CalendarDate, Calendar
from libraries.death_info import Dead, DeadYoung, DeadDontKnowWhen
from libraries.family import Divorced, Separated
from libraries.events import FamMarriage, FamDivorce, FamSeparated
from typing import Dict, Any, List
import time
from datetime import date as python_date


def calculate_age_in_days(birth_date, death_date):
    """
    Calculate age in days between birth and death dates.

    Args:
        birth_date: Birth date (CalendarDate or tuple)
        death_date: Death date (CalendarDate or tuple)

    Returns:
        Dictionary with years, months, days, and total_days
    """
    if not birth_date or not death_date:
        return None

    # Extract date components
    birth_day, birth_month, birth_year = None, None, None
    death_day, death_month, death_year = None, None, None

    if isinstance(birth_date, tuple) and len(birth_date) == 2:
        birth_year = birth_date[1]
    elif isinstance(birth_date, CalendarDate):
        birth_day = birth_date.dmy.day
        birth_month = birth_date.dmy.month
        birth_year = birth_date.dmy.year

    if isinstance(death_date, tuple) and len(death_date) == 2:
        death_year = death_date[1]
    elif isinstance(death_date, CalendarDate):
        death_day = death_date.dmy.day
        death_month = death_date.dmy.month
        death_year = death_date.dmy.year

    if not birth_year or not death_year:
        return None

    # If we have full dates (day, month, year), calculate exact difference
    if (birth_day and birth_month and birth_year and
            death_day and death_month and death_year):
        try:
            birth_py_date = python_date(birth_year, birth_month, birth_day)
            death_py_date = python_date(death_year, death_month, death_day)
            delta = death_py_date - birth_py_date
            total_days = delta.days

            # Calculate years, months, days
            years = death_year - birth_year
            months = death_month - birth_month
            days = death_day - birth_day

            # Adjust if needed
            if days < 0:
                months -= 1
                # Approximate days in previous month
                days += 30
            if months < 0:
                years -= 1
                months += 12

            # Format the age string
            if total_days == 0:
                return "0 days"
            elif total_days == 1:
                return "1 day"
            elif total_days < 31:
                return f"{total_days} days"
            elif years == 0 and months == 1:
                return "1 month"
            elif years == 0 and months > 1:
                return f"{months} months"
            elif years == 1 and months == 0:
                return "1 year"
            elif years > 0:
                if months > 0:
                    return f"{years} years {months} months"
                else:
                    return f"{years} years"
            else:
                return f"{total_days} days"

        except (ValueError, OverflowError):
            # Fallback to year calculation
            return f"{death_year - birth_year} years" \
                if death_year > birth_year else "0 days"
    else:
        # Only have years, calculate approximate
        if birth_year and death_year:
            years = death_year - birth_year
            if years == 0:
                return "less than a year"
            elif years == 1:
                return "1 year"
            else:
                return f"{years} years"

    return None


def get_person_basic_info(person) -> Dict[str, Any]:
    """Extract basic person information."""
    return {
        'person_id': person.index,
        'first_name': person.first_name,
        'surname': person.surname,
        'occupation': person.occupation if person.occupation else None,
    }


def get_person_vital_events(person) -> Dict[str, Any]:
    """Extract birth, death, and related vital events."""
    birth_year = None
    birth_date = None
    birth_place = None

    if person.birth_date is not None:
        if isinstance(
            person.birth_date, tuple
        ) and len(person.birth_date) == 2:
            birth_year = person.birth_date[1]
        elif isinstance(person.birth_date, CalendarDate):
            birth_year = person.birth_date.dmy.year
            birth_date = format_date(person.birth_date)
        birth_place = person.birth_place if person.birth_place else None

    death_year = None
    death_date = None
    death_place = None
    age_at_death = None

    # Check if person.death_status is Dead (or DeadYoung, DeadDontKnowWhen)
    if isinstance(person.death_status, Dead):
        # person.death_status is the Dead object itself
        if person.death_status.date_of_death:
            death_info = person.death_status.date_of_death
            if isinstance(death_info, tuple) and len(death_info) == 2:
                death_year = death_info[1]
            elif isinstance(death_info, CalendarDate):
                death_year = death_info.dmy.year
                death_date = format_date(death_info)

        death_place = person.death_place if person.death_place else None

        # Calculate age at death in days
        if person.birth_date and person.death_status.date_of_death:
            age_at_death = calculate_age_in_days(
                person.birth_date,
                person.death_status.date_of_death
            )
    elif isinstance(person.death_status, (DeadYoung, DeadDontKnowWhen)):
        # These types don't have date_of_death
        death_place = person.death_place if person.death_place else None
    return {
        'birth_year': birth_year,
        'birth_date': birth_date,
        'birth_place': birth_place,
        'death_year': death_year,
        'death_date': death_date,
        'death_place': death_place,
        'age_at_death': age_at_death,
    }


def get_family_info(
    person,
    family_repo: FamilyRepository,
    person_repo: PersonRepository
) -> Dict[str, Any]:
    """Extract spouse and family information."""
    if not person.families or len(person.families) == 0:
        return {
            'family_id': None,
            'spouse_id': None,
            'spouse_first_name': None,
            'spouse_surname': None,
            'spouse_birth_year': None,
            'spouse_death_year': None,
            'marriage_date': None,
            'marriage_place': None,
            'has_marriage': False,
            'divorce_date': None,
            'divorce_note': None,
        }

    family_id = person.families[0]
    family = family_repo.get_family_by_id(family_id)

    # Get spouse (the other parent in the family)
    spouse_id = None
    spouse = None
    if family.parents.is_couple():
        father_id, mother_id = family.parents.couple()
        spouse_id = mother_id if father_id == person.index else father_id
        spouse = person_repo.get_person_by_id(spouse_id)

    spouse_first_name = spouse.first_name if spouse else None
    spouse_surname = spouse.surname if spouse else None
    spouse_birth_year = None
    spouse_death_year = None

    if spouse:
        if spouse.birth_date:
            if (
                isinstance(spouse.birth_date, tuple)
                and len(spouse.birth_date) == 2
            ):
                spouse_birth_year = spouse.birth_date[1]
            elif isinstance(spouse.birth_date, CalendarDate):
                spouse_birth_year = spouse.birth_date.dmy.year

        death_types = (Dead, DeadYoung, DeadDontKnowWhen)
        if isinstance(spouse.death_status, death_types):
            if (
                hasattr(spouse.death_status, 'death_date')
                and spouse.death_status.death_date
            ):
                death_info = spouse.death_status.death_date
                if isinstance(death_info, tuple) and len(death_info) == 2:
                    spouse_death_year = death_info[1]
                elif isinstance(death_info, CalendarDate):
                    spouse_death_year = death_info.dmy.year

    marriage_date = None
    marriage_place = None

    # Only set marriage info if there's actual marriage data
    if family.marriage_date:
        if isinstance(family.marriage_date, CalendarDate):
            marriage_date = format_date(family.marriage_date)
        if family.marriage_place:
            marriage_place = family.marriage_place

    # Check if marriage exists (has date or place)
    has_marriage = marriage_date is not None or marriage_place is not None

    divorce_date = None
    divorce_note = None
    if isinstance(family.divorce_status, (Divorced, Separated)):
        if hasattr(family.divorce_status, 'divorce_date'):
            div_date = family.divorce_status.divorce_date
            if isinstance(div_date, CalendarDate):
                divorce_date = format_date(div_date)

    return {
        'family_id': family_id,
        'spouse_id': spouse_id,
        'spouse_first_name': spouse_first_name,
        'spouse_surname': spouse_surname,
        'spouse_birth_year': spouse_birth_year,
        'spouse_death_year': spouse_death_year,
        'marriage_date': marriage_date,
        'marriage_place': marriage_place,
        'has_marriage': has_marriage,
        'divorce_date': divorce_date,
        'divorce_note': divorce_note,
    }


def get_children_info(
    person,
    family_repo: FamilyRepository,
    person_repo: PersonRepository
) -> List[Dict[str, Any]]:
    """Extract children information from all families."""
    children: List[Dict[str, Any]] = []

    if not person.families:
        return children

    for family_id in person.families:
        family = family_repo.get_family_by_id(family_id)

        for child_id in family.children:
            child = person_repo.get_person_by_id(child_id)

            birth_year = None
            if child.birth_date:
                if (
                    isinstance(child.birth_date, tuple)
                    and len(child.birth_date) == 2
                ):
                    birth_year = child.birth_date[1]
                elif isinstance(child.birth_date, CalendarDate):
                    birth_year = child.birth_date.dmy.year

            death_year = None
            death_types = (Dead, DeadYoung, DeadDontKnowWhen)
            if isinstance(child.death_status, death_types):
                if (
                    hasattr(child.death_status, 'death_date')
                    and child.death_status.death_date
                ):
                    death_info = child.death_status.death_date
                    if isinstance(death_info, tuple) and len(death_info) == 2:
                        death_year = death_info[1]
                    elif isinstance(death_info, CalendarDate):
                        death_year = death_info.dmy.year

            age_years = None
            if birth_year and death_year:
                age_years = death_year - birth_year

            children.append({
                'id': child.index,
                'first_name': child.first_name,
                'surname': child.surname,
                'birth_year': birth_year,
                'death_year': death_year,
                'age_years': age_years,
            })

    return children


def get_witness_info(
    witness_id: int,
    person_repo: PersonRepository
) -> Dict[str, Any]:
    """Extract witness information."""
    try:
        witness = person_repo.get_person_by_id(witness_id)

        # Get witness birth and death years for date range
        witness_birth_year = None
        witness_death_year = None

        if witness.birth_date:
            if isinstance(witness.birth_date, tuple):
                witness_birth_year = witness.birth_date[1]
            elif isinstance(witness.birth_date, CalendarDate):
                witness_birth_year = witness.birth_date.dmy.year

        death_types = (Dead, DeadYoung, DeadDontKnowWhen)
        if isinstance(witness.death_status, death_types):
            if (
                hasattr(witness.death_status, 'death_date')
                and witness.death_status.death_date
            ):
                death_info = witness.death_status.death_date
                if isinstance(death_info, tuple):
                    witness_death_year = death_info[1]
                elif isinstance(death_info, CalendarDate):
                    witness_death_year = death_info.dmy.year

        # Format date range
        date_range = ''
        if witness_birth_year:
            date_range = f"{witness_birth_year}-"
            if witness_death_year:
                date_range = f"{witness_birth_year}-{witness_death_year}"

        return {
            'id': witness.index,
            'first_name': witness.first_name,
            'surname': witness.surname,
            'date_range': date_range,
            'age': '',
        }
    except Exception:
        # If witness not found, return empty dict
        return {}


def get_sort_key(event: Dict[str, Any]) -> tuple:
    """Generate a sort key for timeline events based on their date."""
    date_obj = event.get('_sort_date')
    if not date_obj or not isinstance(date_obj, CalendarDate):
        # Events without valid dates go to the end
        return (9999, 12, 31)

    year = date_obj.dmy.year if date_obj.dmy.year > 0 else 9999
    month = date_obj.dmy.month if date_obj.dmy.month > 0 else 12
    day = date_obj.dmy.day if date_obj.dmy.day > 0 else 31

    return (year, month, day)


def _extract_person_years(person):
    """
    Helper to extract birth and death years from a person object.

    Returns:
        Tuple of (birth_year, death_year)
    """
    birth_year = None
    death_year = None

    if person.birth_date:
        if isinstance(person.birth_date, tuple) and len(
                person.birth_date) == 2:
            birth_year = person.birth_date[1]
        elif isinstance(person.birth_date, CalendarDate):
            birth_year = person.birth_date.dmy.year

    if isinstance(person.death_status, Dead):
        if person.death_status.date_of_death:
            death_info = person.death_status.date_of_death
            if isinstance(death_info, tuple) and len(death_info) == 2:
                death_year = death_info[1]
            elif isinstance(death_info, CalendarDate):
                death_year = death_info.dmy.year

    return birth_year, death_year


def get_ancestor_recursive(person_id, person_repo,
                           family_repo, depth=0, max_depth=10):
    """
    Recursively get complete ancestor tree for a person.

    Args:
        person_id: ID of the person
        person_repo: Person repository
        family_repo: Family repository
        depth: Current recursion depth
        max_depth: Maximum depth to prevent infinite loops

    Returns:
        Dictionary with person info and nested father/mother ancestors
    """
    if person_id is None or depth >= max_depth:
        return None

    try:
        person = person_repo.get_person_by_id(person_id)
        if not person:
            return None

        birth_year, death_year = _extract_person_years(person)

        ancestor_info = {
            'id': person.index,
            'first_name': person.first_name,
            'surname': person.surname,
            'birth_year': birth_year,
            'death_year': death_year,
        }

        # Recursively get parents if they exist
        father_ancestor = None
        mother_ancestor = None

        if person.ascend.parents is not None:
            try:
                parent_family = family_repo.get_family_by_id(
                    person.ascend.parents
                )

                if (parent_family is not None and
                        parent_family.parents.is_couple()):
                    father_id, mother_id = parent_family.parents.couple()

                    # Recursively get father and all his ancestors
                    if father_id is not None:
                        father_ancestor = get_ancestor_recursive(
                            father_id, person_repo, family_repo,
                            depth + 1, max_depth
                        )

                    # Recursively get mother and all her ancestors
                    if mother_id is not None:
                        mother_ancestor = get_ancestor_recursive(
                            mother_id, person_repo, family_repo,
                            depth + 1, max_depth
                        )
            except Exception:
                pass

        # Only add father/mother keys if at least one exists
        if father_ancestor is not None or mother_ancestor is not None:
            if father_ancestor is not None:
                ancestor_info['father'] = father_ancestor
            if mother_ancestor is not None:
                ancestor_info['mother'] = mother_ancestor

        return ancestor_info
    except Exception:
        return None


def get_siblings_info(
    person,
    family_repo: FamilyRepository,
    person_repo: PersonRepository
) -> List[Dict[str, Any]]:
    """
    Get information about person's siblings.

    Returns:
        List of siblings with their information
    """
    siblings: List[Dict[str, Any]] = []

    # Get person's parent family
    if person.ascend.parents is None:
        return siblings

    try:
        parent_family = family_repo.get_family_by_id(person.ascend.parents)

        if not parent_family:
            return siblings

        # Get all children from parent family (including the person themselves)
        for child_id in parent_family.children:
            try:
                sibling = person_repo.get_person_by_id(child_id)

                # Extract birth and death years
                birth_year = None
                death_year = None

                if sibling.birth_date:
                    if isinstance(sibling.birth_date, tuple) and len(
                            sibling.birth_date) == 2:
                        birth_year = sibling.birth_date[1]
                    elif isinstance(sibling.birth_date, CalendarDate):
                        birth_year = sibling.birth_date.dmy.year

                if isinstance(sibling.death_status, Dead):
                    if sibling.death_status.date_of_death:
                        death_info = sibling.death_status.date_of_death
                        if isinstance(death_info, tuple) and len(
                                death_info) == 2:
                            death_year = death_info[1]
                        elif isinstance(death_info, CalendarDate):
                            death_year = death_info.dmy.year

                # Calculate age
                age_years = None
                if birth_year and death_year:
                    age_years = death_year - birth_year

                siblings.append({
                    'id': sibling.index,
                    'first_name': sibling.first_name,
                    'surname': sibling.surname,
                    'birth_year': birth_year,
                    'death_year': death_year,
                    'age_years': age_years,
                })
            except Exception:
                # Skip sibling if error
                continue
    except Exception:
        pass

    return siblings


def get_ancestors_all(person, person_repo, family_repo):
    """
    Get ALL generations of ancestors recursively.

    Returns:
        Nested dictionary with complete ancestor tree (all generations)
    """
    # Use the recursive function to get the complete ancestor tree
    return get_ancestor_recursive(person.index, person_repo, family_repo)


def get_ancestors_3gen(person, person_repo, family_repo):
    """
    Get 3 generations of ancestors for backward compatibility.
    This now uses the recursive function and flattens the result.

    Returns:
        Dictionary with parents and grandparents information
    """
    # Get complete ancestor tree recursively with max_depth=2
    ancestor_tree = get_ancestor_recursive(
        person.index, person_repo, family_repo, depth=0, max_depth=2
    )

    if not ancestor_tree:
        return {
            'father': None,
            'mother': None,
            'paternal_grandfather': None,
            'paternal_grandmother': None,
            'maternal_grandfather': None,
            'maternal_grandmother': None,
        }

    # Flatten for 3-gen display (for backward compatibility with the template)
    ancestors = {
        'father': ancestor_tree.get('father'),
        'mother': ancestor_tree.get('mother'),
        'paternal_grandfather': None,
        'paternal_grandmother': None,
        'maternal_grandfather': None,
        'maternal_grandmother': None,
    }

    # Extract grandparents from the nested structure
    if ancestor_tree.get('father'):
        ancestors['paternal_grandfather'] = ancestor_tree['father'].get(
            'father')
        ancestors['paternal_grandmother'] = ancestor_tree['father'].get(
            'mother')

    if ancestor_tree.get('mother'):
        ancestors['maternal_grandfather'] = ancestor_tree['mother'].get(
            'father')
        ancestors['maternal_grandmother'] = ancestor_tree['mother'].get(
            'mother')

    return ancestors


def get_timeline_events(
    person,
    family_repo: FamilyRepository,
    person_repo: PersonRepository
) -> List[Dict[str, Any]]:
    """Extract timeline events."""
    events: List[Dict[str, Any]] = []

    # Birth event
    if person.birth_date:
        birth_display = ''
        if isinstance(person.birth_date, CalendarDate):
            birth_display = format_date(person.birth_date)
        events.append({
            'type': 'birth',
            'date_display': birth_display,
            'place': person.birth_place if person.birth_place else None,
            '_sort_date': person.birth_date,
        })

    # Marriage events
    if person.families:
        for family_id in person.families:
            family = family_repo.get_family_by_id(family_id)

            # Get spouse
            spouse_id = None
            spouse = None
            if family.parents.is_couple():
                father_id, mother_id = family.parents.couple()
                spouse_id = (
                    mother_id if father_id == person.index else father_id
                )
                spouse = person_repo.get_person_by_id(spouse_id)

            if family.marriage_date:
                marriage_display = ''
                if isinstance(family.marriage_date, CalendarDate):
                    marriage_display = format_date(family.marriage_date)

                # Get witnesses and note for marriage event
                witnesses = []
                marriage_note = ''
                for fam_event in family.family_events:
                    if isinstance(fam_event.name, FamMarriage):
                        for witness_tuple in fam_event.witnesses:
                            witness_id = witness_tuple[0]
                            witness_info = get_witness_info(
                                witness_id,
                                person_repo
                            )
                            if witness_info:
                                witnesses.append(witness_info)
                        if fam_event.note:
                            marriage_note = fam_event.note
                        break

                marriage_event: Dict[str, Any] = {
                    'type': 'marriage',
                    'date_display': marriage_display,
                    'place': (
                        family.marriage_place
                        if family.marriage_place else None
                    ),
                    'spouse_id': spouse_id,
                    'spouse_first_name': (
                        spouse.first_name if spouse else None
                    ),
                    'spouse_surname': spouse.surname if spouse else None,
                    'date_range': '',
                    'duration': '',
                    'witnesses': witnesses,
                    'note': marriage_note,
                    '_sort_date': family.marriage_date,
                }
                events.append(marriage_event)

            # Children births
            for child_id in family.children:
                child = person_repo.get_person_by_id(child_id)
                if child.birth_date:
                    child_display = ''
                    if isinstance(child.birth_date, CalendarDate):
                        child_display = format_date(child.birth_date)

                    # Get child's birth and death years for date range
                    child_birth_year = None
                    child_death_year = None

                    if isinstance(child.birth_date, tuple):
                        child_birth_year = child.birth_date[1]
                    elif isinstance(child.birth_date, CalendarDate):
                        child_birth_year = child.birth_date.dmy.year

                    death_types = (Dead, DeadYoung, DeadDontKnowWhen)
                    if isinstance(child.death_status, death_types):
                        if (
                            hasattr(child.death_status, 'death_date')
                            and child.death_status.death_date
                        ):
                            death_info = child.death_status.death_date
                            if isinstance(death_info, tuple):
                                child_death_year = death_info[1]
                            elif isinstance(death_info, CalendarDate):
                                child_death_year = death_info.dmy.year

                    # Format date range like "2015-2023" or "2015-"
                    child_date_range = ''
                    if child_birth_year:
                        child_date_range = f"{child_birth_year}-"
                        if child_death_year:
                            child_date_range = (
                                f"{child_birth_year}-{child_death_year}"
                            )

                    events.append({
                        'type': 'child_birth',
                        'date_display': child_display,
                        'id': child.index,
                        'child_first_name': child.first_name,
                        'child_surname': child.surname,
                        'child_date_range': child_date_range,
                        'child_age': '',
                        '_sort_date': child.birth_date,
                    })

            # Divorce event
            if isinstance(family.divorce_status, (Divorced, Separated)):
                if (
                    hasattr(family.divorce_status, 'divorce_date')
                    and family.divorce_status.divorce_date
                ):
                    divorce_display = ''
                    div_date = family.divorce_status.divorce_date
                    if isinstance(div_date, CalendarDate):
                        divorce_display = format_date(div_date)

                    # Get witnesses and note for divorce event
                    witnesses = []
                    divorce_note = ''
                    for fam_event in family.family_events:
                        if isinstance(
                            fam_event.name,
                            (FamDivorce, FamSeparated)
                        ):
                            for witness_tuple in fam_event.witnesses:
                                witness_id = witness_tuple[0]
                                witness_info = get_witness_info(
                                    witness_id,
                                    person_repo
                                )
                                if witness_info:
                                    witnesses.append(witness_info)
                            if fam_event.note:
                                divorce_note = fam_event.note
                            break

                    events.append({
                        'type': 'divorce',
                        'date_display': divorce_display,
                        'spouse_id': spouse_id,
                        'spouse_first_name': (
                            spouse.first_name if spouse else None
                        ),
                        'spouse_surname': spouse.surname if spouse else None,
                        'date_range': '',
                        'duration': '',
                        'witnesses': witnesses,
                        'note': divorce_note,
                        '_sort_date': div_date,
                    })

    # Death event
    death_types = (Dead, DeadYoung, DeadDontKnowWhen)
    if isinstance(person.death_status, death_types):
        if (
            hasattr(person.death_status, 'death_date')
            and person.death_status.death_date
        ):
            if isinstance(person.death_status.death_date, CalendarDate):
                death_display = format_date(person.death_status.death_date)
            events.append({
                'type': 'death',
                'date_display': death_display,
                'place': person.death_place if person.death_place else None,
                '_sort_date': person.death_status.death_date,
            })

    # Sort events chronologically by date
    events.sort(key=get_sort_key)

    # Remove the internal _sort_date field from final output
    for event in events:
        event.pop('_sort_date', None)

    return events


def get_notes(
    person,
    family_repo: FamilyRepository,
    person_repo: PersonRepository
) -> Dict[str, Any]:
    """Extract individual and marriage notes."""
    individual_notes: List[str] = []

    marriage_notes: List[Dict[str, str]] = []
    if person.families:
        for family_id in person.families:
            family = family_repo.get_family_by_id(family_id)

            # Get spouse name
            spouse_name = ''
            if family.parents.is_couple():
                father_id, mother_id = family.parents.couple()
                spouse_id = (
                    mother_id if father_id == person.index else father_id
                )
                spouse = person_repo.get_person_by_id(spouse_id)
                spouse_name = f"{spouse.first_name} {spouse.surname}"

            # Collect all marriage-related notes
            note_content = ''

            if family.marriage_note:
                note_content = family.marriage_note

            if family.comment:
                if note_content:
                    note_content += f"\n{family.comment}"
                else:
                    note_content = family.comment

            # Only add if there's actual content
            if note_content:
                marriage_notes.append({
                    'spouse_name': spouse_name,
                    'content': note_content,
                })

    return {
        'individual_notes': individual_notes,
        'marriage_notes': marriage_notes,
    }


def get_event_name(event_name) -> str:
    """Get the event name as a capitalized string."""
    import re
    event_type = type(event_name).__name__
    # Convert from CamelCase to readable format
    # e.g., FamMarriage -> Marriage, FamDivorce -> Divorce
    if event_type.startswith('Fam'):
        event_type = event_type[3:]  # Remove 'Fam' prefix
    elif event_type.startswith('Pers'):
        event_type = event_type[4:]  # Remove 'Pers' prefix

    # Add spaces before capital letters
    readable = re.sub(r'([A-Z])', r' \1', event_type).strip()
    return readable.capitalize()


def get_sources(
    person,
    family_repo: FamilyRepository
) -> List[Dict[str, Any]]:
    """Extract sources from person and families."""
    sources = []

    if person.src:
        sources.append({
            'type': 'individual',
            'content': person.src,
        })

    if person.birth_src:
        sources.append({
            'type': 'birth',
            'content': person.birth_src,
        })

    if person.death_src:
        sources.append({
            'type': 'death',
            'content': person.death_src,
        })

    if person.families:
        for family_id in person.families:
            family = family_repo.get_family_by_id(family_id)

            # Get family source
            if family.src:
                sources.append({
                    'type': 'family',
                    'content': family.src,
                })

            # Get sources from all family events
            for fam_event in family.family_events:
                if fam_event.src:
                    event_type = get_event_name(fam_event.name)
                    sources.append({
                        'type': event_type,
                        'content': fam_event.src,
                    })

    return sources


# Month names for different calendar types
GREGORIAN_MONTHS = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
}

JULIAN_MONTHS = GREGORIAN_MONTHS  # Same as Gregorian

FRENCH_MONTHS = {
    1: 'Vendémiaire', 2: 'Brumaire', 3: 'Frimaire', 4: 'Nivôse',
    5: 'Pluviôse', 6: 'Ventôse', 7: 'Germinal', 8: 'Floréal',
    9: 'Prairial', 10: 'Messidor', 11: 'Thermidor', 12: 'Fructidor',
    13: 'Sansculottides'
}

HEBREW_MONTHS = {
    1: 'Tishrei', 2: 'Heshvan', 3: 'Kislev', 4: 'Tevet',
    5: 'Shevat', 6: 'Adar', 7: 'Nisan', 8: 'Iyar',
    9: 'Sivan', 10: 'Tammuz', 11: 'Av', 12: 'Elul',
    13: 'Adar I', 14: 'Adar II'  # For leap years
}


def format_date(date) -> str:
    """Format a date for display as 'day month year'."""
    if not isinstance(date, CalendarDate):
        return ''

    day = date.dmy.day if date.dmy.day > 0 else None
    month = date.dmy.month if date.dmy.month > 0 else None
    year = date.dmy.year if date.dmy.year > 0 else None

    # Select appropriate month names based on calendar type
    if date.cal == Calendar.GREGORIAN:
        month_names = GREGORIAN_MONTHS
    elif date.cal == Calendar.JULIAN:
        month_names = JULIAN_MONTHS
    elif date.cal == Calendar.FRENCH:
        month_names = FRENCH_MONTHS
    elif date.cal == Calendar.HEBREW:
        month_names = HEBREW_MONTHS
    else:
        month_names = GREGORIAN_MONTHS  # Default

    # Format the date based on available components
    parts = []
    if day:
        parts.append(str(day))
    if month and month in month_names:
        parts.append(month_names[month])
    if year:
        parts.append(str(year))

    return ' '.join(parts) if parts else ''


def implem_gwd_details(base, lang="en"):
    """Main route handler for person details page."""
    start_time = time.time()

    # Get query parameters
    person_id = request.args.get('i', type=int)
    person_first_name = request.args.get('p', type=str)
    person_surname = request.args.get('n', type=str)

    # Validate query parameters
    if person_id is None:
        # If no ID, both first name and surname are required
        if not person_first_name or not person_surname:
            return render_template(
                "gwd/bad_request.html",
                base=base,
                lang=lang
            )
    # Initialize repositories
    try:
        db_service = get_db_service(base)
        person_repo = PersonRepository(db_service)
        family_repo = FamilyRepository(db_service)
    except FileNotFoundError:
        return render_template("gwd/not_found.html", base=base, lang=lang)

    # Get person data by ID or by name (ID has priority)
    person = None
    try:
        if person_id is not None:
            person = person_repo.get_person_by_id(person_id)
        elif person_first_name and person_surname:
            # Try to find person by name
            all_persons = person_repo.get_all_persons()
            for p in all_persons:
                if (
                    p.first_name == person_first_name and
                    p.surname == person_surname
                ):
                    person = p
                    break
    except (ValueError, Exception):
        # Person not found or error occurred
        person = None

    # If person not found, return not_found template
    if person is None:
        return render_template(
            "gwd/not_found.html",
            base=base,
            lang=lang,
            first_name=person_first_name,
            surname=person_surname
        )
    # Gather all data using separate functions
    basic_info = get_person_basic_info(person)
    vital_events = get_person_vital_events(person)
    family_info = get_family_info(person, family_repo, person_repo)
    children = get_children_info(person, family_repo, person_repo)
    siblings = get_siblings_info(person, family_repo, person_repo)
    timeline_events = get_timeline_events(person, family_repo, person_repo)
    notes = get_notes(person, family_repo, person_repo)
    sources = get_sources(person, family_repo)
    # Get ancestor tree with depth=2 (parents and grandparents only)
    ancestor_tree = get_ancestor_recursive(
        person.index, person_repo, family_repo, depth=0, max_depth=2
    )

    # Pass nested structure directly to template
    ancestors = {
        'father': ancestor_tree.get('father') if ancestor_tree else None,
        'mother': ancestor_tree.get('mother') if ancestor_tree else None,
    }

    # Calculate query time
    q_time = round(time.time() - start_time, 2)

    # Merge all data for template
    template_data = {
        'base': base,
        'lang': lang,
        **basic_info,
        **vital_events,
        **family_info,
        'children': children,
        'siblings': siblings,
        'timeline_events': timeline_events,
        **notes,
        'sources': sources,
        'ancestors': ancestors,
        'q_time': q_time,
        'nb_errors': 0,
        'errors_list': '',
    }

    return render_template("gwd/details.html", **template_data)
