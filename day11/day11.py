import numpy as np
from scipy import ndimage

file = '''
3265255276
1537412665
7335746422
6426325658
3854434364
8717377486
4522286326
6337772845
8824387665
6351586484'''

octo = np.array([[int(char) for char in line.strip()] for line in file.split('\n') if line.strip()]).astype(np.ubyte)

STEPS = 100

count_flashes = 0
for i in range(1, 2000):
    octo = octo + 1
    oct_to_flash = octo > 9
    while np.any(oct_to_flash):
        count_flashes += np.sum(oct_to_flash)
        # get all neigbhors and count
        neighbours = ndimage.generic_filter(oct_to_flash.astype(np.ubyte), np.count_nonzero, size=(3,3),
                                            mode='constant', cval=0)
        # add + 1 to all neighbours
        octo = octo + neighbours
        # remove already flashed from further processing
        octo = np.where(oct_to_flash, np.nan, octo)
        oct_to_flash = octo > 9
    octo[np.isnan(octo)] = 0
    if np.all(octo == 0):
        print(i)
        break
