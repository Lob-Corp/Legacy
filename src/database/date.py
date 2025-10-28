from sqlalchemy import Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
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

    id = mapped_column(Integer, primary_key=True, nullable=False)
    precision_level = mapped_column(Enum(DatePrecision), nullable=False)
    iso_date = mapped_column(Text, nullable=True)
    calendar = mapped_column(Enum(Calendar), nullable=True)
    delta = mapped_column(Integer, nullable=True)


class Date(Base):
    __tablename__ = "Date"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    iso_date = mapped_column(Text, nullable=False)
    calendar = mapped_column(Enum(Calendar), nullable=False)
    precision_id = mapped_column(Integer,
                                 ForeignKey("Precision.id"), nullable=False)
    delta = mapped_column(Integer, nullable=False)

    precision_obj = relationship(
        "Precision",
        uselist=False,
        foreign_keys=[precision_id],
        cascade="all, delete-orphan",
        single_parent=True
    )
