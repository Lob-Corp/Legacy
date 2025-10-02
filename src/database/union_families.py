from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class UnionFamilies(Base):
    __tablename__ = "UnionFamilies"

    id = Column(Integer, primary_key=True, nullable=False)
    union_id = Column(Integer, ForeignKey("Unions.id"), nullable=False)
    family_id = Column(Integer, ForeignKey("Family.id"), nullable=False)
