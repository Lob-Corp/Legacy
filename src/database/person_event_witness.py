from sqlalchemy import Column, Integer, Enum, ForeignKey
from database import Base
from libraries.events import EventWitnessKind


class PersonEventWitness(Base):
    __tablename__ = "PersonEventWitness"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("PersonalEvent.id"), nullable=False)
    kind = Column(Enum(EventWitnessKind), nullable=False)
