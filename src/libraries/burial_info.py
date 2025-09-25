from typing import Callable, override

from libraries.date import CompressedDate, Date


class BurialInfoBase:
    """Base class for different burial/body disposition methods.

    Represents the various ways a deceased person's body was handled,
    from traditional burial to cremation or unknown disposition.
    """

    def __init__(self):
        raise NotImplementedError(
            "BurialInfoBase is a base class and cannot be"
            "instantiated directly. Use one of its subclasses instead."
        )

    def map_burial(self, _: Callable[[Date], Date]) -> "BurialInfoBase":
        """Transform the burial date using the provided mapper function.

        Args:
            date_mapper: Function to transform the burial date

        Returns:
            New BurialInfoBase instance with transformed burial date,
            or None if there is no burial or cremation date to transform
        """
        return self


class UnknownBurial(BurialInfoBase):
    """Burial information is not known or not recorded."""

    def __init__(self):
        pass


class Burial(BurialInfoBase):
    """Traditional burial with known date."""

    def __init__(self, burial_date: CompressedDate):
        self.burial_date: CompressedDate = burial_date

    @override
    def map_burial(self, date_mapper: Callable[[Date], Date]) -> "Burial":
        """Transform the burial date using the provided mapper function.

        Args:
            date_mapper: Function to transform the burial date

        Returns:
            New Burial instance with transformed burial date
        """
        return Burial(burial_date=self.burial_date.map_cdate(date_mapper))


class Cremated(BurialInfoBase):
    """Body was cremated with known date."""

    def __init__(self, cremation_date: CompressedDate):
        self.cremation_date: CompressedDate = cremation_date

    @override
    def map_burial(self, date_mapper: Callable[[Date], Date]) -> "Cremated":
        """Transform the cremation date using the provided mapper function.

        Args:
            date_mapper: Function to transform the cremation date

        Returns:
            New Cremated instance with transformed cremation date
        """
        return Cremated(cremation_date=self.cremation_date.map_cdate(date_mapper))
