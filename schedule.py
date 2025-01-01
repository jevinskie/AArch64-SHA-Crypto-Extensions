#!/usr/bin/env python3

import collections
import enum
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import types
from collections.abc import Mapping, MutableMapping

import bidict
import networkx as nx
import pandas as pd
import tabulate
from more_itertools import all_unique, always_reversible
from ortools.sat.python import cp_model
from rich import print as rprint
from rich.pretty import pprint

import sha1_arm
from sha1_arm import cf, op_color

tabulate
pd


_NumInPorts: dict[str, int] = {
    "sha1c": 3,
    "sha1h": 1,
    "sha1m": 3,
    "sha1p": 3,
    "sha1su0": 3,
    "sha1su1": 2,
    "vaddX": 2,
    "vaddXY": 2,
    "vaddY": 2,
}

NumInPorts = types.MappingProxyType(_NumInPorts)


def dot_format(dot_src: str) -> str:
    bin_path = shutil.which("nop")
    args = (bin_path,)
    with tempfile.TemporaryFile("w") as tf:
        tf.write(dot_src)
        tf.seek(0, io.SEEK_SET)
        r = subprocess.run(args, stdin=tf, capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write(r.stdout)
            sys.stderr.write(r.stderr)
            raise subprocess.CalledProcessError(r.returncode, args, r.stdout, r.stderr)
        return r.stdout


class BiDictStrInt(Mapping[str, int]):
    def __init__(self) -> None:
        self._mapping: bidict.bidict[str, int] = bidict.bidict()
        self._mapping.on_dup = bidict.ON_DUP_RAISE

    @property
    def rev(self) -> bidict.bidict[int, str]:
        return self._mapping.inverse

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(f"key '{key}' is not str")
        if key in self._mapping:
            return self._mapping[key]
        else:
            val = len(self)
            self._mapping[key] = val
            return val

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def __repr__(self):
        return repr(self._mapping)

    def __str__(self):
        return str(self._mapping)


class VRegIdx(BiDictStrInt): ...


class MutBiDictStrInt(MutableMapping[str, int]):
    def __init__(self) -> None:
        self._mapping: bidict.bidict[str, int] = bidict.bidict()
        self._mapping.on_dup = bidict.ON_DUP_RAISE

    @property
    def rev(self) -> bidict.bidict[int, str]:
        return self._mapping.inverse

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(f"key '{key}' is not str")
        return self._mapping[key]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"key '{key}' is not str")
        if not isinstance(value, int):
            raise TypeError(f"value '{value}' is not int")
        self._mapping[key] = value

    def __delitem__(self, key):
        del self._mapping[key]

    def __iter__(self):
        return iter(self._mapping)

    def __len__(self):
        return len(self._mapping)

    def __repr__(self):
        return repr(self._mapping)

    def __str__(self):
        return str(self._mapping)


class BatchIdx(MutBiDictStrInt): ...


g_dod_orig = json.load(open("g_dod_orig.json"))

g_dod = json.load(open("g_dod.json"))

sha1comp_dod = json.load(open("sha1-compress-one-hand-graph-f.json"))

# GO = nx.DiGraph(g_dod_orig)
# G = nx.DiGraph(g_dod)
G = nx.DiGraph(sha1comp_dod)
# rprint(f"G: {G}")
# rprint(f"G.adjacency(): {list(G.adjacency())}")
# rprint(f"G.predecessors('res'): {list(G.predecessors('res'))}")

_suffix_underscore_pattern = r"^(.+?)_(\d+)$"
_suffix_n_pattern = r"^(.+?)N(\d+)$"


def get_eu(definition: str) -> tuple[str, int]:
    m = re.match(_suffix_underscore_pattern, definition)
    s = m.group(1)
    n = int(m.group(2))
    return s, n


def nize_def(definition: str) -> str:
    m = re.match(_suffix_underscore_pattern, definition)
    s = m.group(1)
    n = int(m.group(2))
    return f"{s}N{n}"


def portize_use(use: str, port: int) -> str:
    assert 0 <= port <= 2
    return f"{use}P{port}"


def get_eun(definition: str) -> tuple[str, int]:
    m = re.match(_suffix_n_pattern, definition)
    s = m.group(1)
    n = int(m.group(2))
    return s, n


for n in list(G.nodes()):
    if n in (
        "ByteRevLUT",
        "K0",
        "K1",
        "K2",
        "K3",
        "blocks_a",
        "blocks",
        "abcd_a",
        "e_a",
        "abcd",
        "e",
        "shuf_0",
        "shuf_1",
        "shuf_2",
        "shuf_3",
        "vaddXY_16",
        "add_0",
        "inselm_0",
        "insval_0",
        "insval_1",
        "res",
    ):
        G.remove_node(n)
        # pass

