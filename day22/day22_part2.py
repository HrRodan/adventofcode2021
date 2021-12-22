from typing import Tuple, List

import numpy as np

MAX_DIM = 50
SHAPE = tuple(MAX_DIM * 2 + 1 for i in range(3))

with open('input.txt', 'r') as file:
    seq = [tuple([True if on_off == 'on' else False, tuple([x[2:].split('..'), y[2:].split('..'), z[2:].split('..')])])
           for line in file.readlines()
           for on_off, ranges in [line.split()]
           for x, y, z in [ranges.split(',')]]


def convert_array_to_tuples(array: Tuple):
    return [tuple([int(start), int(end)]) for edge in array for start, end in [edge]]


# seq_as_tuples = [[on_off, convert_array_to_tuples(array)] for on_off, array in seq
#                  if np.abs(np.array(array).astype(int)).max() <= MAX_DIM]


seq_as_tuples = [[on_off, convert_array_to_tuples(array)] for on_off, array in seq]


class Cube():
    def __init__(self, edges: List[Tuple[int, int]]):
        self.x0, self.x1 = edges[0]
        self.y0, self.y1 = edges[1]
        self.z0, self.z1 = edges[2]
        self.x = edges[0]
        self.y = edges[1]
        self.z = edges[2]

    def __repr__(self):
        return f'Cube: {self.x},{self.y},{self.z}'

    def get_diff_cubes(self, other: 'Cube'):
        # returns the sliced initial cube, when it overlaps with 'other' cube
        # a maximum of six cubes (3*2 axes) is returned
        # The sum of the returned cubes is the difference between self and other, as is reflected in the volume

        diff_cubes = []
        if not self.any_overlap(other):
            return diff_cubes
        # -x direction
        if self.x0 < other.x0 <= self.x1:
            x_right = other.x0 - 1
            diff_cubes.append(Cube([(self.x0, x_right), self.y, self.z]))
        else:
            x_right = self.x0 - 1
        # +x direction
        if self.x0 <= other.x1 < self.x1:
            x_left = other.x1 + 1
            diff_cubes.append(Cube([(x_left, self.x1), self.y, self.z]))
        else:
            x_left = self.x1 + 1

        # -y direction
        if self.y0 < other.y0 <= self.y1:
            y_right = other.y0 - 1
            diff_cubes.append(Cube([(x_right + 1, x_left - 1), (self.y0, y_right), self.z]))
        else:
            y_right = self.y0 - 1
        # +y direction
        if self.y0 <= other.y1 < self.y1:
            y_left = other.y1 + 1
            diff_cubes.append(Cube([(x_right + 1, x_left - 1), (y_left, self.y1), self.z]))
        else:
            y_left = self.y1 + 1

        # -z direction
        if self.z0 < other.z0 <= self.z1:
            z_right = other.z0 - 1
            diff_cubes.append(Cube([(x_right + 1, x_left - 1), (y_right + 1, y_left - 1), (self.z0, z_right)]))
        # +z direction
        if self.z0 <= other.z1 < self.z1:
            z_left = other.z1 + 1
            diff_cubes.append(Cube([(x_right + 1, x_left - 1), (y_right + 1, y_left - 1), (z_left, self.z1)]))

        return diff_cubes

    def is_in(self, other: 'Cube'):
        # Checks if other is in self
        return (other.x0 <= self.x0 <= self.x1 <= other.x1 and other.y0 <= self.y0 <= self.y1 <= other.y1
                and other.z0 <= self.z0 <= self.z1 <= other.z1)

    def volume(self):
        return (self.x1 - self.x0 + 1) * (self.y1 - self.y0 + 1) * (self.z1 - self.z0 + 1)

    def any_overlap(self, other: 'Cube'):
        # checks if there is any overlap between self and other
        return ((
                        self.x0 <= other.x0 <= self.x1 or self.x0 <= other.x1 <= self.x1
                        or other.x0 <= self.x0 <= self.x1 <= other.x1) and
                (
                        self.y0 <= other.y0 <= self.y1 or self.y0 <= other.y1 <= self.y1
                        or other.y0 <= self.y0 <= self.y1 <= other.y1) and
                (
                        self.z0 <= other.z0 <= self.z1 or self.z0 <= other.z1 <= self.z1
                        or other.z0 <= self.z0 <= self.z1 <= other.z1))


if __name__ == '__main__':

    cubicles: List['Cube'] = [Cube(seq_as_tuples[0][1])]
    for on_off, seq in seq_as_tuples[1:]:
        cube_new = Cube(seq)
        cubicles_new = cubicles.copy()
        for cube in cubicles:
            if cube.is_in(cube_new):
                cubicles_new.remove(cube)
            else:
                diff = cube.get_diff_cubes(cube_new)
                if diff:
                    cubicles_new.remove(cube)
                    cubicles_new.extend(diff)
        if on_off:
            cubicles_new.append(cube_new)
        cubicles = cubicles_new

    sum_volume = sum([c.volume() for c in cubicles])
    print(sum_volume)
