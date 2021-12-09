import numpy as np

# a='''
# 2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678'''
#
# ground = np.array([[int(value) for value in linestrip] for line in a.split('\n') if (linestrip := line.strip())])

with open('input.txt', 'r') as file:
    ground = np.array([[int(value) for value in linestrip] for line in file if (linestrip := line.strip())])

h_2nd = np.diff(np.sign(np.diff(ground, axis=1, prepend=99, append=99)), axis=1)
v_2nd = np.diff(np.sign(np.diff(ground, axis=0, prepend=99, append=99)), axis=0)

mins = np.where((h_2nd == 2) & (v_2nd == 2), ground, np.nan)
sum = np.nansum(mins + 1)
# print(sum)

ground9 = np.where(ground == 9, 1, 0).astype(np.ubyte)
ground9 = np.pad(ground9, (1, 1), 'constant', constant_values=(1, 1))

search_complete = np.transpose((ground9 == 0).nonzero())
search_complete_set = {(x, y) for x, y in search_complete}

bases = {}
searched_items = set()
for x, y in search_complete_set:
    if (x, y) not in searched_items:
        bases[(x, y)] = []
        local_search = {(x, y)}
        while local_search:
            x2, y2 = local_search.pop()
            searched_items.add((x2, y2))
            for i in [-1, 1]:
                if (x2 + i, y2) in search_complete_set and (x2 + i, y2) not in searched_items:
                    local_search.add((x2 + i, y2))
                if (x2, y2 + i) in search_complete_set and (x2, y2 + i) not in searched_items:
                    local_search.add((x2, y2 + i))
            if (x2, y2) in search_complete_set:
                bases[(x, y)].append((x2, y2))

count = np.array([len(value) for _, value in bases.items()])
count_max = np.sort(count)[-1:-4:-1]
print(np.prod(count_max))
