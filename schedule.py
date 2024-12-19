#!/usr/bin/env python3

import collections
import enum

import networkx as nx
from ortools.sat.python import cp_model
from rich import print as rprint
from rich.pretty import pprint

from sha1_arm import cf, op_color

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
# rprint(f"batch_sizes: {batch_sizes}")
# num_schedules = functools.reduce(operator.mul, [math.factorial(len(b)) for b in batches], 1)
# rprint(f"num_schedules: {num_schedules}")

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
# rprint(f"batch_sizes: {batch_sizes}")
# num_schedules = functools.reduce(operator.mul, [math.factorial(len(b)) for b in batches_norm], 1)
# rprint(f"num_schedules: {num_schedules}")

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
    "sha1su0_0": {"sha1su1_0": {"opnum": 0}, "sha1su0_1": {"opnum": -1}},
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
        "addX_6": {"opnum": 1},
        "addX_7": {"opnum": 1},
        "addX_8": {"opnum": 1},
        "addX_9": {"opnum": 1},
    },
    "sha1su1_2": {
        "addX_6": {"opnum": 0},
        "sha1su1_3": {"opnum": 1},
        "sha1su0_4": {"opnum": 2},
        "sha1su0_5": {"opnum": 1},
        "sha1su0_6": {"opnum": 0},
    },
    "sha1su0_3": {"sha1su1_3": {"opnum": 0}},
    "sha1h_4": {"sha1p_0": {"opnum": 1}},
    "sha1c_4": {"sha1h_5": {"opnum": 0}, "sha1p_0": {"opnum": 0}},
    "addX_6": {"sha1p_1": {"opnum": 2}},
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
        "addX_11": {"opnum": 1},
        "addX_12": {"opnum": 1},
        "addX_13": {"opnum": 1},
        "addX_14": {"opnum": 1},
    },
    "sha1su1_7": {
        "addX_11": {"opnum": 0},
        "sha1su1_8": {"opnum": 1},
        "sha1su0_9": {"opnum": 2},
        "sha1su0_10": {"opnum": 1},
        "sha1su0_11": {"opnum": 0},
    },
    "sha1su0_8": {"sha1su1_8": {"opnum": 0}},
    "sha1h_9": {"sha1m_0": {"opnum": 1}},
    "sha1p_4": {"sha1h_10": {"opnum": 0}, "sha1m_0": {"opnum": 0}},
    "addX_11": {"sha1m_1": {"opnum": 2}},
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
        "addX_16": {"opnum": 1},
        "addX_17": {"opnum": 1},
        "addX_18": {"opnum": 1},
        "addX_19": {"opnum": 1},
    },
    "sha1su1_12": {
        "addX_16": {"opnum": 0},
        "sha1su1_13": {"opnum": 1},
        "sha1su0_14": {"opnum": 2},
        "sha1su0_15": {"opnum": 1},
    },
    "sha1su0_13": {"sha1su1_13": {"opnum": 0}},
    "sha1h_14": {"sha1p_5": {"opnum": 1}},
    "sha1m_4": {"sha1h_15": {"opnum": 0}, "sha1p_5": {"opnum": 0}},
    "addX_16": {"sha1p_6": {"opnum": 2}},
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
# rprint(f"G: {G}")
# rprint(f"G.adjacency(): {list(G.adjacency())}")
# rprint(f"G.predecessors('res'): {list(G.predecessors('res'))}")

for n in list(G.nodes()):
    if n in (
        "ByteRevLUT",
        "K0",
        "K1",
        "K2",
        "K3",
        "blocks",
        "buf",
        "sz",
        "shuf_0",
        "shuf_1",
        "shuf_2",
        "shuf_3",
        "inselm_0",
        "insval_0",
        "insval_1",
        "res",
    ):
        G.remove_node(n)
        # pass

# for i in nx.edge_bfs(G):
#     # inspect(i, all=True)
#     rprint(f"i: {i} i.opnum: {G[i[1]]}")

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
        # rprint(f"i: {i} j: {j} instr: {instr}")
        # rprint(f"G.in_edges(instr): {G.in_edges(instr)}")
        for op in G.in_edges(instr):
            # rprint(f"op: {G.edges[op]}")
            edges = G.edges[op]
            opnum = edges["opnum"]
            if opnum >= 0:
                ops.append((op[0], opnum))
        ops = sorted(ops, key=lambda o: o[1])
        ops = tuple(o[0] for o in ops)
        trace[i].append((instr, ops))
    trace[i] = tuple(sorted(trace[i]))
trace = tuple(trace)

# rprint(f"trace:\n{trace}")


class Instr(enum.IntEnum):
    SHA1C = 0
    SHA1H = 1
    SHA1P = 2
    SHA1M = 3
    SHA1SU0 = 4
    SHA1SU1 = 5
    ADDX = 6
    ADDY = 7


clut = {
    "sha1c": 0,
    "sha1h": 1,
    "sha1p": 2,
    "sha1m": 3,
    "sha1su0": 4,
    "sha1su1": 5,
    "addX": 6,
    "addY": 7,
}


port_usage = {f"{i}_p{p}": collections.defaultdict(int) for p in range(3) for i in clut.keys()}

rprint(f"port_usage:\n{port_usage}")

