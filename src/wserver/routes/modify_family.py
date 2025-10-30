"""
Route and helpers for the modify_family page in Geneweb Flask app.
All helper functions are at module level for clarity and testability.
"""
from flask import (
    render_template, request, current_app, jsonify, redirect, url_for, g, abort
)
from .db_utils import get_db_service
import hashlib
from urllib.parse import urlencode


def gwd_url(base, lang='en', **params):
    """
    Generate a GWD-style URL with query parameters.
    Used as a template helper to replace url_for('base', ...) calls.
    
    Args:
        base: The database base name
        lang: The language code
        **params: Additional query parameters (m, i, ip, p, n, etc.)
    
    Returns:
        A URL string like /gwd/base_name/lang?m=MODE&i=123&ip=456
    """
    # Build the base URL path
    url_path = f"/gwd/{base}/{lang}"
    
    # Add query parameters if any
    if params:
        clean_params = {k: v for k, v in params.items() if v is not None}
        query_string = urlencode(clean_params)
        url_path = f"{url_path}?{query_string}"
    
    return url_path


def get_first(form_data, single_key: str, default: str = "") -> str:
    """Get the first value for a form field, or default if missing."""
    vals = form_data.get(single_key)
    return vals[0] if vals and len(vals) > 0 else default


def implem_route_MOD_FAM(base, lang='en'):
    """
    Handle GET and POST requests for the modify_family page.
    On GET, displays the family modification form with existing data.
    On POST, updates the family in the database.
    """
    g.locale = lang

    # Get family_id from query parameters
    family_id = request.args.get('i', type=int)
    person_id = request.args.get('ip', type=int)
    print(f"MOD_FAM called with family_id={family_id}, person_id={person_id}")

    if not family_id:
        abort(400, description="Missing family ID parameter 'i'")

    if not person_id:
        abort(400, description="Missing person ID parameter 'ip'")

    try:
        db_service = get_db_service(base)
    except FileNotFoundError as e:
        msg = str(e)
        if request.accept_mimetypes.best == 'application/json':
            return jsonify({'ok': False, 'error': msg}), 404
        abort(404, description=msg)

    from repositories.family_repository import FamilyRepository
    from repositories.person_repository import PersonRepository

    family_repo = FamilyRepository(db_service)
    person_repo = PersonRepository(db_service)

    try:
        # Fetch the family using repository
        lib_family = family_repo.get_family_by_id(family_id)
        
        # Fetch the reference person using repository
        lib_person = person_repo.get_person_by_id(person_id)
        
        # Get parents (father_id and mother_id are in lib_family.parents tuple)
        father_id, mother_id = lib_family.parents.couple()
        
        # Fetch parent persons
        father = None
        mother = None
        if father_id:
            try:
                father = person_repo.get_person_by_id(father_id)
            except ValueError:
                pass
        if mother_id:
            try:
                mother = person_repo.get_person_by_id(mother_id)
            except ValueError:
                pass
        
        # Determine spouse (the parent who is not the reference person)
        if father and father.index == person_id:
            spouse = mother
        else:
            spouse = father
        parent1 = father
        parent2 = mother
        
        # Get children - they're already in lib_family.children list
        # Children are person IDs, need to fetch them
        children_persons = []
        for child_id in lib_family.children:
            try:
                child_person = person_repo.get_person_by_id(child_id)
                children_persons.append(child_person)
            except ValueError:
                continue

        # Convert library objects to template-friendly dictionaries
        person_data = {
            'id': lib_person.index,
            'first_name': lib_person.first_name or '',
            'last_name': lib_person.surname or '',
            'occ': lib_person.occ or 0,
            'sex': lib_person.sex.name if lib_person.sex else 'NEUTER'
        }

        spouse_data = {
            'first_name': spouse.first_name if spouse else '',
            'last_name': spouse.surname if spouse else '',
            'occ': spouse.occ if spouse else 0,
            'id': spouse.index if spouse else None
        } if spouse else {
            'first_name': '',
            'last_name': '',
            'occ': 0,
            'id': None
        }

        parent1_data = {
            'first_name': parent1.first_name if parent1 else '',
            'surname': parent1.surname if parent1 else '',
            'occ': parent1.occ if parent1 else 0,
            'id': parent1.index if parent1 else None,
            'sex': parent1.sex.name if parent1 and parent1.sex else 'MALE'
        }

        parent2_data = {
            'first_name': parent2.first_name if parent2 else '',
            'surname': parent2.surname if parent2 else '',
            'occ': parent2.occ if parent2 else 0,
            'id': parent2.index if parent2 else None,
            'sex': parent2.sex.name if parent2 and parent2.sex else 'FEMALE'
        }

        children_data = []
        for child in children_persons:
            children_data.append({
                'id': child.index,
                'first_name': child.first_name or '',
                'surname': child.surname or '',
                'occ': child.occ or 0,
                'sex': child.sex.name if child.sex else 'NEUTER',
                'link_mode': True  # Existing children are linked
            })

        # Get family events from lib_family
        family_events = []
        for event in lib_family.family_events:
            family_events.append({
                'name': event.name,
                'date': event.date,
                'place': event.place,
                'note': event.note,
                'src': event.src,
                'witnesses': event.witnesses
            })

        # Generate digest for form validation (simple hash of family state)
        digest_data = f"{family_id}:{father_id}:{mother_id}"
        digest = hashlib.md5(digest_data.encode()).hexdigest()

        family_data = {
            'id': family_id,
            'no_sex_check': False,
            'events': family_events,
            'children': children_data,
            'comment': lib_family.comment or '',
            'sources': lib_family.src or '',
            'person_sources': ''
        }

        # Handle POST request (form submission)
        if request.method == 'POST':
            form_data = request.form.to_dict(flat=False)

            # Validate digest
            submitted_digest = get_first(form_data, 'digest', '')
            if submitted_digest != digest:
                msg = ("Form data has been modified. "
                       "Please refresh and try again.")
                abort(400, description=msg)

            # TODO: Implement family update logic here
            # This would involve:
            # 1. Updating parent information
            # 2. Updating/adding/removing children
            # 3. Updating family events
            # 4. Updating sources and comments

            current_app.logger.info(
                f"MOD_FAM_OK would be processed for family {family_id}")

            # For now, redirect back to the family view
            return redirect(
                url_for(
                    'gwd.route_MOD_FAM', base=base, i=family_id,
                    ip=person_id, lang=lang))

        # Render the template
        return render_template(
            'gwd/modify_family.html',
            base=base,
            lang=lang,
            gwd_url=lambda **params: gwd_url(base, lang, **params),
            base_url=url_for('gwd.gwd_base_only', base=base, lang=lang),
            family=family_data,
            person=person_data,
            spouse=spouse_data,
            parent1=parent1_data,
            parent2=parent2_data,
            digest=digest,
            query_time=0.0,  # TODO: calculate actual query time
            errors=[],
            errors_list=''
        )
    
    except ValueError as e:
        abort(404, description=str(e))
    except Exception as e:
        current_app.logger.error(f"Error in MOD_FAM: {e}")
        abort(500, description="Internal server error")


