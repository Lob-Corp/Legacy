from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PersonRelations(Base):
    __tablename__ = "PersonRelations"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    related_person_id = Column(
        Integer, ForeignKey("Person.id"), nullable=False)

    person_obj = relationship("Person", foreign_keys=[person_id])
    related_person_obj = relationship(
        "Person", foreign_keys=[related_person_id])
