from sqlalchemy import Column, Integer, Text
from database import Base

class Place(Base):
    __tablename__ = "Place"

    id = Column(Integer, primary_key=True, nullable=False)
    town = Column(Text, nullable=False)
    township = Column(Text, nullable=False)
    canton = Column(Text, nullable=False)
    district = Column(Text, nullable=False)
    county = Column(Text, nullable=False)
    region = Column(Text, nullable=False)
    country = Column(Text, nullable=False)
    other = Column(Text, nullable=False)
