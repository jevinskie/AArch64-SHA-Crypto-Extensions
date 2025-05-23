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
import time
import types
from collections.abc import Mapping, MutableMapping
from itertools import combinations
from typing import Any

import attrs
import bidict
import networkx as nx
import pandas as pd
import tabulate
import xlsxwriter
from more_itertools import all_unique, always_reversible
from ortools.sat.python import cp_model
from rich import print as rprint
from rich.pretty import pprint
from yattag import Doc

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

# width, height for font Menlo 16 points
# from grid-v1-pipeline-raw-rendered.dot
instr_sizes: dict[str, tuple[float, float]] = {
    "sha1c": (1.5243, 1.5278),
    "sha1h": (1.3889, 0.81944),
    "sha1m": (1.5243, 1.5278),
    "sha1p": (1.2535, 1.5278),
    "sha1su0": (1.6597, 1.5278),
    "sha1su1": (1.6597, 1.1736),
    "vaddX": (1.5243, 1.1736),
    "vaddXY": (1.5243, 1.1736),
    "vaddY": (1.5243, 1.1736),
}


# https://github.com/d-krupke/cpsat-primer/blob/main/examples/add_all_different.ipynb
def solve_coloring(
    g: nx.Graph,
    nlut: dict[int, str],
    use_all_different: bool,
    disable_infer_diff: bool = False,
    add_single_all_different: bool = False,
) -> int:
    """
    Solves the graph coloring problem for the given graph.
    :param g: the graph to color
    :param use_all_different: whether to use the all_different constraint or != constraint
    :param disable_infer_diff: whether to disable the all_different constraint inference for !=
    :param add_single_all_different: whether to add a single all_different constraint
    """
    model = cp_model.CpModel()
    # specify valid coloring
    x = [model.new_int_var(0, g.degree[v] - 1, f"v{v}_{nlut[v]}") for v in g.nodes()]
    for v, w in g.edges():
        if use_all_different:
            model.add_all_different([x[v], x[w]])
        else:
            model.add(x[v] != x[w])
    if add_single_all_different:
        # adding a single all_different will disable the inference of all_different
        # for the != constraint and drastically increase the runtime
        v, w = next(iter(g.edges()))
        model.add_all_different([x[v], x[w]])
    # minimize the maximum color
    max_x = model.new_int_var(0, max(g.degree[v] for v in g.nodes()), "xc")
    model.add_max_equality(max_x, x)
    model.minimize(max_x)

    for i, v in enumerate(model.proto.variables):
        rprint(f"Domain (init) for variable {i} '{v.name}' v: {v}")

    # set up solver
    solver = cp_model.CpSolver()
    if disable_infer_diff:
        solver.parameters.infer_all_diffs = False
    solver.parameters.max_time_in_seconds = 300
    solver.parameters.log_search_progress = True
    # solver.log_callback = print
    # pprint(model)
    status = solver.solve(model)
    # rprint(f"status: {status}")
    # pprint(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Solution: {solver.status_name(status)}")
    else:
        print("No solution found.")

    # Statistics.
    print("\nStatistics")
    rprint(f"  - booleans : {solver.num_booleans}")
    rprint(f"  - conflicts: {solver.num_conflicts}")
    rprint(f"  - branches : {solver.num_branches}")
    rprint(f"  - wall time: {solver.wall_time:0.3} s")

    rprint(solver.solution_info())
    rprint(model.model_stats())
    for i, v in enumerate(model.proto.variables):
        rprint(f"Domain for variable {i} '{v.name}' v: {v}")

    ls: list[int] = []
    for v in x:
        # for v2 in v1:
        s = solver.value(v)
        ls.append(s)
        # print(s)
        rprint(f"v: {v} s: {s}")
    rprint(f"max(ls): {max(ls)} +1: {max(ls) + 1}")

    return status


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
_suffix_nd_pattern = r"^(.+?)(N|ND)?(\d+)$"


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


def get_eund(definition: str) -> tuple[str, int, bool]:
    m = re.match(_suffix_nd_pattern, definition)
    s = m.group(1)
    n = int(m.group(3))
    d = True if m.group(2) == "ND" else False
    return s, n, d


