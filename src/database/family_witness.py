from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column
from database import Base


class FamilyWitness(Base):
    __tablename__ = "FamilyWitness"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    family_id = mapped_column(Integer, ForeignKey("Family.id"), nullable=False)
    person_id = mapped_column(Integer, ForeignKey("Person.id"), nullable=False)
