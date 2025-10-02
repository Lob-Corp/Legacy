from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class PersonEvents(Base):
    __tablename__ = "PersonEvents"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("PersonalEvent.id"), nullable=False)
