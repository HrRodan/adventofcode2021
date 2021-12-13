input = '''kc-qy
qy-FN
kc-ZP
end-FN
li-ZP
yc-start
end-qy
yc-ZP
wx-ZP
qy-li
yc-li
yc-wx
kc-FN
FN-li
li-wx
kc-wx
ZP-start
li-kc
qy-nv
ZP-qy
nv-xr
wx-start
end-nv
kc-nv
nv-XQ'''

combinations = [tuple(line.split('-')) for line in input.split('\n') if line.strip()]

all_caverns = {cavern for c in combinations for cavern in c}
start_end = {'start', 'end'}
small_caverns = {cavern for cavern in all_caverns if cavern.islower()} - start_end
big_caverns = all_caverns - small_caverns - start_end

count_small_base = {key: 0 for key in small_caverns}

cavern_combinations = {key: set() for key in all_caverns}

for a, b in combinations:
    if b != 'start':
        cavern_combinations[a].add(b)
    if a != 'start':
        cavern_combinations[b].add(a)

paths = [['start']]


def small_cave_visited_twice(path_in):
    count_small = count_small_base.copy()
    for cavern in path_in:
        if cavern in small_caverns:
            count_small[cavern] += 1
            if count_small[cavern] > 1:
                return True

    return False

#bfs search
for i in range(300):
    new_paths = []
    for path in paths:
        path_end = path[-1]
        if path_end != 'end':
            visited_twice = small_cave_visited_twice(path)
            path_set = set(path)
            path_next = [path + [following] for following in cavern_combinations[path_end]
                         if (following in big_caverns or following == 'end' or
                             (following in small_caverns and (following not in path_set
                                                              or not visited_twice)))]
            new_paths.extend(path_next)
    paths = [path for path in paths if path[-1] == 'end'] + new_paths
    print(i)
    if all(path[-1] == 'end' for path in paths):
        break

#Alternative use recursion for depth first search
#     from collections import defaultdict
#
# maps = [line.strip('\n').split('-') for line in open('input_.txt')]
# graph = defaultdict(set)
# for a,b in maps:
#     graph[a].add(b)
#     graph[b].add(a)
#
# def traverse(path=['start']):
#     if path[-1] == 'end': return 1
#     newnodes = [node for node in graph[path[-1]] if node not in path or node.upper()==node]
#     if len(newnodes)==0: return 0
#     return sum([traverse(path=path+[node]) for node in newnodes])
#
# print(traverse())
