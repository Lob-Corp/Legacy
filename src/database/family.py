from sqlalchemy import Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base
from libraries.family import MaritalStatus
import enum


class DivorceStatus(enum.Enum):
    NOT_DIVORCED = "NOT_DIVORCED"
    DIVORCED = "DIVORCED"
    SEPARATED = "SEPARATED"


class Family(Base):
    __tablename__ = "Family"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    marriage_date = mapped_column(Integer, ForeignKey("Date.id"),
                                  nullable=False)
    marriage_place = mapped_column(Text, nullable=False)
    marriage_note = mapped_column(Text, nullable=False)
    marriage_src = mapped_column(Text, nullable=False)
    relation_kind = mapped_column(Enum(MaritalStatus), nullable=False)
    divorce_status = mapped_column(Enum(DivorceStatus), nullable=False)
    divorce_date = mapped_column(Integer, ForeignKey("Date.id"))
    parents_id = mapped_column(Integer, ForeignKey("Couple.id"))
    children_id = mapped_column(Integer, ForeignKey("Descends.id"))
    comment = mapped_column(Text, nullable=False)
    origin_file = mapped_column(Text, nullable=False)
    src = mapped_column(Text, nullable=False)

    parents = relationship(
        "Couple",
        uselist=False,
        foreign_keys=[parents_id],
        cascade="all, delete-orphan",
        single_parent=True,
    )
    children = relationship(
        "Descends",
        uselist=False,
        foreign_keys=[children_id],
        cascade="all, delete-orphan",
        single_parent=True
    )

    marriage_date_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[marriage_date]
    )
    divorce_date_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[divorce_date]
    )
