from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class CoupleParents(Base):
    __tablename__ = "CoupleParents"

    id = Column(Integer, primary_key=True, nullable=False)
    couple_id = Column(Integer, ForeignKey("Couple.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)

    couple_obj = relationship("Couple", foreign_keys=[couple_id])
    person_obj = relationship("Person", foreign_keys=[person_id])
