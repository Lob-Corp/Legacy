from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
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

    date_start_obj = relationship(
        "DateValue",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[date_start]
    )
    date_end_obj = relationship(
        "DateValue",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[date_end]
    )
