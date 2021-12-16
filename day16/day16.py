import re
from functools import partial
from itertools import islice, zip_longest

basetwo = partial(int, base=2)

translate_input = '''0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111'''

translate = {ord(key): value for line in translate_input.split('\n') for key, value in [line.split(' = ')]}

with open('input.txt') as file:
    input_ = file.read().strip()

#input_ = '9C0141080250320F1802104A08'

input_binary = input_.translate(translate)
input_binary_iter = iter(input_binary)

packet_functions = {
    0: 'np.sum',
    1: 'np.prod',
    2: 'np.min',
    3: 'np.max',
    4: '',
    5: 'np.greater',
    6: 'np.less',
    7: 'np.equal'
}


def next_as_decimal(iterator: iter, n):
    return basetwo(''.join(islice(iterator, n)))

#traverse the binary iter and build a list with decoded values
def get_packet(it: iter, number_packets=None):
    decoded = []
    count = 0
    while it:
        count += 1
        try:
            version = next_as_decimal(it, 3)
            type_id = next_as_decimal(it, 3)
        except ValueError:
            break
        decoded.append({'version': version, 'type_id': type_id})
        # literal value
        if type_id == 4:
            start_bit = '1'
            literal = []
            while start_bit == '1':
                start_bit = next(it)
                literal.extend(list(islice(it, 4)))
            decoded.append(basetwo(''.join(literal)))
        # operator
        else:
            try:
                length_type_id = next(it)
            except:
                decoded.pop()
                break
            if type_id in [5, 6, 7]:
                decoded.append('(')
            else:
                decoded.append('((')
            if length_type_id == '0':
                # error handling for trailing 0s
                try:
                    operator_length_bits = next_as_decimal(it, 15)
                except ValueError:
                    # remove last two elements
                    [decoded.pop() for _ in range(2)]
                    break
                if operator_length_bits == 0:
                    [decoded.pop() for _ in range(2)]
                    break
                decoded.append({'length_type_id': length_type_id, 'operator_length_bits': operator_length_bits})
                decoded.extend(get_packet(islice(it, operator_length_bits)))
            else:
                packet_number = next_as_decimal(it, 11)
                decoded.append({'length_type_id': length_type_id, 'packet_number': packet_number})
                decoded.extend(get_packet(it, number_packets=packet_number))
            if type_id in [5, 6, 7]:
                decoded.append(')')
            else:
                decoded.append('))')
        if number_packets and count >= number_packets:
            break
    return decoded


decoded = get_packet(input_binary_iter)

sum_version = sum(element.get('version', 0) for element in decoded if type(element) == dict)
print(f'Part 1: {sum_version}')

#build string array from decoded values
eval_string = []
for current, next_ in zip_longest(decoded, decoded[1:], fillvalue=None):
    current_type = type(current)
    next_type = type(next_)
    if current_type == int:
        eval_string.append(str(current))
        # add comma
        if next_ not in [')', '))']:
            eval_string.append(',')
    elif current_type == str:
        eval_string.append(current)
    elif current_type == dict and 'type_id' in current:
        eval_string.append(packet_functions[current['type_id']])

eval_string = ''.join(eval_string)
#fix some comma problems
eval_string = re.sub(r'\)(?!$|\))','),', eval_string )

print(f'Part 2: {eval(eval_string)}')

