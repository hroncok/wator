import numpy


def random_population(shape, nfish, nsharks, age_fish, age_shark):
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
                c[i, j] = numpy.random.randint(1, age_fish + 1)
                nfish -= 1
            else:
                c[i, j] = -numpy.random.randint(1, age_shark + 1)
                nsharks -= 1
    assert not empties
    assert not nfish
    assert not nsharks
    return c
