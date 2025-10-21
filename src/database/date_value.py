from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum


class DatePrecision(enum.Enum):
    SURE = "SURE"
    ABOUT = "ABOUT"
    MAYBE = "MAYBE"
    BEFORE = "BEFORE"
    AFTER = "AFTER"
    ORYEAR = "ORYEAR"
    YEARINT = "YEARINT"


class DateValue(Base):
    __tablename__ = "DateValue"

    id = Column(Integer, primary_key=True, nullable=False)
    greg_date = Column(Text, nullable=False)
    precision = Column(Enum(DatePrecision), nullable=False)
    precision_date_value = Column(
        Integer, ForeignKey("DateValue.id"), nullable=False)

    precision_date_value_obj = relationship(
        "DateValue",
        remote_side=[id],
        foreign_keys=[precision_date_value]
    )


class Date(Base):
    id = Column(Integer, primary_key=True, nullable=False)
    iso_date = Column(Text, nullable=False)
