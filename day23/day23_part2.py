import heapq
from collections import defaultdict
from copy import copy
from itertools import chain
from typing import Tuple, Set, Dict, List

import numpy as np

final_position = '''#############
#...........#
###A#B#C#D###
  #A#B#C#D#  
  #A#B#C#D#  
  #A#B#C#D#  
  #########  '''

burrow = np.array([[c for c in list(line)] for line in final_position.split('\n')])
burrow[burrow == ' '] = '#'
hallway = {tuple(h) for h in np.transpose((burrow == '.').nonzero())}
rooms = {'A': {tuple(h) for h in np.transpose((burrow == 'A').nonzero())},
         'B': {tuple(h) for h in np.transpose((burrow == 'B').nonzero())},
         'C': {tuple(h) for h in np.transpose((burrow == 'C').nonzero())},
         'D': {tuple(h) for h in np.transpose((burrow == 'D').nonzero())}}
all_rooms = set().union(*rooms.values())
open_space = hallway.copy()
for value in rooms.values():
    open_space.update(value)
entries = {(1, 3), (1, 5), (1, 7), (1, 9)}

neighbors = defaultdict(list)
for point in open_space:
    x, y = point
    close_points = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
    for target in close_points:
        if target in open_space:
            neighbors[point].append(target)

costs = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}


class Burrow():
    def __init__(self, a1: 'Amphipod', a2: 'Amphipod', b1: 'Amphipod', b2: 'Amphipod',
                 c1: 'Amphipod', c2: 'Amphipod', d1: 'Amphipod', d2: 'Amphipod',
                 a3: 'Amphipod', a4: 'Amphipod', b3: 'Amphipod', b4: 'Amphipod',
                 c3: 'Amphipod', c4: 'Amphipod', d3: 'Amphipod', d4: 'Amphipod',total_costs=0):
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2
        self.c1 = c1
        self.c2 = c2
        self.d1 = d1
        self.d2 = d2
        self.a3 = a3
        self.a4 = a4
        self.b3 = b3
        self.b4 = b4
        self.c3 = c3
        self.c4 = c4
        self.d3 = d3
        self.d4 = d4
        self.total_cost = total_costs
        self.all = [self.a1, self.a2, self.b1, self.b2, self.c1, self.c2, self.d1, self.d2,
                    self.a3, self.a4, self.b3, self.b4, self.c3, self.c4, self.d3, self.d4]

    def __repr__(self):
        return f'a1: {self.a1.position}, a2: {self.a2.position}, ' \
               f'b1: {self.b1.position}, b2: {self.b2.position}, ' \
               f'c1: {self.c1.position}, c2: {self.c2.position},' \
               f'd1: {self.d1.position}, d2: {self.d2.position},' \
               f'total_costs: {self.total_cost}'

    def amphipod_positions(self) -> Set[Tuple[int, int]]:
        return {a.position for a in self.all}

    def get_possible_burrows(self):
        occupied_rooms = self.room_occupied()
        all_positions = self.amphipod_positions()
        next_burrows = []
        for i, amphi in enumerate(self.all):
            for pos, costs_ in amphi.get_possible_positions(all_positions,occupied_rooms[amphi.type_]).items():
                all_temp = [copy(a) for a in self.all]
                all_temp[i].move(pos)
                next_burrows.append(Burrow(*all_temp, total_costs=self.total_cost + costs_))

        return next_burrows

    def room_occupied(self):
        occupied_rooms = {'A':False, 'B':False, 'C':False, 'D':False}
        for a in self.all:
            for room_type in occupied_rooms:
                if a.type_ != room_type and a.position in rooms[room_type]:
                    occupied_rooms[room_type]=True

        return occupied_rooms



    def __hash__(self):
        return hash((self.a1.position, self.a2.position, self.b1.position, self.b2.position, self.c1.position,
                     self.c2.position, self.d1.position, self.d2.position,
                     self.a3.position, self.a4.position, self.b3.position, self.b4.position, self.c3.position,
                     self.c4.position, self.d3.position, self.d4.position
                     ))

    def __eq__(self, other: 'Burrow'):
        if not isinstance(other, type(self)): return NotImplemented
        return (self.a1.position == other.a1.position and self.a2.position == other.a2.position and
                self.b1.position == other.b1.position and self.b2.position == other.b2.position and
                self.c1.position == other.c1.position and self.c2.position == other.c2.position and
                self.d1.position == other.d1.position and self.d2.position == other.d2.position and
                self.a3.position == other.a3.position and self.a4.position == other.a4.position and
                self.b3.position == other.b3.position and self.b4.position == other.b4.position and
                self.c3.position == other.c3.position and self.c4.position == other.c4.position and
                self.d3.position == other.d3.position and self.d4.position == other.d4.position
                )

    def is_final_position(self):
        return all(p.position in rooms[p.type_] for p in self.all)

    def get_amphis_not_in_place(self):
        return sum(a.position not in rooms[a.type_] for a in self.all)


