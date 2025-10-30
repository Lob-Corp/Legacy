from datetime import datetime, timedelta
from flask import request, render_template

from ..i18n import get_translator


def implem_route_AN(base):
    """Render the anniversaries-by-birth (AN) page for the given base.
    """
    req_lang = request.args.get('lang') or 'en'
    translator = get_translator()

    def _(key, capitalize_first=True):
        return translator.gettext(key, req_lang, capitalize_first)

    today = datetime.now().date()
    tomorrow = (today + timedelta(days=1))
    day_after = (today + timedelta(days=2))

    sections = [
        {'label': _('today', False), 'date': today, 'items': []},
        {'label': _('tomorrow', False), 'date': tomorrow, 'items': []},
        {'label': _('the day after tomorrow', False),
         'date': day_after, 'items': []},
    ]

    months = [(i + 1, _('(month)').split('/')[i]) for i in range(12)]

    current_month = datetime.now().month

    try:
        from ..routes.db_utils import get_db_service
        from repositories.person_repository import PersonRepository
        import libraries.death_info as death_info
        import libraries.date as lib_date

        db_service = get_db_service(base)
        person_repo = PersonRepository(db_service)
        persons = person_repo.get_all_persons()

        def extract_dmy(compressed_date):
            if compressed_date is None:
                return None
            if isinstance(compressed_date, lib_date.CalendarDate):
                dv = compressed_date.dmy
                if dv.day and dv.month:
                    return (dv.day, dv.month, dv.year)
            return None
        month_items = []

        for p in persons:
            if isinstance(p.death_status, death_info.NotDead):
                dmy = extract_dmy(p.birth_date)
                if dmy is None:
                    continue
                day, month, year = dmy
                display_name = f"{p.first_name} {p.surname}".strip()

                item = {
                    'id': p.index,
                    'name': display_name,
                    'given': p.first_name,
                    'occ': p.occ,
                    'surname': p.surname,
                    'day': day,
                    'month': month,
                    'year': year,
                }
                if month == current_month:
                    month_items.append(item)
                if (day == today.day and month == today.month):
                    sections[0]['items'].append(item)
                elif (day == tomorrow.day and month == tomorrow.month):
                    sections[1]['items'].append(item)
                elif (day == day_after.day and month == day_after.month):
                    sections[2]['items'].append(item)
        month_items.sort(key=lambda it: it['day'])

    except Exception:
        month_items = []
    data = {
        'lang': req_lang,
        'title': _('anniversaries of birth'),
        'base': base,
        'prefix': f'/gwd/{base}/',
        '_': _,
        'sections': sections,
        'months': months,
        'current_month': current_month,
        'month_items': month_items,
    }

    return render_template('gwd/an.html', **data)
