from sqlalchemy import Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base
import enum


class FamilyEventName(enum.Enum):
    MARRIAGE = "MARRIAGE"
    NO_MARRIAGE = "NO_MARRIAGE"
    NO_MENTION = "NO_MENTION"
    ENGAGE = "ENGAGE"
    DIVORCE = "DIVORCE"
    SEPARATED = "SEPARATED"
    ANNULATION = "ANNULATION"
    MARRIAGE_BANN = "MARRIAGE_BANN"
    MARRIAGE_CONTRACT = "MARRIAGE_CONTRACT"
    MARRIAGE_LICENSE = "MARRIAGE_LICENSE"
    PACS = "PACS"
    RESIDENCE = "RESIDENCE"
    NAMED_EVENT = "NAMED_EVENT"


class FamilyEvent(Base):
    __tablename__ = "FamilyEvent"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    family_id = mapped_column(Integer, ForeignKey("Family.id"), nullable=False)
    name = mapped_column(Enum(FamilyEventName), nullable=False)
    date = mapped_column(Integer, ForeignKey("Date.id"), nullable=False)
    place = mapped_column(Text, nullable=False)
    reason = mapped_column(Text, nullable=False)
    note = mapped_column(Text, nullable=False)
    src = mapped_column(Text, nullable=False)

    family_obj = relationship("Family", foreign_keys=[family_id])
    date_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[date]
    )