def implem_route_MOD_FAM_OK(base, lang='en'):
    """
    Handle the POST request to actually modify the family data.
    This is the action route that processes the form submission.
    """
    g.locale = lang

    if request.method != 'POST':
        abort(405, description="Method not allowed. Use POST.")

    form_data = request.form.to_dict(flat=False)
    family_id = get_first(form_data, 'i', '')
    person_id = get_first(form_data, 'ip', '')

    if not family_id or not person_id:
        abort(400, description="Missing required form data")

    try:
        family_id = int(family_id)
        person_id = int(person_id)
    except ValueError:
        abort(400, description="Invalid family or person ID")

    try:
        # Get database service for repositories
        # db_service = get_db_service(base)
        # family_repo = db_service.get_family_repository()
        # person_repo = db_service.get_person_repository()
        pass
    except FileNotFoundError as e:
        msg = str(e)
        if request.accept_mimetypes.best == 'application/json':
            return jsonify({'ok': False, 'error': msg}), 404
        abort(404, description=msg)

    # TODO: Implement the actual family update logic
    # This would involve:
    # 1. Parse all form fields
    # 2. Validate data
    # 3. Update database records
    # 4. Handle parent changes
    # 5. Handle children additions/removals
    # 6. Update events
    # 7. Update sources and comments

    current_app.logger.info(
        f"Family {family_id} would be updated with form data")

    # For now, redirect back to the person's page or family view
    # In production, this would redirect after successful update
    return redirect(
        url_for(
            'gwd.route_MOD_FAM', base=base, i=family_id,
            ip=person_id, lang=lang))
