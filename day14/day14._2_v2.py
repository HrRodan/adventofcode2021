from collections import defaultdict

# %%

STEPS = 40

# char_to_int = {key:value for value in range()}

with open('input_test.txt', 'r') as input_:
    polymer, pairs_input = input_.read().split('\n\n')
    pairs = {key: [key[0] + value, value + key[1]] for line in pairs_input.split('\n')
             if line.strip()
             for key, value in [line.strip().split(' -> ')]}

#collect possible pairs
start_pairs = {polymer[i:i + 2] for i in range(len(polymer) - 1)}

pairs_count=defaultdict(lambda:0)
pairs_count.update({key: polymer.count(key) for key in sorted(start_pairs)})

# %%

for _ in range(STEPS):
    pairs_count_next = pairs_count.copy()
    for key, value in pairs.items():
        key_count = pairs_count[key]
        if key_count != 0:
            pairs_count_next[key] -= key_count
            for target in value:
                pairs_count_next[target] += key_count
    pairs_count = pairs_count_next

#count only first char of pair
count_char = defaultdict(lambda :0)
for key, value in pairs_count.items():
    count_char[key[0]]+=value

# add one to last count because the last one is missing in the count
count_char[polymer[-1]] += 1

print(max(count_char.values())-min(count_char.values()))
