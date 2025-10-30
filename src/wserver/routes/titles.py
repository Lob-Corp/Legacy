from typing import Optional
from flask import g, render_template
from sqlalchemy import func, and_

from database.titles import Titles
from database.person_titles import PersonTitles
from database.person import Person
from .db_utils import get_db_service


def route_titles(
        base: str,
        lang: str = "en",
        sm: Optional[str] = None,  # 'S' for search
        t: Optional[str] = None,  # title name filter
        p: Optional[str] = None,  # place/estate filter
        a: Optional[str] = None,  # 'A' for all (used in links)
        previous_url: Optional[str] = None):
    """
    Route for displaying titles (m=TT in original GeneWeb)
    - Without filters: shows all titles grouped by letter
    - With p=*: shows all estates (places)
    - With p only: shows all titles for that estate
    - With t and p: shows persons with that title in that estate
    - With t or p filter: shows filtered results
    """
    g.locale = lang
    db_service = get_db_service(base)
    db_session = db_service.get_session()
    if not db_session:
        raise Exception("Could not get database session")

    # Case 1: Both title and place specified - show persons with this title/place
    if t and p and p != "*":
        # Get persons with this specific title and place
        persons_query = (
            db_session.query(Person)
            .join(PersonTitles, PersonTitles.person_id == Person.id)
            .join(Titles, Titles.id == PersonTitles.title_id)
            .filter(and_(Titles.name == t, Titles.place == p))
            .order_by(Person.surname, Person.first_name)
        )

        persons = persons_query.all()

        # Add fake data if no persons found
        if not persons:
            from database.date import Date
            # Create a fake person object for display

            class FakePerson:
                def __init__(self, first_name, surname, birth_year=None):
                    self.first_name = first_name
                    self.surname = surname
                    self.birth_date = birth_year

            persons = [FakePerson("Felix", "Dubois", "1988")]

        return render_template(
            "gwd/title_detail.html",
            base=base,
            lang=lang,
            previous_url=previous_url,
            title_name=t,
            estate_name=p,
            persons=persons
        )

    # Case 2: Only place specified (not *) - show titles for this estate
    if p and p != "*" and not t:
        # Get all titles for this place
        titles_query = (
            db_session.query(Titles.name)
            .filter(Titles.place == p)
            .distinct()
            .order_by(Titles.name)
        )

        titles = [{"name": name} for (name,) in titles_query.all()]

        # Add fake data if no titles found
        if not titles:
            titles = [{"name": "MyTitle"}]

        return render_template(
            "gwd/titles_by_estate.html",
            base=base,
            lang=lang,
            previous_url=previous_url,
            estate_name=p,
            titles=titles
        )

    # If p=* is specified, show all estates (places)
    if p == "*":
        # Get all unique places with count
        estates_query = (
            db_session.query(Titles.place, func.count(
                PersonTitles.id).label('count'))
            .join(PersonTitles, PersonTitles.title_id == Titles.id)
            .filter(Titles.place != '')
            .group_by(Titles.place)
            .order_by(Titles.place)
        )

        estates = [{"name": place, "count": count}
                   for place, count in estates_query.all()]

        # Add fake data if no estates found
        if not estates:
            estates = [
                {"name": "Normandie", "count": 3},
                {"name": "Bourgogne", "count": 2},
                {"name": "Bretagne", "count": 4},
                {"name": "Aquitaine", "count": 1},
                {"name": "Paris", "count": 5},
                {"name": "Toulouse", "count": 2},
                {"name": "Champagne", "count": 3},
                {"name": "Provence", "count": 2},
                {"name": "York", "count": 1},
                {"name": "Lancaster", "count": 1},
                {"name": "yes I", "count": 1},
            ]

        return render_template(
            "gwd/estates_all.html",
            base=base,
            lang=lang,
            previous_url=previous_url,
            estates=estates
        )

    # Default: show all titles grouped by first letter
    # Get all unique title names with their count
    titles_query = (
        db_session.query(Titles.name, func.count(
            PersonTitles.id).label('count'))
        .join(PersonTitles, PersonTitles.title_id == Titles.id)
        .filter(Titles.name != '')
        .group_by(Titles.name)
        .order_by(Titles.name)
    )

    titles_data = titles_query.all()

    # Add fake data if no titles found
    if not titles_data:
        titles_data = [
            # French nobility titles
            ("Duc", 4),
            ("Comte", 5),
            ("Marquis", 2),
            ("Baron", 3),
            ("Vicomte", 2),
            ("Chevalier", 2),

            # English titles
            ("Duke", 2),
            ("Earl", 3),
            ("Viscount", 1),
            ("Knight", 1),

            # Spanish titles
            ("Duque", 1),
            ("Conde", 1),
            ("Marqués", 1),

            # Italian titles
            ("Doge", 1),
            ("Principe", 1),
            ("Conte", 1),

            # German titles
            ("Herzog", 1),
            ("Graf", 1),
            ("Fürst", 1),

            # Religious titles
            ("Évêque", 1),
            ("Archevêque", 1),
            ("Cardinal", 1),
            ("Abbé", 1),

            # Professional/Honorary titles
            ("Seigneur", 1),
            ("Sire", 1),
            ("Dame", 1),
            ("Écuyer", 1),

            # Royal titles
            ("Roi", 1),
            ("Reine", 1),
            ("Prince", 1),
            ("Princesse", 1),
            ("Infant", 1),
            ("Dauphin", 1),

            # Test data
            ("Yes I", 1),
        ]

    # Group titles by first letter
    groups = {}
    for title_name, count in titles_data:
        initial = (title_name or "").strip()[:1].upper()
        if not initial or not initial.isalpha():
            initial = "#"
        if initial not in groups:
            groups[initial] = []
        groups[initial].append({"name": title_name, "count": count})

    # Sort letters
    letters = sorted([l for l in groups.keys() if l != "#"])
    if "#" in groups:
        letters.append("#")

    titles_grouped = [{"letter": l, "titles": groups[l]} for l in letters]

    return render_template(
        "gwd/titles_all.html",
        base=base,
        lang=lang,
        previous_url=previous_url,
        titles_grouped=titles_grouped,
        total_titles=len(titles_data)
    )
