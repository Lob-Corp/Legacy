from enum import Enum
from typing import Generic, TypeVar

from date import CompressedDate

class MaritalStatus(Enum):
    MARRIED = "Married"
    NOT_MARRIED = "NotMarried"
    ENGAGED = "Engaged"
    NO_SEXES_CHECK_NOT_MARRIED = "NoSexesCheckNotMarried"
    NO_MENTION = "NoMention"
    NO_SEXES_CHECK_MARRIED = "NoSexesCheckMarried"
    MARRIAGE_BANN = "MarriageBann"
    MARRIAGE_CONTRACT = "MarriageContract"
    MARRIAGE_LICENSE = "MarriageLicense"
    PACS = "Pacs"
    RESIDENCE = "Residence"

Person = TypeVar('Person')

class Parents(Generic[Person]):
    def __init__(self, parents: list[Person]):
        assert len(parents) != 0, "Parents list cannot be empty"
        assert all(isinstance(p, type(parents[0])) for p in parents), "All parents must be of the same type"
        self.parents = parents

    @staticmethod
    def from_couple(a: Person, b: Person) -> 'Parents[Person]':
        return Parents([a, b])

    def is_couple(self) -> bool:
        return len(self.parents) == 2

    def couple(self) -> tuple[Person, Person]:
        assert len(self.parents) == 2, "Is not a couple"
        return (self.parents[0], self.parents[1])

    def father(self) -> Person:
        assert len(self.parents) >= 1
        return self.parents[0]

    def mother(self) -> Person:
        assert len(self.parents) >= 2
        return self.parents[1]

    def __getitem__(self, index: int) -> Person:
        assert 0 <= index < len(self.parents), "Index out of range"
        return self.parents[index]

class DivorceStatusBase:
    def __init__(self):
        raise NotImplementedError(
            "DivorceStatusBase is a base class and cannot be instantiated directly. Use one of its subclasses instead.")

class NotDivorced(DivorceStatusBase):
    def __init__(self):
        pass

class Divorced(DivorceStatusBase):
    def __init__(self, divorce_date: CompressedDate):
        self.divorce_date = divorce_date

class Separated(DivorceStatusBase):
    def __init__(self):
        pass
