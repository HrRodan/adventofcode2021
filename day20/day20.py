import numpy as np
from scipy import ndimage

COUNT_OPT = 50

with open('input.txt', 'r') as file:
    decode, input_map = file.read().strip().split('\n\n')

decode = np.fromiter((True if char == '#' else False for char in decode.strip()), dtype=bool, count=len(decode.strip()))

input_array = np.array([[True if char == '#' else False for char in line]
                        for line in input_map.split('\n') if line.strip()]).astype(bool)


def decode_image(subarray: np.array):
    # astype of numpy had bad performance
    return decode[int(''.join('1' if bool_ else '0' for bool_ in subarray), 2)]


# initial pad of False value
output = np.pad(input_array, 1, mode='constant', constant_values=False)
for i in range(COUNT_OPT):
    # expand edge/nearest to account for possibility of decode[0]==True
    output = ndimage.generic_filter(np.pad(output, 1, mode='edge'), decode_image, size=(3, 3), mode='nearest')

print(np.count_nonzero(output))
