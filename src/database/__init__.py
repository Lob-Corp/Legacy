from .union_families import UnionFamilies  # noqa: F401
from .person_event_witness import PersonEventWitness  # noqa: F401
from sqlalchemy.orm import DeclarativeBase

# Import all models to ensure SQLAlchemy can resolve relationships
# Import order matters - import base models first, then models that
# reference them
from .date import Date  # noqa: F401
from .place import Place  # noqa: F401
from .titles import Titles  # noqa: F401
from .family import Family  # noqa: F401
from .couple import Couple  # noqa: F401
from .ascends import Ascends  # noqa: F401
from .unions import Unions  # noqa: F401
from .person import Person  # noqa: F401
from .relation import Relation  # noqa: F401
from .personal_event import PersonalEvent  # noqa: F401
from .family_event import FamilyEvent  # noqa: F401
from .family_events import FamilyEvents  # noqa: F401
from .person_events import PersonEvents  # noqa: F401
from .person_titles import PersonTitles  # noqa: F401
from .person_relations import PersonRelations  # noqa: F401
from .person_non_native_relations import PersonNonNativeRelations  # noqa: F401
from .descends import Descends  # noqa: F401
from .descend_children import DescendChildren  # noqa: F401
from .family_event_witness import FamilyEventWitness  # noqa: F401
from .family_witness import FamilyWitness  # noqa: F401


class Base(DeclarativeBase):
    pass
