import heapq

import numpy as np

input_ = '''1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581'''
#
# cave = np.array([[char for char in line] for line in input_.split('\n')]).astype(np.ubyte)

with open('input.txt', 'r') as file:
    cave = np.array([[char for char in line.strip()] for line in file.readlines()]).astype(np.ubyte)

cave_current_part = cave
# expand array in 2 dimensions
for ax in range(2):
    for _ in range(4):
        cave_next_part = np.where(cave_current_part == 9, 1, cave_current_part + 1)
        cave = np.concatenate((cave, cave_next_part), axis=ax)
        cave_current_part = cave_next_part
    cave_current_part = cave

# %% Calc Edges

edges = {}
shape = cave.shape

next_list = np.array([(1, 0), (0, 1), (-1, 0), (0, -1)])
point_list = np.vstack(np.transpose(np.indices(shape)))

# for point in point_list:
#     close_points = (tuple(point_next)
#                     for delta in next_list
#                     if not np.any((point_next := point + delta) >= shape[0])
#                     and not np.any(point_next < 0))
#
#     edges[tuple(point)] = {close_point: cave[close_point] for close_point in close_points}

for point in point_list:
    x, y = point
    close_points = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
    # close_points = ((p_x, p_y)
    #                 for dx, dy in next_list
    #                 if 0 <= (p_x := point[0] + dx) < shape[0]
    #                 and 0 <= (p_y := point[1] + dy) < shape[1])

    edges[tuple(point)] = {point: cave[point] for point in close_points if -1 not in point
                           and shape[0] != point[0] and shape[1] != point[1]}

# %%

start = (0, 0)
end = (shape[0] - 1, shape[1] - 1)

shortest_paths = {start: (0, None)}
visited = set()
points_to_visit = []
heapq.heappush(points_to_visit, (0, start))

# Dijkstra's algorithm
while points_to_visit:
    risk_current, point_current = heapq.heappop(points_to_visit)
    visited.add(point_current)
    for point_next, risk_additional in edges[point_current].items():
        risk_next = risk_current + risk_additional
        if point_next not in shortest_paths or risk_next < shortest_paths[point_next][0]:
            shortest_paths[point_next] = (risk_next, point_current)
            if point_next not in visited:
                heapq.heappush(points_to_visit, (risk_next, point_next))

path = [end]
while path[-1] is not None:
    path.append(shortest_paths[path[-1]][1])

total_risk = shortest_paths[end][0]
