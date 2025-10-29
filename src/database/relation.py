from sqlalchemy import Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base
from libraries.family import RelationToParentType


class Relation(Base):
    __tablename__ = "Relation"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    type = mapped_column(Enum(RelationToParentType), nullable=False)
    father_id = mapped_column(Integer, ForeignKey("Person.id"), nullable=False)
    mother_id = mapped_column(Integer, ForeignKey("Person.id"), nullable=False)
    sources = mapped_column(Text, nullable=False)

    father_obj = relationship("Person", foreign_keys=[father_id])
    mother_obj = relationship("Person", foreign_keys=[mother_id])
