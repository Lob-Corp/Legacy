from typing import List
from database.sqlite_database_service import SQLiteDatabaseService

import libraries.family as app_family
import database.family as db_family
import database.family_event as db_family_event
import database.family_event_witness as db_family_event_witness
import database.descend_children as db_descend_children
import database.family_witness as db_witness
from repositories.converter_from_db import convert_family_from_db


class FamilyRepository:
    def __init__(self, db_service: SQLiteDatabaseService):
        self.db_service = db_service

    def get_family_by_id(self, family_id: int) -> app_family.Family:
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")
        family = self.db_service.get(
            session, db_family.Family, {
                "id": family_id})
        witnesses = self.db_service.get_all(session=session,
                                            model=db_witness.FamilyWitness,
                                            filters={"family_id": family_id})
        events = self.db_service.get_all(
            session=session,
            model=db_family_event.FamilyEvent,
            filters={"family_id": family_id}
        )
        events_with_witnesses = [(event, self.db_service.get_all(
            session=session,
            model=db_family_event_witness.FamilyEventWitness,
            filters={"event_id": event.id}
        )) for event in events]
        children = self.db_service.get_all(
            session=session,
            model=db_descend_children.DescendChildren,
            filters={"descend_id": family.children_id}
        )
        session.close()
        if family is None:
            raise ValueError(f"Family with id {family_id} not found")
        if witnesses is None:
            witnesses = []
        return convert_family_from_db(
            family, witnesses, events_with_witnesses, children)

    def get_all_families(self) -> List[app_family.Family]:
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")
        families = self.db_service.get_all(session, db_family.Family)
        result = []
        for family in families:
            witnesses = self.db_service.get_all(session=session,
                                                model=db_witness.FamilyWitness,
                                                filters={"family_id":
                                                         family.id})
            events = self.db_service.get_all(
                session=session,
                model=db_family_event.FamilyEvent,
                filters={"family_id": family.id}
            )
            events_with_witnesses = [(event, self.db_service.get_all(
                session=session,
                model=db_family_event_witness.FamilyEventWitness,
                filters={"event_id": event.id}
            )) for event in events]
            children = self.db_service.get_all(
                session=session,
                model=db_descend_children.DescendChildren,
                filters={"descend_id": family.children_id}
            )
            if witnesses is None:
                witnesses = []
            app_family_instance = convert_family_from_db(
                family, witnesses, events_with_witnesses, children)
            result.append(app_family_instance)
        session.close()
        return result
