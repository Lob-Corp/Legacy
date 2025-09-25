from libraries.date import Calendar
from libraries.death_info import (
    Dead,
    DeadDontKnowWhen,
    DeadYoung,
    DeathReason,
    DeathStatusBase,
    DontKnowIfDead,
    NotDead,
    OfCourseDead,
)
from libraries.burial_info import Burial, BurialInfoBase, Cremated, UnknownBurial
import pytest

# DeathStatusBase hierarchy


def test_deathstatusbase_cannot_instantiate():
    with pytest.raises(NotImplementedError):
        DeathStatusBase()


def test_notdead_instantiation():
    nd = NotDead()
    assert isinstance(nd, NotDead)
    assert isinstance(nd, DeathStatusBase)


def test_dead_instantiation_and_reason():
    date = (Calendar.GREGORIAN, 123)
    d = Dead(DeathReason.KILLED, date)
    assert isinstance(d, Dead)
    assert d.death_reason == DeathReason.KILLED


### A REVOIR

# def test_dead_does_not_store_date_of_death():
#     date = (Calendar.GREGORIAN, 123)
#     d = Dead(DeathReason.MURDERED, date)
#     assert not hasattr(d, "date_of_death")

###


def test_deadyoung_instantiation():
    dy = DeadYoung()
    assert isinstance(dy, DeadYoung)
    assert isinstance(dy, DeathStatusBase)


def test_deaddonknowwhen_instantiation():
    ddk = DeadDontKnowWhen()
    assert isinstance(ddk, DeadDontKnowWhen)
    assert isinstance(ddk, DeathStatusBase)


def test_dontknowifdead_instantiation():
    dkid = DontKnowIfDead()
    assert isinstance(dkid, DontKnowIfDead)
    assert isinstance(dkid, DeathStatusBase)


def test_ofcoursedead_instantiation():
    ocd = OfCourseDead()
    assert isinstance(ocd, OfCourseDead)
    assert isinstance(ocd, DeathStatusBase)


# BurialInfoBase hierarchy


def test_burialinfobase_cannot_instantiate():
    with pytest.raises(NotImplementedError):
        BurialInfoBase()


def test_unknownburial_instantiation():
    ub = UnknownBurial()
    assert isinstance(ub, UnknownBurial)
    assert isinstance(ub, BurialInfoBase)


def test_burial_instantiation_and_date():
    date = (Calendar.GREGORIAN, 123)
    b = Burial(date)
    assert isinstance(b, Burial)
    assert b.burial_date == date


def test_cremated_instantiation_and_date():
    date = (Calendar.GREGORIAN, 123)
    c = Cremated(date)
    assert isinstance(c, Cremated)
    assert c.cremation_date == date
