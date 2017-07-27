import numpy


ENERGY_INITIAL = 5
ENERGY_EAT = 1
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
            return creatures

        if shape is None or nfish is None or nsharks is None:
            raise ValueError('when using shape/nfish/nsharks, '
                             'you need to define all')
        return self.random_population(shape, nfish, nsharks)

    @classmethod
    def random_cell(cls, shape):
        return (numpy.random.randint(shape[0]),
                numpy.random.randint(shape[1]))

    def random_population(self, shape, nfish, nsharks):
        creatures = numpy.zeros(shape, dtype=numpy.int8)
        if (nfish + nsharks) > creatures.size:
            raise ValueError('too many creatures for small shape')
        while nfish > 0 or nsharks > 0:
            cell = self.random_cell(shape)
            while creatures[cell] != 0:
                cell = self.random_cell(shape)
            if nfish > 0:
                creatures[cell] = numpy.random.randint(1, self.age_fish + 1)
                nfish -= 1
            else:
                creatures[cell] = -numpy.random.randint(1, self.age_shark + 1)
                nsharks -= 1
        return creatures

    @classmethod
    def create_energies(cls, energy_initial, energies, shape):
        if energy_initial is None:
            if energies is None:
                return numpy.full(shape, ENERGY_INITIAL)
            if energies.shape != shape:
                raise ValueError('energies array has incorrect shape')
            return energies
        if energies is not None:
            raise ValueError('cannot use energies and energy_initial together')
        return numpy.full(shape, int(energy_initial))

    def count_fish(self):
        return (self.creatures > 0).sum()

    def count_sharks(self):
        return (self.creatures < 0).sum()

    def move_fish(self):
        for ij in self.cells():
            if self.is_fish(*ij):
                ...

                self.creatures[ij] += 1

    def move_sharks(self):
        for ij in self.cells():
            if self.is_shark(*ij):
                ...

                self.energies[ij] -= 1
                self.creatures[ij] -= 1

    def remove_dead_sharks(self):
        for ij in self.cells():
            if self.is_shark(*ij) and self.is_dead(*ij):
                self.creatures[ij] = 0

    def is_fish(self, i, j):
        return self.creatures[i, j] > 0

    def is_shark(self, i, j):
        return self.creatures[i, j] < 0

    def is_dead(self, i, j):
        return self.energies[i, j] <= 0

    def cells(self):
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                yield i, j

    def tick(self):
        self.move_fish()
        self.move_sharks()
        self.remove_dead_sharks()
        return self
