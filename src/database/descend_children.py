from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database import Base


class DescendChildren(Base):
    __tablename__ = "DescendChildren"
    id = mapped_column(Integer, primary_key=True, nullable=False)
    descend_id = mapped_column(Integer, ForeignKey("Descends.id"),
                               nullable=False)
    person_id = mapped_column(Integer, ForeignKey("Person.id"), nullable=False)

    descend_obj = relationship("Descends", foreign_keys=[descend_id])
    person_obj = relationship("Person", foreign_keys=[person_id])
