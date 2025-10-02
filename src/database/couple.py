from sqlalchemy import Column, Integer
from database import Base

class Couple(Base):
    __tablename__ = "Couple"

    id = Column(Integer, primary_key=True, nullable=False)
