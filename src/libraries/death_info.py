from enum import Enum
from typing import Callable, override

from libraries.date import CompressedDate, Date


class DeathReason(Enum):
    """Specific cause or manner of death for genealogical records."""

    KILLED = "Killed"
    MURDERED = "Murdered"
    EXECUTED = "Executed"
    DISAPPEARED = "Disappeared"
    UNSPECIFIED = "Unspecified"


class DeathStatusBase:
    """Base class for different death status representations in genealogy.

    This abstract class represents the various ways a person's death status
    can be recorded, from definitely alive to various states of being deceased
    or having unknown status.
    """

    def __init__(self):
        raise NotImplementedError(
            "DeathStatusBase is a base class and cannot be instantiated"
            "directly. Use one of its subclasses instead."
        )

    def map_death(self, _: Callable[[Date], Date]):
        """Transform dates within death information using provided mapper.

        Args:
            date_mapper: Function to transform Date objects

        Returns:
            New instance with transformed dates, or self if no dates
        """
        return self


class NotDead(DeathStatusBase):
    def __init__(self):
        pass


class Dead(DeathStatusBase):
    """Person is confirmed dead with known reason and date."""

    def __init__(
        self, death_reason: DeathReason, date_of_death: CompressedDate
    ):
        self.death_reason: DeathReason = death_reason
        self.date_of_death: CompressedDate = date_of_death

    @override
    def map_death(self, date_mapper: Callable[[Date], Date]):
        """Transform the death date using the provided mapper function.

        Args:
            date_mapper: Function to transform the death date

        Returns:
            New Dead instance with transformed death date
        """
        return Dead(
            death_reason=self.death_reason,
            date_of_death=self.date_of_death.map_cdate(date_mapper),
        )


class DeadYoung(DeathStatusBase):
    def __init__(self):
        pass


class DeadDontKnowWhen(DeathStatusBase):
    def __init__(self):
        pass


class DontKnowIfDead(DeathStatusBase):
    def __init__(self):
        pass


class OfCourseDead(DeathStatusBase):
    def __init__(self):
        pass
