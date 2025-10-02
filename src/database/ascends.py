from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class Ascends(Base):
    __tablename__ = "Ascends"

    id = Column(Integer, primary_key=True, nullable=False)
    parents = Column(Integer, ForeignKey("Family.id"))
    consang = Column(Integer, nullable=False)
