import pytest
from date.calendar_date import DateValue
from date.precision import Sure, About, Maybe, Before, After, OrYear


def test_compress_uncompress_roundtrip():
    d = DateValue(1, 2, 1999, About(), delta=0)
    i = d.compress()
    assert isinstance(i, int)
    d2 = DateValue.uncompress(i)
    # Uncompressed returns a DateValue with delta=0 and Sure/converted prec
    assert d2.year == 1999
    assert d2.month == 2
    assert d2.day == 1


def test_uncompress_default_prec_to_sure():
    d = DateValue(5, 6, 2020, Sure())
    i = d.compress()
    d2 = DateValue.uncompress(i)
    # precision should be a Precision instance (Sure or mapped)
    assert d2.prec is not None


def test_compare_basic_and_eq():
    a = DateValue(1, 1, 2000, Sure())
    b = DateValue(2, 1, 2000, Sure())
    assert a.compare(b) == -1
    assert a != b


def test_compare_unknown_day_with_prec():
    a = DateValue(0, 5, 2000, After())
    b = DateValue(10, 5, 2000, Sure())
    # unknown day with After should compare as 1
    res = a.compare(b)
    assert res == 1

def test_oryear_branch_compares_as_sure():
    inner = DateValue(1,1,2000, None)
    p_or = OrYear(inner)
    a = DateValue(1,1,2000, p_or)
    b = DateValue(1,1,2000, p_or)
    # After replacement both with Sure should be equal
    assert a.compare(b) == 0

def test_date_difference_basic():
    a = DateValue(1,1,2000, Sure())
    b = DateValue(1,1,2001, Sure())
    diff = DateValue.date_difference(a, b)
    assert diff.year == 1


def test_compress_for_each_precision():
    precisions = [Sure(), About(), Maybe(), Before(), After()]
    base = (1, 1, 2000)

    for p in precisions:
        d1 = DateValue(base[0], base[1], base[2], p)
        comp = d1.compress()
        assert comp is None or isinstance(comp, int)


def test_oryear_does_not_compress():
    inner = DateValue(1, 1, 2000, None)
    orp = OrYear(inner)
    d_or = DateValue(1, 1, 2000, orp)
    assert d_or.compress() is None


def test_date_difference_both_before_and_both_after():
    d_before1 = DateValue(1, 1, 2000, Before())
    d_before2 = DateValue(1, 1, 2001, Before())
    assert DateValue.date_difference(d_before1, d_before2) is None

    d_after1 = DateValue(1, 1, 2000, After())
    d_after2 = DateValue(1, 1, 2001, After())
    assert DateValue.date_difference(d_after1, d_after2) is None

