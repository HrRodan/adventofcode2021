import numpy as np

with open('game.txt', 'r', newline='\n') as file:
    data = file.read().split('\n\n')

boards = []
numbers = -1
for i, element in enumerate(data):
    if i == 0:
        numbers = [int(e) for e in element.strip().split(',')]
    else:
        boards.append(np.array([[int(y) for y in x.split()] for x in element.strip().split('\n') if element.strip()]))

def find_winning_board(boards, game_numbers):
    boards_game = [board.copy() for board in boards]
    for value in game_numbers:
        for i, board in enumerate(boards_game):
            board[board == value] = 100
            for ax in range(2):
                if 500 in board.sum(axis=ax):
                    final_board = boards_game[i]
                    final_number = value
                    return (final_board, final_number)

def find_loosing_board(boards, game_numbers):
    boards_game = [board.copy() for board in boards]
    boards_never_won_index = list(range(len(boards_game)-1))
    for value in game_numbers:
        for i, board in enumerate(boards_game):
            board[board == value] = 100
            for ax in range(2):
                if 500 in board.sum(axis=ax):
                    if i in boards_never_won_index:
                        boards_never_won_index.remove(i)
                    if not boards_never_won_index:
                        final_board = board
                        final_number = value
                        return (final_board, final_number)

final_board, final_number = find_winning_board(boards, numbers)

# print(final_board)
# print(final_number)
# result=final_board[final_board!=100].sum()*final_number
# print(result)

final_board_lost, final_number_lost = find_loosing_board(boards, numbers)

print(final_board_lost)
print(final_number_lost)
result_lost=final_board_lost[final_board_lost!=100].sum()*final_number_lost
print(result_lost)
