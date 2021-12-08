from itertools import zip_longest
from typing import List

import numpy as np


def list_minus(x, y) -> List:
    return [item for item in x if item not in y]


def list_plus(x, y) -> List:
    return list(set(x + y))


def is_subset(main_set, subset):
    return set(subset).issubset(main_set)


class Display():

    def __init__(self, unique_sequences: List[str], output: List[str]):
        self.unique_sequences = [sorted(a) for a in unique_sequences]
        self.output = [sorted(a) for a in output]
        self.pattern = {i: [] for i in range(10)}
        self.output_decimal = [np.nan for _ in self.output]
        self.generate_pattern()
        self.output_to_decimal()

    def generate_pattern(self):
        for seq in self.unique_sequences:
            length = len(seq)
            if length == 2:
                self.pattern[1] = seq
            elif length == 4:
                self.pattern[4] = seq
            elif length == 3:
                self.pattern[7] = seq
            elif length == 7:
                self.pattern[8] = seq
        # a=7-1
        a = list_minus(self.pattern[7], self.pattern[1])
        # eg=8-4-a
        eg = list_minus(list_minus(self.pattern[8], self.pattern[4]), a)

        for seq in self.unique_sequences:
            length = len(seq)
            if length == 5:
                if is_subset(seq, self.pattern[7]):
                    self.pattern[3] = seq
                elif is_subset(seq, eg):
                    self.pattern[2] = seq
                else:
                    self.pattern[5] = seq
            elif length == 6:
                if not is_subset(seq, self.pattern[1]):
                    self.pattern[6] = seq
                elif is_subset(seq, self.pattern[4]):
                    self.pattern[9] = seq
                else:
                    self.pattern[0] = seq

    def output_to_decimal(self):
        for i, digit in enumerate(self.output):
            for key, value in self.pattern.items():
                if all(a == b for a, b in zip_longest(sorted(digit), sorted(value), fillvalue='z')):
                    self.output_decimal[i] = key


with open('digits.txt', 'r') as file:
    displays = [Display(unique.strip().split(), output.strip().split())
                for unique, output in (line.split('|') for line in file)]

values = [int(''.join((str(integer) for integer in display.output_decimal))) for display in displays]
sum = np.sum(values)
print(sum)