old_nodes = G.nodes()
nodes_map: dict[str, str] = {}

for n in G.nodes():
    nodes_map[n] = nize_def(n)

G = nx.relabel_nodes(G, nodes_map)


# for i in nx.edge_bfs(G):
#     # inspect(i, all=True)
#     rprint(f"i: {i} i.opnum: {G[i[1]]}")

def_uses: dict[str, tuple[str, ...]] = {}

for definition in G.nodes():
    # print(f"definition: {definition} G.in_edges(definition): {G.in_edges(definition)}")
    uses = tuple(e[0] for e in G.in_edges(definition))
    def_uses[definition] = uses

rprint(def_uses)

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
    ADD = 6
    ADDX = 6
    ADDY = 7
    VADDX = 6
    VADDY = 7
    VADDXY = 6
    ABCD = 6
    E = 6


clut = {
    "sha1c": 0,
    "sha1h": 1,
    "sha1p": 2,
    "sha1m": 3,
    "sha1su0": 4,
    "sha1su1": 5,
    "vaddX": 6,
    "vaddY": 7,
    "vaddXY": 6,
    "add": 6,
    "abcd": 6,
    "e": 6,
}

port_assignments = {
    portize_use(i, p): collections.defaultdict() for p in range(3) for i in clut.keys()
}

rprint(f"port_assignments:\n{port_assignments}")

port_usage = {
    portize_use(i, p): collections.defaultdict(int) for p in range(3) for i in clut.keys()
}

rprint(f"port_usage:\n{port_usage}")

for i, batch in enumerate(trace):
    # rprint(f"batch[{i:2}]:")
    # rprint(f"batch[{i:2}]: {[x[0] for x in batch]}")
    batch_inputs = []
    for j, instr in enumerate(batch):
        # rprint(f"batch[{i:2}]: instr[{j}]: {instr}")
        # si = instr[0].split("_")
        # name = si[0]
        name, _ = get_eun(instr[0])
        preds = instr[1]
        for k, p in enumerate(preds):
            # pname = p.split("_")[0]
            pname, _ = get_eun(p)
            batch_inputs.append((name, k, pname, op_color(clut[pname], k)))
            # rprint(f"i: {i} j: {j} k: {k} name: {name} p: {p} pname: {pname}")
            port_usage[portize_use(name, k)][pname] += 1
    # batch_inputs = list(sorted(batch_inputs, key=lambda v: (v[0], v[1])))
    # rprint(f"batch_inputs[{i:2}]: {batch_inputs}")
    rprint(f"batch[{i:2}]: ", end="")
    print(" ".join([f"{b[3]}{b[0]}{cf.reset}" for b in batch_inputs]))

for k in list(port_usage.keys()):
    if len(port_usage[k]) == 0:
        del port_usage[k]
    else:
        port_usage[k] = dict(port_usage[k])

rprint("port_usage:")
pprint(port_usage)

batches_v2: list[list[str]] = []
batches_v2_linear: list[str] = []
batches_v2_instrs: list[list[str]] = []
batches_v2_batchidx: dict[str, int] = {}
batches_v2_vregidx = VRegIdx()
all_instrs_set: set[str] = set()
batch_uses: list[list[str]] = []
batch_defs: list[list[str]] = []

for batch in nx.topological_generations(G):
    for definition in batch:
        instr, _ = get_eun(definition)
        all_instrs_set.add(instr)

all_instrs: tuple[str, ...] = tuple(sorted(all_instrs_set))

rprint("all_instrs:")
pprint(all_instrs)

for i, batch in enumerate(nx.topological_generations(G)):
    batch = sorted(batch)
    binstrs: list[str] = []
    b_uses: set[str] = set()
    batch_defs.append(batch)
    for definition in batch:
        batches_v2_vregidx[definition]
        batches_v2_batchidx[definition] = i
        # print(f"definition: {definition}")
        binstr, _ = get_eun(definition)
        # print(f"binstr: {binstr}")
        binstrs.append(binstr)
        duses = [e[0] for e in G.in_edges(definition)]
        b_uses.update(duses)
        batches_v2_linear.append(definition)
    rprint(f"i: {i} batch: {batch}")
    batches_v2.append(batch)
    batches_v2_instrs.append(binstrs)
    batch_uses.append(list(sorted(b_uses)))

assert all_unique(batches_v2_linear)

