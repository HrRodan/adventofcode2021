import collections
from itertools import zip_longest
from typing import List

Point = collections.namedtuple('Point', ['x', 'y'])


class Line():
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.covered_points_straight = self.get_all_covered_points_straight()
        self.covered_points = self.get_all_covered_points()

    def get_all_covered_points_straight(self) -> List['Point']:
        covered_points = []
        if self.start.x == self.end.x:
            min_y, max_y = (self.start.y, self.end.y) if self.end.y > self.start.y else (self.end.y, self.start.y)
            covered_points = [Point(self.start.x, y) for y in range(min_y, max_y + 1)]
        elif self.start.y == self.end.y:
            min_x, max_x = (self.start.x, self.end.x) if self.end.x > self.start.x else (self.end.x, self.start.x)
            covered_points = [Point(x, self.start.y) for x in range(min_x, max_x + 1)]
        return covered_points

    def get_all_covered_points(self) -> List['Point']:
        x_values = range_flexible(self.start.x, self.end.x)
        y_values = range_flexible(self.start.y, self.end.y)
        x_y = zip_longest(x_values, y_values, fillvalue=self.start.x) if len(x_values) <= len(y_values) \
            else zip_longest(x_values, y_values, fillvalue=self.start.y)
        return [Point(x, y) for x, y in x_y]


def range_flexible(start, end):
    if start <= end:
        return range(start, end + 1)
    else:
        return range(start, end - 1, -1)


with open('lines.txt', 'r', newline='\n') as file:
    data = ((element.strip().split(',') for element in line.strip().split(' -> ')) for line in file.readlines())
    lines = [Line(Point(int(start[0]), int(start[1])), Point(int(end[0]), int(end[1]))) for start, end in data]

point_count = collections.Counter()
for line in lines:
    point_count.update(iter(line.covered_points))

count_per_point_twice = {k: v for k, v in point_count.items() if v >= 2}
#analog
count_twice=sum(1 for k,v in point_count.items() if v >=2)
print(len(count_per_point_twice))
