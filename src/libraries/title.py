from enum import Enum
from dataclasses import dataclass
from typing import Generic, TypeVar

from date import CompressedDate


class AccessRight(Enum):
    IFTITLES = "IfTitles"
    PUBLIC = "Public"
    PRIVATE = "Private"


TitleDescriptorType = TypeVar('TitleDescriptorType')

class TitleNameBase(Generic[TitleDescriptorType]):
    def __init__(self):
        raise NotImplementedError(
            "TitleNameBase is a base class and cannot be instantiated directly. Use one of its subclasses instead.")


class UseMainTitle(TitleNameBase[None]):
    def __init__(self):
        pass

class TitleName(TitleNameBase[TitleDescriptorType]):
    def __init__(self, title_name: TitleDescriptorType):
        self.title_name = title_name


class NoTitle(TitleNameBase[None]):
    def __init__(self):
        pass

@dataclass(frozen=True)
class Title(Generic[TitleDescriptorType]):
    title_name: TitleNameBase
    ident: str
    place: str
    date_start: CompressedDate
    date_end: CompressedDate
    nth: int
