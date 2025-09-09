import pytest
from consanguinity_rate import ConsanguinityRate

def test_init():
    cr = ConsanguinityRate(123456)
    assert int(cr) == 123456

def test_from_rate_rounding_down():
    rate = 0.1234562
    cr = ConsanguinityRate.from_rate(rate)
    assert int(cr) == 123456


def test_from_rate_rounding_up():
    rate = 0.3333333
    cr = ConsanguinityRate.from_rate(rate)
    assert int(cr) == 333333


def test_from_rate_exact_half_rounds_up():
    rate = 0.0000005
    cr = ConsanguinityRate.from_rate(rate)
    assert int(cr) == 1


def test_rate_conversion():
    cr = ConsanguinityRate.from_integer(250000)
    assert cr.rate() == pytest.approx(0.25)

def test_int_dunder_returns_fix_value():
    cr = ConsanguinityRate.from_integer(123456)
    assert int(cr) == 123456

def test_eq_same_fix_value():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(100000)
    assert a == b

def test_eq_different_fix_value():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(200000)
    assert not (a == b)

def test_eq_with_non_consanguinityrate_raises():
    a = ConsanguinityRate.from_integer(100000)
    with pytest.raises(TypeError):
        _ = a == 42

def test_ne_same_fix_value():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(100000)
    assert not (a != b)

def test_ne_different_fix_value():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(200000)
    assert a != b

def test_gt_true_case():
    a = ConsanguinityRate.from_integer(200000)
    b = ConsanguinityRate.from_integer(100000)
    assert a > b

def test_gt_false_case():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(200000)
    assert not (a > b)

def test_gt_with_non_consanguinityrate_raises():
    a = ConsanguinityRate.from_integer(100000)
    with pytest.raises(TypeError):
        _ = a > 5

def test_lt_true_case():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(200000)
    assert a < b

def test_lt_false_case():
    a = ConsanguinityRate.from_integer(200000)
    b = ConsanguinityRate.from_integer(100000)
    assert not (a < b)

def test_lt_with_non_consanguinityrate_raises():
    a = ConsanguinityRate.from_integer(100000)
    with pytest.raises(TypeError):
        _ = a < 5

def test_ge_true_when_greater():
    a = ConsanguinityRate.from_integer(200000)
    b = ConsanguinityRate.from_integer(100000)
    assert a >= b

def test_ge_true_when_equal():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(100000)
    assert a >= b

def test_ge_false_case():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(200000)
    assert not (a >= b)

def test_le_true_when_less():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(200000)
    assert a <= b

def test_le_true_when_equal():
    a = ConsanguinityRate.from_integer(100000)
    b = ConsanguinityRate.from_integer(100000)
    assert a <= b

def test_le_false_case():
    a = ConsanguinityRate.from_integer(200000)
    b = ConsanguinityRate.from_integer(100000)
    assert not (a <= b)
