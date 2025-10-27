from sqlalchemy import Column, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from libraries.events import EventWitnessKind


class PersonEventWitness(Base):
    __tablename__ = "PersonEventWitness"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("PersonalEvent.id"), nullable=False)
    kind = Column(Enum(EventWitnessKind), nullable=False)

    person_obj = relationship("Person", foreign_keys=[person_id])
    event_obj = relationship("PersonalEvent", foreign_keys=[event_id])
