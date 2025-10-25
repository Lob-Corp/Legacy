from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Ascends(Base):
    __tablename__ = "Ascends"

    id = Column(Integer, primary_key=True, nullable=False)
    parents = Column(Integer, ForeignKey("Family.id"))
    consang = Column(Integer, nullable=False)

    parents_obj = relationship("Family", foreign_keys=[parents])
