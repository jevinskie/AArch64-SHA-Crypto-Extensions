#!/usr/bin/env python3


import networkx as nx
from rich import print

batches = [
    ["sha1h_0", "shuf_0", "shuf_1", "shuf_2", "shuf_3"],
    ["add_0", "add_1", "add_2", "add_3", "sha1su0_0", "sha1su0_1"],
    ["sha1c_0", "sha1su1_0"],
    ["add_4", "sha1c_1", "sha1h_1", "sha1su0_2", "sha1su1_1"],
    ["add_5", "sha1c_2", "sha1h_2", "sha1su0_3", "sha1su1_2"],
    ["add_6", "sha1c_3", "sha1h_3", "sha1su0_4", "sha1su1_3"],
    ["add_7", "sha1c_4", "sha1h_4", "sha1su0_5", "sha1su1_4"],
    ["add_8", "sha1h_5", "sha1p_0", "sha1su0_6", "sha1su1_5"],
    ["add_9", "sha1h_6", "sha1p_1", "sha1su0_7", "sha1su1_6"],
    ["add_10", "sha1h_7", "sha1p_2", "sha1su0_8", "sha1su1_7"],
    ["add_11", "sha1h_8", "sha1p_3", "sha1su0_9", "sha1su1_8"],
    ["add_12", "sha1h_9", "sha1p_4", "sha1su0_10", "sha1su1_9"],
    ["add_13", "sha1h_10", "sha1m_0", "sha1su0_11", "sha1su1_10"],
    ["add_14", "sha1h_11", "sha1m_1", "sha1su0_12", "sha1su1_11"],
    ["add_15", "sha1h_12", "sha1m_2", "sha1su0_13", "sha1su1_12"],
    ["add_16", "sha1h_13", "sha1m_3", "sha1su0_14", "sha1su1_13"],
    ["add_17", "sha1h_14", "sha1m_4", "sha1su0_15", "sha1su1_14"],
    ["add_18", "sha1h_15", "sha1p_5", "sha1su1_15"],
    ["add_19", "sha1h_16", "sha1p_6"],
    ["sha1h_17", "sha1p_7"],
    ["sha1h_18", "sha1p_8"],
    ["sha1h_19", "sha1p_9"],
    ["add_20", "add_21"],
]

batch_sizes = [len(b) for b in batches]
# print(f"batch_sizes: {batch_sizes}")
# num_schedules = functools.reduce(operator.mul, [math.factorial(len(b)) for b in batches], 1)
# print(f"num_schedules: {num_schedules}")

batches_norm = [
    ["sha1h", "shuf", "shuf", "shuf", "shuf"],
    ["add", "add", "add", "add", "sha1su0", "sha1su0"],
    ["sha1c", "sha1su1"],
    ["add", "sha1c", "sha1h", "sha1su0", "sha1su1"],
    ["add", "sha1c", "sha1h", "sha1su0", "sha1su1"],
    ["add", "sha1c", "sha1h", "sha1su0", "sha1su1"],
    ["add", "sha1c", "sha1h", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1p", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1p", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1p", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1p", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1p", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1m", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1m", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1m", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1m", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1m", "sha1su0", "sha1su1"],
    ["add", "sha1h", "sha1p", "sha1su1"],
    ["add", "sha1h", "sha1p"],
    ["sha1h", "sha1p"],
    ["sha1h", "sha1p"],
    ["sha1h", "sha1p"],
    ["add", "add"],
]

batch_sizes = [len(b) for b in batches_norm]
# print(f"batch_sizes: {batch_sizes}")
# num_schedules = functools.reduce(operator.mul, [math.factorial(len(b)) for b in batches_norm], 1)
# print(f"num_schedules: {num_schedules}")

