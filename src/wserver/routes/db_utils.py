"""
Database utility functions for Geneweb Flask routes.
"""

import os
from database.sqlite_database_service import SQLiteDatabaseService


def get_db_service(base: str) -> SQLiteDatabaseService:
    """
    Return a connected SQLiteDatabaseService for the given base name.
    Raises FileNotFoundError if the database does not exist.
    """

    db_path = os.path.join("bases", f"{base}.db")
    if not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Database for base '{base}' not found. Expected at: {db_path}"
        )
    db_service = SQLiteDatabaseService(database_path=db_path)
    db_service.connect()
    return db_service
