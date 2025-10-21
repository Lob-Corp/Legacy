from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class UnionFamilies(Base):
    __tablename__ = "UnionFamilies"

    id = Column(Integer, primary_key=True, nullable=False)
    union_id = Column(Integer, ForeignKey("Unions.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("Family.id"), nullable=False)

    union_obj = relationship("Unions", foreign_keys=[union_id])
    family_obj = relationship("Family", foreign_keys=[family_id])
