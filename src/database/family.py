from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from libraries.family import MaritalStatus
import enum


class DivorceStatus(enum.Enum):
    NOT_DIVORCED = "NOT_DIVORCED"
    DIVORCED = "DIVORCED"
    SEPARATED = "SEPARATED"


class Family(Base):
    __tablename__ = "Family"

    id = Column(Integer, primary_key=True, nullable=False)
    marriage_date = Column(Integer, ForeignKey("Date.id"), nullable=False)
    marriage_place = Column(Text, nullable=False)
    marriage_note = Column(Text, nullable=False)
    marriage_src = Column(Text, nullable=False)
    relation_kind = Column(Enum(MaritalStatus), nullable=False)
    divorce_status = Column(Enum(DivorceStatus), nullable=False)
    divorce_date = Column(Integer, ForeignKey("Date.id"))
    parents_id = Column(Integer, ForeignKey("Couple.id"))
    children_id = Column(Integer, ForeignKey("Descends.id"))
    comment = Column(Text, nullable=False)
    origin_file = Column(Text, nullable=False)
    src = Column(Text, nullable=False)

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
