#!/usr/bin/env python3

import functools
import math
import operator

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
print(f"batch_sizes: {batch_sizes}")
num_schedules = functools.reduce(operator.mul, [math.factorial(len(b)) for b in batches], 1)
print(f"num_schedules: {num_schedules}")

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
print(f"batch_sizes: {batch_sizes}")
num_schedules = functools.reduce(operator.mul, [math.factorial(len(b)) for b in batches_norm], 1)
print(f"num_schedules: {num_schedules}")