from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class CoupleParents(Base):
    __tablename__ = "CoupleParents"

    id = Column(Integer, primary_key=True, nullable=False)
    couple_id = Column(Integer, ForeignKey("Couple.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
