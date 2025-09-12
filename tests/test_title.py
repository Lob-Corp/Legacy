import pytest
from title import *

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
        nth=1
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
