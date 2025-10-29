from __future__ import annotations

import os
import re
import sys
from typing import Sequence

import click

from database.sqlite_database_service import SQLiteDatabaseService
from database.ascends import Ascends  # noqa: F401
from database.couple import Couple  # noqa: F401
from database.date import Date  # noqa: F401
from database.descend_children import DescendChildren  # noqa: F401
from database.descends import Descends  # noqa: F401
from database.family import Family  # noqa: F401
from database.family_event import FamilyEvent  # noqa: F401
from database.family_event_witness import FamilyEventWitness  # noqa: F401
from database.family_events import FamilyEvents  # noqa: F401
from database.family_witness import FamilyWitness  # noqa: F401
from database.person import Person  # noqa: F401
from database.person_event_witness import PersonEventWitness  # noqa: F401
from database.person_events import PersonEvents  # noqa: F401
from database.person_non_native_relations import PersonNonNativeRelations  # noqa: F401
from database.person_relations import PersonRelations  # noqa: F401
from database.person_titles import PersonTitles  # noqa: F401
from database.personal_event import PersonalEvent  # noqa: F401
from database.place import Place  # noqa: F401
from database.relation import Relation  # noqa: F401
from database.titles import Titles  # noqa: F401
from database.union_families import UnionFamilies  # noqa: F401
from database.unions import Unions  # noqa: F401

_NAME_RE = re.compile(r"^[A-Za-z0-9_\-]+$")

DEFAULT_BASES_DIR = "bases"


def _validate_database_name(name: str) -> tuple[bool, str]:
    if not name:
        return False, "database name is required"
    if not _NAME_RE.match(name):
        return False, "invalid database name: [A-Za-z0-9_\\-] are allowed"
    return True, ""


def create_database(name: str) -> tuple[bool, str]:
    ok, err = _validate_database_name(name)
    if not ok:
        return False, err

    if not os.path.exists(DEFAULT_BASES_DIR):
        os.makedirs(DEFAULT_BASES_DIR)

    db_path = os.path.join(DEFAULT_BASES_DIR, f"{name}.db")
    if os.path.exists(db_path):
        return False, f"database '{name}' already exists at {db_path}"

    db_service = SQLiteDatabaseService(database_path=db_path)
    try:
        db_service.connect()
    except Exception as e:
        return False, f"failed to create database '{name}': {e}"
    return True, f"Created database '{name}' at {db_path}"


def delete_database(name: str) -> tuple[bool, str]:
    ok, err = _validate_database_name(name)
    if not ok:
        return False, err

    db_path = os.path.join(DEFAULT_BASES_DIR, f"{name}.db")
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception as e:
            return False, f"failed to remove database file: {e}"
        return True, f"Deleted database '{name}' (file removed)"
    return False, f"database '{name}' does not exist at {db_path}"


@click.group()
def cli() -> None:
    pass


@cli.group()
def database() -> None:
    pass


@database.command("create")
@click.argument("name")
def create_cmd(name: str) -> None:
    ok, msg = create_database(name)
    click.echo(msg)
    if not ok:
        raise SystemExit(1)


@database.command("delete")
@click.argument("name")
def delete_cmd(name: str) -> None:
    ok, msg = delete_database(name)
    click.echo(msg)
    if not ok:
        raise SystemExit(1)


def run(argv: Sequence[str]) -> int:
    try:
        # standalone_mode=False prevents Click from calling sys.exit
        cli.main(args=list(argv), prog_name="gwsetup.py",
                 standalone_mode=False)
        return 0
    except SystemExit as e:
        # e.code may be None, int, or other; normalize to int
        code = e.code
        if code is None:
            return 0
        try:
            return int(code)
        except Exception:
            return 1


def main() -> None:
    rc = run(sys.argv[1:])
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
