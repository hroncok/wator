import numpy

from wator import WaTor


def test_tick_returns_self():
    creatures = numpy.zeros((2, 2))
    wator = WaTor(creatures)
    assert wator.tick() == wator


def test_ticking_empty_does_nothing():
    creatures = numpy.zeros((2, 2))
    wator = WaTor(creatures)
    assert (wator.tick().creatures == creatures).all()


def test_ticking_full_of_fish_does_nothing():
    creatures = numpy.ones((2, 2))
    wator = WaTor(creatures)
    assert (wator.tick().creatures == creatures).all()


def test_ticking_full_of_sharks_starves_them():
    creatures = numpy.full((2, 2), -1)
    wator = WaTor(creatures)
    assert (wator.tick().creatures == creatures).all()
    wator.tick().tick().tick().tick()  # total 5 times
    assert (wator.tick().creatures == numpy.zeros((2, 2))).all()
