from sqlalchemy import Column, Integer
from database import Base


class Unions(Base):
    __tablename__ = "Unions"

    id = Column(Integer, primary_key=True, nullable=False)