for i, batch in enumerate(trace):
    # rprint(f"batch[{i:2}]:")
    # rprint(f"batch[{i:2}]: {[x[0] for x in batch]}")
    batch_inputs = []
    for j, instr in enumerate(batch):
        # rprint(f"batch[{i:2}]: instr[{j}]: {instr}")
        si = instr[0].split("_")
        name = si[0]
        preds = instr[1]
        for k, p in enumerate(preds):
            pname = p.split("_")[0]
            batch_inputs.append((name, k, pname, op_color(clut[pname], k)))
            rprint(f"i: {i} j: {j} k: {k} name: {name} p: {p} pname: {pname}")
            port_usage[f"{name}_p{k}"][pname] += 1
    # batch_inputs = sorted(batch_inputs, key=lambda v: (v[0], v[1]))
    # rprint(f"batch_inputs[{i:2}]: {batch_inputs}")
    rprint(f"batch[{i:2}]: ", end=None)
    print(" ".join([f"{b[3]}{b[0]}{cf.reset}" for b in batch_inputs]))

for k in list(port_usage.keys()):
    if len(port_usage[k]) == 0:
        del port_usage[k]
    else:
        port_usage[k] = dict(port_usage[k])

rprint("port_usage:")
pprint(port_usage)

for i, batch in enumerate(nx.topological_generations(G)):
    batch = sorted(batch)
    rprint(f"i: {i} batch: {batch}")

# for i, batch in enumerate(nx.topological_generations(GO)):
#     batch = sorted(batch)
#     rprint(f"i: {i} batch: {batch}")

# rprint(f"node2batch: {node2batch}")

"""Minimal jobshop problem."""
# Data.
jobs_data = [  # task = (machine_id, ).
    [0, 1, 2],  # Job0
    [0, 2, 1],  # Job1
    [1, 2],  # Job2
]

machines_count = 1 + max(task for job in jobs_data for task in job)
all_machines = range(machines_count)
# Computes horizon dynamically as the sum of all durations.
horizon = sum(len(job) for job in jobs_data)

# Create the model.
model = cp_model.CpModel()

# Named tuple to store information about created variables.
task_type = collections.namedtuple("task_type", "start end interval")
# Named tuple to manipulate solution information.
assigned_task_type = collections.namedtuple("assigned_task_type", "start job index duration")

# Creates job intervals and add to the corresponding machine lists.
all_tasks = {}
machine_to_intervals = collections.defaultdict(list)

for job_id, job in enumerate(jobs_data):
    for task_id, task in enumerate(job):
        duration = 1
        machine = task
        suffix = f"_{job_id}_{task_id}"
        start_var = model.new_int_var(0, horizon, "start" + suffix)
        end_var = model.new_int_var(0, horizon, "end" + suffix)
        interval_var = model.new_interval_var(start_var, duration, end_var, "interval" + suffix)
        all_tasks[job_id, task_id] = task_type(start=start_var, end=end_var, interval=interval_var)
        machine_to_intervals[machine].append(interval_var)

# Create and add disjunctive constraints.
for machine in all_machines:
    model.add_no_overlap(machine_to_intervals[machine])

# Precedences inside a job.
for job_id, job in enumerate(jobs_data):
    for task_id in range(len(job) - 1):
        model.add(all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end)

# Makespan objective.
obj_var = model.new_int_var(0, horizon, "makespan")
model.add_max_equality(
    obj_var,
    [all_tasks[job_id, len(job) - 1].end for job_id, job in enumerate(jobs_data)],
)
# rprint(f"model: {model}")
model.minimize(obj_var)
# rprint(f"min(model): {model}")

# Creates the solver and solve.
solver = cp_model.CpSolver()
# rprint(f"solver: {solver}")
status = solver.solve(model)
# rprint(f"status: {status}")
# rprint(f"solver2: {solver}")

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    strstat = None
    if status == cp_model.OPTIMAL:
        strstat = "OPTIMAL"
    elif status == cp_model.FEASIBLE:
        strstat = "FEASIBLE"
    print(f"Solution: {strstat}")

    # Create one list of assigned tasks per machine.
    assigned_jobs = collections.defaultdict(list)
    for job_id, job in enumerate(jobs_data):
        for task_id, task in enumerate(job):
            machine = task
            assigned_jobs[machine].append(
                assigned_task_type(
                    start=solver.value(all_tasks[job_id, task_id].start),
                    job=job_id,
                    index=task_id,
                    duration=1,
                )
            )

    # Create per machine output lines.
    output = ""
    for machine in all_machines:
        # Sort by starting time.
        assigned_jobs[machine].sort()
        sol_line_tasks = "Machine " + str(machine) + ": "
        sol_line = "           "

        for assigned_task in assigned_jobs[machine]:
            name = f"job_{assigned_task.job}_task_{assigned_task.index}"
            # add spaces to output to align columns.
            sol_line_tasks += f"{name:15}"

            start = assigned_task.start
            duration = assigned_task.duration
            sol_tmp = f"[{start},{start + duration}]"
            # add spaces to output to align columns.
            sol_line += f"{sol_tmp:15}"

        sol_line += "\n"
        sol_line_tasks += "\n"
        output += sol_line_tasks
        output += sol_line

    # Finally print the solution found.
    print(f"Optimal Schedule Length: {solver.objective_value}")
    print(output)
else:
    print("No solution found.")

    # Statistics.
    print("\nStatistics")
    print(f"  - conflicts: {solver.num_conflicts}")
    print(f"  - branches : {solver.num_branches}")
    print(f"  - wall time: {solver.wall_time}s")


rprint("done")
