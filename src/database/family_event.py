from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
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

    id = Column(Integer, primary_key=True, nullable=False)
    family_id = Column(Integer, ForeignKey("Family.id"), nullable=False)
    name = Column(Enum(FamilyEventName), nullable=False)
    date = Column(Integer, ForeignKey("DateValue.id"), nullable=False)
    place = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    note = Column(Text, nullable=False)
    src = Column(Text, nullable=False)
