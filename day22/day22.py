from typing import Tuple, List

import numpy as np

MAX_DIM = 50
SHAPE = tuple(MAX_DIM * 2 + 1 for i in range(3))

with open('input.txt', 'r') as file:
    seq = [tuple([True if on_off == 'on' else False, tuple([x[2:].split('..'), y[2:].split('..'), z[2:].split('..')])])
           for line in file.readlines()
           for on_off, ranges in [line.split()]
           for x, y, z in [ranges.split(',')]]


def convert_array_to_slice(array: Tuple):
    x, y, z = np.array(array).astype(int) + MAX_DIM
    return np.s_[x[0]:x[1] + 1, y[0]:y[1] + 1, z[0]:z[1] + 1]


seq_as_slice = [tuple([on_off, convert_array_to_slice(array)]) for on_off, array in seq
                if np.array(array).astype(int).max() <= MAX_DIM]

reactor = np.full(SHAPE, False, dtype=bool)

for key, slice_ in seq_as_slice:
    reactor[slice_] = key

print(np.count_nonzero(reactor))


class Cube():
    def __init__(self, edges: List[Tuple[int, int], Tuple[int, int], Tuple[int, int]]):
        self.x0, self.x1 = edges[0]
        self.y0, self.y1 = edges[1]
        self.z0, self.z1 = edges[2]
        self.x = edges[0]
        self.y = edges[1]
        self.z = edges[2]

    def get_diff_cubes(self, other: 'Cube'):
        diff_cubes = []
        # -x direction
        x_left = self.x0
        x_right = self.x1
        y_left = self.y0
        y_right = self.y1

        if self.x0 < other.x0 <= self.x1:
            x_right = other.x0 - 1
            diff_cubes.append(Cube([(self.x0, x_right), self.y, self.z]))
        # +x direction
        if self.x0 <= other.x1 < self.x1:
            x_left = other.x1 + 1
            diff_cubes.append(Cube([(x_left, self.x1), self.y, self.z]))

        # -y direction
        if self.y0 < other.y0 <= self.y1:
            y_right = other.y0 - 1
            diff_cubes.append(Cube([(x_left + 1, x_right - 1), (self.y0, y_right), self.z]))
        # +y direction
        if self.y0 <= other.y1 < self.y1:
            y_left = other.y1 + 1
            diff_cubes.append(Cube([(x_left + 1, x_right - 1), (y_left, self.y1), self.z]))

        # -z direction
        if self.z0 < other.z0 <= self.z1:
            z_right = other.z0 - 1
            diff_cubes.append(Cube([(x_left + 1, x_right - 1), (y_left+1, y_right-1), (self.z0, z_right)]))
        # +z direction
        if self.z0 <= other.z1 < self.z1:
            z_left = other.z1 + 1
            diff_cubes.append(Cube([(x_left + 1, x_right - 1), (y_left+1, y_right-1), (z_left, self.z1)]))

        return diff_cubes

    def volume(self):
        return (self.x1-self.x0+1)*(self.y1-self.y0+1)*(self.z1-self.z0+1)