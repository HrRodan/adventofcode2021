import numpy as np

with open('input.txt', 'r') as file:
    raw = np.array([[char for char in line.strip()] for line in file.readlines()])

shape = raw.shape
east = raw == '>'
south = raw == 'v'

for i in range(1000):
    east_old = east.copy()
    south_old = south.copy()
    #east
    #roll and select only if there is nothing already
    roll_possible = np.roll(east, 1, axis=1) & (~(east | south))
    #roll back to compare with input
    roll_back = np.roll(roll_possible, -1, axis=1)
    #calc new array form rolled back on possible rolls
    east = np.where(roll_back, False, roll_possible | east)
    #south
    roll_possible = np.roll(south, 1, axis=0) & (~(east | south))
    roll_back = np.roll(roll_possible, -1, axis=0)
    south = np.where(roll_back, False, roll_possible | south)

    if np.all(east == east_old) and np.all(south==south_old):
        print(i+1)
        break


def char_view():
    view = np.full(shape, fill_value='.')
    view[east]='>'
    view[south]='v'
    return view
