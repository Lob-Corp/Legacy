from sqlalchemy import Column, Integer, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum


class PersonalEventName(enum.Enum):
    BIRTH = "BIRTH"
    BAPTISM = "BAPTISM"
    DEATH = "DEATH"
    BURIAL = "BURIAL"
    CREMATION = "CREMATION"
    ACCOMPLISHMENT = "ACCOMPLISHMENT"
    ACQUISITION = "ACQUISITION"
    ADHESION = "ADHESION"
    BAPTISM_LDS = "BAPTISM_LDS"
    BAR_MITZVAH = "BAR_MITZVAH"
    BAT_MITZVAH = "BAT_MITZVAH"
    BENEDICTION = "BENEDICTION"
    CHANGE_NAME = "CHANGE_NAME"
    CIRCUMCISION = "CIRCUMCISION"
    CONFIRMATION = "CONFIRMATION"
    CONFIRMATION_LDS = "CONFIRMATION_LDS"
    DECORATION = "DECORATION"
    DEMOBILISATION_MILITAIRE = "DEMOBILISATION_MILITAIRE"
    DIPLOMA = "DIPLOMA"
    DISTINCTION = "DISTINCTION"
    DOTATION = "DOTATION"
    DOTATION_LDS = "DOTATION_LDS"
    EDUCATION = "EDUCATION"
    ELECTION = "ELECTION"
    EMIGRATION = "EMIGRATION"
    EXCOMMUNICATION = "EXCOMMUNICATION"
    FAMILY_LINK_LDS = "FAMILY_LINK_LDS"
    FIRST_COMMUNION = "FIRST_COMMUNION"
    FUNERAL = "FUNERAL"
    GRADUATE = "GRADUATE"
    HOSPITALISATION = "HOSPITALISATION"
    ILLNESS = "ILLNESS"
    IMMIGRATION = "IMMIGRATION"
    LISTE_PASSENGER = "LISTE_PASSENGER"
    MILITARY_DISTINCTION = "MILITARY_DISTINCTION"
    MILITARY_PROMOTION = "MILITARY_PROMOTION"
    MILITARY_SERVICE = "MILITARY_SERVICE"
    MOBILISATION_MILITAIRE = "MOBILISATION_MILITAIRE"
    NATURALISATION = "NATURALISATION"
    OCCUPATION = "OCCUPATION"
    ORDINATION = "ORDINATION"
    PROPERTY = "PROPERTY"
    RECENSEMENT = "RECENSEMENT"
    RESIDENCE = "RESIDENCE"
    RETIRED = "RETIRED"
    SCELLENT_CHILD_LDS = "SCELLENT_CHILD_LDS"
    SCELLENT_PARENT_LDS = "SCELLENT_PARENT_LDS"
    SCELLENT_SPOUSE_LDS = "SCELLENT_SPOUSE_LDS"
    VENTE_BIEN = "VENTE_BIEN"
    WILL = "WILL"
    NAMED_EVENT = "NAMED_EVENT"


class PersonalEvent(Base):
    __tablename__ = "PersonalEvent"

    id = Column(Integer, primary_key=True, nullable=False)
    person_id = Column(Integer, ForeignKey("Person.id"), nullable=False)
    name = Column(Enum(PersonalEventName), nullable=False)
    date = Column(Integer, ForeignKey("DateValue.id"), nullable=False)
    place = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
    note = Column(Text, nullable=False)
    src = Column(Text, nullable=False)

    person_obj = relationship("Person", foreign_keys=[person_id])
    date_obj = relationship(
        "DateValue",
        cascade="all, delete-orphan",
        single_parent=True,
        foreign_keys=[date]
    )
