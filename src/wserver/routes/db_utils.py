"""
Database utility functions for Geneweb Flask routes.
"""

import os
from database.sqlite_database_service import SQLiteDatabaseService


def _import_all_models() -> None:
    """Import all ORM models so SQLAlchemy registers mappers before create_all.

    This avoids string-based relationship resolution failures like 'Couple'
    not found when only a subset of models were imported before engine init.
    """
    try:  # pragma: no cover - import side effects only
        import database.person  # noqa: F401
        import database.family  # noqa: F401
        import database.couple  # noqa: F401
        import database.ascends  # noqa: F401
        import database.descends  # noqa: F401
        import database.unions  # noqa: F401
        import database.union_families  # noqa: F401
        import database.date  # noqa: F401
        import database.place  # noqa: F401
        import database.relation  # noqa: F401
        import database.titles  # noqa: F401
        import database.personal_event  # noqa: F401
        import database.person_event_witness  # noqa: F401
        import database.person_events  # noqa: F401
        import database.person_relations  # noqa: F401
        import database.person_non_native_relations  # noqa: F401
        import database.person_titles  # noqa: F401
        import database.family_event  # noqa: F401
        import database.family_events  # noqa: F401
        # Optional extras if present
        try:
            import database.family_event_witness  # noqa: F401
            import database.family_witness  # noqa: F401
        except Exception:
            pass
    except Exception:
        # If any import fails here, we'll let SQLAlchemy resolve later; this
        # hook primarily ensures typical routes load all models.
        pass


def get_db_service(base: str) -> SQLiteDatabaseService:
    """
    Return a connected SQLiteDatabaseService for the given base name.
    Raises FileNotFoundError if the database does not exist.

    Note: This function imports all database models to ensure SQLAlchemy
    can properly initialize all mappers and resolve relationships.
    """
    # Get the project root (3 levels up from this file)
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(current_file))))
    db_path = os.path.join(project_root, 'bases', f'{base}.db')
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Database for base '{base}' not found. Expected at: {db_path}"
        )
    db_service = SQLiteDatabaseService(database_path=db_path)
    # Ensure models are registered before connecting/creating metadata
    _import_all_models()
    db_service.connect()
    return db_service
