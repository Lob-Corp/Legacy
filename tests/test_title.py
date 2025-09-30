import pytest
from libraries.calendar_date import Calendar, CalendarDate
from libraries.date import CompressedDate, Date, DateValue
from libraries.precision import Sure
from libraries.title import (
    Title,
    TitleName,
    UseMainTitle,
    NoTitle,
    TitleNameBase,
)

# --- Base class enforcement ---


def test_title_name_base_instantiation():
    with pytest.raises(NotImplementedError):
        TitleNameBase()


# --- Singleton subclasses ---


def test_use_main_title():
    t = UseMainTitle()
    assert isinstance(t, UseMainTitle)
    assert isinstance(t, TitleNameBase)


def test_no_title():
    t = NoTitle()
    assert isinstance(t, NoTitle)
    assert isinstance(t, TitleNameBase)


# --- Parameterized subclass ---


def test_title_name():
    name_value = "Duke of Python"
    t = TitleName(name_value)
    assert t.title_name == name_value
    assert isinstance(t, TitleName)
    assert isinstance(t, TitleNameBase)


# --- Dataclass Title ---


def test_title_dataclass():
    date_start = "2025-01-01"
    date_end = "2030-01-01"

    title_name = TitleName("Duke of Python")
    title = Title(
        title_name=title_name,
        ident="ID123",
        place="Paris",
        date_start=date_start,
        date_end=date_end,
        nth=1,
    )

    assert title.title_name == title_name
    assert title.ident == "ID123"
    assert title.place == "Paris"
    assert title.date_start == date_start
    assert title.date_end == date_end
    assert title.nth == 1


# --- Match behavior ---


def test_title_match():
    t1 = UseMainTitle()
    t2 = TitleName("Duke of Python")
    t3 = NoTitle()

    matched = []

    for t in [t1, t2, t3]:
        match t:
            case UseMainTitle():
                matched.append("use_main")
            case TitleName(title_name=name):
                matched.append(f"title:{name}")
            case NoTitle():
                matched.append("no_title")
            case _:
                matched.append("unknown")
    assert matched == ["use_main", "title:Duke of Python", "no_title"]


# --- Equality checks ---


def test_titlename_equality():
    t1 = TitleName("Duke of Python")
    t2 = TitleName("Duke of Python")
    t3 = TitleName("Duke of Java")
    t4 = "TitleName"

    assert t1 == t2
    assert t1 != t3
    assert t1 != t4


def test_title_namebase_equality():
    t1 = UseMainTitle()
    t2 = UseMainTitle()
    t3 = NoTitle()
    t4 = NoTitle()

    assert t1 == t2
    assert t1 != t3
    assert t3 == t4


def test_title_equality():
    t1 = Title(
        title_name=TitleName("Duke of Python"),
        ident="ID123",
        place="Paris",
        date_start="2025-01-01",
        date_end="2030-01-01",
        nth=1,
    )
    t2 = Title(
        title_name=TitleName("Duke of Rust"),
        ident="ID123",
        place="Paris",
        date_start="2025-01-01",
        date_end="2030-01-01",
        nth=1,
    )
    t3 = "No title"

    assert t1 != t2
    assert t1 != t3


def test_title_without_date_mapper():
    def _string_mapper(s: str):
        return s.upper() if isinstance(s, str) else s

    t1 = Title(
        title_name=TitleName("Duke of Python"),
        ident="ID123",
        place="Paris",
        date_start=CompressedDate(
            Date(
                CalendarDate(
                    dmy=DateValue(1, 1, 2025, Sure()), cal=Calendar.GREGORIAN
                ),
            )
        ),
        date_end=CompressedDate(
            Date(
                CalendarDate(
                    dmy=DateValue(1, 1, 2030, Sure()),
                    cal=Calendar.GREGORIAN,
                ),
            )
        ),
        nth=1,
    )

    t2 = t1.map_title(_string_mapper)

    assert t2.title_name == TitleName("DUKE OF PYTHON")
    assert t2.ident == "ID123"
    assert t2.place == "PARIS"
    assert t2.date_start == CompressedDate((Calendar.GREGORIAN, 37025))
    assert t2.date_end == CompressedDate((Calendar.GREGORIAN, 37030))
    assert t2.nth == 1


def test_title_with_date_mapper():
    def _string_mapper(s: str):
        return s.upper() if isinstance(s, str) else s

    def _date_mapper(d: Date) -> Date:
        if isinstance(d, Date) and isinstance(d.date, CalendarDate):
            return Date(
                CalendarDate(
                    dmy=d.date.dmy,
                    cal=(
                        Calendar.GREGORIAN
                        if d.date.cal == Calendar.JULIAN
                        else Calendar.JULIAN
                    ),
                ),
            )
        return d

    t1 = Title(
        title_name=TitleName("Duke of Python"),
        ident="ID123",
        place="Paris",
        date_start=CompressedDate(
            Date(
                CalendarDate(
                    dmy=DateValue(1, 1, 2025, Sure()), cal=Calendar.GREGORIAN
                ),
            )
        ),
        date_end=CompressedDate(
            Date(
                CalendarDate(
                    dmy=DateValue(1, 1, 2030, Sure()),
                    cal=Calendar.GREGORIAN,
                ),
            )
        ),
        nth=1,
    )

    t2 = t1.map_title(_string_mapper, _date_mapper)

    assert t2.title_name == TitleName("DUKE OF PYTHON")
    assert t2.ident == "ID123"
    assert t2.place == "PARIS"
    assert t2.date_start == CompressedDate((Calendar.JULIAN, 37025))
    assert t2.date_end == CompressedDate((Calendar.JULIAN, 37030))
    assert t2.nth == 1


def test_no_title_date_mapper():
    def _string_mapper(s: str):
        return s.upper() if isinstance(s, str) else s

    t1 = Title(
        title_name=NoTitle(),
        ident="ID123",
        place="Paris",
        date_start=CompressedDate(
            Date(
                CalendarDate(
                    dmy=DateValue(1, 1, 2025, Sure()), cal=Calendar.GREGORIAN
                ),
            )
        ),
        date_end=CompressedDate(
            Date(
                CalendarDate(
                    dmy=DateValue(1, 1, 2030, Sure()),
                    cal=Calendar.GREGORIAN,
                ),
            )
        ),
        nth=1,
    )

    t2 = t1.map_title(_string_mapper)

    assert t2.title_name == NoTitle()
    assert t2.ident == "ID123"
    assert t2.place == "PARIS"
    assert t2.date_start == CompressedDate((Calendar.GREGORIAN, 37025))
    assert t2.date_end == CompressedDate((Calendar.GREGORIAN, 37030))
    assert t2.nth == 1
