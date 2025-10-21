from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from libraries.date import Calendar
import enum


class DatePrecision(enum.Enum):
    SURE = "SURE"
    ABOUT = "ABOUT"
    MAYBE = "MAYBE"
    BEFORE = "BEFORE"
    AFTER = "AFTER"
    ORYEAR = "ORYEAR"
    YEARINT = "YEARINT"


class Precision(Base):
    __tablename__ = "Precision"

    id = Column(Integer, primary_key=True, nullable=False)
    precision_level = Column(Enum(DatePrecision), nullable=False)
    iso_date = Column(Text, nullable=True)
    calendar = Column(Enum(Calendar), nullable=True)
    delta = Column(Integer, nullable=True)


class Date(Base):
    __tablename__ = "Date"

    id = Column(Integer, primary_key=True, nullable=False)
    iso_date = Column(Text, nullable=False)
    calendar = Column(Enum(Calendar), nullable=False)
    precision_id = Column(Integer, ForeignKey("Precision.id"), nullable=False)
    delta = Column(Integer, nullable=False)

    precision_obj = relationship(
        "Precision",
        uselist=False,
        foreign_keys=[precision_id],
        cascade="all, delete-orphan",
        single_parent=True
    )
