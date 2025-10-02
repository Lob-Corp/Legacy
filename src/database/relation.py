from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
from database import Base
from libraries.family import RelationToParentType
import enum

class Relation(Base):
    __tablename__ = "Relation"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum(RelationToParentType), nullable=False)
    father_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    mother_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    sources = Column(Text, nullable=False)