good_ordering_top2bot: dict[str, int] = {
    "sha1su0": 0,
    "sha1su1": 1,
    "vaddXY": 2,
    "vaddY": 3,
    "vaddX": 4,
    "sha1h": 5,
    "sha1p": 6,
    "sha1m": 7,
    "sha1c": 8,
}


def gv_instr_sort(instrs: list[str]) -> list[str]:
    return sorted(instrs, key=lambda t: good_ordering_top2bot[t])


def gv_def_sort(defs: list[str]) -> list[str]:
    return sorted(defs, key=lambda d: (good_ordering_top2bot[get_eun(d)[0]], get_eun(d)[1]))


clut_palette_d_9 = {
    "sha1c": 0,
    "sha1h": 2,
    "sha1p": 1,
    "sha1m": 8,
    "sha1su0": 3,
    "sha1su1": 5,
    "vaddX": 6,
    "vaddY": 4,
    "vaddXY": 7,
    "add": 6,
    "abcd": 6,
    "e": 6,
}

clut_palette_c_8 = {
    "sha1c": 0,
    "sha1h": 4,
    "sha1p": 2,
    "sha1m": 7,
    "sha1su0": 3,
    "sha1su1": 6,
    "vaddX": 5,
    "vaddY": 1,
    "vaddXY": 5,
    "add": 5,
    "abcd": 5,
    "e": 5,
}

# clut = clut_palette_d_9
clut = clut_palette_c_8


def gen_table(name: str, num_ops: int, dummy: bool = False) -> str:
    doc, tag, text = Doc().tagtext()
    instr, _, _ = get_eund(name)
    node_hexc = sha1_arm.rgb_pack_int(*sha1_arm.op_rgb(clut[instr], 0, dummy=dummy))

    with tag("table", border="0", cellborder="1", cellspacing="0", bgcolor=node_hexc):
        # First row: overall node label spanning two cells
        with tag("tr"):
            with tag("td", colspan="2"):
                text(name)

        # Second row: Left cell split into operands, right cell is result
        for i in range(num_ops):
            with tag("tr"):
                with tag("td", port=f"op{i}"):
                    text(f"op{i}")
                if i == 0:
                    with tag("td", rowspan=f"{num_ops}", port="res"):
                        text("res")

    return doc.getvalue()


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
rprint(f"G: {G}")

# for i in nx.edge_bfs(G):
#     # inspect(i, all=True)
#     rprint(f"i: {i} i.opnum: {G[i[1]]}")

def_uses: dict[str, tuple[str, ...]] = {}

for definition in G.nodes():
    # rprint(f"definition: {definition} G.in_edges(definition): {G.in_edges(definition)}")
    uses = []
    for op in G.in_edges(definition):
        # rprint(f"op: {G.edges[op]}")
        edges = G.edges[op]
        opnum = edges["opnum"]
        if opnum >= 0:
            uses.append((op[0], opnum))
    uses.sort(key=lambda o: o[1])
    uses = tuple(o[0] for o in uses)
    uses = tuple(
        sorted(
            uses, key=lambda u: (good_ordering_top2bot[get_eun(u)[0]], get_eun(u)[1]), reverse=True
        )
    )
    def_uses[definition] = uses

rprint("def_uses:")
pprint(def_uses)

G2 = nx.DiGraph()
for d in def_uses:
    G2.add_node(d)
for d, us in def_uses.items():
    for u in us:
        G2.add_edge(u, d)

rprint(f"G2: {G2}")
# pprint(nx.to_dict_of_dicts(G2))
# pprint(nx.to_dict_of_lists(G2))  # better

for i, batch in enumerate(nx.topological_generations(G2)):
    batch.sort()
    rprint(f"G2 batch[{i:2}]: {batch}")

G3 = G2.to_undirected()
rprint(f"G3: {G3}")
# pprint(nx.to_dict_of_lists(G3))  # better
# rprint(f"number_of_cliques(G3): {nx.number_of_cliques(G3)}")
# for i, c in enumerate(nx.clique.enumerate_all_cliques(G3)):
#     rprint(f"ci: {i} c: {c}")


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


