import numpy as np
from matplotlib import pyplot as plt

with open('input.txt', 'r') as file:
    input_ = file.read()


# input_ = '''6,10
# 0,14
# 9,10
# 0,3
# 10,4
# 4,11
# 6,0
# 6,12
# 4,1
# 0,13
# 10,12
# 3,4
# 3,0
# 8,4
# 1,10
# 2,14
# 8,10
# 9,0
#
# fold along y=7
# fold along x=5'''


def fold_to_tuple(input: str):
    ax, line = input[11:].split('=')
    ax_int = 0 if ax == 'y' else 1
    return (ax_int, int(line))


dots_in, fold_in = input_.split('\n\n')
dots = [(int(y), int(x)) for line in dots_in.split('\n') if line.strip() for x, y in [line.split(',')]]
folds = [fold_to_tuple(line) for line in fold_in.split('\n') if line.strip()]

# convert to numpy array
array = np.full(np.max(dots, axis=0) + 1, False)
#array[tuple([*np.transpose(dots)])]=1
for dot in dots:
    array[dot] = True

for ax, ix in folds:
    if ax == 0:
        fold = array[:ix]
        new_fold = array[ix + 1:]
    else:
        fold = array[:, :ix]
        new_fold = array[:, ix + 1:]
    new_fold = np.flip(new_fold, axis=ax)
    array = new_fold | fold

plt.imshow(array, interpolation='nearest')
plt.show()
