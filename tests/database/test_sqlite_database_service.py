import pytest
import os

from sqlalchemy.orm import Session
from typing import Generator, Optional
from database.sqlite_database_service import SQLiteDatabaseService, DEFAULT_DATABASE_PATH
from database.person import Person, Sex, DeathStatus, BurialStatus
from libraries.title import AccessRight


class TestSQLiteDatabaseService:

    @pytest.fixture
    def db_service(self) -> Generator[SQLiteDatabaseService, None, None]:
        database_path: str = "test.db"
        db_service: SQLiteDatabaseService = SQLiteDatabaseService(
            database_path)
        yield db_service

        if os.path.exists(database_path):
            os.remove(database_path)

    @pytest.fixture
    def connected_db_service(self, db_service: SQLiteDatabaseService) -> Generator[SQLiteDatabaseService, None, None]:
        db_service.connect()
        yield db_service
        db_service.disconnect()

    @pytest.fixture
    def test_person(self) -> Person:
        return Person(
            first_name="Benjamin",
            surname="Carter",
            occ=0,
            image="",
            public_name="Benjamin Carter",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="Software Engineer",
            sex=Sex.MALE,
            access_right=AccessRight.PUBLIC,
            birth_date=0,
            birth_place="New York, USA",
            birth_note="",
            birth_src="",
            baptism_date=0,
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_date=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_date=None,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

    @pytest.fixture
    def test_person2(self) -> Person:
        return Person(
            first_name="Alice",
            surname="Morgan",
            occ=0,
            image="",
            public_name="Alice Morgan",
            qualifiers="",
            aliases="",
            first_names_aliases="",
            surname_aliases="",
            occupation="Architect",
            sex=Sex.FEMALE,
            access_right=AccessRight.PUBLIC,
            birth_date=0,
            birth_place="London, UK",
            birth_note="",
            birth_src="",
            baptism_date=0,
            baptism_place="",
            baptism_note="",
            baptism_src="",
            death_status=DeathStatus.NOT_DEAD,
            death_reason=None,
            death_date=None,
            death_place="",
            death_note="",
            death_src="",
            burial_status=BurialStatus.UNKNOWN_BURIAL,
            burial_date=None,
            burial_place="",
            burial_note="",
            burial_src="",
            notes="",
            src=""
        )

    # === Initialization ===

    def test_init_with_default_path(self):
        db_service: SQLiteDatabaseService = SQLiteDatabaseService()
        assert db_service._database_path == DEFAULT_DATABASE_PATH
        assert db_service._engine is None
        assert db_service._sessionmaker is None

    def test_init_with_custom_path(self, db_service: SQLiteDatabaseService):
        assert db_service._database_path == "test.db"
        assert db_service._engine is None
        assert db_service._sessionmaker is None

    # === Connect / Disconnect ===

    def test_connect(self, db_service: SQLiteDatabaseService):
        db_service.connect()
        assert db_service._engine is not None
        assert db_service._sessionmaker is not None

    def test_connect_when_already_connected(self, db_service: SQLiteDatabaseService):
        db_service.connect()
        engine = db_service._engine
        sessionmaker = db_service._sessionmaker

        db_service.connect()

        assert db_service._engine is engine
        assert db_service._sessionmaker is sessionmaker

        db_service.disconnect()

    def test_disconnect(self, db_service: SQLiteDatabaseService):
        db_service.connect()
        db_service.disconnect()
        assert db_service._engine is None
        assert db_service._sessionmaker is None

    def test_disconnect_without_connection(self, db_service: SQLiteDatabaseService):
        assert db_service._engine is None
        db_service.disconnect()
        assert db_service._engine is None

    # === Get session ===

    def test_get_session(self, connected_db_service: SQLiteDatabaseService):
        db_session = connected_db_service.get_session()
        assert db_session is not None
        assert isinstance(db_session, Session)
        db_session.close()

    def test_get_session_without_connection(self, db_service: SQLiteDatabaseService):
        db_session = db_service.get_session()
        assert db_session is None

    def test_get_session_returns_different_instances(self, connected_db_service: SQLiteDatabaseService):
        db_session1: Optional[Session] = connected_db_service.get_session()
        db_session2: Optional[Session] = connected_db_service.get_session()

        assert db_session1 is not None
        assert db_session2 is not None
        assert db_session1 is not db_session2
        db_session1.close()
        db_session2.close()

    # === Add objects ===

    def test_add_with_none_session(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        connected_db_service.add(None, test_person)  # type: ignore

    def test_add_object(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add(db_session, test_person)
        connected_db_service.apply(db_session)

        result = connected_db_service.get(
            db_session, Person, {"first_name": "Benjamin"})
        assert result is not None
        assert result.surname == "Carter"  # type: ignore
        db_session.close()

    def test_add_multiple_objects_with_none_session(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        connected_db_service.add_all(None, [test_person])  # type: ignore

    def test_add_multiple_objects(self, connected_db_service: SQLiteDatabaseService, test_person: Person, test_person2: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add_all(db_session, [test_person, test_person2])
        connected_db_service.apply(db_session)

        result = connected_db_service.get_all(db_session, Person)
        assert len(result) == 2
        db_session.close()

    def test_add_multiple_empty_list(self, connected_db_service: SQLiteDatabaseService):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add_all(db_session, [])
        connected_db_service.apply(db_session)

        result = connected_db_service.get_all(db_session, Person)
        assert len(result) == 0
        db_session.close()

    # === Delete objects ===

    def test_delete_with_none_session(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        connected_db_service.delete(None, test_person)  # type: ignore

    def test_delete_object(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add(db_session, test_person)
        connected_db_service.apply(db_session)

        result = connected_db_service.get(
            db_session, Person, {"first_name": "Benjamin"})
        assert result is not None

        connected_db_service.delete(db_session, result)
        connected_db_service.apply(db_session)

        result = connected_db_service.get(
            db_session, Person, {"first_name": "Benjamin"})
        assert result is None
        db_session.close()

    def test_delete_multiple_objects_with_none_session(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        connected_db_service.delete_all(None, [test_person])  # type: ignore

    def test_delete_multiple_objects(self, connected_db_service: SQLiteDatabaseService, test_person: Person, test_person2: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add_all(db_session, [test_person, test_person2])
        connected_db_service.apply(db_session)

        result = connected_db_service.get_all(db_session, Person)
        assert len(result) == 2

        connected_db_service.delete_all(db_session, list(result))
        connected_db_service.apply(db_session)

        result = connected_db_service.get_all(db_session, Person)
        assert len(result) == 0
        db_session.close()

    def test_delete_multiple_empty_list(self, connected_db_service: SQLiteDatabaseService):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.delete_all(db_session, [])
        connected_db_service.apply(db_session)

        db_session.close()

    # === Get objects ===

    def test_get_with_none_session(self, connected_db_service: SQLiteDatabaseService):
        result = connected_db_service.get(None, Person)  # type: ignore
        assert result is None

    def test_get_object_not_found(self, connected_db_service: SQLiteDatabaseService):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        result = connected_db_service.get(
            db_session, Person, {"first_name": "Inexistant"})
        assert result is None
        db_session.close()

    def test_get_object_found(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add(db_session, test_person)
        connected_db_service.apply(db_session)

        result = connected_db_service.get(
            db_session, Person, {"first_name": "Benjamin"})
        assert result is not None
        assert result.surname == "Carter"  # type: ignore
        db_session.close()

    def test_get_object_with_multiple_criteria(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add(db_session, test_person)
        connected_db_service.apply(db_session)

        result = connected_db_service.get(
            db_session, Person, {"first_name": "Benjamin", "surname": "Carter"})
        assert result is not None
        assert result.occupation == "Software Engineer"  # type: ignore
        db_session.close()

    def test_get_object_with_empty_query(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add(db_session, test_person)
        connected_db_service.apply(db_session)

        result = connected_db_service.get(db_session, Person, {})
        assert result is not None  # Retourne le premier trouvé
        db_session.close()

    # === Get all objects ===

    def test_get_all_with_none_session(self, connected_db_service: SQLiteDatabaseService):
        result = connected_db_service.get_all(None, Person)  # type: ignore
        assert result == []

    def test_get_all_empty_table(self, connected_db_service: SQLiteDatabaseService):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        result = connected_db_service.get_all(db_session, Person)
        assert result == []
        db_session.close()

    def test_get_all_objects(self, connected_db_service: SQLiteDatabaseService, test_person: Person, test_person2: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add_all(db_session, [test_person, test_person2])
        connected_db_service.apply(db_session)

        result = connected_db_service.get_all(db_session, Person)
        assert len(result) == 2
        db_session.close()

    def test_get_all_with_filter(self, connected_db_service: SQLiteDatabaseService, test_person: Person, test_person2: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add_all(db_session, [test_person, test_person2])
        connected_db_service.apply(db_session)

        result = connected_db_service.get_all(
            db_session, Person, {"sex": Sex.FEMALE})
        assert len(result) == 1
        assert result[0].first_name == "Alice"  # type: ignore
        db_session.close()

    def test_get_all_with_pagination(self, connected_db_service: SQLiteDatabaseService, test_person: Person, test_person2: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add_all(db_session, [test_person, test_person2])
        connected_db_service.apply(db_session)

        result = connected_db_service.get_all(db_session, Person, {}, limit=1)
        assert len(result) == 1

        result = connected_db_service.get_all(
            db_session, Person, {}, offset=1, limit=1)
        assert len(result) == 1
        db_session.close()

    def test_get_all_with_offset_beyond_results(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add(db_session, test_person)
        connected_db_service.apply(db_session)

        result = connected_db_service.get_all(
            db_session, Person, {}, offset=10)
        assert len(result) == 0
        db_session.close()

    # === Refresh objects ===

    def test_refresh_with_none_session(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        connected_db_service.refresh(None, test_person)  # type: ignore

    def test_refresh_object(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add(db_session, test_person)
        connected_db_service.apply(db_session)

        result = connected_db_service.get(
            db_session, Person, {"first_name": "Benjamin"})
        assert result is not None
        original_occupation = result.occupation

        db_session2: Optional[Session] = connected_db_service.get_session()
        assert db_session2 is not None

        result2 = connected_db_service.get(
            db_session2, Person, {"first_name": "Benjamin"})
        assert result2 is not None

        result2.occupation = "Ingénieur"  # type: ignore
        connected_db_service.apply(db_session2)
        db_session2.close()

        assert result.occupation == original_occupation  # type: ignore

        connected_db_service.refresh(db_session, result)
        assert result.occupation == "Ingénieur"  # type: ignore
        db_session.close()

    # === Apply changes ===

    def test_apply_with_none_session(self, connected_db_service: SQLiteDatabaseService):
        connected_db_service.apply(None)  # type: ignore

    def test_apply_commits_changes(self, connected_db_service: SQLiteDatabaseService, test_person: Person):
        db_session: Optional[Session] = connected_db_service.get_session()
        assert db_session is not None

        connected_db_service.add(db_session, test_person)

        db_session2: Optional[Session] = connected_db_service.get_session()
        assert db_session2 is not None
        result = connected_db_service.get(
            db_session2, Person, {"first_name": "Benjamin"})
        assert result is None
        db_session2.close()

        connected_db_service.apply(db_session)

        db_session3: Optional[Session] = connected_db_service.get_session()
        assert db_session3 is not None
        result = connected_db_service.get(
            db_session3, Person, {"first_name": "Benjamin"})
        assert result is not None
        db_session3.close()
        db_session.close()
