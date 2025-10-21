from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PersonTitles(Base):
    __tablename__ = "PersonTitles"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    title_id = Column(Integer, ForeignKey("Titles.id"), nullable=False)

    person_obj = relationship("Person", foreign_keys=[person_id])
    title_obj = relationship("Titles", foreign_keys=[title_id])
