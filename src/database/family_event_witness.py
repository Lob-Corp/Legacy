from sqlalchemy import Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base
from libraries.events import EventWitnessKind


class FamilyEventWitness(Base):
    __tablename__ = "FamilyEventWitness"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    person_id = mapped_column(Integer, ForeignKey("Person.id"), nullable=False)
    event_id = mapped_column(Integer, ForeignKey("FamilyEvent.id"),
                             nullable=False)
    kind = mapped_column(Enum(EventWitnessKind), nullable=False)

    person_obj = relationship("Person", foreign_keys=[person_id])
    event_obj = relationship("FamilyEvent", foreign_keys=[event_id])
