from typing import Optional
from flask import g, render_template

from database.person import Person
from .db_utils import get_db_service


def route_search(
        base: str,
        lang: str = "en",
        sort: Optional[str] = None,
        on: Optional[str] = None,
        surname: Optional[str] = None,
        firstname: Optional[str] = None,
        previous_url: Optional[str] = None):

    g.locale = lang
    db_service = get_db_service(base)
    db_session = db_service.get_session()
    if not db_session:
        raise Exception("Could not get database session")

    # TODO: link to detail page
    # direct search
    # if surname and firstname:
    #     person = db_service.get(db_session, Person, {
    #         "surname": surname, "first_name": firstname})

    if sort is None and surname and (firstname is None or firstname == ""):
        persons = db_service.get_all(db_session, Person, {"surname": surname})
        return render_template(
            "gwd/search_surname.html",
            base=base,
            lang=lang,
            surname=surname,
            persons=persons,
            total_persons=len(persons),
            previous_url=previous_url)
    if sort is None and firstname and (surname is None or surname == ""):
        persons = db_service.get_all(
            db_session, Person, {"first_name": firstname})
        return render_template(
            "gwd/search_firstname.html",
            base=base,
            lang=lang,
            firstname=firstname,
            persons=persons,
            total_persons=len(persons),
            previous_url=previous_url)

    persons = db_service.get_all(db_session, Person)

    if sort == "alpha" and on == "surname":
        persons_sorted = sorted(
            persons,
            key=lambda p: ((p.surname or "").lower(),
                           (p.first_name or "").lower()),
        )
        groups: dict[str, list[Person]] = {}
        for p in persons_sorted:
            initial = (p.surname or "").strip()[:1].lower()
            if not initial or not initial.isalpha():
                initial = "#"
            groups.setdefault(initial, []).append(p)

        letters = sorted([letter for letter in groups.keys() if letter != "#"])
        if "#" in groups:
            letters.append("#")

        persons_grouped = [{"letter": letter, "persons": groups[letter]}
                           for letter in letters]

        return render_template(
            "gwd/search_surnames_alpha.html",
            base=base,
            lang=lang,
            previous_url=previous_url,
            persons_grouped=persons_grouped,
            total_persons=len(persons_sorted),
            total_surnames=len(groups),
        )

    if sort == "freq" and on == "surname":
        surname_groups: dict[str, list[Person]] = {}
        for p in persons:
            key = (p.surname or "").strip()
            surname_groups.setdefault(key, []).append(p)
        sorted_items = sorted(
            surname_groups.items(),
            key=lambda kv: (-len(kv[1]), (kv[0] or "").lower()),
        )
        persons_by_surname = [
            {"surname": name, "count": len(lst), "persons": lst}
            for name, lst in sorted_items
        ]

        return render_template(
            "gwd/search_surnames_freq.html",
            base=base,
            lang=lang,
            previous_url=previous_url,
            persons_grouped=persons_by_surname,
            total_persons=len(persons),
            total_surnames=len(surname_groups),
        )

    if sort == "alpha" and on == "firstname":
        persons_sorted = sorted(
            persons,
            key=lambda p: ((p.first_name or "").lower(),
                           (p.surname or "").lower()),
        )
        groups = {}
        for p in persons_sorted:
            initial = (p.first_name or "").strip()[:1].lower()
            if not initial or not initial.isalpha():
                initial = "#"
            groups.setdefault(initial, []).append(p)

        letters = sorted([letter for letter in groups.keys() if letter != "#"])
        if "#" in groups:
            letters.append("#")

        persons_grouped = [{"letter": letter, "persons": groups[letter]}
                           for letter in letters]

        return render_template(
            "gwd/search_firstnames_alpha.html",
            base=base,
            lang=lang,
            previous_url=previous_url,
            persons_grouped=persons_grouped,
            total_persons=len(persons_sorted),
            total_firstnames=len(groups),
        )

    if sort == "freq" and on == "firstname":
        firstname_groups: dict[str, list[Person]] = {}
        for p in persons:
            key = (p.first_name or "").strip()
            firstname_groups.setdefault(key, []).append(p)

        sorted_items = sorted(
            firstname_groups.items(),
            key=lambda kv: (-len(kv[1]), (kv[0] or "").lower())
        )
        persons_by_firstname = [
            {"firstname": name, "count": len(lst), "persons": lst}
            for name, lst in sorted_items
        ]

        return render_template(
            "gwd/search_firstnames_freq.html",
            base=base,
            lang=lang,
            previous_url=previous_url,
            persons_grouped=persons_by_firstname,
            total_persons=len(persons),
            total_firstnames=len(firstname_groups),
        )
    return "Error: missing surname and/or firstname", 400
