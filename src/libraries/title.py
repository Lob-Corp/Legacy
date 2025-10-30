from enum import Enum
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, Optional, Callable

from libraries.date import CompressedDate, Date


class AccessRight(Enum):
    """Defines the visibility/access level for genealogical information."""

    IFTITLES = "IFTITLES"
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


# Type variable for title descriptors (strings, identifiers, etc.)
TitleDescriptorT = TypeVar("TitleDescriptorT")
TitleDescriptorT2 = TypeVar("TitleDescriptorT2")


class TitleNameBase(Generic[TitleDescriptorT]):
    """Base class for different ways a title can be named.

    This is an abstract base class that represents the different strategies
    for naming a title: using a main title, having no title, or having
    a specific title name.
    """

    def __init__(
        self,
    ):
        raise NotImplementedError(
            "TitleNameBase is a base class and cannot be instantiated"
            "directly. Use one of its subclasses instead."
        )

    def __eq__(self, other):
        if isinstance(other, TitleNameBase):
            if isinstance(self, UseMainTitle) and isinstance(
                other, UseMainTitle
            ):
                return True
            if isinstance(self, NoTitle) and isinstance(other, NoTitle):
                return True
        return False


class UseMainTitle(TitleNameBase[Any]):
    """Indicates that a person's main title should be used for this title."""

    def __init__(self):
        pass


class TitleName(TitleNameBase[TitleDescriptorT]):
    """A specific title name provided explicitly."""

    def __init__(self, title_name: TitleDescriptorT):
        self.title_name = title_name

    def __eq__(self, other):
        if not isinstance(other, TitleName):
            return False
        return self.title_name == other.title_name


class NoTitle(TitleNameBase[Any]):
    """Indicates that no title should be displayed for this title field."""

    def __init__(self):
        pass


@dataclass(frozen=True)
class Title(Generic[TitleDescriptorT]):
    """Represents a noble or honorary title with its associated metadata.

    A title includes the name, identification, place, date range, and
    ordinal number (e.g., "John III" where nth=3).
    """

    title_name: TitleNameBase[TitleDescriptorT]
    ident: TitleDescriptorT
    place: TitleDescriptorT
    date_start: CompressedDate
    date_end: CompressedDate
    nth: int

    def __eq__(self, other) -> bool:
        if not isinstance(other, Title):
            return False
        return (
            self.title_name == other.title_name
            and self.ident == other.ident
            and self.place == other.place
            and self.date_start == other.date_start
            and self.date_end == other.date_end
            and self.nth == other.nth
        )

    def map_title(
        self,
        string_mapper: Callable[[TitleDescriptorT], TitleDescriptorT2],
        date_mapper: Optional[Callable[[Date], Date]] = None,
    ) -> "Title[TitleDescriptorT2]":
        """Transform string and date fields using provided mapper functions.

        Args:
            string_mapper: Function to transform string fields (ident, place)
            date_mapper: Optional function to transform dates.
                         If None, dates are unchanged.

        Returns:
            New Title instance with transformed fields
        """

        if date_mapper is None:

            def date_mapper(x: Date) -> Date:
                return x

        title_name: TitleNameBase[TitleDescriptorT2]
        if isinstance(self.title_name, NoTitle):
            title_name = NoTitle()
        elif isinstance(self.title_name, UseMainTitle):
            title_name = UseMainTitle()
        elif isinstance(self.title_name, TitleName):
            title_name = TitleName(string_mapper(self.title_name.title_name))
        else:
            # This should never happen, but provides a safety fallback
            raise TypeError(f"Unknown TitleNameBase type: \
                {type(self.title_name)}")

        return Title(
            title_name=title_name,
            ident=string_mapper(self.ident),
            place=string_mapper(self.place),
            date_start=date_mapper(self.date_start),
            date_end=date_mapper(self.date_end),
            nth=self.nth,
        )
