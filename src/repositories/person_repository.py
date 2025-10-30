from typing import List
from database.sqlite_database_service import SQLiteDatabaseService

import libraries.person as app_person
import database.person as db_person
import database.titles as db_titles
import database.relation as db_relation
import database.person_relations as db_person_relations
import database.personal_event as db_personal_event
import database.person_event_witness as db_person_event_witness
import database.person_titles as db_person_titles
import database.person_non_native_relations as db_person_non_native_relations
import database.ascends as db_ascends
import database.unions as db_unions
import database.union_families as db_union_families
from repositories.converter_from_db import convert_person_from_db
from repositories.converter_to_db import convert_person_to_db


class PersonRepository:
    def __init__(self, db_service: SQLiteDatabaseService):
        self.db_service = db_service

    def get_person_by_id(
            self, person_id: int) -> app_person.Person[int, int, str, int]:
        """Get a person by ID from the database."""
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")

        try:
            person = self.db_service.get(
                session, db_person.Person, {"id": person_id}
            )
            if person is None:
                raise ValueError(f"Person with id {person_id} not found")

            person_title_links = self.db_service.get_all(
                session=session,
                model=db_person_titles.PersonTitles,
                query={"person_id": person_id}
            )
            titles = []
            for link in person_title_links:
                title = self.db_service.get(
                    session, db_titles.Titles, {"id": link.title_id}
                )
                if title:
                    titles.append(title)

            non_native_links = self.db_service.get_all(
                session=session,
                model=(db_person_non_native_relations.
                       PersonNonNativeRelations),
                query={"person_id": person.id}
            )
            non_native_relations = []
            for link in non_native_links:
                relation = self.db_service.get(
                    session, db_relation.Relation, {"id": link.relation_id}
                )
                if relation:
                    non_native_relations.append(relation)

            related_persons = self.db_service.get_all(
                session=session,
                model=db_person_relations.PersonRelations,
                query={"person_id": person_id}
            )

            events = self.db_service.get_all(
                session=session,
                model=db_personal_event.PersonalEvent,
                query={"person_id": person_id}
            )
            events_with_witnesses = []
            for event in events:
                witnesses = self.db_service.get_all(
                    session=session,
                    model=db_person_event_witness.PersonEventWitness,
                    query={"event_id": event.id}
                )
                events_with_witnesses.append((event, witnesses))

            family_ids = []
            if person.families_id:
                union_families = self.db_service.get_all(
                    session, db_union_families.UnionFamilies,
                    query={"union_id": person.families_id}
                )
                family_ids = [uf.family_id for uf in union_families]

            return convert_person_from_db(
                person,
                titles,
                non_native_relations,
                related_persons,
                events_with_witnesses,
                family_ids
            )
        finally:
            session.close()

    def get_person_by_name(
            self,
            first_name: str,
            surname: str
    ) -> app_person.Person[int, int, str, int]:
        """Get a person by first name and surname from the database."""
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")

        try:
            person = self.db_service.get(
                session,
                db_person.Person,
                {"first_name": first_name, "surname": surname}
            )
            if person is None:
                raise ValueError(
                    f"Person with name {first_name} {surname} not found"
                )

            person_title_links = self.db_service.get_all(
                session=session,
                model=db_person_titles.PersonTitles,
                query={"person_id": person.id}
            )
            titles = []
            for link in person_title_links:
                title = self.db_service.get(
                    session, db_titles.Titles, {"id": link.title_id}
                )
                if title:
                    titles.append(title)

            non_native_links = self.db_service.get_all(
                session=session,
                model=(db_person_non_native_relations.
                       PersonNonNativeRelations),
                query={"person_id": person.id}
            )
            non_native_relations = []
            for link in non_native_links:
                relation = self.db_service.get(
                    session, db_relation.Relation, {"id": link.relation_id}
                )
                if relation:
                    non_native_relations.append(relation)

            related_persons = self.db_service.get_all(
                session=session,
                model=db_person_relations.PersonRelations,
                query={"person_id": person.id}
            )

            events = self.db_service.get_all(
                session=session,
                model=db_personal_event.PersonalEvent,
                query={"person_id": person.id}
            )
            events_with_witnesses = []
            for event in events:
                witnesses = self.db_service.get_all(
                    session=session,
                    model=db_person_event_witness.PersonEventWitness,
                    query={"event_id": event.id}
                )
                events_with_witnesses.append((event, witnesses))

            family_ids = []
            if person.families_id:
                union_families = self.db_service.get_all(
                    session, db_union_families.UnionFamilies,
                    query={"union_id": person.families_id}
                )
                family_ids = [uf.family_id for uf in union_families]

            return convert_person_from_db(
                person,
                titles,
                non_native_relations,
                related_persons,
                events_with_witnesses,
                family_ids
            )
        finally:
            session.close()

    def get_all_persons(self) -> List[app_person.Person[int, int, str, int]]:
        """Get all persons from the database."""
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")

        try:
            persons = self.db_service.get_all(session, db_person.Person)
            result = []

            for person in persons:
                person_title_links = self.db_service.get_all(
                    session=session,
                    model=db_person_titles.PersonTitles,
                    query={"person_id": person.id}
                )
                titles = []
                for link in person_title_links:
                    title = self.db_service.get(
                        session, db_titles.Titles, {"id": link.title_id}
                    )
                    if title:
                        titles.append(title)

                non_native_links = self.db_service.get_all(
                    session=session,
                    model=(db_person_non_native_relations.
                           PersonNonNativeRelations),
                    query={"person_id": person.id}
                )
                non_native_relations = []
                for link in non_native_links:
                    relation = self.db_service.get(
                        session, db_relation.Relation, {"id": link.relation_id}
                    )
                    if relation:
                        non_native_relations.append(relation)

                related_persons = self.db_service.get_all(
                    session=session,
                    model=db_person_relations.PersonRelations,
                    query={"person_id": person.id}
                )

                events = self.db_service.get_all(
                    session=session,
                    model=db_personal_event.PersonalEvent,
                    query={"person_id": person.id}
                )
                events_with_witnesses = []
                for event in events:
                    witnesses = self.db_service.get_all(
                        session=session,
                        model=db_person_event_witness.PersonEventWitness,
                        query={"event_id": event.id}
                    )
                    events_with_witnesses.append((event, witnesses))

                family_ids = []
                if person.families_id:
                    union_families = self.db_service.get_all(
                        session, db_union_families.UnionFamilies,
                        query={"union_id": person.families_id}
                    )
                    family_ids = [uf.family_id for uf in union_families]

                app_person_instance = convert_person_from_db(
                    person,
                    titles,
                    non_native_relations,
                    related_persons,
                    events_with_witnesses,
                    family_ids
                )
                result.append(app_person_instance)

            return result
        finally:
            session.close()

    def add_person(
            self, person: app_person.Person[int, int, str, int]) -> bool:
        """Add a new person to the database."""
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")

        try:
            ascend_id = None
            if person.ascend.parents is not None:
                ascend = db_ascends.Ascends(
                    parents=person.ascend.parents,
                    consang=int(person.ascend.consanguinity_rate)
                )
                self.db_service.add(session, ascend)
                session.flush()
                ascend_id = ascend.id

            families_id = None
            if person.families:
                unions = db_unions.Unions()
                self.db_service.add(session, unions)
                session.flush()
                families_id = unions.id

                for family_id in person.families:
                    union_family = db_union_families.UnionFamilies(
                        union_id=unions.id,
                        family_id=family_id
                    )
                    self.db_service.add(session, union_family)

            (db_person_instance, titles, non_native_relations,
             related_persons, events_with_witnesses) = convert_person_to_db(
                person, ascend_id, families_id
            )

            self.db_service.add(session, db_person_instance)
            session.flush()

            for title in titles:
                self.db_service.add(session, title)
                session.flush()

                person_title_link = db_person_titles.PersonTitles(
                    person_id=db_person_instance.id,
                    title_id=title.id
                )
                self.db_service.add(session, person_title_link)

            for relation in non_native_relations:
                self.db_service.add(session, relation)
                session.flush()

                person_relation_link = (
                    db_person_non_native_relations.PersonNonNativeRelations(
                        person_id=db_person_instance.id,
                        relation_id=relation.id
                    )
                )
                self.db_service.add(session, person_relation_link)

            for related_person in related_persons:
                related_person.person_id = db_person_instance.id
                self.db_service.add(session, related_person)

            for event, event_witnesses in events_with_witnesses:
                event.person_id = db_person_instance.id
                self.db_service.add(session, event)
                session.flush()

                for event_witness in event_witnesses:
                    event_witness.event_id = event.id
                    self.db_service.add(session, event_witness)

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def edit_person(
            self, person: app_person.Person[int, int, str, int]) -> bool:
        """Edit an existing person in the database."""
        session = self.db_service.get_session()
        if session is None:
            raise RuntimeError("Database session is not available")

        try:
            existing_person = self.db_service.get(
                session, db_person.Person, {"id": person.index}
            )
            if existing_person is None:
                raise ValueError(f"Person with id {person.index} not found")

            ascend_id = existing_person.ascend_id
            if person.ascend.parents is not None:
                if ascend_id:
                    ascend = self.db_service.get(
                        session, db_ascends.Ascends, {"id": ascend_id}
                    )
                    if ascend:
                        ascend.parents = person.ascend.parents
                        consang = int(person.ascend.consanguinity_rate)
                        ascend.consang = consang
                else:
                    ascend = db_ascends.Ascends(
                        parents=person.ascend.parents,
                        consang=int(person.ascend.consanguinity_rate)
                    )
                    self.db_service.add(session, ascend)
                    session.flush()
                    ascend_id = ascend.id

            families_id = existing_person.families_id
            if person.families:
                if families_id:
                    old_union_families = self.db_service.get_all(
                        session, db_union_families.UnionFamilies,
                        query={"union_id": families_id}
                    )
                    self.db_service.delete_all(session, old_union_families)
                else:
                    unions = db_unions.Unions()
                    self.db_service.add(session, unions)
                    session.flush()
                    families_id = unions.id

                for family_id in person.families:
                    union_family = db_union_families.UnionFamilies(
                        union_id=families_id,
                        family_id=family_id
                    )
                    self.db_service.add(session, union_family)

            (db_person_instance, titles, non_native_relations,
             related_persons, events_with_witnesses) = convert_person_to_db(
                person, ascend_id, families_id
            )

            existing_person.first_name = db_person_instance.first_name
            existing_person.surname = db_person_instance.surname
            existing_person.occ = db_person_instance.occ
            existing_person.image = db_person_instance.image
            existing_person.public_name = db_person_instance.public_name
            existing_person.qualifiers = db_person_instance.qualifiers
            existing_person.aliases = db_person_instance.aliases
            existing_person.first_names_aliases = (
                db_person_instance.first_names_aliases
            )
            existing_person.surname_aliases = (
                db_person_instance.surname_aliases
            )
            existing_person.occupation = db_person_instance.occupation
            existing_person.sex = db_person_instance.sex
            existing_person.access_right = db_person_instance.access_right
            existing_person.birth_date_obj = db_person_instance.birth_date_obj
            existing_person.birth_place = db_person_instance.birth_place
            existing_person.birth_note = db_person_instance.birth_note
            existing_person.birth_src = db_person_instance.birth_src
            existing_person.baptism_date_obj = (
                db_person_instance.baptism_date_obj
            )
            existing_person.baptism_place = db_person_instance.baptism_place
            existing_person.baptism_note = db_person_instance.baptism_note
            existing_person.baptism_src = db_person_instance.baptism_src
            existing_person.death_status = db_person_instance.death_status
            existing_person.death_reason = db_person_instance.death_reason
            existing_person.death_date_obj = db_person_instance.death_date_obj
            existing_person.death_place = db_person_instance.death_place
            existing_person.death_note = db_person_instance.death_note
            existing_person.death_src = db_person_instance.death_src
            existing_person.burial_status = db_person_instance.burial_status
            existing_person.burial_date_obj = (
                db_person_instance.burial_date_obj
            )
            existing_person.burial_place = db_person_instance.burial_place
            existing_person.burial_note = db_person_instance.burial_note
            existing_person.burial_src = db_person_instance.burial_src
            existing_person.notes = db_person_instance.notes
            existing_person.src = db_person_instance.src
            existing_person.ascend_id = ascend_id
            existing_person.families_id = families_id

            old_title_links = self.db_service.get_all(
                session, db_person_titles.PersonTitles,
                query={"person_id": person.index}
            )
            for link in old_title_links:
                title = self.db_service.get(
                    session, db_titles.Titles, {"id": link.title_id}
                )
                if title:
                    self.db_service.delete(session, title)
                self.db_service.delete(session, link)

            for title in titles:
                self.db_service.add(session, title)
                session.flush()

                person_title_link = db_person_titles.PersonTitles(
                    person_id=person.index,
                    title_id=title.id
                )
                self.db_service.add(session, person_title_link)

            old_relation_links = self.db_service.get_all(
                session,
                db_person_non_native_relations.PersonNonNativeRelations,
                query={"person_id": person.index}
            )
            for link in old_relation_links:
                relation = self.db_service.get(
                    session, db_relation.Relation, {"id": link.relation_id}
                )
                if relation:
                    self.db_service.delete(session, relation)
                self.db_service.delete(session, link)

            for relation in non_native_relations:
                self.db_service.add(session, relation)
                session.flush()

                person_relation_link = (
                    db_person_non_native_relations.PersonNonNativeRelations(
                        person_id=person.index,
                        relation_id=relation.id
                    )
                )
                self.db_service.add(session, person_relation_link)

            old_related_persons = self.db_service.get_all(
                session, db_person_relations.PersonRelations,
                query={"person_id": person.index}
            )
            for old_related in old_related_persons:
                self.db_service.delete(session, old_related)

            for related_person in related_persons:
                related_person.person_id = person.index
                self.db_service.add(session, related_person)

            old_events = self.db_service.get_all(
                session, db_personal_event.PersonalEvent,
                query={"person_id": person.index}
            )
            for old_event in old_events:
                old_event_witnesses = self.db_service.get_all(
                    session, db_person_event_witness.PersonEventWitness,
                    query={"event_id": old_event.id}
                )
                for old_event_witness in old_event_witnesses:
                    self.db_service.delete(session, old_event_witness)
                self.db_service.delete(session, old_event)

            for event, event_witnesses in events_with_witnesses:
                event.person_id = person.index
                self.db_service.add(session, event)
                session.flush()

                for event_witness in event_witnesses:
                    event_witness.event_id = event.id
                    self.db_service.add(session, event_witness)

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
