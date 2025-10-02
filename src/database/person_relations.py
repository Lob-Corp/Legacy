from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class PersonRelations(Base):
    __tablename__ = "PersonRelations"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    related_person_id = Column(
        Integer, ForeignKey("Person.id"), nullable=False)
