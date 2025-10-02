from sqlalchemy import Column, Integer
from database import Base


class Descends(Base):
    __tablename__ = "Descends"

    id = Column(Integer, primary_key=True, nullable=False)