rprint("batches_v2:")
rprint(batches_v2)
rprint("batches_v2_linear:")
rprint(batches_v2_linear)
rprint("batches_v2_instrs:")
rprint(batches_v2_instrs)
rprint("batches_v2_vregidx:")
rprint(batches_v2_vregidx)
rprint(batches_v2_batchidx)
rprint(f"batch_uses:\n{batch_uses}")
rprint(f"batch_defs:\n{batch_defs}")


PG = nx.DiGraph(outputorder="edgesfirst")
for i, batch in enumerate(batches_v2):
    for ldef in batch:
        ldef_instr, _ = get_eun(ldef)
        PG.add_node(ldef, label=ldef_instr)
        # defs_port_uses[ldef] = [None] * NumInPorts[ldef_instr]
        ldef_uses = sorted(u for u, ui in G[ldef].items() if ui["opnum"] >= 0)
        rprint(f"ldef: {ldef} ldef_uses: {ldef_uses}")
        # for ldef_user, ldef_user_opnum in ldef_uses.items():
        # defs_port_uses[ldef_user][ldef_user_opnum] = ldef

nx.nx_agraph.write_dot(PG, "pipeline.dot")

rprint(f"PG: {PG}")

defs_port_uses: dict[str, list[str | None]] = {}
for i, batch in always_reversible(enumerate(batches_v2)):
    for ldef in batch:
        ldef_instr, _ = get_eun(ldef)
        defs_port_uses[ldef] = [None] * NumInPorts[ldef_instr]
        ldef_uses = {u: ui["opnum"] for u, ui in G[ldef].items() if ui["opnum"] >= 0}
        for ldef_user, ldef_user_opnum in ldef_uses.items():
            defs_port_uses[ldef_user][ldef_user_opnum] = ldef

defs_port_uses = dict(reversed(defs_port_uses.items()))

rprint("defs_port_uses:")
pprint(defs_port_uses)

instr_port_uses: dict[str, list[dict[str, dict[int, int]] | None]] = {
    i: [None] * NumInPorts[i] for i in NumInPorts
}
for d, pu in defs_port_uses.items():
    instr, _ = get_eun(d)
    for i, u in enumerate(pu):
        if u is None:
            continue

        uinstr, _ = get_eun(u)
        ubidx = batches_v2_batchidx[u]
        dbidx = batches_v2_batchidx[d]
        dist = dbidx - ubidx
        assert dist > 0
        if instr_port_uses[instr][i] is None:
            instr_port_uses[instr][i] = {}
        if uinstr not in instr_port_uses[instr][i]:
            instr_port_uses[instr][i][uinstr] = collections.Counter()
        instr_port_uses[instr][i][uinstr][f"d{dist}"] += 1

rprint("instr_port_uses:")
pprint(instr_port_uses)

_instr_op_delays: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
for i, instr in enumerate(list(instr_port_uses)):
    op_list = instr_port_uses[instr]
    for j, op_sources in enumerate(op_list):
        if op_sources is None:
            continue
        for oinstr in op_sources:
            _instr_op_delays[oinstr] += op_list[j][oinstr]

rprint("_instr_op_delays:")
pprint(_instr_op_delays)

instr_op_delays: dict[str, dict[int, int]] = {}
for instr, delays in _instr_op_delays.items():
    idelays = dict(sorted({int(d[1:]): c for d, c in delays.items()}.items()))
    instr_op_delays[instr] = idelays
instr_op_delays = dict(sorted(instr_op_delays.items()))

rprint("instr_op_delays:")
pprint(instr_op_delays)


def get_node(ssa_def: str, num_ops: int) -> str:
    # vaddX [label="vaddX|{{<f0> op0| <f1> op2}| <f2> res}", shape=record];
    ops = "|".join(f"<op{n}> op{n}" for n in range(num_ops))
    label = f"{ssa_def}|{{{{{ops}}}|<res> res}}"
    return f'{ssa_def} [label="{label}", shape=record];'


def write_pipeline_dot(sched_info: object, out_path: str) -> None:
    s = "digraph g {\n\tgraph [rankdir=LR];\n\tnode [fontsize=16];\n"
    for batch in batches_v2:
        for d in batch:
            print(f"d: {d}")
            instr, _ = get_eun(d)
            s += f"\t{get_node(d, NumInPorts[instr])}\n"
    for d, uses in defs_port_uses.items():
        for pnum, u in enumerate(uses):
            if u is None:
                continue
            s += f"\t{u}:res -> {d}:op{pnum}\n"
    s += "\n}\n"
    ps = dot_format(s)
    print(f"ps: {ps}")
    with open(out_path, "w") as f:
        f.write(ps)


write_pipeline_dot(object(), "pipeline.dot")

rprint(G["sha1hN16"])

