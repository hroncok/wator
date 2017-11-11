import numpy


ENERGY_INITIAL = 5
ENERGY_EAT = 3
AGE_FISH = 5
AGE_SHARK = 10
FISH = 1
SHARK = -1


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

        self._moved = numpy.empty(self.shape, dtype=numpy.bool)

    @property
    def shape(self):
        return self.creatures.shape

    @property
    def height(self):
        return self.shape[0]

    @property
    def width(self):
        return self.shape[1]

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
        c = numpy.zeros(shape, dtype=numpy.int8)
        empties = c.size - nfish - nsharks
        if empties < 0:
            raise ValueError('too many creatures for small shape')
        for i in range(shape[0]):
            for j in range(shape[1]):
                rand = numpy.random.randint(empties + nfish + nsharks)
                if rand < empties:
                    empties -= 1
                elif rand < empties + nfish:
                    c[i, j] = numpy.random.randint(1, self.age_fish + 1)
                    nfish -= 1
                else:
                    c[i, j] = -numpy.random.randint(1, self.age_shark + 1)
                    nsharks -= 1
        assert not empties
        assert not nfish
        assert not nsharks
        return c

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

    def north(self, i, j):
        return (i - 1) % self.height, j

    def south(self, i, j):
        return (i + 1) % self.height, j

    def west(self, i, j):
        return i, (j - 1) % self.width

    def east(self, i, j):
        return i, (j + 1) % self.width

    @property
    def directions(self):
        return {self.north, self.south, self.west, self.east}

    def _move_one_creature(self, i, j, creature):
        targets = []
        if creature == SHARK:
            for direction in self.directions:
                newpos = direction(i, j)
                if self.is_fish(*newpos):
                    targets.append(newpos)
        if not targets:
            for direction in self.directions:
                newpos = direction(i, j)
                if self.is_empty(*newpos):
                    targets.append(newpos)

        if creature == SHARK:
            self.energies[i, j] -= 1
        if targets:
            # numpy.random.choice cannot choose from list of tuples
            # ValueError: a must be 1-dimensional
            target = targets[numpy.random.choice(len(targets))]
            is_fish = self.is_fish(*target)
            if self.should_breed(i, j):
                self.creatures[target] = creature
                self.creatures[i, j] = creature
                self._moved[i, j] = True
            else:
                self.creatures[target] = self.creatures[i, j] + creature
                self.creatures[i, j] = 0
            self._moved[target] = True

            if creature == SHARK:
                self.energies[target] = self.energies[i, j]
                if is_fish:
                    self.energies[target] += self.energy_eat
        else:
            self._moved[i, j] = True
            if not self.should_breed(i, j):
                self.creatures[i, j] += creature

    def move_one_fish(self, i, j):
        return self._move_one_creature(i, j, FISH)

    def move_one_shark(self, i, j):
        return self._move_one_creature(i, j, SHARK)

    def move_fish(self):
        self._moved[::] = False
        for ij in self.cells():
            if self.is_fish(*ij) and not self.is_moved(*ij):
                self.move_one_fish(*ij)

    def move_sharks(self):
        self._moved[::] = False
        for ij in self.cells():
            if self.is_shark(*ij) and not self.is_moved(*ij):
                self.move_one_shark(*ij)

    def remove_dead_sharks(self):
        for ij in self.cells():
            if self.is_shark(*ij) and self.is_dead(*ij):
                self.creatures[ij] = 0

    def is_fish(self, i, j):
        return self.creatures[i, j] > 0

    def is_shark(self, i, j):
        return self.creatures[i, j] < 0

    def is_empty(self, i, j):
        return self.creatures[i, j] == 0

    def is_dead(self, i, j):
        return self.energies[i, j] <= 0

    def is_moved(self, i, j):
        return self._moved[i, j]

    def should_breed(self, i, j):
        return not (-self.age_shark <= self.creatures[i, j] <= self.age_fish)

    def cells(self):
        for i in range(self.height):
            for j in range(self.width):
                yield i, j

    def tick(self):
        self.move_fish()
        self.move_sharks()
        self.remove_dead_sharks()
        return self
