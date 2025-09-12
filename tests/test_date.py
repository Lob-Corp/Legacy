from libraries.date import About, After, Before, Calendar, CalendarDate, Date, DateValue, Maybe, OrYear, PrecisionBase, Sure, YearInt
import pytest


def test_precision_instantiation():
    with pytest.raises(NotImplementedError):
        _ = PrecisionBase()

def test_sure_instantiation():
    p = Sure()
    assert isinstance(p, Sure)

def test_about_instantiation():
    p = About()
    assert isinstance(p, About)

def test_maybe_instantiation():
    p = Maybe()
    assert isinstance(p, Maybe)

def test_before_instantiation():
    p = Before()
    assert isinstance(p, Before)

def test_after_instantiation():
    p = After()
    assert isinstance(p, After)

def test_oryear_valid():
    d = DateValue(day=1, month=1, year=2000, prec=None, delta=0)
    p = OrYear(d)
    assert isinstance(p, OrYear)
    assert p.date_value == d

def test_oryear_invalid_precision_raises():
    d = DateValue(day=1, month=1, year=2000, prec=Sure(), delta=0)
    with pytest.raises(ValueError):
        OrYear(d)

def test_yearint_valid():
    d = DateValue(day=1, month=1, year=2000, prec=None, delta=0)
    p = YearInt(d)
    assert isinstance(p, YearInt)
    assert p.date_value == d

def test_yearint_invalid_precision_raises():
    d = DateValue(day=1, month=1, year=2000, prec=Sure(), delta=0)
    with pytest.raises(ValueError):
        YearInt(d)


def test_datevalue_creation():
    p = Sure()
    d = DateValue(day=10, month=5, year=1990, prec=p, delta=0)
    assert d.day == 10
    assert d.month == 5
    assert d.year == 1990
    assert d.prec == p
    assert d.delta == 0


def test_calendar_date_gregorian():
    d = DateValue(day=15, month=8, year=1947, prec=About(), delta=0)
    c = CalendarDate(dmy=d, cal=Calendar.GREGORIAN)
    assert c.dmy == d
    assert c.cal == Calendar.GREGORIAN

def test_calendar_date_julian():
    d = DateValue(day=4, month=10, year=1582, prec=About(), delta=0)
    c = CalendarDate(dmy=d, cal=Calendar.JULIAN)
    assert c.dmy == d
    assert c.cal == Calendar.JULIAN

def test_calendar_date_french():
    d = DateValue(day=1, month=1, year=1800, prec=About(), delta=0)
    c = CalendarDate(dmy=d, cal=Calendar.FRENCH)
    assert c.dmy == d
    assert c.cal == Calendar.FRENCH

def test_calendar_date_hebrew():
    d = DateValue(day=15, month=1, year=5784, prec=About(), delta=0)
    c = CalendarDate(dmy=d, cal=Calendar.HEBREW)
    assert c.dmy == d
    assert c.cal == Calendar.HEBREW


def test_date_as_calendar_date():
    d = DateValue(day=1, month=1, year=2000, prec=About(), delta=0)
    c = CalendarDate(dmy=d, cal=Calendar.GREGORIAN)
    date_var: Date = c
    assert isinstance(date_var, CalendarDate)
    assert date_var.dmy == d
    assert date_var.cal == Calendar.GREGORIAN

def test_date_as_text():
    date_text: Date = "circa 1800"
    assert isinstance(date_text, str)
    assert date_text == "circa 1800"