g_dod = {
    "blocks": {
        "shuf_0": {"opnum": 0},
        "shuf_1": {"opnum": 0},
        "shuf_2": {"opnum": 0},
        "shuf_3": {"opnum": 0},
    },
    "shuf_0": {"add_0": {"opnum": 0}, "sha1su0_0": {"opnum": 0}},
    "ByteRevLUT": {
        "shuf_0": {"opnum": 1},
        "shuf_1": {"opnum": 1},
        "shuf_2": {"opnum": 1},
        "shuf_3": {"opnum": 1},
    },
    "shuf_1": {"add_1": {"opnum": 0}, "sha1su0_0": {"opnum": 1}, "sha1su0_1": {"opnum": 0}},
    "shuf_2": {
        "add_2": {"opnum": 0},
        "sha1su0_0": {"opnum": 2},
        "sha1su0_1": {"opnum": 1},
        "sha1su0_2": {"opnum": 0},
    },
    "shuf_3": {
        "add_3": {"opnum": 0},
        "sha1su1_0": {"opnum": 1},
        "sha1su0_1": {"opnum": 2},
        "sha1su0_2": {"opnum": 1},
        "sha1su0_3": {"opnum": 0},
    },
    "add_0": {"sha1c_0": {"opnum": 2}},
    "K0": {
        "add_0": {"opnum": 1},
        "add_1": {"opnum": 1},
        "add_2": {"opnum": 1},
        "add_3": {"opnum": 1},
        "add_4": {"opnum": 1},
    },
    "add_1": {"sha1c_1": {"opnum": 2}},
    "buf": {"sha1h_0": {"opnum": 0}, "sha1c_0": {"opnum": 0}, "add_20": {"opnum": 1}},
    "sha1h_0": {"sha1c_1": {"opnum": 1}},
    "sha1c_0": {"sha1h_1": {"opnum": 0}, "sha1c_1": {"opnum": 0}},
    "sz": {"sha1c_0": {"opnum": 1}, "add_21": {"opnum": 1}},
    "add_2": {"sha1c_2": {"opnum": 2}},
    "sha1su0_0": {"sha1su1_0": {"opnum": 0}},
    "sha1h_1": {"sha1c_2": {"opnum": 1}},
    "sha1c_1": {"sha1h_2": {"opnum": 0}, "sha1c_2": {"opnum": 0}},
    "add_3": {"sha1c_3": {"opnum": 2}},
    "sha1su1_0": {
        "add_4": {"opnum": 0},
        "sha1su1_1": {"opnum": 1},
        "sha1su0_2": {"opnum": 2},
        "sha1su0_3": {"opnum": 1},
        "sha1su0_4": {"opnum": 0},
    },
    "sha1su0_1": {"sha1su1_1": {"opnum": 0}},
    "sha1h_2": {"sha1c_3": {"opnum": 1}},
    "sha1c_2": {"sha1h_3": {"opnum": 0}, "sha1c_3": {"opnum": 0}},
    "add_4": {"sha1c_4": {"opnum": 2}},
    "sha1su1_1": {
        "add_5": {"opnum": 0},
        "sha1su1_2": {"opnum": 1},
        "sha1su0_3": {"opnum": 2},
        "sha1su0_4": {"opnum": 1},
        "sha1su0_5": {"opnum": 0},
    },
    "sha1su0_2": {"sha1su1_2": {"opnum": 0}},
    "sha1h_3": {"sha1c_4": {"opnum": 1}},
    "sha1c_3": {"sha1h_4": {"opnum": 0}, "sha1c_4": {"opnum": 0}},
    "add_5": {"sha1p_0": {"opnum": 2}},
    "K1": {
        "add_5": {"opnum": 1},
        "add_6": {"opnum": 1},
        "add_7": {"opnum": 1},
        "add_8": {"opnum": 1},
        "add_9": {"opnum": 1},
    },
    "sha1su1_2": {
        "add_6": {"opnum": 0},
        "sha1su1_3": {"opnum": 1},
        "sha1su0_4": {"opnum": 2},
        "sha1su0_5": {"opnum": 1},
        "sha1su0_6": {"opnum": 0},
    },
    "sha1su0_3": {"sha1su1_3": {"opnum": 0}},
    "sha1h_4": {"sha1p_0": {"opnum": 1}},
    "sha1c_4": {"sha1h_5": {"opnum": 0}, "sha1p_0": {"opnum": 0}},
    "add_6": {"sha1p_1": {"opnum": 2}},
    "sha1su1_3": {
        "add_7": {"opnum": 0},
        "sha1su1_4": {"opnum": 1},
        "sha1su0_5": {"opnum": 2},
        "sha1su0_6": {"opnum": 1},
        "sha1su0_7": {"opnum": 0},
    },
    "sha1su0_4": {"sha1su1_4": {"opnum": 0}},
    "sha1h_5": {"sha1p_1": {"opnum": 1}},
    "sha1p_0": {"sha1h_6": {"opnum": 0}, "sha1p_1": {"opnum": 0}},
    "add_7": {"sha1p_2": {"opnum": 2}},
    "sha1su1_4": {
        "add_8": {"opnum": 0},
        "sha1su1_5": {"opnum": 1},
        "sha1su0_6": {"opnum": 2},
        "sha1su0_7": {"opnum": 1},
        "sha1su0_8": {"opnum": 0},
    },
    "sha1su0_5": {"sha1su1_5": {"opnum": 0}},
    "sha1h_6": {"sha1p_2": {"opnum": 1}},
    "sha1p_1": {"sha1h_7": {"opnum": 0}, "sha1p_2": {"opnum": 0}},
    "add_8": {"sha1p_3": {"opnum": 2}},
    "sha1su1_5": {
        "add_9": {"opnum": 0},
        "sha1su1_6": {"opnum": 1},
        "sha1su0_7": {"opnum": 2},
        "sha1su0_8": {"opnum": 1},
        "sha1su0_9": {"opnum": 0},
    },
    "sha1su0_6": {"sha1su1_6": {"opnum": 0}},
    "sha1h_7": {"sha1p_3": {"opnum": 1}},
    "sha1p_2": {"sha1h_8": {"opnum": 0}, "sha1p_3": {"opnum": 0}},
    "add_9": {"sha1p_4": {"opnum": 2}},
    "sha1su1_6": {
        "add_10": {"opnum": 0},
        "sha1su1_7": {"opnum": 1},
        "sha1su0_8": {"opnum": 2},
        "sha1su0_9": {"opnum": 1},
        "sha1su0_10": {"opnum": 0},
    },
    "sha1su0_7": {"sha1su1_7": {"opnum": 0}},
    "sha1h_8": {"sha1p_4": {"opnum": 1}},
    "sha1p_3": {"sha1h_9": {"opnum": 0}, "sha1p_4": {"opnum": 0}},
    "add_10": {"sha1m_0": {"opnum": 2}},
    "K2": {
        "add_10": {"opnum": 1},
        "add_11": {"opnum": 1},
        "add_12": {"opnum": 1},
        "add_13": {"opnum": 1},
        "add_14": {"opnum": 1},
    },
    "sha1su1_7": {
        "add_11": {"opnum": 0},
        "sha1su1_8": {"opnum": 1},
        "sha1su0_9": {"opnum": 2},
        "sha1su0_10": {"opnum": 1},
        "sha1su0_11": {"opnum": 0},
    },
    "sha1su0_8": {"sha1su1_8": {"opnum": 0}},
    "sha1h_9": {"sha1m_0": {"opnum": 1}},
    "sha1p_4": {"sha1h_10": {"opnum": 0}, "sha1m_0": {"opnum": 0}},
    "add_11": {"sha1m_1": {"opnum": 2}},
    "sha1su1_8": {
        "add_12": {"opnum": 0},
        "sha1su1_9": {"opnum": 1},
        "sha1su0_10": {"opnum": 2},
        "sha1su0_11": {"opnum": 1},
        "sha1su0_12": {"opnum": 0},
    },
    "sha1su0_9": {"sha1su1_9": {"opnum": 0}},
    "sha1h_10": {"sha1m_1": {"opnum": 1}},
    "sha1m_0": {"sha1h_11": {"opnum": 0}, "sha1m_1": {"opnum": 0}},
    "add_12": {"sha1m_2": {"opnum": 2}},
    "sha1su1_9": {
        "add_13": {"opnum": 0},
        "sha1su1_10": {"opnum": 1},
        "sha1su0_11": {"opnum": 2},
        "sha1su0_12": {"opnum": 1},
        "sha1su0_13": {"opnum": 0},
    },
    "sha1su0_10": {"sha1su1_10": {"opnum": 0}},
    "sha1h_11": {"sha1m_2": {"opnum": 1}},
    "sha1m_1": {"sha1h_12": {"opnum": 0}, "sha1m_2": {"opnum": 0}},
    "add_13": {"sha1m_3": {"opnum": 2}},
    "sha1su1_10": {
        "add_14": {"opnum": 0},
        "sha1su1_11": {"opnum": 1},
        "sha1su0_12": {"opnum": 2},
        "sha1su0_13": {"opnum": 1},
        "sha1su0_14": {"opnum": 0},
    },
    "sha1su0_11": {"sha1su1_11": {"opnum": 0}},
    "sha1h_12": {"sha1m_3": {"opnum": 1}},
    "sha1m_2": {"sha1h_13": {"opnum": 0}, "sha1m_3": {"opnum": 0}},
    "add_14": {"sha1m_4": {"opnum": 2}},
    "sha1su1_11": {
        "add_15": {"opnum": 0},
        "sha1su1_12": {"opnum": 1},
        "sha1su0_13": {"opnum": 2},
        "sha1su0_14": {"opnum": 1},
        "sha1su0_15": {"opnum": 0},
    },
    "sha1su0_12": {"sha1su1_12": {"opnum": 0}},
    "sha1h_13": {"sha1m_4": {"opnum": 1}},
    "sha1m_3": {"sha1h_14": {"opnum": 0}, "sha1m_4": {"opnum": 0}},
    "add_15": {"sha1p_5": {"opnum": 2}},
    "K3": {
        "add_15": {"opnum": 1},
        "add_16": {"opnum": 1},
        "add_17": {"opnum": 1},
        "add_18": {"opnum": 1},
        "add_19": {"opnum": 1},
    },
    "sha1su1_12": {
        "add_16": {"opnum": 0},
        "sha1su1_13": {"opnum": 1},
        "sha1su0_14": {"opnum": 2},
        "sha1su0_15": {"opnum": 1},
    },
    "sha1su0_13": {"sha1su1_13": {"opnum": 0}},
    "sha1h_14": {"sha1p_5": {"opnum": 1}},
    "sha1m_4": {"sha1h_15": {"opnum": 0}, "sha1p_5": {"opnum": 0}},
    "add_16": {"sha1p_6": {"opnum": 2}},
    "sha1su1_13": {"add_17": {"opnum": 0}, "sha1su1_14": {"opnum": 1}, "sha1su0_15": {"opnum": 2}},
    "sha1su0_14": {"sha1su1_14": {"opnum": 0}},
    "sha1h_15": {"sha1p_6": {"opnum": 1}},
    "sha1p_5": {"sha1h_16": {"opnum": 0}, "sha1p_6": {"opnum": 0}},
    "add_17": {"sha1p_7": {"opnum": 2}},
    "sha1su1_14": {"add_18": {"opnum": 0}, "sha1su1_15": {"opnum": 1}},
    "sha1su0_15": {"sha1su1_15": {"opnum": 0}},
    "sha1h_16": {"sha1p_7": {"opnum": 1}},
    "sha1p_6": {"sha1h_17": {"opnum": 0}, "sha1p_7": {"opnum": 0}},
    "add_18": {"sha1p_8": {"opnum": 2}},
    "sha1su1_15": {"add_19": {"opnum": 0}},
    "sha1h_17": {"sha1p_8": {"opnum": 1}},
    "sha1p_7": {"sha1h_18": {"opnum": 0}, "sha1p_8": {"opnum": 0}},
    "add_19": {"sha1p_9": {"opnum": 2}},
    "sha1h_18": {"sha1p_9": {"opnum": 1}},
    "sha1p_8": {"sha1h_19": {"opnum": 0}, "sha1p_9": {"opnum": 0}},
    "sha1h_19": {"add_21": {"opnum": 0}},
    "sha1p_9": {"add_20": {"opnum": 0}},
    "add_20": {"insval_0": {"opnum": 0}},
    "add_21": {"inselm_0": {"opnum": 0}},
    "inselm_0": {"insval_1": {"opnum": 1}},
    "insval_0": {"insval_1": {"opnum": 0}},
    "insval_1": {"res": {"opnum": 0}},
    "res": {},
}

G = nx.DiGraph(g_dod)
print(f"G: {G}")
print(f"G.adjacency(): {list(G.adjacency())}")
print(f"G.predecessors('res'): {list(G.predecessors('res'))}")

for i in nx.edge_bfs(G):
    # inspect(i, all=True)
    print(f"i: {i} i.opnum: {G[i[1]]}")

print("done")
