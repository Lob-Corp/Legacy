from enum import Enum

from libraries.date import CompressedDate


class DeathReason(Enum):
    KILLED = "Killed"
    MURDERED = "Murdered"
    EXECUTED = "Executed"
    DISAPPEARED = "Disappeared"
    UNSPECIFIED = "Unspecified"


class DeathStatusBase:
    def __init__(self):
        raise NotImplementedError(
            "DeathStatusBase is a base class and cannot be instantiated directly. Use one of its subclasses instead.")


class NotDead(DeathStatusBase):
    def __init__(self):
        pass


class Dead(DeathStatusBase):
    def __init__(self, death_reason: DeathReason, date_of_death: CompressedDate):
        self.death_reason = death_reason


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


class BurialInfoBase():
    def __init__(self):
        raise NotImplementedError(
            "BurialInfoBase is a base class and cannot be instantiated directly. Use one of its subclasses instead.")


class UnknownBurial(BurialInfoBase):
    def __init__(self):
        pass


class Burial(BurialInfoBase):
    def __init__(self, burial_date: CompressedDate):
        self.burial_date = burial_date


class Cremated(BurialInfoBase):
    def __init__(self, cremation_date: CompressedDate):
        self.cremation_date = cremation_date