class Amphipod():
    def __init__(self, type_: str, id_: str, position: Tuple[int, int]):
        self.id_ = id
        self.position = position
        self.type_ = type_
        self.hallway_stop = False

    def get_possible_positions(self, all_amphipod_pos, room_occupied : bool) -> Dict[Tuple[int, int], int]:
        visited = {}

        def dfs(pos, path_costs):
            if pos not in visited.keys():
                visited[pos] = path_costs
                path_costs += costs[self.type_]
                for n in neighbors[pos]:
                    if n not in all_amphipod_pos:
                        dfs(n, path_costs)

        dfs(self.position, 0)

        # remove all unvalid targets
        targets_to_remove = chain(entries, [self.position], (all_rooms - rooms[self.type_]))
        if self.hallway_stop:
            targets_to_remove = chain(targets_to_remove, hallway)
        if room_occupied:
            targets_to_remove = chain(targets_to_remove, rooms[self.type_])
        for key in targets_to_remove:
            visited.pop(key, None)

        return visited

    def move(self, target_: Tuple[int, int]):
        if target in hallway:
            self.hallway_stop = True
        self.position = target_

if __name__ == '__main__':
    my_input = '''#############
    #...........#
    ###A#C#B#D###
    #B#A#D#C#
    #########'''
    # Test
    a1 = Amphipod('A', 'a1', (5, 3))
    a2 = Amphipod('A', 'a2', (5, 9))
    b1 = Amphipod('B', 'b1', (2, 3))
    b2 = Amphipod('B', 'b2', (2, 7))
    c1 = Amphipod('C', 'c1', (2, 5))
    c2 = Amphipod('C', 'c2', (5, 7))
    d1 = Amphipod('D', 'd1', (5, 9))
    d2 = Amphipod('D', 'd2', (5, 5))

    #myinput
    # a1 = Amphipod('A', 'a1', (2, 3))
    # a2 = Amphipod('A', 'a2', (3, 5))
    # b1 = Amphipod('B', 'b1', (3, 3))
    # b2 = Amphipod('B', 'b2', (2, 7))
    # c1 = Amphipod('C', 'c1', (2, 5))
    # c2 = Amphipod('C', 'c2', (3, 9))
    # d1 = Amphipod('D', 'd1', (3, 7))
    # d2 = Amphipod('D', 'd2', (2, 9))

    a3 = Amphipod('A', 'a3', (3, 9))
    a4 = Amphipod('A', 'a4', (4, 7))
    b3 = Amphipod('B', 'b3', (4, 5))
    b4 = Amphipod('B', 'b4', (3, 7))
    c3 = Amphipod('C', 'c3', (4, 9))
    c4 = Amphipod('C', 'c4', (3, 5))
    d3 = Amphipod('D', 'd3', (3, 3))
    d4 = Amphipod('D', 'd4', (4, 3))



    start = Burrow(a1, a2, b1, b2, c1, c2, d1, d2,a3,a4,b3,b4,c3, c4, d3,d4, 0)
    # n = start.get_possible_burrows()
    #
    # #B moved
    # n2 = n[11].get_possible_burrows()
    # #C moved
    # a = n2[3]
    # n3 = a.get_possible_burrows()
    # #D moved
    # n4 = n3[7].get_possible_burrows()
    # #b moved
    # n5 = n4[3].get_possible_burrows()
    # #b moved
    # n6=n5[1].get_possible_burrows()
    # # #D moves
    # n7 = n6[6].get_possible_burrows()
    # # #Amoves
    # n8 = n7[4].get_possible_burrows()
    #  # D moves
    # n9 = n8[5].get_possible_burrows()
    # # # D moves
    # n10 = n9[5].get_possible_burrows()
    #
    # n11 = n10[6]

    shortest_paths = {start: 0}
    visited: Set['Burrow'] = set()
    burrows_to_visit: List[Tuple[int, int, 'Burrow']] = []
    heapq.heappush(burrows_to_visit, (start.get_amphis_not_in_place()*100000, start.__hash__(), start))
    printcounter = 0
    current_min_final_cost = 100000
    # Dijkstra's algorithm
    while burrows_to_visit:
        cost_current, _, burrow_current = heapq.heappop(burrows_to_visit)
        visited.add(burrow_current)
        possible_next_burrows = burrow_current.get_possible_burrows()
        for burrow_next in possible_next_burrows:
            cost_next = burrow_next.total_cost

            if burrow_next not in shortest_paths or cost_next < shortest_paths[burrow_next]:
                shortest_paths[burrow_next] = cost_next
                if burrow_next not in visited:
                    heapq.heappush(burrows_to_visit, (start.get_amphis_not_in_place()*100000+cost_next,
                                                      burrow_next.__hash__(), burrow_next))
                    if burrow_next.is_final_position():
                        print(f'success: {burrow_next}')
                    printcounter += 1
                    if printcounter > 50000:
                        print(len(burrows_to_visit))
                        printcounter = 0

    final_paths = [burrow for burrow, tup in shortest_paths.items() if burrow.is_final_position()]
    print(min([path.total_cost for path in final_paths]))

