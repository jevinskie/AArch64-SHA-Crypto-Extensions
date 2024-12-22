#!/usr/bin/env python3

import collections
import enum
import json
import typing
from collections.abc import Mapping, MutableMapping

import bidict
import networkx as nx
import pandas as pd
import tabulate
from ortools.sat.python import cp_model
from rich import print as rprint
from rich.pretty import pprint

from sha1_arm import cf, op_color

tabulate
pd


class BiDictStrInt(Mapping[str, int]):
    def __init__(self) -> None:
        self._mapping: bidict.bidict[str, int] = bidict.bidict()
        self._mapping.on_dup = bidict.ON_DUP_RAISE

    @property
    def rev(self) -> bidict.bidict[int, str]:
        return self._mapping.inverse

    def __getitem__(self, key):
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
        return self._mapping[key]

    def __setitem__(self, key, value):
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

batches_v2: list[list[str]] = []
batches_v2_instrs: list[list[str]] = []
batches_v2_batchidx: dict[str, int] = {}
batches_v2_vregidx = VRegIdx()
all_instrs: set[str] = set()

for i, batch in enumerate(nx.topological_generations(G)):
    batch: typing.Iterable[str] = sorted(batch)
    binstrs: list[str] = []
    for definition in batch:
        batches_v2_vregidx[definition]
        batches_v2_batchidx[definition] = i
        binstr = definition.split("_")[0]
        binstrs.append(binstr)
        all_instrs.add(binstr)
    rprint(f"i: {i} batch: {batch}")
    batches_v2.append(batch)
    batches_v2_instrs.append(binstrs)

rprint(all_instrs)
rprint(batches_v2)
rprint(batches_v2_instrs)
rprint("batches_v2_vregidx:")
rprint(batches_v2_vregidx)
rprint(batches_v2_batchidx)

# for i, batch in enumerate(nx.topological_generations(GO)):
#     batch = sorted(batch)
#     rprint(f"i: {i} batch: {batch}")

# rprint(f"node2batch: {node2batch}")

"""Minimal jobshop problem."""
# Data.
instrs = tuple(sorted(all_instrs))
instrs_lut = bidict.bidict(zip(instrs, range(len(instrs))))
rprint(instrs)
rprint(instrs_lut)
rprint(instrs_lut.inverse)

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
ticks = [f"t{i}" for i in range(22)]

# list of instructions/definitions that must be made
instr_seq = batches_v2_vregidx

# List of possible operations
operations = ("sha1c", "sha1h", "sha1m", "sha1p", "sha1su0", "sha1su1", "vaddX", "vaddXY", "vaddY")
add_operations = {"vaddX", "vaddY", "vaddXY"}
rprint(add_operations)

# `schedule[e][o][t]` indicates if exec unit `e`
# performs operation `o` on tick `t`
schedule = {
    e: {o: {t: model.new_bool_var(f"schedule_{e}_{o}_{t}") for t in ticks} for o in operations}
    for e in exec_units
}

# A cashier has to be present at all times
# for d in ticks:
#     for s in shifts:
#         model.add(sum(schedule[e]["Cashier"][d][s] for e in exec_units) == 1)

# We need a vaddX once per tick
# for t in ticks:
#     model.add(sum(schedule[e]["vaddXY"][t] for e in exec_units) == 1)

# `instr_ticks[i][t]` indicates if instr/def `i` is produced on tick `t`
instr_ticks = {
    i: {t: model.new_bool_var(f"instr_ticks_{i}_{t}") for t in ticks} for i in instr_seq.rev
}

# All defs must occur once and only once
for i in instr_seq.rev:
    model.add(sum(instr_ticks[i][t] for t in ticks) == 1)

# An exec unit can only perform one operation per tick
for e in exec_units:
    for t in ticks:
        model.add(sum(schedule[e][o][t] for o in operations) <= 1)

# An exec unit can only perform one operation per tick
for e in ("vaddX", "vaddY"):
    for t in ticks:
        model.add(schedule[e]["vaddXY"][t] + schedule[e][e][t] <= 1)

# Some exec units can only perform certain operations
for e in exec_units:
    for o in operations:
        for t in ticks:
            if o not in exec_units[e]:
                model.add(schedule[e][o][t] == 0)

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

solved_schedule = collections.defaultdict(lambda: collections.defaultdict(collections.defaultdict))
for e in exec_units:
    for o in operations:
        for t in ticks:
            solved_schedule[e][o][t] = not not solver.value(schedule[e][o][t])

# rprint(solved_schedule)

solved_instr_ticks = collections.defaultdict(
    lambda: collections.defaultdict(collections.defaultdict)
)
for i in instr_seq.rev:
    for t in ticks:
        solved_instr_ticks[i][t] = solver.value(instr_ticks[i][t])

# rprint(solved_instr_ticks)

# pdf = pd.DataFrame(schedule)
# rprint(pdf.describe())
# rprint(pdf)

# Print the solution
print(f"{' '*3} | " + " | ".join([f"{t:^3}" for t in ticks]) + " | Total |")

print(f"{' '*10} | " + " | ".join(["M | A | E" for t in range(len(ticks))]) + " |       |")

for e in exec_units:
    ticks_execed = sum([solver.value(schedule[e][o][t]) for o in operations for t in ticks])

    print(
        f"{e:<10} | "
        + " | ".join([schedule[e]["sha1p"][t] for t in ticks])
        + " | "
        + f"{ticks_execed:^5}"
        + " | "
    )

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
