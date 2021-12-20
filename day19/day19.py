from itertools import product, permutations

import numpy as np
from scipy.spatial import distance

with open('input.txt', 'r') as file:
    scanner_raw = file.read().split('\n\n')

scanner = []
for s in scanner_raw:
    scanner.append(np.array([(int(x), int(y), int(z)) for i, line in enumerate(s.split('\n')) if i > 0
                             for x, y, z in [line.split(',')]]))

#48 possibilities -> should be 24
#axes = [(0, 1, 2), (2, 0, 1), (1, 2, 0)]
axes =list(permutations((0,1,2)))
switches = list((product([-1, 1], repeat=3)))
combinations = list(product(switches, axes))


def switch_columns(array: np.array, combination):
    signs, axs = combination
    array_new = np.copy(array)
    for ax_old, ax_new in enumerate(axs):
        if ax_old != ax_new:
            array_new[:, ax_old] = array[:, ax_new]
    for ax, sign in enumerate(signs):
        if sign == -1:
            array_new[:, ax] = -array_new[:, ax]
    return array_new


matches = []
matches_found=set()
def find_matches(scanner_test, ix):
    for i, s in enumerate(scanner):
        if ix != i and i not in matches_found:
            max_count_combination = 0
            scanner_location = None
            index = None
            scanner_final = None
            difference_final = None
            for c in combinations:
                scanner_new = switch_columns(s, c)
                #possible with scanner_test(:,None) - scanner_new(None,:)
                #a = distance.cdist(scanner_test, scanner_new)
                a = scanner_test[:,None] - scanner_new[None,:]
                values, counts = np.unique(np.vstack(a), return_counts=True, axis=0)
                count_max_values = counts.max()
                if count_max_values > max_count_combination:
                    max_count_combination = count_max_values
                    # find index of max values
                    #index = np.array(a == values[counts == count_max_values][0]).nonzero()
                    difference_final = values[counts==count_max_values]
                    scanner_final = scanner_new.copy()
            if max_count_combination > 11:
                matches_found.add(ix)
                scanner_location = difference_final
                result = {'scanner': (ix, i), 'scanner_location': scanner_location, 'counts_max': max_count_combination}
                matches.append(result)
                # replace matched rotation in original array
                scanner[i] = scanner_final + scanner_location
                #print(scanner_final + scanner_location)
                find_matches(scanner[i],i)




if __name__ == '__main__':
    find_matches(scanner[0],0)
    unique_count = np.unique(np.concatenate(scanner, axis=0), axis=0).shape[0]
    print(unique_count)

    scanner_locations = np.vstack([value for element in matches
                                  for key, value in element.items() if key == 'scanner_location'])

    scanner_locations_distances = distance.cdist(scanner_locations, scanner_locations, 'cityblock')
    print(scanner_locations_distances.max())