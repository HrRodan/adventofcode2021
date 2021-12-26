# by https://www.reddit.com/user/liviuc
# Generic math solution in Python 3. 200 ms runtime for both parts on my input. (just pass your input file via stdin)
#
# Each of the 14 sections in the input can be simplified down to a single step:
#
# z_next = (0 if (z % 26 + B) == w else 1) * ((z//A) * 25 + w + C) + (z//A)
#
# , where:
#
#     z is the input reg z value
#     w is the input reg w (i.e. the current digit)
#     A, B, C are the changing constants on relative lines 5, 6 and 16 of each section
#
# Fun fact: this leads to a very fast MONAD number evaluator function. The sad part is that we won't even use it once as part of the final solution:
#
# def is_monad(num):
#     z = 0
#     for i, w in enumerate(num):
#         A,B,C = const[i]
#         z = (0 if (z % 26 + B) == w else 1) * ((z//A) * 25 + w + C) + (z//A)
#     return z == 0
#
# Now, it turns out we can actually solve the equation for z. Solving a quotient equation can be tricky, because it produces multiple solutions. But it's possible. Because of the if condition, there are two forms of solutions (notice the multiple solutions):
#
# z_next * A + a, for a in [0, A-1]
# (z_next - w - C) / 26 * A + a, for a in [0, A-1]
#
# Now we have full power to reverse-solve the entire thing! Basically we start from a z value of 0 (desired final state), then generate all possible solutions, working our way up from digit 14 to digit 1, and storing all solutions and their z in a well-organized data structure.
#
# Finally, the best part: just casually walk the solutions data structure using "max digit solve" on each step from digit 1 to 14, an operation which will complete in O(14) steps and print out the P1 solution. Do the same for "min digit solves" and you will have P2.
#
# To end, one more fun fact! The only useful piece of data in today's input file are actually 42 numbers (14 * 3 constants). Everything else can be discarded.
#
# per /u/olive247: A is always 26 when B is negative, otherwise 1.


import sys
from collections import defaultdict

with open('input.txt', 'r') as file:
    input_=file.read()

l = [line.split() for line in input_.split('\n')]

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