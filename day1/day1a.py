import numpy as np

with open('depths.txt',newline='\n') as file:
    depths = np.array(file.read().split('\n')).astype(int)

sum=np.sum(np.diff(depths)>0)


