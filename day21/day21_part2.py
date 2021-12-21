from collections import Counter, defaultdict
from itertools import product

# get all combinations of 3 dice rolls and sum them
COMBINATIONS = {
    combination: sum(combination)
    for combination in product([1, 2, 3], repeat=3)
}

# Get Counter of all possible outcomes (sums) of three dice rolls
# Counter({3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1})
COUNTER = Counter(COMBINATIONS.values())


def move_player(position, score, steps):
    mod = (position + steps) % 10
    position_final = mod if mod != 0 else 10
    return position_final, score + position_final


def roll_next(position, score, length, p, length_dict):
    for roll_sum, count in COUNTER.items():
        if score >= 21:
            return
        new_position, new_score = move_player(position, score, roll_sum)
        new_length = length + 1
        p_new = p * count
        length_dict[(new_length, new_score)] += p_new
        roll_next(new_position, new_score, new_length, p_new, length_dict)


if __name__ == '__main__':
    # player_positions = [7,8]
    player_positions = [4, 8]
    # the length dicts contain all possibilities for a given (number of rolls, score)
    length_dicts = []
    for player_position in player_positions:
        d = defaultdict(lambda: 0)
        roll_next(player_position, 0, 0, 1, d)
        length_dicts.append(d)

    won = [0, 0]
    for (length1, score1), value1 in length_dicts[0].items():
        for (length2, score2), value2 in length_dicts[1].items():
            # Player1 plays first -> Player2 is one roll behind and must not have won (score>=21)
            if score1 >= 21 and length2 == length1 - 1 and score2 < 21:
                won[0] += value1 * value2
            # Player2 plays 2nd -> 1 and 2 must have same number of rolls, 1 must not have won
            if score2 >= 21 and length2 == length1 and score1 < 21:
                won[1] += value1 * value2

    print(max(won))
