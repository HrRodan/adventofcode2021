import re
from typing import Tuple, List

import numpy as np

#input_ = 'target area: x=20..30, y=-10..-5'
input_ = 'target area: x=235..259, y=-118..-62'

target_area = [int(x) for x in re.findall(r'-?\d+', input_)]
x_target_in = (target_area[0], target_area[1])
y_target_in = (target_area[2], target_area[3])


class Trajectory():
    def __init__(self, x_target: Tuple[int, int], y_target: Tuple[int, int], v0: Tuple[int, int]):
        self.x_target = x_target
        self.y_target = y_target
        self.start = np.array([0, 0])
        self.v0 = v0
        self._v = np.array(v0)
        self.in_target = False
        self.final_point, self.max_y = self.eval_path()

    def incv(self):
        vx = self._v[0]
        if vx == 0:
            self._v = self._v + (0, -1)
        elif vx < 0:
            self._v = self._v + (1, -1)
        else:
            self._v = self._v + (-1, -1)
        # self._v = np.array((min(0, vx + 1) if vx < 0 else max(0, vx - 1), vy - 1))

    def point_in_target(self, point):
        px, py = point
        return (
                self.y_target[0] <= py <= self.y_target[1]
                and self.x_target[0] <= px <= self.x_target[1]
        )

    def point_in_range(self, point):
        px, py = point
        return py >= self.y_target[0] and (px >= self.x_target[0] if px < 0 else px <= self.x_target[1])

    def eval_path(self) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        point = self.start
        y_max = 0
        while self.point_in_range(point):
            if self.point_in_target(point):
                self.in_target = True
                break
            point = point + self._v
            y_max = max(y_max, point[1])
            self.incv()
            #break if velocity is 0 and target not reached
            if self._v[0] == 0 and point[0] < self.x_target[0]:
                break
        return (point, y_max)


def iterate_trajectories(x_target: Tuple[int, int], y_target: Tuple[int, int]):
    x_range = range(1, x_target[0] - 1, -1) if x_target[0] < 0 else range(x_target[1] + 1)
    #each shot reaches y=0 at -vy0 and hits bottom of target only if v<bottom_of_target
    vy_min = min(y_target)
    y_max = 0
    T_max = None
    count = 0
    for vy0 in range(vy_min, abs(vy_min)):
        for vx0 in x_range:
            t = Trajectory(x_target, y_target, (vx0, vy0))
            if t.in_target:
                count += 1
                if t.max_y > y_max:
                    y_max = max(y_max, t.max_y)
                    T_max = t
    return (T_max, count)


if __name__ == '__main__':
    t = iterate_trajectories(x_target_in, y_target_in)
    print(t[1])
