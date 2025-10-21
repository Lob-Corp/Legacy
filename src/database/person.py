from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

from libraries.person import Sex
from libraries.title import AccessRight
from libraries.death_info import DeathReason

import enum


class DeathStatus(enum.Enum):
    NOT_DEAD = "NOT_DEAD"
    DEAD = "DEAD"
    DEAD_YOUNG = "DEAD_YOUNG"
    DEAD_DONT_KNOW_WHEN = "DEAD_DONT_KNOW_WHEN"
    DONT_KNOW_IF_DEAD = "DONT_KNOW_IF_DEAD"
    OF_COURSE_DEAD = "OF_COURSE_DEAD"


class BurialStatus(enum.Enum):
    UNKNOWN_BURIAL = "UNKNOWN_BURIAL"
    BURIAL = "BURIAL"
    CREMATED = "CREMATED"


class Person(Base):
    __tablename__ = "Person"

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    occ = Column(Integer, nullable=False)
    image = Column(Text, nullable=False)
    public_name = Column(Text, nullable=False)
    qualifiers = Column(Text, nullable=False)
    aliases = Column(Text, nullable=False)
    first_names_aliases = Column(Text, nullable=False)
    surname_aliases = Column(Text, nullable=False)
    occupation = Column(Text, nullable=False)
    sex = Column(Enum(Sex), nullable=False)
    access_right = Column(Enum(AccessRight), nullable=False)
    birth_date = Column(Integer, ForeignKey("Date.id"))
    birth_place = Column(Text, nullable=False)
    birth_note = Column(Text, nullable=False)
    birth_src = Column(Text, nullable=False)
    baptism_date = Column(Integer, ForeignKey("Date.id"))
    baptism_place = Column(Text, nullable=False)
    baptism_note = Column(Text, nullable=False)
    baptism_src = Column(Text, nullable=False)
    death_status = Column(Enum(DeathStatus), nullable=False)
    death_reason = Column(Enum(DeathReason))
    death_date = Column(Integer, ForeignKey("Date.id"))
    death_place = Column(Text, nullable=False)
    death_note = Column(Text, nullable=False)
    death_src = Column(Text, nullable=False)
    burial_status = Column(Enum(BurialStatus), nullable=False)
    burial_date = Column(Integer, ForeignKey("Date.id"))
    burial_place = Column(Text, nullable=False)
    burial_note = Column(Text, nullable=False)
    burial_src = Column(Text, nullable=False)
    notes = Column(Text, nullable=False)
    src = Column(Text, nullable=False)
    ascend_id = Column(Integer, ForeignKey("Ascends.id"))
    families_id = Column(Integer, ForeignKey("Unions.id"))

    ascend = relationship(
        "Ascends",
        uselist=False,
        foreign_keys=[ascend_id],
        cascade="all, delete-orphan",
        single_parent=True,
    )
    families = relationship(
        "Unions",
        uselist=False,
        foreign_keys=[families_id],
        cascade="all, delete-orphan",
        single_parent=True,
    )
    birth_date_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[birth_date]
    )
    baptism_date_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[baptism_date]
    )
    death_date_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[death_date]
    )
    burial_date_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[burial_date]
    )
