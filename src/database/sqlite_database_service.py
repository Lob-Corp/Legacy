from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import TypeVar, Type, List, Optional
from database import Base


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

    def get_session(self) -> Session | None:
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

    def get(self, session: Session, model: Type[ModelType], query: dict = {}) -> ModelType | None:
        if session is None:
            return None
        return session.query(model).filter_by(**query).first()

    def get_all(self, session: Session, model: Type[ModelType], query: dict = {}, offset: int = 0, limit: int = 100) -> List[ModelType]:
        if session is None:
            return []
        return session.query(model).filter_by(**query).offset(offset).limit(limit).all()

    def refresh(self, session: Session, obj: object) -> None:
        if session is None:
            return
        session.refresh(obj)

    def apply(self, session: Session) -> None:
        if session is None:
            return
        session.commit()
