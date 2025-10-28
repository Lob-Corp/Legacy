from enum import Enum
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from libraries.date import CompressedDate


class AccessRight(Enum):
    IFTITLES = "IFTITLES"
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


TitleDescriptorT = TypeVar("TitleDescriptorT")


class TitleNameBase(Generic[TitleDescriptorT]):
    def __init__(self):
        raise NotImplementedError(
            "TitleNameBase is a base class and cannot be instantiated"
            "directly. Use one of its subclasses instead.")


class UseMainTitle(TitleNameBase[Any]):
    def __init__(self):
        pass


class TitleName(TitleNameBase[TitleDescriptorT]):
    def __init__(self, title_name: TitleDescriptorT):
        self.title_name = title_name


class NoTitle(TitleNameBase[Any]):
    def __init__(self):
        pass


@dataclass(frozen=True)
class Title(Generic[TitleDescriptorT]):
    title_name: TitleNameBase[TitleDescriptorT]
    ident: str
    place: str
    date_start: CompressedDate
    date_end: CompressedDate
    nth: int
