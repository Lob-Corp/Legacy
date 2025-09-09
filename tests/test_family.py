import pytest
from familly import *


# ---- __init__ ----
def test_init_with_list_of_ints():
    p = Parents([1, 2])
    assert p.parents == [1, 2]

def test_init_empty_list():
    with pytest.raises(AssertionError):
        _ = Parents([])

def test_init_type_check_fails():
    with pytest.raises(AssertionError):
        Parents([1, "not same type"])


# ---- from_couple ----
def test_from_couple_with_ints():
    p = Parents.from_couple(1, 2)
    assert isinstance(p, Parents)
    assert p.parents == [1, 2]

def test_from_couple_type_check_fails():
    with pytest.raises(AssertionError):
        Parents.from_couple(1, "x")


# ---- is_couple ----
def test_is_couple_true():
    p = Parents([1, 2])
    assert p.is_couple() is True

def test_is_couple_false():
    p = Parents([1])
    assert p.is_couple() is False


# ---- couple ----
def test_couple_returns_tuple():
    p = Parents([1, 2])
    assert p.couple() == (1, 2)

def test_couple_raises_if_not_two():
    p = Parents([1])
    with pytest.raises(AssertionError):
        p.couple()


# ---- father ----
def test_father_returns_first():
    p = Parents([1, 2])
    assert p.father() == 1

def test_father_with_one_parent():
    p = Parents([42])
    assert p.father() == 42


# ---- mother ----
def test_mother_returns_second():
    p = Parents([1, 2])
    assert p.mother() == 2

def test_mother_raises_if_not_enough():
    p = Parents([1])
    with pytest.raises(AssertionError):
        p.mother()


# ---- __getitem__ ----
def test_getitem_valid_index():
    p = Parents([1, 2, 3])
    assert p[0] == 1
    assert p[2] == 3

def test_getitem_out_of_range():
    p = Parents([1])
    with pytest.raises(AssertionError):
        _ = p[5]
