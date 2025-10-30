from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models to ensure SQLAlchemy can resolve relationships
# Import order matters - import base models first, then models that reference them
from .date import Date
from .place import Place
from .titles import Titles
from .family import Family
from .couple import Couple
from .ascends import Ascends
from .unions import Unions
from .person import Person
from .relation import Relation
from .personal_event import PersonalEvent
from .family_event import FamilyEvent
from .family_events import FamilyEvents
from .person_events import PersonEvents
from .person_titles import PersonTitles
from .person_relations import PersonRelations
from .person_non_native_relations import PersonNonNativeRelations
from .descends import Descends
from .descend_children import DescendChildren
from .family_event_witness import FamilyEventWitness
from .family_witness import FamilyWitness
from .person_event_witness import PersonEventWitness
from .union_families import UnionFamilies
