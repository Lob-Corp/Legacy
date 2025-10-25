from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from libraries.family import RelationToParentType


class Relation(Base):
    __tablename__ = "Relation"

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(Enum(RelationToParentType), nullable=False)
    father_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    mother_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    sources = Column(Text, nullable=False)

    father_obj = relationship("Person", foreign_keys=[father_id])
    mother_obj = relationship("Person", foreign_keys=[mother_id])
