from database.sqlite_database_service import SQLiteDatabaseService
from sqlalchemy.orm import Session

import libraries.family as app_family
import database.family as db_family


class FamilyRepository:
    def __init__(self, db_service: SQLiteDatabaseService):
        self.db_service = db_service

    def get_family_by_id(self, family_id: int) -> app_family.Family:
        session: Session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")
        family = self.db_service.get(
            session, db_family.Family, {
                "id": family_id})
        session.close()
        return convert_from_db(family)
