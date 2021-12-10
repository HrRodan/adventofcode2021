import numpy as np

# a='''
# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678'''
#
# ground = np.array([[int(value) for value in linestrip] for line in a.split('\n') if (linestrip := line.strip())])

# alternatives by scipy.ndimage measurement and generic filter

with open('input.txt', 'r') as file:
    ground = np.array([[int(value) for value in linestrip] for line in file if (linestrip := line.strip())])
# basicall 2nd derivative in each direction
h_2nd = np.diff(np.sign(np.diff(ground, axis=1, prepend=99, append=99)), axis=1)
v_2nd = np.diff(np.sign(np.diff(ground, axis=0, prepend=99, append=99)), axis=0)

mins = np.where((h_2nd == 2) & (v_2nd == 2), ground, np.nan)
print(f'Part1: {np.nansum(mins + 1)}')

# convert to binary
ground9 = np.where(ground == 9, 1, 0).astype(np.ubyte)

# transform to list of indices for easier looping
# only add non boarders to list
search_complete = np.transpose((ground9 == 0).nonzero())
# Use sets for easy tracking
search_complete_set = {(x, y) for x, y in search_complete}

bases = {}
searched_items = set()

#iterating version
for x, y in search_complete_set:
    if (x, y) not in searched_items:
        bases[(x, y)] = []
        local_search = {(x, y)}
        while local_search:
            x2, y2 = local_search.pop()
            searched_items.add((x2, y2))
            for x3, y3 in [(x2 - 1, y2), (x2 + 1, y2), (x2, y2 + 1), (x2, y2 - 1)]:
                if (x3, y3) in search_complete_set and (x3, y3) not in searched_items:
                    local_search.add((x3, y3))
            if (x2, y2) in search_complete_set:
                bases[(x, y)].append((x2, y2))

#recursion version
# def local_search(xy):
#     x2, y2 = xy
#     searched_items.add((x2, y2))
#     for x3, y3 in [(x2 - 1, y2), (x2 + 1, y2), (x2, y2 + 1), (x2, y2 - 1)]:
#         if (x3, y3) in search_complete_set and (x3, y3) not in searched_items:
#             local_search((x3, y3))
#     if xy in search_complete_set:
#         bases[(x, y)].append(xy)
#
#
# for x, y in search_complete_set:
#     if (x, y) not in searched_items:
#         bases[(x, y)] = []
#         local_search((x, y))

count_max = np.sort([len(value) for _, value in bases.items()])[-1:-4:-1]
print(f'Part2: {np.prod(count_max)}')

