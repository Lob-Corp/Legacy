import re
from database.sqlite_database_service import SQLiteDatabaseService
from database.person import Person
from .gedcom_parser import parse_gedcom
from libraries.title import AccessRight
from libraries.death_info import DeathReason
from database.person import DeathStatus, BurialStatus


def get_indi_sex(gedcom_individual: dict):
    sex = gedcom_individual.get("sex")
    if not sex:
        return "unknown"
    sex = sex.upper()
    if sex == "M":
        gender = "male"
    elif sex == "F":
        gender = "female"
    elif sex in {"U", "", "UNKNOWN", "UNSPECIFIED"}:
        gender = "unknown"
    else:
        gender = "other"
    return gender


def gedcom_to_person(gedcom_individual: dict) -> Person:
    """Convert a parsed GEDCOM individual dict to a Person instance."""
    occus = gedcom_individual.get("occupation", [""])
    occupation = ", ".join(occus)
    return Person(
        first_name=gedcom_individual.get("name", ""),
        surname=gedcom_individual.get("surname", ""),
        occ=1,
        image=gedcom_individual.get("image", ""),
        public_name= gedcom_individual.get("name", "") + " " + gedcom_individual.get("surname", ""),
        qualifiers=gedcom_individual.get("qualifiers", ""),
        aliases=",".join(gedcom_individual.get("aliases", [])),
        first_names_aliases=gedcom_individual.get("first_names_aliases", ""),
        surname_aliases=gedcom_individual.get("surname_aliases", ""),
        occupation=occupation,
        sex=get_indi_sex(gedcom_individual),
        access_right=AccessRight.PUBLIC,
        birth_date="",
        birth_place="",
        birth_note=gedcom_individual.get("birth_note", ""),
        birth_src=gedcom_individual.get("birth_src", ""),
        baptism_date="",
        baptism_place=gedcom_individual.get("baptism_place", ""),
        baptism_note=gedcom_individual.get("baptism_note", ""),
        baptism_src=gedcom_individual.get("baptism_src", ""),
        death_status=gedcom_individual.get("death_status", DeathStatus.DONT_KNOW_IF_DEAD),
        death_reason=DeathReason.UNSPECIFIED,
        death_date=str(gedcom_individual.get("death_date", "")),
        death_place=str(gedcom_individual.get("death_place", "")),
        death_note=gedcom_individual.get("death_note", ""),
        death_src=gedcom_individual.get("death_src", ""),
        burial_status=BurialStatus.UNKNOWN_BURIAL,
        burial_date="",
        burial_place=gedcom_individual.get("burial_place", ""),
        burial_note=gedcom_individual.get("burial_note", ""),
        burial_src=gedcom_individual.get("burial_src", ""),
        notes="\n".join(gedcom_individual.get("notes", [])),
        src=gedcom_individual.get("src", "")
    )


def import_gedcom(path: str, db: SQLiteDatabaseService) -> None:
    """
    Import a GEDCOM file into the database.
    Args:
        path (str): Path to the GEDCOM file.
        db (SQLiteDatabaseService): Service of the SQLite database file.
    """
    sess = db.get_session()

    data = parse_gedcom(path)
    persons = []
    print(f"Parsed {len(data['data'])} individuals using {data['method']} (GEDCOM {data['version']})")
    for individual in data['data']:
        persons.append(gedcom_to_person(individual))
    db.add_all(sess, persons)
    db.apply(sess)


if __name__ == "__main__":
    db_service = SQLiteDatabaseService("aldric.db")
    db_service.connect()
    import_gedcom("src/gedcom_import/washington.ged", db_service)
