# by https://www.reddit.com/user/liviuc

import sys
from collections import defaultdict

l = [line.split() for line in sys.stdin]

const = []
for i in range(14):
    off = i * 18
    A = int(l[4+off][2])
    B = int(l[5+off][2])
    C = int(l[15+off][2])
    const.append((A,B,C))

levels = {}
def build_deps(i, zl):
    A,B,C = const[i]

    sols = defaultdict(list)
    for w in range(9, 0, -1):
        for z in zl:
            for a in range(A):
                pz = z * A + a
                if pz % 26 + B == w:
                    if pz // A == z:
                        sols[pz].append((w, z))

                pz = round((z - w - C) / 26 * A + a)
                if pz % 26 + B != w:
                    if pz//A * 26 + w + C == z:
                        sols[pz].append((w, z))

    assert sols
    levels[i] = sols

    if i > 0:
        build_deps(i-1, list(sols.keys()))

def solve(i, z, sol, largest):
    if i == 14:
        return ''.join(str(j) for j in sol)

    for w, nz in sorted(levels[i][z], reverse=largest):
        ans = solve(i+1, nz, (*sol, w), largest)
        if ans:
            return ans

build_deps(13, [0])

print(solve(0, 0, (), largest=True))
print(solve(0, 0, (), largest=False))