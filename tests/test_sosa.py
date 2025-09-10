import pytest
from sosa import Sosa

def test_constructor_and_static_methods():
    assert Sosa.zero().value == 0
    assert Sosa.one().value == 1

    with pytest.raises(ValueError):
        Sosa(-1)

def test_equality_and_comparison():
    s1 = Sosa(5)
    s2 = Sosa(5)
    s3 = Sosa(7)

    assert s1.eq(s2)
    assert not s1.eq(s3)
    assert s3.gt(s1)
    assert not s1.gt(s3)

    assert s1.compare(s2) == 0
    assert s3.compare(s1) == 1
    assert s1.compare(s3) == -1

def test_arithmetic_operations():
    s1 = Sosa(10)
    s2 = Sosa(3)

    assert s1.add(s2).value == 13
    assert s1.sub(s2).value == 7
    with pytest.raises(ValueError):
        s2.sub(s1)

    assert s2.twice().value == 6
    assert s1.half().value == 5
    assert Sosa(4).even()
    assert not Sosa(5).even()

    assert s1.inc(5).value == 15
    assert s2.mul(4).value == 12
    assert s2.exp(3).value == 27

    assert s1.div(2).value == 5
    with pytest.raises(ZeroDivisionError):
        s1.div(0)

    assert s1.modl(6).value == 4
    with pytest.raises(ZeroDivisionError):
        s1.modl(0)

def test_generation():
    assert Sosa.zero().gen() == 0
    assert Sosa.one().gen() == 1
    assert Sosa(2).gen() == 2
    assert Sosa(3).gen() == 2
    assert Sosa(4).gen() == 3
    assert Sosa(8).gen() == 4

def test_branches():
    assert Sosa(1).branches() == []
    assert Sosa(2).branches() == [0]
    assert Sosa(3).branches() == [1]
    assert Sosa(4).branches() == [0, 0]
    assert Sosa(5).branches() == [0, 1]
    assert Sosa(6).branches() == [1, 0]
    assert Sosa(7).branches() == [1, 1]

def test_conversions():
    s = Sosa.of_int(42)
    assert isinstance(s, Sosa)
    assert s.value == 42

    s2 = Sosa.of_string("123")
    assert s2.value == 123

    assert Sosa(9999).to_string() == "9999"
    assert Sosa(1234567).to_string_sep(",") == "1,234,567"
    assert Sosa(1234567).to_string_sep(" ") == "1 234 567"
