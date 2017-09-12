import numpy
import pytest

from wator import WaTor

SIZE = 2048
SHAPE = (SIZE, SIZE)
N = SIZE ** 2 // 3


@pytest.mark.timeout(5)
def test_random_geenerator_speed():
    for i in range(20):
        wator = WaTor(shape=SHAPE, nfish=N, nsharks=N)
        print(i)
        assert wator.count_fish() == N
        assert wator.count_sharks() == N


# create this outside of test scope (not to be timed)
WATOR = WaTor(shape=SHAPE, nfish=N, nsharks=N)


@pytest.fixture
def wator():
    '''
    A large wator with copies of global creatures and energies
    '''
    return WaTor(numpy.copy(WATOR.creatures),
                 energies=numpy.copy(WATOR.energies))


@pytest.mark.timeout(60)
def test_tick_speed(wator):
    for i in range(4):
        wator.tick()
        print(i)
