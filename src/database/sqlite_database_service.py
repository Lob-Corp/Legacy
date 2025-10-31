from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import TypeVar, Type, List, Optional
from database import Base

from .ascends import Ascends
from .couple import Couple
from .date import Date
from .descend_children import DescendChildren
from .descends import Descends
from .family import Family
from .family_event import FamilyEvent
from .family_event_witness import FamilyEventWitness
from .family_events import FamilyEvents
from .family_witness import FamilyWitness
from .person import Person
from .person_event_witness import PersonEventWitness
from .person_events import PersonEvents
from .person_non_native_relations import (
    PersonNonNativeRelations,
)
from .person_relations import PersonRelations
from .person_titles import PersonTitles
from .personal_event import PersonalEvent
from .place import Place
from .relation import Relation
from .titles import Titles
from .union_families import UnionFamilies
from .unions import Unions

_models = (
    Ascends,
    Couple,
    Date,
    DescendChildren,
    Descends,
    Family,
    FamilyEvent,
    FamilyEventWitness,
    FamilyEvents,
    FamilyWitness,
    Person,
    PersonEventWitness,
    PersonEvents,
    PersonNonNativeRelations,
    PersonRelations,
    PersonTitles,
    PersonalEvent,
    Place,
    Relation,
    Titles,
    UnionFamilies,
    Unions,
)
del _models

ModelType = TypeVar("ModelType", bound=Base)

DEFAULT_DATABASE_PATH = "base.db"


class SQLiteDatabaseService:

    _database_path: str = DEFAULT_DATABASE_PATH
    _engine: Optional[Engine] = None
    _sessionmaker: Optional[sessionmaker[Session]] = None

    def __init__(self, database_path=DEFAULT_DATABASE_PATH):
        self._database_path = database_path
        self._engine = None
        self._sessionmaker = None

    def connect(self):
        if self._engine is not None:
            return

        self._engine = create_engine(f"sqlite:///{self._database_path}")
        self._sessionmaker = sessionmaker(bind=self._engine)
        Base.metadata.create_all(self._engine)

    def disconnect(self):
        if self._engine is None:
            return
        self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    def get_session(self) -> Optional[Session]:
        if self._sessionmaker is None:
            return None
        return self._sessionmaker()

    def add(self, session: Session, obj: object) -> None:
        if session is None:
            return
        session.add(obj)

    def add_all(self, session: Session, objs: list[object]) -> None:
        if session is None:
            return
        session.add_all(objs)

    def delete(self, session: Session, obj: object) -> None:
        if session is None:
            return
        session.delete(obj)

    def delete_all(self, session: Session, objs: list[object]) -> None:
        if session is None:
            return
        for obj in objs:
            session.delete(obj)

    def get(
        self, session: Session, model: Type[ModelType], query: dict = {}
    ) -> Optional[ModelType]:
        if session is None:
            return None
        return session.query(model).filter_by(**query).first()

    def get_all(
        self,
        session: Session,
        model: Type[ModelType],
        query: dict = {},
        offset: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        if session is None:
            return []
        return (session.query(model).filter_by(**query)
                .offset(offset).limit(limit).all())

    def refresh(self, session: Session, obj: object) -> None:
        if session is None:
            return
        session.refresh(obj)

    def apply(self, session: Session) -> None:
        if session is None:
            return
        session.commit()
