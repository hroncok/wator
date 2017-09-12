#cython: language_level=3, cdivision=True, boundscheck=False, initializedcheck=False, wraparound=False, nonecheck=False, overflowcheck=False
cimport numpy
from libc.stdlib cimport rand, srand
from libc.time cimport time

import numpy


ctypedef numpy.int8_t i8
ctypedef numpy.int64_t i64


cdef int randint(int low, int high):
    return low + (rand() % (high - low))


srand(time(NULL))


def random_population(shape, int nfish, int nsharks,
                      int age_fish, int age_shark):
    cdef numpy.ndarray[i8, ndim=2] c = numpy.zeros(shape, dtype=numpy.int8)
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


cdef bint is_fish(numpy.ndarray[i8, ndim=2] creatures, int i, int j):
    return creatures[i, j] > 0


cdef bint is_shark(numpy.ndarray[i8, ndim=2] creatures, int i, int j):
    return creatures[i, j] < 0


cdef bint is_empty(numpy.ndarray[i8, ndim=2] creatures, int i, int j):
    return creatures[i, j] == 0


cdef bint is_dead(numpy.ndarray[i64, ndim=2] energies, int i, int j):
    return energies[i, j] <= 0


cdef bint is_moved(numpy.ndarray[i8, ndim=2] moved, int i, int j):
    return moved[i, j]


cdef void move_one_fish(numpy.ndarray[i8, ndim=2] creatures,
                        numpy.ndarray[i64, ndim=2] energies,
                        numpy.ndarray[i8, ndim=2] moved,
                        numpy.ndarray[i64, ndim=2] targets,
                        int age_fish,
                        int shape0, int shape1,
                        int i, int j):
    cdef int tcount = 0
    cdef int tmp, t0, t1

    tmp = (i - 1 + shape0) % shape0
    if is_empty(creatures, tmp, j):
        targets[tcount, 0] = tmp
        targets[tcount, 1] = j
        tcount +=1

    tmp = (i + 1) % shape0
    if is_empty(creatures, tmp, j):
        targets[tcount, 0] = tmp
        targets[tcount, 1] = j
        tcount +=1

    tmp = (j - 1 + shape1) % shape1
    if is_empty(creatures, i, tmp):
        targets[tcount, 0] = i
        targets[tcount, 1] = tmp
        tcount +=1

    tmp = (j + 1) % shape1
    if is_empty(creatures, i, tmp):
        targets[tcount, 0] = i
        targets[tcount, 1] = tmp
        tcount +=1

    if tcount > 0:
        tmp = randint(0, tcount)
        t0 = targets[tmp, 0]
        t1 = targets[tmp, 1]

        if creatures[i, j] > age_fish:
            creatures[t0, t1] = 1
            creatures[i, j] = 1
            moved[i, j] = True
        else:
            creatures[t0, t1] = creatures[i, j] + 1
            creatures[i, j] = 0
        moved[t0, t1] = True
    else:
        moved[i, j] = True
        if creatures[i, j] <= age_fish:
            creatures[i, j] += 1


