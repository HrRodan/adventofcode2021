import numpy as np

with open('crabs.txt', 'r') as file:
    crabs: np.array = np.fromiter((int(crab) for crab in file.readline().strip().split(',')), dtype=np.int32)


def fuel(x0: int, x: np.array):
    absolute = np.abs(x - x0)
    return (absolute * (absolute + 1) / 2).sum()


crabs_max_position = crabs.max() + 1

fuel_consumption = np.fromiter((fuel(x0, crabs) for x0 in range(crabs_max_position)),
                               dtype=np.int32, count=crabs_max_position).min()
