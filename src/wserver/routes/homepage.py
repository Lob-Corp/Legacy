from typing import Optional
from flask import g, render_template

from database.person import Person
from wserver.routes.db_utils import get_db_service


def route_homepage(base: str, lang: str = "en", previous_url: Optional[str] = None) -> str:
    g.locale = lang
    db_service = get_db_service(base)
    db_session = db_service.get_session()
    if not db_session:
        raise Exception("Could not get database session")

    persons = db_service.get_all(db_session, Person)
    return render_template(
        "gwd/homepage.html",
        base=base,
        lang=lang,
        previous_url=previous_url,
        total_persons=len(persons)
    )
