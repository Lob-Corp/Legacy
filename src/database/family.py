from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
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
    marriage_date = Column(Integer, ForeignKey("DateValue.id"), nullable=False)
    marriage_place = Column(Text, nullable=False)
    marriage_note = Column(Text, nullable=False)
    marriage_src = Column(Text, nullable=False)
    relation_kind = Column(Enum(MaritalStatus), nullable=False)
    divorce_status = Column(Enum(DivorceStatus), nullable=False)
    divorce_date = Column(Integer, ForeignKey("DateValue.id"))
    comment = Column(Text, nullable=False)
    origin_file = Column(Text, nullable=False)
    src = Column(Text, nullable=False)
