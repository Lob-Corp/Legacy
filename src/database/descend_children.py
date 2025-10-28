from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class DescendChildren(Base):
    __tablename__ = "DescendChildren"
    id = Column(Integer, primary_key=True, nullable=False)
    descend_id = Column(Integer, ForeignKey("Descends.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)

    descend_obj = relationship("Descends", foreign_keys=[descend_id])
    person_obj = relationship("Person", foreign_keys=[person_id])
