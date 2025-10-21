from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database import Base


class Couple(Base):
    __tablename__ = "Couple"

    id = Column(Integer, primary_key=True, nullable=False)

    father_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    mother_id = Column(Integer, ForeignKey("Person.id"), nullable=False)

    father_obj = relationship("Person", foreign_keys=[father_id])
    mother_obj = relationship("Person", foreign_keys=[mother_id])
