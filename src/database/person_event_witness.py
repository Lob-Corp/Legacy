from sqlalchemy import Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base
from libraries.events import EventWitnessKind


class PersonEventWitness(Base):
    __tablename__ = "PersonEventWitness"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    person_id = mapped_column(Integer, ForeignKey("Person.id"), nullable=False)
    event_id = mapped_column(Integer, ForeignKey("PersonalEvent.id"),
                             nullable=False)
    kind = mapped_column(Enum(EventWitnessKind), nullable=False)

    person_obj = relationship("Person", foreign_keys=[person_id])
    event_obj = relationship("PersonalEvent", foreign_keys=[event_id])
