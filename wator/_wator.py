import numpy

from . import _cwator


ENERGY_INITIAL = 5
ENERGY_EAT = 3
AGE_FISH = 5
AGE_SHARK = 10


class WaTor:
    def __init__(self, creatures=None, *, shape=None,
                 nfish=None, nsharks=None,
                 age_fish=AGE_FISH, age_shark=AGE_SHARK,
                 energy_initial=None, energies=None, energy_eat=ENERGY_EAT):
        self.age_fish, self.age_shark = int(age_fish), int(age_shark)

        self.creatures = self.create_creatures(creatures, shape,
                                               nfish, nsharks)

        self.energies = self.create_energies(energy_initial, energies,
                                             self.shape)

        self.energy_eat = int(energy_eat)

    @property
    def shape(self):
        return self.creatures.shape

    def create_creatures(self, creatures, shape, nfish, nsharks):
        if isinstance(creatures, numpy.ndarray):
            if shape is not None or nfish is not None or nsharks is not None:
                raise ValueError('cannot use creatures and '
                                 'shape/nfish/nsharks together')
            return creatures.astype(numpy.int8, copy=False)

        if shape is None or nfish is None or nsharks is None:
            raise ValueError('when using shape/nfish/nsharks, '
                             'you need to define all')
        return self.random_population(shape, nfish, nsharks)

    def random_population(self, shape, nfish, nsharks):
        return _cwator.random_population(shape, nfish, nsharks,
                                         self.age_fish, self.age_shark)

    @classmethod
    def create_energies(cls, energy_initial, energies, shape):
        if energy_initial is None:
            if energies is None:
                return numpy.full(shape, ENERGY_INITIAL)
            if energies.shape != shape:
                raise ValueError('energies array has incorrect shape')
            return energies.astype(numpy.int64, copy=False)
        if energies is not None:
            raise ValueError('cannot use energies and energy_initial together')
        return numpy.full(shape, int(energy_initial))

    def count_fish(self):
        return (self.creatures > 0).sum()

    def count_sharks(self):
        return (self.creatures < 0).sum()

    def tick(self):
        self.creatures, self.energies = _cwator.tick(self.creatures,
                                                     self.energies,
                                                     self.age_fish,
                                                     self.age_shark,
                                                     self.energy_eat,
                                                     self.shape)
        return self
