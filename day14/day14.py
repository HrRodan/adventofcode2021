from collections import Counter

STEPS = 10

#char_to_int = {key:value for value in range()}

with open('input.txt','r') as input:
    polymer, pairs_input = input.read().split('\n\n')
    pairs = {key: key[0] + value for line in pairs_input.split('\n')
             if line.strip()
             for key, value in [line.strip().split(' -> ')]}

pairs_get = pairs.get
last_char = polymer[-1]

for i in range(STEPS):
    polymer_pairs = (polymer[i:i+2] for i in range(len(polymer)-1))
    polymer = ''.join(pairs_get(pair, '') for pair in polymer_pairs) + last_char
    print(i)

count_chars = Counter(polymer).most_common()
print(count_chars[0][1]-count_chars[-1][1])