import pandas as pd

depths = pd.read_csv('../day2/depths.txt', names=['depth'], usecols=[0], header=None)
d = depths.rolling(3).sum().diff()
sum = (d['depth'] > 0).sum()