port_assignments = {
    portize_use(i, p): collections.defaultdict() for p in range(3) for i in clut.keys()
}

port_usage = {
    portize_use(i, p): collections.defaultdict(int) for p in range(3) for i in clut.keys()
}

for i, batch in enumerate(trace):
    rprint(f"batch[{i:2}]: {batch}")
    # rprint(f"batch[{i:2}]: {[x[0] for x in batch]}")
    batch = sorted(batch, key=lambda b: good_ordering_top2bot[get_eun(b[0])[0]], reverse=True)
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
    # rprint(f"batch[{i:2}]: ", end="")
    # print(" ".join([f"{b[3]}{b[0]}{cf.reset}" for b in batch_inputs]))

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
def2tick: dict[str, int] = {}

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
        def2tick[definition] = i
        batches_v2_vregidx[definition]
        batches_v2_batchidx[definition] = i
        # print(f"definition: {definition}")
        binstr, _ = get_eun(definition)
        # print(f"binstr: {binstr}")
        binstrs.append(binstr)
        # duses = [e[0] for e in G.in_edges(definition)]
        duses = []
        for op in G.in_edges(definition):
            # rprint(f"op: {G.edges[op]}")
            edges = G.edges[op]
            opnum = edges["opnum"]
            if opnum >= 0:
                duses.append((op[0], opnum))
        duses = sorted(duses, key=lambda o: o[1])
        duses = tuple(o[0] for o in duses)
        # rprint(f"duses: {duses} G.in_edges(definition): {G.in_edges(definition)}")
        b_uses.update(duses)
        batches_v2_linear.append(definition)
    rprint(f"i: {i} batch: {batch}")
    batches_v2.append(batch)
    batches_v2_instrs.append(binstrs)
    batch_uses.append(list(sorted(b_uses)))

assert all_unique(batches_v2_linear)

print()
rprint("batch defs:")
for i, batch in enumerate(batches_v2):
    bd = []
    for j, instr in enumerate(batch):
        name, _ = get_eun(instr)
        bd.append((instr, op_color(clut[name], 0), good_ordering_top2bot[name]))
    bd.sort(key=lambda d: d[2], reverse=True)
    rprint(f"batch_defs[{i:2}]: ", end="")
    print(" ".join([f"{b[1]}{b[0]}{cf.reset}" for b in bd]))
print()


rprint("batch uses:")
for i, batch in enumerate(batches_v2):
    batch = sorted(batch, key=lambda b: good_ordering_top2bot[get_eun(b)[0]], reverse=True)
    batch_inputs = []
    for j, instr in enumerate(batch):
        name, _ = get_eun(instr)
        for k, p in enumerate(
            sorted(
                def_uses[instr], key=lambda b: good_ordering_top2bot[get_eun(b)[0]], reverse=True
            )
        ):
            pname, _ = get_eun(p)
            batch_inputs.append((name, k, pname, op_color(clut[pname], k)))
    rprint(f"batch_uses[{i:2}]: ", end="")
    print(" ".join([f"{b[3]}{b[0]}{cf.reset}" for b in batch_inputs]))
print()


rprint("batch uses detailed:")
for i, batch in enumerate(batches_v2):
    batch = sorted(batch, key=lambda b: good_ordering_top2bot[get_eun(b)[0]], reverse=True)
    batch_inputs = []
    for j, instr in enumerate(batch):
        name, _ = get_eun(instr)
        for p in sorted(
            def_uses[instr], key=lambda b: good_ordering_top2bot[get_eun(b)[0]], reverse=True
        ):
            pname, _ = get_eun(p)
            batch_inputs.append((p, op_color(clut[pname], 0)))
    rprint(f"batch_uses[{i:2}]: ", end="")
    print(" ".join([f"{b[1]}{b[0]}{cf.reset}" for b in batch_inputs]))
print()