print("palette_a_8")
sha1_arm.dump_palette(sha1_arm.palette_a_8)
print("\n\n\n")
print("palette_b_7")
sha1_arm.dump_palette(sha1_arm.palette_b_7)
print("\n\n\n")
print("palette_c_8")
sha1_arm.dump_palette(sha1_arm.palette_c_8)
print("\n\n\n")
print("palette_d_8")
sha1_arm.dump_palette(sha1_arm.palette_d_9)
print("\n\n\n")

sys.exit(0)

# for i, batch in enumerate(nx.topological_generations(GO)):
#     batch = sorted(batch)
#     rprint(f"i: {i} batch: {batch}")

# rprint(f"node2batch: {node2batch}")

"""Minimal jobshop problem."""
# Data.
instrs = tuple(sorted(all_instrs_set))
rprint(instrs)

instrs_lut = bidict.bidict(zip(instrs, range(len(instrs))))
rprint(instrs_lut)
rprint(instrs_lut.inverse)

instrs_eus = tuple([get_eun(d) for d in instrs])
rprint(instrs_eus)

instrs_counts = collections.defaultdict(int)
for d in instrs:
    eu, _ = get_eun(d)
    print(f"d: {d} eu: {eu}")
    instrs_counts[eu] += 1
instrs_counts = dict(instrs_counts)
rprint(instrs_counts)


# https://github.com/pganalyze/cp-sat-python-example/blob/main/shift_schedule.py
model = cp_model.CpModel()

# The execution units and the operations they can perform
exec_units = {
    "sha1c": ["sha1c"],
    "sha1h": ["sha1h"],
    "sha1m": ["sha1m"],
    "sha1p": ["sha1p"],
    "sha1su0": ["sha1su0"],
    "sha1su1": ["sha1su1"],
    "vaddX": ["vaddX", "vaddXY"],
    "vaddY": ["vaddY", "vaddXY"],
}

# List of ticks ("cycles") for the schedule
ticks_int = list(range(22))
ticks = [f"t{i}" for i in ticks_int]

# list of instructions/definitions that must be made
instr_seq = batches_v2_vregidx

# List of possible operations
operations = ("sha1c", "sha1h", "sha1m", "sha1p", "sha1su0", "sha1su1", "vaddX", "vaddXY", "vaddY")
add_operations = {"vaddX", "vaddY", "vaddXY"}
rprint(add_operations)

sz = len(instr_seq)
num_cycles = len(batches)

# order[o][k] = which op node is in the k-th cycle
order = {}
for o in operations:
    order[o] = [
        model.NewIntVar(0, instrs_counts[o] - 1, f"order_{o}_{k}") for k in range(num_cycles)
    ]
    # below unsafe?
    # model.AddAllDifferent(order[o])

order_s = [model.NewIntVar(0, sz - 1, f"order_s_{k}") for k in range(sz)]
model.AddAllDifferent(order_s)
for u, v in G.edges():
    model.Add(order_s[instr_seq[u]] < order_s[instr_seq[v]])

# pos[i] = the position of node i in the order array
# pos = [model.NewIntVar(0, sz - 1, f"pos_{i}") for i in range(sz)]
# # Link pos <-> order:
# # For each k in [0..n-1], we have order[k] = i  ->  pos[i] = k
# for i in range(sz):
#     # One straightforward way is to add a table constraint
#     # or encode the equivalences. For brevity we skip the details,
#     # but in practice you'd use model.AddElement(...) or a flow/circuit approach
#     model.AddElement(pos[i], order, i)
# model.AddAllDifferent(pos)

for i, batch in enumerate(batches_v2):
    for d in batch:
        pass


# Add the precedence constraints for edges:
for u, v in G.edges():
    u_eu, u_n = get_eun(u)
    v_eu, v_n = get_eun(v)
    # model.Add(order[u_eu] < order[v_eu])

# # `schedule[e][o][t]` indicates if exec unit `e`
# # performs operation `o` on tick `t`
# schedule = {
#     e: {o: {t: model.new_bool_var(f"schedule_{e}_{o}_{t}") for t in ticks} for o in operations}
#     for e in exec_units
# }

# # A cashier has to be present at all times
# # for d in ticks:
# #     for s in shifts:
# #         model.add(sum(schedule[e]["Cashier"][d][s] for e in exec_units) == 1)

# # We need a vaddX once per tick
# # for t in ticks:
# #     model.add(sum(schedule[e]["vaddXY"][t] for e in exec_units) == 1)

# # `def_ticks[d][t]` indicates if def `d` is produced on tick `t`
# def_ticks = {d: {t: model.new_bool_var(f"def_ticks_{d}_{t}") for t in ticks} for d in instr_seq}

