from typing import List
from database.sqlite_database_service import SQLiteDatabaseService

import libraries.family as app_family
import database.family as db_family
import database.family_event as db_family_event
import database.family_event_witness as db_family_event_witness
import database.descend_children as db_descend_children
import database.family_witness as db_witness
import database.descends as db_descend
import database.couple as db_couple
from repositories.converter_from_db import convert_family_from_db
from repositories.converter_to_db import convert_family_to_db


class FamilyRepository:
    def __init__(self, db_service: SQLiteDatabaseService):
        self.db_service = db_service

    def get_family_by_id(
            self, family_id: int) -> app_family.Family[int, int, str]:
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")
        family = self.db_service.get(
            session, db_family.Family, {
                "id": family_id})
        if family is None:
            session.close()
            raise ValueError(f"Family with id {family_id} not found")
        witnesses = self.db_service.get_all(session=session,
                                            model=db_witness.FamilyWitness,
                                            query={"family_id": family_id})
        events = self.db_service.get_all(
            session=session,
            model=db_family_event.FamilyEvent,
            query={"family_id": family_id}
        )
        events_with_witnesses = [(event, self.db_service.get_all(
            session=session,
            model=db_family_event_witness.FamilyEventWitness,
            query={"event_id": event.id}
        )) for event in events]
        children = self.db_service.get_all(
            session=session,
            model=db_descend_children.DescendChildren,
            query={"descend_id": family.children_id}
        )
        if witnesses is None:
            witnesses = []
        result = convert_family_from_db(
            family, witnesses, events_with_witnesses, children)
        session.close()
        return result

    def get_all_families(self) -> List[app_family.Family[int, int, str]]:
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")
        families = self.db_service.get_all(session, db_family.Family)
        result = []
        for family in families:
            witnesses = self.db_service.get_all(
                session=session,
                model=db_witness.FamilyWitness,
                query={"family_id": family.id}
            )
            events = self.db_service.get_all(
                session=session,
                model=db_family_event.FamilyEvent,
                query={"family_id": family.id}
            )
            events_with_witnesses = [(event, self.db_service.get_all(
                session=session,
                model=db_family_event_witness.FamilyEventWitness,
                query={"event_id": event.id}
            )) for event in events]
            children = self.db_service.get_all(
                session=session,
                model=db_descend_children.DescendChildren,
                query={"descend_id": family.children_id}
            )
            if witnesses is None:
                witnesses = []
            app_family_instance = convert_family_from_db(
                family, witnesses, events_with_witnesses, children)
            result.append(app_family_instance)
        session.close()
        return result

    def add_family(self, family: app_family.Family[int, int, str]) -> bool:
        """Add a new family to the database."""
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")

        try:
            from database.couple import Couple
            couple = Couple(
                father_id=family.parents[0],
                mother_id=family.parents[1]
            )
            self.db_service.add(session, couple)
            session.flush()  # Get couple ID

            (db_family_instance, witnesses, events_with_witnesses,
             children) = convert_family_to_db(family, couple.id)

            self.db_service.add(session, db_family_instance)
            session.flush()

            for witness in witnesses:
                witness.family_id = db_family_instance.id
                self.db_service.add(session, witness)

            for event, event_witnesses in events_with_witnesses:
                event.family_id = db_family_instance.id
                self.db_service.add(session, event)
                session.flush()  # Get event ID

                for event_witness in event_witnesses:
                    event_witness.event_id = event.id
                    self.db_service.add(session, event_witness)

            descend = db_descend.Descends()
            self.db_service.add(session, descend)
            session.flush()  # Get descend ID

            for child in children:
                child.descend_id = descend.id
                self.db_service.add(session, child)

            db_family_instance.children_id = descend.id

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def edit_family(self, family: app_family.Family[int, int, str]) -> bool:
        """Edit an existing family in the database."""
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")

        try:
            existing_family = self.db_service.get(
                session, db_family.Family, {"id": family.index}
            )
            if existing_family is None:
                raise ValueError(f"Family with id {family.index} not found")

            couple_id = existing_family.parents_id

            (db_family_instance, witnesses, events_with_witnesses,
             children) = convert_family_to_db(family, couple_id)

            existing_family.marriage_date_obj = (
                db_family_instance.marriage_date_obj
            )
            existing_family.marriage_place = (
                db_family_instance.marriage_place
            )
            existing_family.marriage_note = db_family_instance.marriage_note
            existing_family.marriage_src = db_family_instance.marriage_src
            existing_family.relation_kind = db_family_instance.relation_kind
            existing_family.divorce_status = (
                db_family_instance.divorce_status
            )
            existing_family.divorce_date_obj = (
                db_family_instance.divorce_date_obj
            )
            existing_family.comment = db_family_instance.comment
            existing_family.origin_file = db_family_instance.origin_file
            existing_family.src = db_family_instance.src

            old_witnesses = self.db_service.get_all(
                session, db_witness.FamilyWitness,
                query={"family_id": family.index}
            )
            for old_witness in old_witnesses:
                self.db_service.delete(session, old_witness)

            for witness in witnesses:
                witness.family_id = family.index
                self.db_service.add(session, witness)

            old_events = self.db_service.get_all(
                session, db_family_event.FamilyEvent,
                query={"family_id": family.index}
            )
            for old_event in old_events:
                old_event_witnesses = self.db_service.get_all(
                    session, db_family_event_witness.FamilyEventWitness,
                    query={"event_id": old_event.id}
                )
                for old_event_witness in old_event_witnesses:
                    self.db_service.delete(session, old_event_witness)
                self.db_service.delete(session, old_event)

            for event, event_witnesses in events_with_witnesses:
                event.family_id = family.index
                self.db_service.add(session, event)
                session.flush()  # Get event ID

                for event_witness in event_witnesses:
                    event_witness.event_id = event.id
                    self.db_service.add(session, event_witness)

            descend_id = existing_family.children_id
            if descend_id:
                old_children = self.db_service.get_all(
                    session, db_descend_children.DescendChildren,
                    query={"descend_id": descend_id}
                )
                for old_child in old_children:
                    self.db_service.delete(session, old_child)
                for child in children:
                    child.descend_id = descend_id
                    self.db_service.add(session, child)

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
