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


def test_ticking_full_of_fish_makes_them_older():
    creatures = numpy.ones((2, 2))
    wator = WaTor(creatures)
    for i in range(2, 6):
        assert (wator.tick().creatures == numpy.full((2, 2), i)).all()


def test_ticking_full_of_sharks_starves_them():
    creatures = numpy.full((2, 2), -1)
    wator = WaTor(creatures)
    assert (wator.tick().creatures == numpy.full((2, 2), -2)).all()
    wator.tick().tick().tick().tick()  # total 5 times
    assert (wator.tick().creatures == numpy.zeros((2, 2))).all()


def test_fish_moves():
    creatures = numpy.zeros((1, 2))
    creatures[0, 0] = 1
    wator = WaTor(creatures)
    wator.tick()
    assert wator.creatures[0, 0] == 0
    assert wator.creatures[0, 1] == 2


def test_shark_moves_and_wastes_1_energy():
    creatures = numpy.zeros((1, 2))
    creatures[0, 0] = -1
    wator = WaTor(creatures)
    wator.tick()
    assert wator.creatures[0, 0] == 0
    assert wator.creatures[0, 1] == -2
    assert wator.energies[0, 1] == 5 - 1


def test_shark_prefers_fish():
    creatures = numpy.zeros((1, 3))
    creatures[0, 0] = -1
    creatures[0, 1] = 1  # the fish will move to 0, 2
    wator = WaTor(creatures)
    wator.tick()
    assert wator.creatures[0, 0] == 0
    assert wator.creatures[0, 1] == 0
    assert wator.creatures[0, 2] == -2
    assert wator.energies[0, 2] == 5 - 1 + 3  # initial - 1 + eat


def test_without_sharks_fish_overbreed():
    nfish = 16
    wator = WaTor(shape=(32, 8), nsharks=0, nfish=nfish)
    assert wator.count_fish() == nfish
    while wator.count_fish() < wator.creatures.size:
        wator.tick()
        assert wator.count_fish() >= nfish
        nfish = wator.count_fish()


def test_fish_move_over_border():
    creatures = numpy.zeros((2048, 16))
    creatures[:, 0] = 1
    wator = WaTor(creatures)
    wator.tick()
    # warning: theoretically this might not happen,
    # but statistically it will happen
    assert wator.creatures[:, -1].any()


def test_shark_energy_is_properly_risen():
    creatures = numpy.ones((1, 2))  # 2 fish
    creatures[0, 0] = -1  # turn a fish into a shark
    energy_initial = 5
    energy_eat = 20
    wator = WaTor(creatures, energy_initial=energy_initial,
                  energy_eat=energy_eat)
    assert wator.energies[0, 0] == energy_initial
    wator.tick()
    assert wator.energies[0, 1] == energy_initial + energy_eat - 1
