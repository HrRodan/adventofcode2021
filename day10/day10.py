from collections import Counter

import numpy as np

# file = '''
# [({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]'''
#
# log = [line.strip() for line in file.split('\n') if line.strip()]

with open('log.txt', 'r') as file:
    log = [line.strip() for line in file if line.strip()]

b_open = '([{<'
b_close = ')]}>'
points = {')': 3, ']': 57, '}': 1197, '>': 25137}

close_open = dict(zip(b_close, b_open))
open_close = dict(zip(b_open, b_close))

count = Counter({key: 0 for key in b_close})
log_clean = log.copy()

for line in log:
    open_brackets = []
    for char in line:
        if char in b_open:
            open_brackets.append(char)
        if char in b_close:
            if open_brackets and close_open[char] == open_brackets[-1]:
                open_brackets.pop(-1)
            else:
                count[char] += 1
                log_clean.remove(line)
                break

error_score = sum(count * points[key] for key, count in count.items())

open_brackets_list = []
# part 2
points_close = {')': 1, ']': 2, '}': 3, '>': 4}

for line in log_clean:
    open_brackets = []
    for char in line:
        if char in b_open:
            open_brackets.append(char)
        if char in b_close and close_open[char] == open_brackets[-1]:
            open_brackets.pop(-1)
    open_brackets_list.append(open_brackets)

close_brackets = [[open_close[element] for element in line[::-1]] for line in open_brackets_list]

points_list = []
for line in close_brackets:
    points = 0
    for char in line:
        points *= 5
        points += points_close[char]
    points_list.append(points)

print(np.median(points_list))
