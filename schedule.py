#!/usr/bin/env python3

import enum

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

g_dod_orig = {
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

g_dod = {
    "blocks": {
        "shuf_0": {"opnum": 0},
        "shuf_1": {"opnum": 0},
        "shuf_2": {"opnum": 0},
        "shuf_3": {"opnum": 0},
    },
    "shuf_0": {"addX_0": {"opnum": 0}, "sha1su0_0": {"opnum": 0}},
    "ByteRevLUT": {
        "shuf_0": {"opnum": 1},
        "shuf_1": {"opnum": 1},
        "shuf_2": {"opnum": 1},
        "shuf_3": {"opnum": 1},
    },
    "shuf_1": {"addY_1": {"opnum": 0}, "sha1su0_0": {"opnum": 1}, "sha1su0_1": {"opnum": 0}},
    "shuf_2": {
        "addX_2": {"opnum": 0},
        "sha1su0_0": {"opnum": 2},
        "sha1su0_1": {"opnum": 1},
        "sha1su0_2": {"opnum": 0},
    },
    "shuf_3": {
        "addY_3": {"opnum": 0},
        "sha1su1_0": {"opnum": 1},
        "sha1su0_1": {"opnum": 2},
        "sha1su0_2": {"opnum": 1},
        "sha1su0_3": {"opnum": 0},
    },
    "addX_0": {"sha1c_0": {"opnum": 2}, "addX_2": {"opnum": -1}},
    "K0": {
        "addX_0": {"opnum": 1},
        "addY_1": {"opnum": 1},
        "addX_2": {"opnum": 1},
        "addY_3": {"opnum": 1},
        "addX_4": {"opnum": 1},
    },
    "addY_1": {"sha1c_1": {"opnum": 2}, "addY_3": {"opnum": -1}},
    "buf": {"sha1h_0": {"opnum": 0}, "sha1c_0": {"opnum": 0}, "addX_20": {"opnum": 1}},
    "sha1h_0": {"sha1c_1": {"opnum": 1}},
    "sha1c_0": {"sha1h_1": {"opnum": 0}, "sha1c_1": {"opnum": 0}},
    "sz": {"sha1c_0": {"opnum": 1}, "addY_21": {"opnum": 1}},
    "addX_2": {"sha1c_2": {"opnum": 2}},
    "sha1su0_0": {"sha1su1_0": {"opnum": 0}},
    "sha1h_1": {"sha1c_2": {"opnum": 1}},
    "sha1c_1": {"sha1h_2": {"opnum": 0}, "sha1c_2": {"opnum": 0}},
    "addY_3": {"sha1c_3": {"opnum": 2}},
    "sha1su1_0": {
        "addX_4": {"opnum": 0},
        "sha1su1_1": {"opnum": 1},
        "sha1su0_2": {"opnum": 2},
        "sha1su0_3": {"opnum": 1},
        "sha1su0_4": {"opnum": 0},
    },
    "sha1su0_1": {"sha1su1_1": {"opnum": 0}},
    "sha1h_2": {"sha1c_3": {"opnum": 1}},
    "sha1c_2": {"sha1h_3": {"opnum": 0}, "sha1c_3": {"opnum": 0}},
    "addX_4": {"sha1c_4": {"opnum": 2}},
    "sha1su1_1": {
        "addX_5": {"opnum": 0},
        "sha1su1_2": {"opnum": 1},
        "sha1su0_3": {"opnum": 2},
        "sha1su0_4": {"opnum": 1},
        "sha1su0_5": {"opnum": 0},
    },
    "sha1su0_2": {"sha1su1_2": {"opnum": 0}},
    "sha1h_3": {"sha1c_4": {"opnum": 1}},
    "sha1c_3": {"sha1h_4": {"opnum": 0}, "sha1c_4": {"opnum": 0}},
    "addX_5": {"sha1p_0": {"opnum": 2}},
    "K1": {
        "addX_5": {"opnum": 1},
        "addY_6": {"opnum": 1},
        "addX_7": {"opnum": 1},
        "addX_8": {"opnum": 1},
        "addX_9": {"opnum": 1},
    },
    "sha1su1_2": {
        "addY_6": {"opnum": 0},
        "sha1su1_3": {"opnum": 1},
        "sha1su0_4": {"opnum": 2},
        "sha1su0_5": {"opnum": 1},
        "sha1su0_6": {"opnum": 0},
    },
    "sha1su0_3": {"sha1su1_3": {"opnum": 0}},
    "sha1h_4": {"sha1p_0": {"opnum": 1}},
    "sha1c_4": {"sha1h_5": {"opnum": 0}, "sha1p_0": {"opnum": 0}},
    "addY_6": {"sha1p_1": {"opnum": 2}},
    "sha1su1_3": {
        "addX_7": {"opnum": 0},
        "sha1su1_4": {"opnum": 1},
        "sha1su0_5": {"opnum": 2},
        "sha1su0_6": {"opnum": 1},
        "sha1su0_7": {"opnum": 0},
    },
    "sha1su0_4": {"sha1su1_4": {"opnum": 0}},
    "sha1h_5": {"sha1p_1": {"opnum": 1}},
    "sha1p_0": {"sha1h_6": {"opnum": 0}, "sha1p_1": {"opnum": 0}},
    "addX_7": {"sha1p_2": {"opnum": 2}},
    "sha1su1_4": {
        "addX_8": {"opnum": 0},
        "sha1su1_5": {"opnum": 1},
        "sha1su0_6": {"opnum": 2},
        "sha1su0_7": {"opnum": 1},
        "sha1su0_8": {"opnum": 0},
    },
    "sha1su0_5": {"sha1su1_5": {"opnum": 0}},
    "sha1h_6": {"sha1p_2": {"opnum": 1}},
    "sha1p_1": {"sha1h_7": {"opnum": 0}, "sha1p_2": {"opnum": 0}},
    "addX_8": {"sha1p_3": {"opnum": 2}},
    "sha1su1_5": {
        "addX_9": {"opnum": 0},
        "sha1su1_6": {"opnum": 1},
        "sha1su0_7": {"opnum": 2},
        "sha1su0_8": {"opnum": 1},
        "sha1su0_9": {"opnum": 0},
    },
    "sha1su0_6": {"sha1su1_6": {"opnum": 0}},
    "sha1h_7": {"sha1p_3": {"opnum": 1}},
    "sha1p_2": {"sha1h_8": {"opnum": 0}, "sha1p_3": {"opnum": 0}},
    "addX_9": {"sha1p_4": {"opnum": 2}},
    "sha1su1_6": {
        "addX_10": {"opnum": 0},
        "sha1su1_7": {"opnum": 1},
        "sha1su0_8": {"opnum": 2},
        "sha1su0_9": {"opnum": 1},
        "sha1su0_10": {"opnum": 0},
    },
    "sha1su0_7": {"sha1su1_7": {"opnum": 0}},
    "sha1h_8": {"sha1p_4": {"opnum": 1}},
    "sha1p_3": {"sha1h_9": {"opnum": 0}, "sha1p_4": {"opnum": 0}},
    "addX_10": {"sha1m_0": {"opnum": 2}},
    "K2": {
        "addX_10": {"opnum": 1},
        "addY_11": {"opnum": 1},
        "addX_12": {"opnum": 1},
        "addX_13": {"opnum": 1},
        "addX_14": {"opnum": 1},
    },
    "sha1su1_7": {
        "addY_11": {"opnum": 0},
        "sha1su1_8": {"opnum": 1},
        "sha1su0_9": {"opnum": 2},
        "sha1su0_10": {"opnum": 1},
        "sha1su0_11": {"opnum": 0},
    },
    "sha1su0_8": {"sha1su1_8": {"opnum": 0}},
    "sha1h_9": {"sha1m_0": {"opnum": 1}},
    "sha1p_4": {"sha1h_10": {"opnum": 0}, "sha1m_0": {"opnum": 0}},
    "addY_11": {"sha1m_1": {"opnum": 2}},
    "sha1su1_8": {
        "addX_12": {"opnum": 0},
        "sha1su1_9": {"opnum": 1},
        "sha1su0_10": {"opnum": 2},
        "sha1su0_11": {"opnum": 1},
        "sha1su0_12": {"opnum": 0},
    },
    "sha1su0_9": {"sha1su1_9": {"opnum": 0}},
    "sha1h_10": {"sha1m_1": {"opnum": 1}},
    "sha1m_0": {"sha1h_11": {"opnum": 0}, "sha1m_1": {"opnum": 0}},
    "addX_12": {"sha1m_2": {"opnum": 2}},
    "sha1su1_9": {
        "addX_13": {"opnum": 0},
        "sha1su1_10": {"opnum": 1},
        "sha1su0_11": {"opnum": 2},
        "sha1su0_12": {"opnum": 1},
        "sha1su0_13": {"opnum": 0},
    },
    "sha1su0_10": {"sha1su1_10": {"opnum": 0}},
    "sha1h_11": {"sha1m_2": {"opnum": 1}},
    "sha1m_1": {"sha1h_12": {"opnum": 0}, "sha1m_2": {"opnum": 0}},
    "addX_13": {"sha1m_3": {"opnum": 2}},
    "sha1su1_10": {
        "addX_14": {"opnum": 0},
        "sha1su1_11": {"opnum": 1},
        "sha1su0_12": {"opnum": 2},
        "sha1su0_13": {"opnum": 1},
        "sha1su0_14": {"opnum": 0},
    },
    "sha1su0_11": {"sha1su1_11": {"opnum": 0}},
    "sha1h_12": {"sha1m_3": {"opnum": 1}},
    "sha1m_2": {"sha1h_13": {"opnum": 0}, "sha1m_3": {"opnum": 0}},
    "addX_14": {"sha1m_4": {"opnum": 2}},
    "sha1su1_11": {
        "addX_15": {"opnum": 0},
        "sha1su1_12": {"opnum": 1},
        "sha1su0_13": {"opnum": 2},
        "sha1su0_14": {"opnum": 1},
        "sha1su0_15": {"opnum": 0},
    },
    "sha1su0_12": {"sha1su1_12": {"opnum": 0}},
    "sha1h_13": {"sha1m_4": {"opnum": 1}},
    "sha1m_3": {"sha1h_14": {"opnum": 0}, "sha1m_4": {"opnum": 0}},
    "addX_15": {"sha1p_5": {"opnum": 2}},
    "K3": {
        "addX_15": {"opnum": 1},
        "addY_16": {"opnum": 1},
        "addX_17": {"opnum": 1},
        "addX_18": {"opnum": 1},
        "addX_19": {"opnum": 1},
    },
    "sha1su1_12": {
        "addY_16": {"opnum": 0},
        "sha1su1_13": {"opnum": 1},
        "sha1su0_14": {"opnum": 2},
        "sha1su0_15": {"opnum": 1},
    },
    "sha1su0_13": {"sha1su1_13": {"opnum": 0}},
    "sha1h_14": {"sha1p_5": {"opnum": 1}},
    "sha1m_4": {"sha1h_15": {"opnum": 0}, "sha1p_5": {"opnum": 0}},
    "addY_16": {"sha1p_6": {"opnum": 2}},
    "sha1su1_13": {"addX_17": {"opnum": 0}, "sha1su1_14": {"opnum": 1}, "sha1su0_15": {"opnum": 2}},
    "sha1su0_14": {"sha1su1_14": {"opnum": 0}},
    "sha1h_15": {"sha1p_6": {"opnum": 1}},
    "sha1p_5": {"sha1h_16": {"opnum": 0}, "sha1p_6": {"opnum": 0}},
    "addX_17": {"sha1p_7": {"opnum": 2}},
    "sha1su1_14": {"addX_18": {"opnum": 0}, "sha1su1_15": {"opnum": 1}},
    "sha1su0_15": {"sha1su1_15": {"opnum": 0}},
    "sha1h_16": {"sha1p_7": {"opnum": 1}},
    "sha1p_6": {"sha1h_17": {"opnum": 0}, "sha1p_7": {"opnum": 0}},
    "addX_18": {"sha1p_8": {"opnum": 2}},
    "sha1su1_15": {"addX_19": {"opnum": 0}},
    "sha1h_17": {"sha1p_8": {"opnum": 1}},
    "sha1p_7": {"sha1h_18": {"opnum": 0}, "sha1p_8": {"opnum": 0}},
    "addX_19": {"sha1p_9": {"opnum": 2}},
    "sha1h_18": {"sha1p_9": {"opnum": 1}},
    "sha1p_8": {"sha1h_19": {"opnum": 0}, "sha1p_9": {"opnum": 0}},
    "sha1h_19": {"addY_21": {"opnum": 0}},
    "sha1p_9": {"addX_20": {"opnum": 0}},
    "addX_20": {"insval_0": {"opnum": 0}},
    "addY_21": {"inselm_0": {"opnum": 0}},
    "inselm_0": {"insval_1": {"opnum": 1}},
    "insval_0": {"insval_1": {"opnum": 0}},
    "insval_1": {"res": {"opnum": 0}},
    "res": {},
}

GO = nx.DiGraph(g_dod_orig)
G = nx.DiGraph(g_dod)
print(f"G: {G}")
print(f"G.adjacency(): {list(G.adjacency())}")
print(f"G.predecessors('res'): {list(G.predecessors('res'))}")

for i in nx.edge_bfs(G):
    # inspect(i, all=True)
    print(f"i: {i} i.opnum: {G[i[1]]}")

batches: list[list[str]] = []
node2batch: dict[str, int] = {}
for i, batch in enumerate(nx.topological_generations(G)):
    batch = sorted(batch)
    for n in batch:
        node2batch[n] = i
    batches.append(batch)

trace = []
for i, batch in enumerate(batches):
    trace.append([])
    for j, instr in enumerate(batch):
        ops = []
        print(f"i: {i} j: {j} instr: {instr}")
        print(f"G.in_edges(instr): {G.in_edges(instr)}")
        for op in G.in_edges(instr):
            print()
            print(f"op: {G.edges[op]}")
            ops.append((op[0], G.edges[op]["opnum"]))
        ops = sorted(ops, key=lambda o: o[1])
        ops = tuple(o[0] for o in ops)
        trace[i].append((instr, ops))
    trace[i] = tuple(sorted(trace[i]))
trace = tuple(trace)

print(f"trace:\n{trace}")


class Instr(enum.IntEnum):
    SHA1C = 0
    SHA1H = 1
    SHA1P = 2
    SHA1M = 3
    SHA1SU0 = 4
    SHA1SU1 = 5
    ADD_A = 6
    ADD_B = 7


clut = {
    "sha1c": 0,
    "sha1h": 1,
    "sha1p": 2,
    "sha1m": 3,
    "sha1su0": 4,
    "sha1su1": 5,
    "add_a": 6,
    "add_b": 7,
}


for i, batch in enumerate(trace):
    # print(f"batch[{i:2}]:")
    print(f"batch[{i:2}]: {[x[0] for x in batch]}")
    for j, instr in enumerate(batch):
        # print(f"batch[{i:2}]: instr[{j}]: {instr[0]}")
        si = instr[0].split("_")
        name = si[0]
        if len(si) > 1:
            pass
        if name == "add_":
            pass

for i, batch in enumerate(nx.topological_generations(GO)):
    batch = sorted(batch)
    print(f"i: {i} batch: {batch}")

# print(f"node2batch: {node2batch}")

print("done")
