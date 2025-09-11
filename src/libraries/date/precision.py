from dataclasses import dataclass
# from date.calendar_date import DateValue

class Precision:
    def __init__(self):
        raise NotImplementedError(
            "Precision is a base class and cannot be instantiated directly. Use one of its subclasses instead."
        )

    def __eq__(self, other):
        return isinstance(other, self.__class__)



class Sure(Precision):
    def __init__(self):
        pass


class About(Precision):
    def __init__(self):
        pass


class Maybe(Precision):
    def __init__(self):
        pass


class Before(Precision):
    def __init__(self):
        pass


class After(Precision):
    def __init__(self):
        pass


@dataclass(frozen=True)
class OrYear(Precision):
    date_value: "DateValue"

    def __post_init__(self):
        if self.date_value.prec is not None:
            raise ValueError("OrYear precision must have None as its precision.")


@dataclass(frozen=True)
class YearInt(Precision):
    date_value: "DateValue"

    def __post_init__(self):
        if self.date_value.prec is not None:
            raise ValueError("YearInt precision must have None as its precision.")