cdef void move_one_shark(numpy.ndarray[i8, ndim=2] creatures,
                         numpy.ndarray[i64, ndim=2] energies,
                         numpy.ndarray[i8, ndim=2] moved,
                         numpy.ndarray[i64, ndim=2] targets,
                         int age_shark, int energy_eat,
                         int shape0, int shape1,
                         int i, int j):
    cdef int tcount = 0
    cdef int tmp, t0, t1

    tmp = (i - 1 + shape0) % shape0
    if is_fish(creatures, tmp, j):
        targets[tcount, 0] = tmp
        targets[tcount, 1] = j
        tcount +=1

    tmp = (i + 1) % shape0
    if is_fish(creatures, tmp, j):
        targets[tcount, 0] = tmp
        targets[tcount, 1] = j
        tcount +=1

    tmp = (j - 1 + shape1) % shape1
    if is_fish(creatures, i, tmp):
        targets[tcount, 0] = i
        targets[tcount, 1] = tmp
        tcount +=1

    tmp = (j + 1) % shape1
    if is_fish(creatures, i, tmp):
        targets[tcount, 0] = i
        targets[tcount, 1] = tmp
        tcount +=1

    if tcount == 0:
        tmp = (i - 1 + shape0) % shape0
        if is_empty(creatures, tmp, j):
            targets[tcount, 0] = tmp
            targets[tcount, 1] = j
            tcount +=1

        tmp = (i + 1) % shape0
        if is_empty(creatures, tmp, j):
            targets[tcount, 0] = tmp
            targets[tcount, 1] = j
            tcount +=1

        tmp = (j - 1 + shape1) % shape1
        if is_empty(creatures, i, tmp):
            targets[tcount, 0] = i
            targets[tcount, 1] = tmp
            tcount +=1

        tmp = (j + 1) % shape1
        if is_empty(creatures, i, tmp):
            targets[tcount, 0] = i
            targets[tcount, 1] = tmp
            tcount +=1

    energies[i, j] -= 1

    if tcount > 0:
        tmp = randint(0, tcount)
        t0 = targets[tmp, 0]
        t1 = targets[tmp, 1]

        was_fish = is_fish(creatures, t0, t1)

        if creatures[i, j] < -age_shark:
            creatures[t0, t1] = -1
            creatures[i, j] = -1
            moved[i, j] = True
        else:
            creatures[t0, t1] = creatures[i, j] - 1
            creatures[i, j] = 0
        moved[t0, t1] = True

        energies[t0, t1] = energies[i, j]
        if was_fish:
            energies[t0, t1] += energy_eat
    else:
        moved[i, j] = True
        if creatures[i, j] >= -age_shark:
            creatures[i, j] -= 1


cdef void move_fish(numpy.ndarray[i8, ndim=2] creatures,
                    numpy.ndarray[i64, ndim=2] energies,
                    numpy.ndarray[i8, ndim=2] moved,
                    numpy.ndarray[i64, ndim=2] targets,
                    int age_fish,
                    int shape0, int shape1):
    cdef int i, j
    for i in range(shape0):
        for j in range(shape1):
            if is_fish(creatures, i, j) and not is_moved(moved, i, j):
                move_one_fish(creatures, energies, moved, targets, age_fish,
                              shape0, shape1, i, j)


cdef void move_sharks(numpy.ndarray[i8, ndim=2] creatures,
                      numpy.ndarray[i64, ndim=2] energies,
                      numpy.ndarray[i8, ndim=2] moved,
                      numpy.ndarray[i64, ndim=2] targets,
                      int age_shark, int energy_eat,
                      int shape0, int shape1):
    cdef int i, j
    for i in range(shape0):
        for j in range(shape1):
            if is_shark(creatures, i, j) and not is_moved(moved, i, j):
                move_one_shark(creatures, energies, moved, targets, age_shark,
                               energy_eat, shape0, shape1, i, j)


cdef void  remove_dead_sharks(numpy.ndarray[i8, ndim=2] creatures,
                              numpy.ndarray[i64, ndim=2] energies,
                              int shape0, int shape1):
    cdef int i, j
    for i in range(shape0):
        for j in range(shape1):
            if is_shark(creatures, i, j) and is_dead(energies, i, j):
                creatures[i, j] = 0


def tick(numpy.ndarray[i8, ndim=2] creatures,
         numpy.ndarray[i64, ndim=2] energies,
         int age_fish, int age_shark, int energy_eat,
         shape):
    cdef numpy.ndarray[i8, ndim=2] moved
    cdef numpy.ndarray[i64, ndim=2] targets = \
        numpy.ndarray((4, 2), dtype=numpy.int64)

    cdef int shape0 = shape[0]
    cdef int shape1 = shape[1]

    # numpy arrays are references, can change in-place:

    moved = numpy.zeros(shape, dtype=numpy.int8)
    move_fish(creatures, energies, moved, targets, age_fish, shape0, shape1)

    moved[::] = 0
    move_sharks(creatures, energies, moved, targets, age_shark, energy_eat,
                shape0, shape1)

    remove_dead_sharks(creatures, energies, shape0, shape1)
    return creatures, energies
