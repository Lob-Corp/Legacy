from sqlalchemy import Column, Integer, Text, ForeignKey
from database import Base

class Titles(Base):
    __tablename__ = "Titles"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(Text, nullable=False)
    ident = Column(Text, nullable=False)
    place = Column(Text, nullable=False)
    date_start = Column(Integer, ForeignKey("DateValue.id"), nullable=False)
    date_end = Column(Integer, ForeignKey("DateValue.id"), nullable=False)
    nth = Column(Integer, nullable=False)
