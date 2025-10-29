import pytest
from libraries.sosa import Sosa

def test_constructor_and_static_methods():
    assert Sosa.zero().value == 0
    assert Sosa.one().value == 1

    with pytest.raises(ValueError):
        Sosa(-1)

def test_equality_and_comparison():
    s1 = Sosa(5)
    s2 = Sosa(5)
    s3 = Sosa(7)

    assert s1 == s2
    assert s1 != s3
    assert s3 > s1
    assert not (s1 > s3)

    assert s1 <= s2
    assert s1 < s3
    assert s3 >= s2

def test_non_sosa_comparisons_eq_and_gt():
    s = Sosa(5)

    assert (s == 5) is False
    assert (5 == s) is False

    assert (s != 5) is True

    with pytest.raises(TypeError):
        _ = s > 5

    with pytest.raises(TypeError):
        _ = 5 > s

def test_non_sosa_other_comparisons():
    s = Sosa(5)

    with pytest.raises(TypeError):
        _ = s < 5

    with pytest.raises(TypeError):
        _ = 5 < s

    with pytest.raises(TypeError):
        _ = s <= 5

    with pytest.raises(TypeError):
        _ = s >= 5


def test_arithmetic_operations():
    s1 = Sosa(10)
    s2 = Sosa(3)

    assert (s1 + s2).value == 13
    assert (s1 - s2).value == 7
    with pytest.raises(ValueError):
        _ = s2 - s1

    assert (s2 * 4).value == 12
    assert (s2 ** 3).value == 27

    assert (s1 // 2).value == 5
    with pytest.raises(ZeroDivisionError):
        _ = s1 // 0

    assert (s1 % 6).value == 4
    with pytest.raises(ZeroDivisionError):
        _ = s1 % 0

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

def test_conversions_and_str():
    s = Sosa.of_int(42)
    assert isinstance(s, Sosa)
    assert s.value == 42

    s2 = Sosa.of_string("123")
    assert s2.value == 123

    assert str(Sosa(9999)) == "9999"
    assert repr(Sosa(7)) == "Sosa(7)"

    assert Sosa(1234567).to_string_sep(",") == "1,234,567"
    assert Sosa(1234567).to_string_sep(" ") == "1 234 567"

def test_family_methods() -> None:
    s: Sosa = Sosa(3)

    assert s.father() == Sosa(6)
    assert s.mother() == Sosa(7)
    assert s.child() == Sosa(1)

def test_family_relations():
    s1 = Sosa(1)
    s2 = Sosa(2)
    s3 = Sosa(3)

    assert s1.father().value == 2
    assert s1.mother().value == 3

    assert s2.child().value == 1
    assert s3.child().value == 1
    assert Sosa(6).child().value == 3

    with pytest.raises(ValueError):
        Sosa(0).father()
    with pytest.raises(ValueError):
        Sosa(0).mother()
    with pytest.raises(ValueError):
        Sosa(0).child()

    with pytest.raises(ValueError):
        s1.child()
