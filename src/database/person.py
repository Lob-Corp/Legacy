from sqlalchemy import Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
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

    id = mapped_column(Integer, primary_key=True, nullable=False)
    first_name = mapped_column(Text, nullable=False)
    surname = mapped_column(Text, nullable=False)
    occ = mapped_column(Integer, nullable=False)
    image = mapped_column(Text, nullable=False)
    public_name = mapped_column(Text, nullable=False)
    qualifiers = mapped_column(Text, nullable=False)
    aliases = mapped_column(Text, nullable=False)
    first_names_aliases = mapped_column(Text, nullable=False)
    surname_aliases = mapped_column(Text, nullable=False)
    occupation = mapped_column(Text, nullable=False)
    sex = mapped_column(Enum(Sex), nullable=False)
    access_right = mapped_column(Enum(AccessRight), nullable=False)
    birth_date = mapped_column(Integer, ForeignKey("Date.id"))
    birth_place = mapped_column(Text, nullable=False)
    birth_note = mapped_column(Text, nullable=False)
    birth_src = mapped_column(Text, nullable=False)
    baptism_date = mapped_column(Integer, ForeignKey("Date.id"))
    baptism_place = mapped_column(Text, nullable=False)
    baptism_note = mapped_column(Text, nullable=False)
    baptism_src = mapped_column(Text, nullable=False)
    death_status = mapped_column(Enum(DeathStatus), nullable=False)
    death_reason = mapped_column(Enum(DeathReason))
    death_date = mapped_column(Integer, ForeignKey("Date.id"))
    death_place = mapped_column(Text, nullable=False)
    death_note = mapped_column(Text, nullable=False)
    death_src = mapped_column(Text, nullable=False)
    burial_status = mapped_column(Enum(BurialStatus), nullable=False)
    burial_date = mapped_column(Integer, ForeignKey("Date.id"))
    burial_place = mapped_column(Text, nullable=False)
    burial_note = mapped_column(Text, nullable=False)
    burial_src = mapped_column(Text, nullable=False)
    notes = mapped_column(Text, nullable=False)
    src = mapped_column(Text, nullable=False)
    ascend_id = mapped_column(Integer, ForeignKey("Ascends.id"))
    families_id = mapped_column(Integer, ForeignKey("Unions.id"))

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
