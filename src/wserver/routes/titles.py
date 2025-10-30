from typing import Optional
from flask import g, render_template

from database.titles import Titles
from database.person_titles import PersonTitles
from database.person import Person
from .db_utils import get_db_service


def route_titles(
        base: str,
        lang: str = "en",
        title: Optional[str] = None,
        fief: Optional[str] = None,
        previous_url: Optional[str] = None):
    g.locale = lang
    db_service = get_db_service(base)
    db_session = db_service.get_session()
    if not db_session:
        raise Exception("Could not get database session")

    if (title and title != "") or (fief and fief != ""):
        q = db_session.query(Titles)
        if title and title != "":
            q = q.filter(Titles.name.ilike(f"%{title}%"))
        if fief and fief != "":
            q = q.filter(Titles.place.ilike(f"%{fief}%"))
        q = q.order_by(Titles.name)
        titles = q.all()
        if len(titles) == 1:
            the_title = titles[0]
            persons = (
                db_session.query(Person)
                .join(PersonTitles, Person.id == PersonTitles.person_id)
                .filter(PersonTitles.title_id == the_title.id)
                .order_by(Person.surname, Person.first_name)
                .all()
            )

            return render_template(
                "gwd/title_detail.html",
                base=base,
                lang=lang,
                previous_url=previous_url,
                title_name=the_title.name,
                estate_name=the_title.place,
                persons=persons,
            )
    else:
        titles_query = (
            db_session.query(Titles)
            .filter(Titles.name != '')
            .order_by(Titles.name)
        )
        titles = titles_query.all()

    groups = {}
    for t in titles:
        initial = (t.name or "").strip()[:1].upper()
        if not initial or not initial.isalpha():
            initial = "#"
        if initial not in groups:
            groups[initial] = []
        groups[initial].append({"name": t.name})

    letters = sorted([letter for letter in groups.keys() if letter != "#"])
    if "#" in groups:
        letters.append("#")

    persons_grouped = [{
        "letter": letter,
        "titles": groups[letter]} for letter in letters]

    return render_template(
        "gwd/titles_all.html",
        base=base,
        lang=lang,
        previous_url=previous_url,
        persons_grouped=persons_grouped,
        total_titles=len(titles)
    )
