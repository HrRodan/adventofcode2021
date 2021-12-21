from copy import copy
from typing import List, Union, Optional
import re
from itertools import cycle, islice, permutations, combinations, product
from collections import Counter


class Dice():
    @staticmethod
    def loop100():
        return cycle(range(1,101))


class Player():
    def __init__(self, number: int, start_position: int):
        self.position = start_position
        self.number = number
        self.score = 0
        self.probability_count = 0
        self.path_length = 0


class Game():
    board_size = 10
    win_score = 1000
    number_rolls = 3

    def __init__(self, players: List['Player'], dice: iter):
        self.players = players
        self.dice = dice
        self.dice_rolls = 0
        self.winner : Optional[Player] = None
        self.result : Optional[int] = None

    @classmethod
    def move_player(cls, player: Player, steps: int):
        mod = (player.position + steps) % cls.board_size
        position_final = mod if mod != 0 else cls.board_size
        player.position = position_final
        player.score += position_final

    def play(self):
        while True:
            for player in self.players:
                self.move_player(player, self.roll_dice_return_sum(3))
                if player.score >= self.win_score:
                    self.winner = player
                    self.eval_result()
                    return

    def roll_dice_return_sum(self, count: int):
        self.dice_rolls += count
        return sum(islice(self.dice, count))

    def eval_result(self):
        looser = None
        for player in self.players:
            if player.score<self.winner.score:
                looser = player
        self.result = looser.score*self.dice_rolls

if __name__ == '__main__':
    with open('input.txt', 'r') as file:
        players = [Player(int(number), int(start)) for line in file.readlines()
                   for number, start in [re.findall(r'\d', line)]]

    # game = Game(players, Dice.loop100())
    # game.play()
    # print(f'Part 1: {game.result}')

    # players_current = [copy(player) for player in players]
    # for player in players_current:
    #     for i in range(1,100):
    #         Game.move_player(player,6)
    #         if player.score >= 21:
    #             print(f'{player.number}: {i*3}')
    #             break

    combinations = {
        combination: sum(combination)
        for combination in product([1, 2, 3], repeat=3)
    }

    counter = Counter(combinations.values())

    player1 = copy(players[0])

    path=[]

    probability={}

    def roll_next(player : Player):
        for i in counter:
            if player.score>=21:
                print(f'{i} - {player.score}')
                path.append(i)
                return
            Game.move_player(player, i)
            roll_next(player)