rprint("batch uses detailed delta:")
for i, batch in enumerate(batches_v2):
    batch = sorted(batch, key=lambda b: good_ordering_top2bot[get_eun(b)[0]], reverse=True)
    batch_inputs = []
    for j, instr in enumerate(batch):
        name, _ = get_eun(instr)
        for p in sorted(
            def_uses[instr], key=lambda b: good_ordering_top2bot[get_eun(b)[0]], reverse=True
        ):
            pname, _ = get_eun(p)
            batch_inputs.append((p, op_color(clut[pname], 0)))
    rprint(f"batch_uses[{i:2}]: ", end="")
    print(" ".join([f"{b[1]}{b[0]}{cf.reset}" for b in batch_inputs]))
print()


@attrs.define(auto_attribs=True)
class InstInfo:
    val: str
    uses: list[str] = attrs.field(converter=lambda x: list(x))
    use_delays: list[int] = attrs.field(init=False)
    inst: str = attrs.field(init=False)
    num_ops: int = attrs.field(init=False)
    tick: int = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        self.inst, _ = get_eun(self.val)
        self.num_ops = NumInPorts[self.inst]
        assert self.num_ops == len(self.uses)
        self.tick = def2tick[self.val]


cycle2live: list[set[str]] = [set() for t in range(len(batches_v2))]
cycle2lv_defs: list[set[str]] = [set() for t in range(len(batches_v2))]
cycle2lv_kills: list[set[str]] = [set() for t in range(len(batches_v2))]
val2first_cycle: dict[str, int] = {}
val2last_cycle: dict[str, int] = {}
val2live_range: dict[str, tuple[int, int]] = {}


_live: set[str] = set(batches_v2[-1])
# _live: set[str] = set()
for i, batch in always_reversible(enumerate(batches_v2)):
    cycle2live[i] = set(_live)
    # _live.symmetric_difference_update(batch)
    # _live.difference_update(batch)
    _live = set(batch).difference(_live)
    for ldef in batch:
        _live.update(def_uses[ldef])

for i, batch in enumerate(batches_v2):
    cycle2lv_defs[i] = set(batch)

for i in range(1, len(batches_v2)):
    cycle2lv_kills[i] = cycle2live[i - 1].difference(cycle2live[i])
    # cycle2lv_kills[i] = cycle2live[i].difference(cycle2live[i - 1])
# cycle2lv_kills[-1].difference_update(batches_v2[-1])
#     cycle2lv_kills[i] = cycle2live[i].symmetric_difference(cycle2live[i - 1])
# # cycle2lv_kills[-1].symmetric_difference_update(batches_v2[-1])

for i, batch in enumerate(batches_v2):
    for ldef in batch:
        val2first_cycle[ldef] = i
        for u in def_uses[ldef]:
            if u not in val2first_cycle:
                val2first_cycle[u] = i
            else:
                val2first_cycle[u] = min(val2first_cycle[u], i)

for i, batch in enumerate(batches_v2):
    for ldef in batch:
        if i == 16 and ldef == "sha1pN4":
            print(f"wat: batch: {batch}")
        if ldef not in val2last_cycle:
            val2last_cycle[ldef] = i
        else:
            val2last_cycle[ldef] = max(val2last_cycle[ldef], i)
        for u in def_uses[ldef]:
            if i == 16 and u == "sha1pN4":
                print(f"wat2: batch: {batch} ldef: {ldef} u: {u} uses: {def_uses[ldef]}")
            if u not in val2last_cycle:
                val2last_cycle[u] = i
            else:
                val2last_cycle[u] = max(val2last_cycle[u], i)

val2last_cycle["sha1hN19"] += 1
val2last_cycle["sha1pN9"] += 1

val2live_range = {
    v: (val2first_cycle[v], val2last_cycle[v], val2last_cycle[v] - val2first_cycle[v])
    for v in def_uses
}

tick2num_live: dict[str, int] = {f"t_{i}": 0 for i in range(len(batches_v2))}
for val, rng in val2live_range.items():
    for t in range(rng[0], rng[1]):
        tick2num_live[f"t_{t}"] += 1


