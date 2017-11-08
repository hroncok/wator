import numpy
import pytest

from wator import WaTor


def test_creatures():
    creatures = numpy.zeros((8, 8))
    creatures[2, 4] = 3
    creatures[1, :] = -5
    wator = WaTor(creatures)
    print(wator.creatures)
    assert (creatures == wator.creatures).all()
    assert wator.count_fish() == 1
    assert wator.count_sharks() == 8


def test_shape():
    shape = (16, 16)
    wator = WaTor(shape=shape, nfish=16, nsharks=4)
    print(wator.creatures)
    assert wator.creatures.shape == shape
    assert wator.count_fish() == 16
    assert wator.count_sharks() == 4
    assert ((wator.creatures >= -10) & (wator.creatures <= 5)).all()


def test_shape_full_of_fish():
    shape = (16, 16)
    wator = WaTor(shape=shape, nfish=16 * 16, nsharks=0)
    print(wator.creatures)
    assert wator.count_fish() == 16 * 16
    assert wator.count_sharks() == 0


def test_shape_full_of_shark():
    shape = (16, 16)
    wator = WaTor(shape=shape, nfish=0, nsharks=16 * 16)
    print(wator.creatures)
    assert wator.count_fish() == 0
    assert wator.count_sharks() == 16 * 16


def test_shape_full_of_something():
    shape = (16, 16)
    total = 16*16
    nfish = total // 5
    nsharks = total - nfish
    wator = WaTor(shape=shape, nfish=nfish, nsharks=nsharks)
    print(wator.creatures)
    assert wator.count_fish() == nfish
    assert wator.count_sharks() == nsharks


def test_shape_custom_age():
    shape = (16, 16)
    age_fish = 2
    age_shark = 20
    wator = WaTor(shape=shape, nfish=16, nsharks=4,
                  age_fish=age_fish,
                  age_shark=age_shark)
    print(wator.creatures)
    assert wator.creatures.shape == shape
    assert wator.count_fish() == 16
    assert wator.count_sharks() == 4
    assert ((wator.creatures >= -age_shark) &
            (wator.creatures <= age_fish)).all()


def test_energy_initial_default():
    shape = (8, 8)
    creatures = numpy.zeros(shape)
    creatures[1, :] = -5
    wator = WaTor(creatures)
    print(wator.creatures)
    print(wator.energies)
    assert wator.energies.shape == shape
    assert (wator.energies[1, :] == 5).all()


def test_energy_initial_custom():
    shape = (8, 8)
    creatures = numpy.zeros(shape)
    creatures[1, :] = -5
    wator = WaTor(creatures, energy_initial=12)
    print(wator.creatures)
    print(wator.energies)
    assert wator.energies.shape == shape
    assert (wator.energies[1, :] == 12).all()


def test_energies():
    shape = (8, 8)
    creatures = numpy.zeros(shape)
    energies = numpy.zeros(shape)
    creatures[1, :] = -5
    for i in range(8):
        energies[1, i] = i
    wator = WaTor(creatures, energies=energies)
    print(wator.creatures)
    print(wator.energies)
    assert (wator.energies[1, :] == energies[1, :]).all()


def test_nonsense():
    creatures = numpy.zeros((8, 8))

    with pytest.raises(ValueError):
        WaTor(creatures, nfish=20)

    with pytest.raises(ValueError):
        WaTor(creatures, nsharks=20)

    with pytest.raises(ValueError):
        WaTor(creatures, shape=(8, 8))

    with pytest.raises(ValueError):
        WaTor(shape=(8, 8), nsharks=20)

    with pytest.raises(ValueError):
        WaTor(creatures, energies=numpy.zeros((6, 6)))

    with pytest.raises(ValueError):
        WaTor(creatures, energies=numpy.zeros((8, 8)),
              energy_initial=8)

    with pytest.raises(ValueError):
        WaTor(shape=(8, 8), nsharks=20, nfish=1000)

    with pytest.raises(TypeError):
        WaTor(shape=(8, 8), nsharks=20, nfish='nope')
