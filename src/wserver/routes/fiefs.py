from typing import Optional
from flask import g, render_template
from sqlalchemy import func

from database.titles import Titles
from database.person_titles import PersonTitles
from .db_utils import get_db_service


def route_fiefs(
        base: str,
        lang: str = "en",
        previous_url: Optional[str] = None):
    g.locale = lang
    db_service = get_db_service(base)
    db_session = db_service.get_session()
    if not db_session:
        raise Exception("Could not get database session")

    titles_query = (
        db_session.query(Titles.name, func.count(
            PersonTitles.id).label('count'))
        .join(PersonTitles, PersonTitles.title_id == Titles.id)
        .filter(Titles.name != '')
        .group_by(Titles.name)
        .order_by(Titles.name)
    )

    titles = titles_query.all()

    return render_template(
        "gwd/fiefs_all.html",
        base=base,
        lang=lang,
        previous_url=previous_url,
        titles=titles,
        total_titles=len(titles)
    )