tick2live_vals: dict[str, list[str]] = {f"t_{i}": [] for i in range(len(batches_v2))}
for val, rng in val2live_range.items():
    # rprint(f"val: {val} rng: {rng}")
    if rng[0] < rng[1]:
        for t in range(rng[0], rng[1]):
            tick2live_vals[f"t_{t}"].append(val)
            tick2live_vals[f"t_{t}"].sort()
    elif rng[0] == rng[1]:
        tick2live_vals[f"t_{rng[0]}"].append(val)
        tick2live_vals[f"t_{rng[0]}"].sort()
    else:
        raise ValueError(f"rng: {rng}")

# rprint(f"batches_v2: (len: {len(batches_v2)})")
# pprint(batches_v2)
# rprint("batches_v2_linear:")
# rprint(batches_v2_linear)
rprint("batch instrs:")
# pprint(batches_v2_instrs)
for i, batch_instrs in enumerate(batches_v2_instrs):
    batch_instrs.sort(key=lambda i: good_ordering_top2bot[i], reverse=True)
    rprint(f"batch_instrs[{i:2}]: ", end="")
    print(" ".join([f"{op_color(clut[i], 0)}{i}{cf.reset}" for i in batch_instrs]))
print()
# rprint("batches_v2_vregidx:")
# pprint(batches_v2_vregidx)
# rprint("batches_v2_batchidx:")
# pprint(batches_v2_batchidx)
rprint("batch_uses:")
pprint(batch_uses)
rprint("batch_defs:")
pprint(batch_defs)
rprint("cycle2live:")
pprint(cycle2live)
rprint("cycle2lv_defs:")
pprint(cycle2lv_defs)
rprint("cycle2lv_kills:")
pprint(cycle2lv_kills)
rprint("val2first_cycle:")
pprint(val2first_cycle)
rprint("val2last_cycle:")
pprint(val2last_cycle)
rprint("val2live_range:")
pprint(val2live_range)
rprint("tick2num_live:")
pprint(tick2num_live)
rprint("tick2live_vals:")
pprint(tick2live_vals)


GI = nx.Graph()
for d in batches_v2_linear:
    # if d in ("sha1hN19", "sha1pN9"):
    # continue
    GI.add_node(d)
    uses = def_uses[d]
    for u in uses:
        if GI.has_edge(d, u):
            continue
        GI.add_edge(d, u)
for live_set in cycle2live:
    for lv_pair in combinations(live_set, 2):
        # if lv_pair == ("sha1hN19", "sha1pN9") or lv_pair == ("sha1pN9", "sha1hN19"):
        # rprint(f"skipping lv_pair: {lv_pair}")
        # continue
        if GI.has_edge(*lv_pair):
            continue
        GI.add_edge(*lv_pair)

rprint(f"GI: {GI}")
pprint(nx.to_dict_of_lists(GI))
nx.nx_agraph.write_dot(GI, "interference.dot")

GII = nx.Graph()
for d in batches_v2_linear:
    # if d in ("sha1hN19", "sha1pN9"):
    # continue
    GII.add_node(batches_v2_linear.index(d))
    uses = def_uses[d]
    for u in uses:
        di, ui = map(batches_v2_linear.index, (d, u))
        if GII.has_edge(di, ui):
            continue
        GII.add_edge(di, ui)
for live_set in cycle2live:
    for lv_pair in combinations(live_set, 2):
        # if lv_pair == ("sha1hN19", "sha1pN9") or lv_pair == ("sha1pN9", "sha1hN19"):
        # rprint(f"skipping lv_pair: {lv_pair}")
        # continue
        a, b = map(batches_v2_linear.index, lv_pair)
        if GII.has_edge(a, b):
            continue
        GII.add_edge(a, b)


rprint(f"GII: {GII}")
pprint(nx.to_dict_of_lists(GII))
nx.nx_agraph.write_dot(GII, "interference-int.dot")

tstart = time.process_time_ns()
res = solve_coloring(GII, batches_v2_linear, False)
tend = time.process_time_ns()
rprint("solve_coloring(GI, False)")
rprint(f"took {tend - tstart:_} nanoseconds")
rprint(f"res:\n{res}")


