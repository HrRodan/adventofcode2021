from collections import defaultdict
from typing import Dict, List
import pandas as pd
import networkx as nx
from pyvis.network import Network
import random
import matplotlib.pyplot as plt
import numpy as np

w = x = y = z = 0

def inp(a: str):
    exec(f'{a}=next(model_number_iter)', globals())


def add(a: str, b: str):
    exec(f'{a}={a}+int({b})', globals())


def mul(a: str, b: str):
    exec(f'{a}={a}*int({b})', globals())


def div(a: str, b: str):
    exec(f'{a}=int({a}/int({b}))', globals())


def mod(a: str, b: str):
    exec(f'{a}={a}%int({b})', globals())


def eql(a: str, b: str):
    exec(f'{a}=1 if {a}==int({b}) else 0', globals())

def checkInt(str):
    if str[0] in ('-', '+'):
        return str[1:].isdigit()
    return str.isdigit()

if __name__ == '__main__':

    with open('input.txt', 'r') as file:
        raw = file.read()

    cmds = [f'{func}(' + ','.join([f'\'{arg}\'' for arg in args]) + ')'
            for line in raw.split('\n')
            for func, *args in [line.split(' ')]]

    def run_NOMAD():
        for cmd in cmds:
            eval(cmd)

    # generate network
    network = []
    counters: Dict[str, int] = {char: 0 for char in ['w', 'x', 'y', 'z', 'in']}
    for line in raw.split('\n'):
        func, *args = line.split(' ')
        args_str = ','.join([f'\'{arg}\'' for arg in args])
        cmd = f'{func}({args_str})'
        if func == 'inp':
            counters['in'] += 1
            counters[args[0]] += 1
            network.append(['input_' + str(counters['in']), args[0] + '_' + str(counters[args[0]]), cmd])
        else:
            if len(args)>1 and not checkInt(args[1]):
                network.append([args[1] + '_' + str(counters[args[1]]), args[0] + '_' + str(counters[args[0]] + 1), cmd])
            network.append([args[0] + '_' + str(counters[args[0]]), args[0] + '_' + str(counters[args[0]] + 1), cmd])
            counters[args[0]] += 1

    network_df = pd.DataFrame(network, columns=['source','target','label'])
    last_z = network_df['target'][network_df['target'].str.startswith('z')].iloc[-1]

    network_nx = nx.from_pandas_edgelist(network_df, source='source', target='target', edge_attr='label')
    parent_edges = list(nx.edge_dfs(network_nx,'z_41', orientation='reverse'))
    relevant_inputs = [target for _, target, _ in parent_edges if target.startswith('input')]
    network_nx.nodes[last_z]['color']='red'

    output = defaultdict(list)
    for i in range(50000):
        w = x = y = z = 0
        model_number = [random.choice(range(1,10)) for _ in range(14)]
        model_number_str = ''.join(str(value) for value in model_number)
        model_number_iter = iter(model_number)
        run_NOMAD()
        output[int(model_number_str)] = z


    # net = Network(height='750px', width='100%')
    #
    # net.from_nx(network_nx)
    # net.show_buttons()
    #
    # net.show('example.html')