import numba as nb
import numpy as np

# %%
with open('day6.txt', 'r') as file:
    fish_start = np.array([int(x) for x in file.readline().strip().split(',')], dtype=np.ubyte)

DAYS = 256


# for day in range(DAYS):
#     new_fish = fish == 0
#     fish = np.concatenate((np.where(new_fish, 6, fish - 1),
#                            np.full((sum(new_fish),), fill_value=8, dtype=np.ubyte)),
#                           dtype=np.ubyte)
#
#     print(f'Day: {day + 1} - {len(fish)}')

# %%
@nb.jit(cache=True, fastmath=True)
def grow_fish(fish: np.ndarray, days: int):
    for day in range(days):
        new_fish = fish == 0
        fish = np.hstack((np.where(new_fish, 6, fish - 1).astype(np.ubyte),
                          np.full((new_fish.sum(),), fill_value=8, dtype=np.ubyte)))
        print(str(day + 1) + ' - ' + str(len(fish)))


@nb.jit(cache=True, fastmath=True)
def grow_fish_by_hist(bin: np.array, days: int):
    for day in range(days):
        bin = np.roll(bin, -1)
        bin[6] += bin[8]
        print(str(day + 1) + ' - ' + str(np.sum(bin)))


grow_fish_by_hist(np.bincount(fish_start,minlength=9),DAYS)
