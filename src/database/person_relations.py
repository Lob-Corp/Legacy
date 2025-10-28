from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base


class PersonRelations(Base):
    __tablename__ = "PersonRelations"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    person_id = mapped_column(Integer, ForeignKey("Person.id"), nullable=False)
    related_person_id = mapped_column(
        Integer, ForeignKey("Person.id"), nullable=False)

    person_obj = relationship("Person", foreign_keys=[person_id])
    related_person_obj = relationship(
        "Person", foreign_keys=[related_person_id])
