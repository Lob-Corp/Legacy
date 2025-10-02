from sqlalchemy import Column, Integer, Enum, ForeignKey
from database import Base
from libraries.events import EventWitnessKind

class FamilyEventWitness(Base):
    __tablename__ = "FamilyEventWitness"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("FamilyEvent.id"), nullable=False)
    kind = Column(Enum(EventWitnessKind), nullable=False)
