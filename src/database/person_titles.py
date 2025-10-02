from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class PersonTitles(Base):
    __tablename__ = "PersonTitles"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    title_id = Column(Integer, ForeignKey("Titles.id"), nullable=False)