def write_live_vals(sched_info: Any, out_path: str) -> None:
    s = ""
    for i, batch in always_reversible(enumerate(batches_v2)):
        for ldef in batch:
            s += f'box "{ldef}"\n'
            s += "move\n"
    # s += 'box "sha1su0_XX" fit\n'
    with open(out_path, "w") as f:
        f.write(s)


def write_live_vals_xlsx(sched_info: Any, out_path: str) -> None:
    s = ""
    for i, batch in always_reversible(enumerate(batches_v2)):
        for ldef in batch:
            s += f'box "{ldef}"\n'
            s += "move\n"
    wb = xlsxwriter.Workbook(out_path)
    ws = wb.add_worksheet("Live Values")
    bold = wb.add_format({"bold": True})
    for i, val in enumerate(batches_v2_linear):
        ws.write(0, i, val, bold)
    for val, rng in val2live_range.items():
        for t in range(rng[0], rng[1]):
            ws.write(t + 1, batches_v2_linear.index(val), "X")
    wb.close()


PG = nx.DiGraph(outputorder="edgesfirst")
for i, batch in enumerate(batches_v2):
    for ldef in batch:
        ldef_instr, _ = get_eun(ldef)
        PG.add_node(ldef, label=ldef_instr)
        # defs_port_uses[ldef] = [None] * NumInPorts[ldef_instr]
        ldef_uses = sorted(u for u, ui in G[ldef].items() if ui["opnum"] >= 0)
        # rprint(f"ldef: {ldef} ldef_uses: {ldef_uses}")
        # for ldef_user, ldef_user_opnum in ldef_uses.items():
        # defs_port_uses[ldef_user][ldef_user_opnum] = ldef

# nx.nx_agraph.write_dot(PG, "pipeline.dot")

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

for instr, port_uses in instr_port_uses.items():
    for port in port_uses:
        if port is None:
            continue
        else:
            for src_instr in port:
                port[src_instr] = dict(sorted(port[src_instr].items(), key=lambda o: o[0]))

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

# rprint("_instr_op_delays:")
# pprint(_instr_op_delays)

instr_op_delays: dict[str, dict[int, int]] = {}
for instr, delays in _instr_op_delays.items():
    idelays = dict(sorted({int(d[1:]): c for d, c in delays.items()}.items()))
    instr_op_delays[instr] = idelays
instr_op_delays = dict(sorted(instr_op_delays.items()))

rprint("instr_op_delays:")
pprint(instr_op_delays)


def get_node(
    ssa_def: str, instr: str, cycle: int, num_ops: int, bubble: bool = False
) -> tuple[str, str]:
    node_name = f"{instr}T{cycle}"
    table_html = gen_table(ssa_def, num_ops, dummy=bubble)
    style = ""
    # style = "" if not bubble else " style=invis,"
    cmt = "REAL" if not bubble else "BUBBLE"
    return (
        node_name,
        f'{node_name} [group="{instr}",shape=none,{style} label=<{table_html}>]; # {cmt}',
    )
    # vaddX [label="vaddX|{{<f0> op0| <f1> op2}| <f2> res}", shape=record];
    ops = "|".join(f"<op{n}> op{n}" for n in range(num_ops))
    label = f"{ssa_def}|{{{{{ops}}}|<res> res}}"
    style = 'style="filled"' if not bubble else 'style="invis"'
    hexc = sha1_arm.rgb_pack_int(*sha1_arm.op_rgb(clut[instr], 0))
    return (
        node_name,
        f'{node_name} [label="{label}", fillcolor="{hexc}", {style}, shape=record]; # {cmt}',
    )


