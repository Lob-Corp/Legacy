from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class PersonNonNativeRelations(Base):
    __tablename__ = "PersonNonNativeRelations"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    relation_id = Column(Integer, ForeignKey("Relation.id"), nullable=False)
