#cython: language_level=3, cdivision=True
cimport numpy
from libc.stdlib cimport rand, srand
from libc.time cimport time

import numpy


cdef int randint(int low, int high):
    return low + (rand() % (high - low))


srand(time(NULL))


def random_population(shape, int nfish, int nsharks,
                      int age_fish, int age_shark):
    cdef numpy.ndarray[numpy.int8_t, ndim=2] c = numpy.zeros(shape,
                                                             dtype=numpy.int8)
    cdef int sX = shape[0]
    cdef int sY = shape[1]
    cdef int size = sX * sY
    cdef int empties = size - nfish - nsharks

    if empties < 0:
        raise ValueError('too many creatures for small shape')

    cdef int i, j, rand
    for i in range(sX):
        for j in range(sY):
            rand = randint(0, empties + nfish + nsharks)
            if rand < empties:
                empties -= 1
            elif rand < empties + nfish:
                c[i, j] = randint(1, age_fish + 1)
                nfish -= 1
            else:
                c[i, j] = -randint(1, age_shark + 1)
                nsharks -= 1

    assert not empties
    assert not nfish
    assert not nsharks

    return c
