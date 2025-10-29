from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base


class Titles(Base):
    __tablename__ = "Titles"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    name = mapped_column(Text, nullable=False)
    ident = mapped_column(Text, nullable=False)
    place = mapped_column(Text, nullable=False)
    date_start = mapped_column(Integer, ForeignKey("Date.id"), nullable=False)
    date_end = mapped_column(Integer, ForeignKey("Date.id"), nullable=False)
    nth = mapped_column(Integer, nullable=False)

    date_start_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[date_start]
    )
    date_end_obj = relationship(
        "Date",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[date_end]
    )