def write_pipeline_dot(sched_info: object, out_path: str) -> None:
    s = ""
    s += "strict "
    s += "digraph g {\n"
    # s += "\tcompound=true;\n"
    # s += '\tpackmode="node";\n'
    # s += '\tpackmode="cluster";\n'
    # s += '\tpackmode="graph";\n'
    # s += "\tmode=hier;\n"
    # s += "\tmode=ipsep;\n"
    # s += "\tnewrank=true;\n"
    # s += "\tpack=false;\n"
    # s += "\tclusterrank=global;\n"
    # s += "\tesep=150;\n"
    # s += "\tsep=300;\n"
    s += "\trankdir=LR;\n"
    # s += "\tcenter=true;\n"
    # s += "\tmargin=100;\n"
    # s += "\toverlap=false;\n"
    s += "\tranksep=2;\n"
    s += "\tsearchsize=99999;\n"
    # s += "\tsplines=polyline\n"
    # s += "\tsplines=ortho\n"
    # s += "\tsplines=curved;\n"
    # s += "\tmclimit=9999;\n"
    s += "\tnode [fontsize=16, fontname=Menlo];\n"
    num_cycles = len(batches_v2)
    def2node: dict[str, str] = {}
    cycle2instr2node: dict[int, dict[str, str]] = {c: {} for c in range(num_cycles)}
    dummy_count: dict[str, int] = {i: 0 for i in all_instrs}
    super_nodes: list[str] = []
    edges: list[str] = []
    # super_node_order_edges: list[str] = []
    # intra_cycle_order_edges: list[str] = []
    # inter_cycle_order_edges: list[str] = []
    for i, batch in enumerate(batches_v2):
        nodes: list[str] = [""] * len(all_instrs)
        intra_cycle_order_edges: list[str] = []
        real_instrs = set()
        # binstrs: list[str] = []
        prev_instr = None
        sorted_batch_instrs = [(d, get_eun(d)[0]) for d in batch]
        sorted_batch_instrs = [
            t[0] for t in sorted(sorted_batch_instrs, key=lambda t: good_ordering_top2bot[t[1]])
        ]
        for d in sorted_batch_instrs:
            instr, _ = get_eun(d)
            real_instrs.add(instr)
            instr_idx = all_instrs.index(instr)
            node_name, node_dot = get_node(d, instr, i, NumInPorts[instr])
            nodes[instr_idx] = f"\t{node_dot}"
            def2node[d] = node_name
            cycle2instr2node[i][instr] = node_name
            if prev_instr is not None:
                intra_cycle_order_edges.append(
                    f"\t{prev_instr}T{i} -> {instr}T{i} [constraint=true,color=red,style=invis]; # intra-cycle"
                )
            prev_instr = instr
        # rprint(f"partial nodes[{i}]: {nodes}")
        dummy_instrs = all_instrs_set.difference(real_instrs)
        # rprint(f"dummy_instrs[{i}]: {dummy_instrs}")
        for stub_instr in dummy_instrs:
            # rprint(f"stub_instr[{i}]: {stub_instr}")
            instr_idx = all_instrs.index(stub_instr)
            # rprint(f"stub_instr_idx[{i}]: {instr_idx}")
            dc = dummy_count[stub_instr]
            dummy_count[stub_instr] += 1
            d = f"{stub_instr}ND{dc}"
            node_name, node_dot = get_node(d, stub_instr, i, NumInPorts[stub_instr], bubble=True)
            # nodes[instr_idx] = f"\t{node_dot}"
            # def2node[d] = node_name
            # cycle2instr2node[i][stub_instr] = node_name
        # rprint(f"full nodes[{i}]: {nodes}")
        # for j in range(len(all_instrs) - 1):
        #     # intra_cycle_order_edges.append(
        #     #     f"\t{all_instrs[j]}T{i} -> {all_instrs[j+1]}T{i} [constraint=false,weight=100000,color=red]; # intra-cycle"
        #     # )
        #     intra_cycle_order_edges.append(
        #         f"\t{all_instrs[j+1]}T{i} -> {all_instrs[j]}T{i} [constraint=false,weight=100000,color=red]; # intra-cycle"
        #     )
        sn = f'subgraph t{i} {{\n\trank=same;\n\t# rankdir=TD;\n\tlabel="t_{i}";\n\tfontname=Menlo;\n'
        sn += "\n".join(nodes)
        sn += "\n\n\t# intra-cycle order edges\n"
        sn += "\n".join(intra_cycle_order_edges)
        sn += "\n}"
        super_nodes.append(sn)
    # rprint(f"def2node: {def2node}")
    for d, uses in defs_port_uses.items():
        for pnum, u in enumerate(uses):
            if u is None:
                continue
            edges.append(
                # f'\t{def2node[u]}:res -> {def2node[d]}:op{pnum} [sametail="{def2node[u]}_res"]'
                f"\t{def2node[u]}:res:e -> {def2node[d]}:op{pnum}:w [weight=0];"
            )
    # super_node_order_edges = [
    #     f"\tcluster_t{t} -> cluster_t{t + 1};" for t in range(len(batches_v2) - 1)
    # ]
    # super_node_order_edges = [
    #     f"\t{}{t} -> cluster_t{t + 1};" for t in range(len(batches_v2) - 1)
    # ]
    # rprint(f"cycle2instr2node: {cycle2instr2node}")
    # inter-cycle makes staircase

    # inter_cycle_order_edges = [
    #     # f'\t{cycle2instr2node[c][i]} -> {cycle2instr2node[c+1][i]} [constraint=true,weight=10000,color=purple,style=invis,lhead="cluster_t{c+1}",ltail="cluster_t{c}"]; # inter-cycle'
    #     f"\t{cycle2instr2node[c][i]} -> {cycle2instr2node[c+1][i]} [constraint=true,weight=10000,color=purple]; # inter-cycle"
    #     for c in range(num_cycles - 1)
    #     for i in all_instrs
    # ]

    # inter_cycle_order_edges += [
    #     f"\t{cycle2instr2node[c+1][i]} -> {cycle2instr2node[c][i]} [constraint=true,weight=10000,color=purple]; # inter-cycle"
    #     for c in range(num_cycles - 1)
    #     for i in all_instrs
    # ]
    s += "\t# super nodes\n"
    s += "\n".join(super_nodes)
    s += "\n\n\n"
    s += "\t# super node order edges\n"
    # s += "\n".join(super_node_order_edges)
    s += "\n\n\n"
    # s += "\t# intra-cycle order edges\n"
    # s += "\n".join(intra_cycle_order_edges)
    s += "\n\n\n"
    s += "\t# inter-cycle order edges\n"
    # s += "\n".join(inter_cycle_order_edges)
    s += "\n\n\n"
    s += "\t# edges\n"
    s += "\n".join(edges)
    s += "\n}\n"
    with open("pipeline-raw.dot", "w") as f:
        f.write(s)
    ps = dot_format(s)
    with open(out_path, "w") as f:
        f.write(ps)


