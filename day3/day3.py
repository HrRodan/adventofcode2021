import pandas as pd

with open('bin.txt', 'r', newline='\n') as file:
    # Use generator
    log = ((int(letter) for letter in stripped) for line in file if (stripped := line.strip()))
    log_df = pd.DataFrame(log)


# log_mode=log_df.mode(axis=0).loc[0]
# epsilon = ''.join(log_mode.astype(str))
# theta = epsilon.translate(str.maketrans('10', '01'))
# result = int(epsilon, 2) * int(theta, 2)
# print(result)

def find_final_row(df: pd.DataFrame, find_least: bool):
    df_working_copy = log_df.copy()
    for c in df_working_copy.columns:
        bit = 1 if df_working_copy[c].mean() >= 0.5 else 0
        if find_least:
            bit = int(not bool(bit))
        df_working_copy = df_working_copy[df_working_copy[c] == bit]
        if len(df_working_copy) == 1:
            return ''.join(df_working_copy.iloc[0].astype(str))


oxygen = find_final_row(log_df, False)
co2 = find_final_row(log_df, True)
result = int(oxygen, 2) * int(co2, 2)
print(result)
