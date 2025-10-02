from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class FamilyEvents(Base):
    __tablename__ = "FamilyEvents"

    id = Column(Integer, primary_key=True, nullable=False)
    family_id = Column(Integer, ForeignKey("Family.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("FamilyEvent.id"), nullable=False)
