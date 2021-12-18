import math
import re
from typing import Union


class SnailfishNumber():
    def __init__(self, number: str):
        self.number = number

    def __add__(self, other : Union[str, 'SnailfishNumber']):
        if not isinstance(other, SnailfishNumber):
            return SnailfishNumber(f'[{self.number},{other}]')
        return SnailfishNumber(f'[{self.number},{other.number}]')

    def __str__(self):
        return self.number

    def __repr__(self):
        return f'sailfish_number: {self}'

    def find_next_explosion(self):
        open_bracket_count = 0
        for ix, letter in enumerate(self.number):
            if letter == '[':
                open_bracket_count += 1
            elif letter == ']':
                open_bracket_count -= 1
            if open_bracket_count == 5:
                exploding_pair = re.search(r'\[\d+,\d+]', self.number[ix:]).group()
                return (ix, exploding_pair)
        return (None, None)

    @staticmethod
    def get_number_from_pair(pair: str):
        return tuple(int(x) for x in re.findall(r'\d+', pair))

    @staticmethod
    def split_number(match):
        number = int(match.group())
        if number > 9:
            number_by_two = int(number) / 2
            return f'[{math.floor(number_by_two)},{math.ceil(number_by_two)}]'
        return str(number)

    @staticmethod
    def magnitude_of_pair(match):
        x, y = re.findall(r'\d+', match.group())
        return str(int(x)*3+int(y)*2)

    def explode(self):
        ix, pair = self.find_next_explosion()
        if not pair:
            return False
        (prev, following) = self.get_number_from_pair(pair)
        # split string along explosion pair
        number_prev = self.number[:ix]
        number_following = self.number[ix + len(pair):]
        # replace last integer
        number_prev = re.sub(r'(.*\D)(\d+)',
                             lambda m: m.group(1) + str(int(m.group(2)) + prev), number_prev, count=1)
        # replace first integer
        number_following = re.sub(r'\d+',
                                  lambda m: str(int(m.group()) + following), number_following, count=1)
        new_number = number_prev + '0' + number_following
        changed = new_number != self.number
        self.number = new_number
        return changed

    def split(self):
        #find all digits with a starting 1
        new_number = re.sub(r'[1-9]\d+', self.split_number, self.number, count=1)
        changed = new_number != self.number
        self.number = new_number
        return changed

    def reduce(self):
        while self.explode() or self.split():
            pass

    def magnitude(self):
        new_number = self.number
        while True:
            new_number = re.sub(r'\[\d+,\d+]', self.magnitude_of_pair, new_number)
            #break if all chars are numbers
            if re.search(r'^\d+$', new_number):
                break
        return new_number


if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        numbers_to_add = file.read().strip().split()

    #Part 1
    s_number = SnailfishNumber(numbers_to_add[0])
    for number in numbers_to_add[1:]:
        s_number += number
        s_number.reduce()

    print(s_number.magnitude())

    #Part 2
    max_magnitude = 0
    for left in numbers_to_add:
        for right in numbers_to_add:
            a = SnailfishNumber(left)+right
            a.reduce()
            max_magnitude = max(max_magnitude, int(a.magnitude()))

    print(max_magnitude)