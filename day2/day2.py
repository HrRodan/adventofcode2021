import pandas as pd

commands=pd.read_csv('commands.txt',sep=' ',names=['command','value'])
commands_sum=commands.groupby('command').sum()
depth_final=commands_sum.loc['down','value']-commands_sum.loc['up','value']
horizontal_final=commands_sum.loc['forward','value']
result=depth_final*horizontal_final

#part 2
aim = 0
horizontal = 0
depth = 0
for _, row in commands.iterrows():
    command_line=row['command']
    value_line=row['value']
    if command_line == 'down':
        aim+=value_line
    elif command_line == 'forward':
        horizontal+=value_line
        depth+=aim*value_line
    elif command_line == 'up':
        aim -= value_line

result2=horizontal*depth
print(result2)