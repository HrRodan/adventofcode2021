import heapq
from collections import defaultdict
from itertools import chain
from typing import Tuple, Dict, Set, List

import numpy as np

addon = '''  #A#B#C#D#  
  #A#B#C#D#  '''

final_position = '''#############
#...........#
###A#B#C#D###
  #A#B#C#D#  
  #A#B#C#D#  
  #A#B#C#D#  
  #########  '''

translate = {ord('#'): '8', ord('.'): '0', ord('A'): '1', ord('B'): '2', ord('C'): '3', ord('D'): '4', ord(' '): '8'}
final_position = final_position.translate(translate)

burrow_final = np.array([[c for c in list(line)] for line in final_position.split('\n')]).astype(np.ubyte)

hallway = {tuple(h) for h in np.transpose((burrow_final == 0).nonzero())}
rooms = {char: {tuple(h) for h in np.transpose((burrow_final == char).nonzero())} for char in [1, 2, 3, 4]}
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
    1: 1,
    2: 10,
    3: 100,
    4: 1000
}

all_types = [1, 2, 3, 4]


class Burrow_np():
    def __init__(self, array: np.ndarray):
        self.array: np.ndarray = array
        self.hash = hash(tuple(self.array.flatten()))
        self.occupied = self.get_occupied()

    def __hash__(self):
        return self.hash

    def __eq__(self, other: 'Burrow_np'):
        return self.hash == other.hash

    def __lt__(self, other : 'Burrow_np'):
        return self.hash < other.hash

    def get_occupied(self) -> Set[Tuple[int, int]]:
        return {tuple(a) for a in np.transpose(np.nonzero(np.isin(self.array, all_types)))}

    def room_occupied(self) -> Dict[int, bool]:
        occupied_rooms = {value: False for value in all_types}
        for room_type in occupied_rooms:
            for a in self.occupied:
                if self.array[a] != room_type and a in rooms[room_type]:
                    occupied_rooms[room_type] = True
                    break

        return occupied_rooms

    def is_final_position(self) -> bool:
        return all(p in rooms[self.array[p]] for p in self.occupied)

    def get_possible_positions(self, postion: Tuple[int, int],room_occupied: bool) -> Dict[Tuple[int, int], int]:
        if postion in hallway and room_occupied:
            return {}
        excluded = self.occupied.copy()
        type_ = self.array[postion]
        rooms_of_type = rooms[type_]
        costs_of_type = costs[type_]
        visited = {}
        if postion in rooms_of_type and not room_occupied:
            excluded.update(hallway)
            excluded.update((all_rooms - rooms_of_type))

        def dfs(pos, path_costs):
            if pos not in visited:
                    visited[pos] = path_costs
                    path_costs += costs_of_type
                    for n in neighbors[pos]:
                        if n not in excluded:
                            dfs(n, path_costs)

        dfs(postion, 0)

        # remove all unvalid targets
        targets_to_remove = chain(entries, [postion], (all_rooms - rooms_of_type))
        if postion in hallway or (not room_occupied and postion in rooms_of_type):
            targets_to_remove = chain(targets_to_remove, hallway)
        if room_occupied:
            targets_to_remove = chain(targets_to_remove, rooms_of_type)
        targets_to_remove = set(targets_to_remove).intersection(visited)
        for key in targets_to_remove:
            visited.pop(key, None)

        return visited

    def get_possible_burrows(self) -> List[Tuple['Burrow_np', int]]:
        occupied_rooms = self.room_occupied()
        next_burrows = []
        for i, amphi_position in enumerate(self.occupied):
            type_ = self.array[amphi_position]
            for pos, costs_ in self.get_possible_positions(amphi_position, room_occupied=occupied_rooms[type_]).items():
                b_next_array = self.array.copy()
                b_next_array[pos] = b_next_array[amphi_position]
                b_next_array[amphi_position] = 0
                next_burrows.append((Burrow_np(b_next_array), costs_))

        return next_burrows

    def copy(self) -> 'Burrow_np':
        return Burrow_np(self.array.copy())


if __name__ == '__main__':
#     addon2 = '''  #D#C#B#A#
#   #D#B#A#C#  '''
#     my_input = '''#############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########  '''
    my_input='''#############
#...........#
###A#C#B#D###
  #D#C#B#A#  
  #D#B#A#C#  
  #B#A#D#C#  
  #########  '''
    my_input = my_input.translate(translate)
    start = Burrow_np(np.array([[c for c in list(line)]
                                for line in my_input.split('\n')]).astype(np.ubyte))
    final = Burrow_np(burrow_final)
    #final.get_possible_burrows()

    #start.get_possible_burrows()

    shortest_paths = {start: 0}
    visited: Set['Burrow_np'] = set()
    burrows_to_visit: List[Tuple[int, 'Burrow_np']] = []
    heapq.heappush(burrows_to_visit, (0, start))
    printcounter = 0
    # Dijkstra's algorithm
    while burrows_to_visit:
        cost_current, burrow_current = heapq.heappop(burrows_to_visit)
        visited.add(burrow_current)
        possible_next_burrows = burrow_current.get_possible_burrows()
        for burrow_next, cost_next_addon in possible_next_burrows:
            cost_next = cost_current + cost_next_addon
            if burrow_next not in shortest_paths or cost_next < shortest_paths[burrow_next]:
                shortest_paths[burrow_next] = cost_next
                if burrow_next not in visited:
                    heapq.heappush(burrows_to_visit, (cost_next, burrow_next))
                    printcounter += 1
                    if printcounter > 10000:
                        print(str(len(burrows_to_visit)) + ' # ' + str(len(shortest_paths)))
                        printcounter = 0

    final_paths = {p: tup for p, tup in shortest_paths.items() if p.is_final_position()}
    print(min([tup for _, tup in final_paths.items()]))
