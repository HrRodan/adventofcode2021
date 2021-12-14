from collections import Counter
import numpy as np
from itertools import chain

STEPS = 40

with open('input_test.txt','r') as input:
    polymer, pairs_input = input.read().split('\n\n')
    pairs = {(ord(key[0]),ord(key[1])): np.array([ord(key[0]), ord(value)]).astype(np.ubyte)
             for line in pairs_input.split('\n')
             if line.strip()
             for key, value in [line.strip().split(' -> ')]}

polymer_int = np.array([ord(char) for char in polymer]).astype(np.ubyte)
pairs_get = pairs.get
last_int = np.array(polymer_int[-1])

for i in range(STEPS):
    polymer_pairs = (tuple(polymer_int[i:i+2]) for i in range(len(polymer_int)-1))
    #iter_chain = chain(polymer_pairs,last_int)
    polymer_int = np.hstack((pairs_get(pair, pair[0]) for pair in polymer_pairs))
    polymer_int = np.hstack((polymer_int,last_int))
    print(i)

count_chars = Counter(polymer_int).most_common()
print(count_chars[0][1]-count_chars[-1][1])