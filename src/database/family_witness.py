from sqlalchemy import Column, Integer, ForeignKey
from database import Base


class FamilyWitness(Base):
    __tablename__ = "FamilyWitness"

    id = Column(Integer, primary_key=True, nullable=False)
    family_id = Column(Integer, ForeignKey("Family.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