# # All defs must occur once and only once
# for d in instr_seq:
#     model.add(sum(def_ticks[d][t] for t in ticks) == 1)

# # `use_ticks[u][t]` indicates if def `u` is used in tick `t`
# use_ticks = {
#     u: {t: model.new_bool_var(f"use_ticks_{u}_{t}") for t in ticks}
#     for d in instr_seq
#     for u in def_uses[d]
# }


# rprint(def_ticks)
# rprint(use_ticks)

# # All def uses must proceed def
# for d in instr_seq:
#     for u in def_uses[d]:
#         for t in ticks_int:
#             model.add(sum(def_ticks[u][f"t{tp}"] for tp in range(t - 1)) == 1)


# # An exec unit can only perform one operation per tick
# for e in exec_units:
#     for t in ticks:
#         model.add(sum(schedule[e][o][t] for o in operations) <= 1)

# # An exec unit can only perform one operation per tick
# for e in ("vaddX", "vaddY"):
#     for t in ticks:
#         model.add(schedule[e]["vaddXY"][t] + schedule[e][e][t] <= 1)

# Some exec units can only perform certain operations
# for e in exec_units:
#     for o in operations:
#         for t in ticks:
#             if o not in exec_units[e]:
#                 model.add(schedule[e][o][t] == 0)

# Solve the model
solver = cp_model.CpSolver()
status = solver.solve(model)
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    strstat = None
    if status == cp_model.OPTIMAL:
        strstat = "OPTIMAL"
    elif status == cp_model.FEASIBLE:
        strstat = "FEASIBLE"
    print(f"Solution: {strstat}")
else:
    print("No solution found.")

# Statistics.
print("\nStatistics")
print(f"  - conflicts: {solver.num_conflicts}")
print(f"  - branches : {solver.num_branches}")
print(f"  - wall time: {solver.wall_time}s")

print(solver.solution_info())
print(model.model_stats())

# solved_pos = []
# for u, ui in instr_seq.items():
# p = order[ui]
# sp = solver.value(order[ui])
# defs, uses = def_uses[u]

# print(f"p: {p} sp: {sp} i: {instr_seq.rev[sp]}")

for k1, v1 in order.items():
    for v2 in v1:
        s = solver.value(v2)
        print(s)
    print(f"v: {v} s: {s}")

for u, ui in instr_seq.items():
    p = order_s[ui]
    sp = solver.value(order_s[ui])

    print(f"p: {p} sp: {sp} i: {instr_seq.rev[sp]}")

# solved_schedule = collections.defaultdict(lambda: collections.defaultdict(collections.defaultdict))
# for e in exec_units:
#     for o in operations:
#         for t in ticks:
#             solved_schedule[e][o][t] = not not solver.value(schedule[e][o][t])

# # rprint(solved_schedule)

# solved_def_ticks = collections.defaultdict(lambda: collections.defaultdict(collections.defaultdict))
# for i in instr_seq.rev:
#     for t in ticks:
#         solved_def_ticks[i][t] = solver.value(def_ticks[i][t])

# rprint(solved_def_ticks)

# pdf = pd.DataFrame(schedule)
# rprint(pdf.describe())
# rprint(pdf)

# Print the solution
# just draw the owl

print("\n\n\n\n\n\n")
instr_data = [  # execution unit = (machine_id, ).
    [0, 1, 2],  # Job0
    [0, 2, 1],  # Job1
    [1, 2],  # Job2
]

machines_count = 1 + max(task for job in instr_data for task in job)
all_machines = range(machines_count)
# Computes horizon dynamically as the sum of all durations.
horizon = sum(len(job) for job in instr_data)

# Create the model.
model = cp_model.CpModel()

# Named tuple to store information about created variables.
task_type = collections.namedtuple("task_type", "start end interval")
# Named tuple to manipulate solution information.
assigned_task_type = collections.namedtuple("assigned_task_type", "start job index duration")

# Creates job intervals and add to the corresponding machine lists.
all_tasks = {}
machine_to_intervals = collections.defaultdict(list)

for job_id, job in enumerate(instr_data):
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
for job_id, job in enumerate(instr_data):
    for task_id in range(len(job) - 1):
        model.add(all_tasks[job_id, task_id + 1].start >= all_tasks[job_id, task_id].end)

# Makespan objective.
obj_var = model.new_int_var(0, horizon, "makespan")
model.add_max_equality(
    obj_var,
    [all_tasks[job_id, len(job) - 1].end for job_id, job in enumerate(instr_data)],
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
    for job_id, job in enumerate(instr_data):
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