write_pipeline_dot(object(), "pipeline.dot")
write_live_vals(object(), "live-vals.pic")
write_live_vals_xlsx(object(), "live-vals.xlsx")

# rprint(G["sha1hN16"])

# ffmpeg -i input.mp4 -filter_complex "[0]reverse[r];[0][r]concat=n=2:v=1:a=0,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif


# print("palette_a_8")
# sha1_arm.dump_palette(sha1_arm.palette_a_8)
# print("\n\n\n")
# print("palette_b_7")
# sha1_arm.dump_palette(sha1_arm.palette_b_7)
# print("\n\n\n")
# print("palette_c_8")
# sha1_arm.dump_palette(sha1_arm.palette_c_8)
# print("\n\n\n")
# print("palette_d_9")
# sha1_arm.dump_palette(sha1_arm.palette_d_9)
# print("\n\n\n")

# print("palette_a_8")
# sha1_arm.dump_palette_ops(sha1_arm.palette_a_8)
# print("\n\n\n")
# print("palette_b_7")
# sha1_arm.dump_palette_ops(sha1_arm.palette_b_7)
# print("\n\n\n")
# print("palette_c_8")
# sha1_arm.dump_palette_ops(sha1_arm.palette_c_8)
# print("\n\n\n")
# print("palette_d_9")
# sha1_arm.dump_palette_ops(sha1_arm.palette_d_9)
# print("\n\n\n")

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
