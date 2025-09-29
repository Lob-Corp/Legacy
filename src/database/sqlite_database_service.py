from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlite3 import Connection

import sqlite3
import os

class SQLiteDatabaseService:

    DEFAULT_SQL_FILE_PATH: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), "genewebpy_db.sql")

    def __init__(self, database_path: str):
        self._database_path: str = database_path
        self._engine: Optional[Engine] = None
        self._session: Optional[Session] = None

    def connect(self):
        if self._engine is None:
            self._engine = create_engine(f"sqlite:///{self._database_path}")
            self._session = sessionmaker(bind=self._engine)()

    def disconnect(self):
        if self._engine is None:
            return
        self._engine.dispose()
        self._engine = None
        self._session = None

    def apply(self):
        if self._engine is None or self._session is None:
            return
        self._session.commit()

    @staticmethod
    def create_database_from_sql_file(database_path: str, sql_file_path: str = DEFAULT_SQL_FILE_PATH) -> None:
        try:
            if os.path.exists(database_path):
                raise FileExistsError(f"Database '{database_path}' already exists.")

            with open(sql_file_path, "r", encoding="utf-8") as sql_file:
                sql_script = sql_file.read()

            database_connection: Connection = sqlite3.connect(database_path)
            try:
                database_connection.executescript(sql_script)
            finally:
                database_connection.close()
        except Exception as e:
            raise RuntimeError(f"Error creating database: {e}")
