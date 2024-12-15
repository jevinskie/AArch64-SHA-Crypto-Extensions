#!/usr/bin/env python3

import argparse
import re
import typing
from collections import OrderedDict

import matplotlib as mpl
import networkx as nx

mpl
# mpl.use("svg")

identifier_pattern = r"[%][_a-zA-Z0-9][a-zA-Z$._0-9]*"


def substitute_num_val(s: str, old: str, new: str) -> str:
    if not str.isdigit(old):
        return s
    pattern = rf"%{old}(?!\d)"
    return re.sub(pattern, f"%{new}", s)


def substitute_num_vals(s: str, name_map: OrderedDict[str, str]) -> str:
    for on, nn in reversed(name_map.items()):
        s = substitute_num_val(s, on, nn)
    return s


def get_line_defs(lines: list[str]) -> list[str]:
    line_defs: list[str | None] = [None] * (len(lines))
    for i, line in enumerate(lines):
        assert line[0] == "%" or line.startswith("ret ")
        if line[0] == "%":
            name = line.split()[0][1:]
            line_defs[i] = name
    line_defs[-1] = "res"
    return line_defs


def get_line_use_helper(pline: str) -> list[str]:
    r: list[str] = []
    matches = re.findall(identifier_pattern, pline)
    if matches is None:
        return r
    for m in matches:
        if m.startswith("%struct."):
            continue
        r.append(m[1:])
    return r


def get_line_uses(lines: list[str]) -> list[list[str]]:
    u: list[list[str]] = [[] for i in range(len(lines))]
    for i, line in enumerate(lines):
        assert line[0] == "%" or line.startswith("ret ")
        ls = line.split()
        if line[0] == "%":
            u[i] = get_line_use_helper(" ".join(ls[1:]))
        else:
            u[i] = get_line_use_helper(line)
    return u


def get_operation(line: str) -> str:
    if line.startswith("ret "):
        return "ret"
    assert line.startswith("%")
    ls = line.split()
    assert ls[1] == "="
    if ls[2] == "call":
        op = next(filter(lambda s: s[0] == "@", ls))[1:].split("(")[0]
        assert op.startswith("llvm.")
        op = op.split(".")[-1]
        if op == "immediate":
            op = "imm"
        return op
    else:
        op = ls[2]
        if op == "shufflevector":
            op = "shuf"
        elif op == "insertelement":
            op = "inselm"
        elif op == "insertvalue":
            op = "insval"
        return op


def get_def_use(lines: list[str], gfd: typing.TextIO | None, dfd: typing.TextIO | None) -> None:
    d = get_line_defs(lines)
    u = get_line_uses(lines)
    print(f"uses: {u}")
    print(f"defs: {d}")
    sz = len(lines)
    ops: list[str] = [get_operation(line) for line in lines]
    print(f"ops: {ops}")
    print(f"set(ops): {set(ops)}")
    G = nx.DiGraph()
    for i in range(sz):
        ld = d[i]
        for lu in u[i]:
            G.add_edge(lu, ld)
    assert G.is_directed()
    print(f"G: {G}")
    print(f"G.nodes(): {G.nodes()}")
    print(f"G.edges(): {G.edges()}")
    # pos = nx.spring_layout(G)
    # nodes = nx.draw_networkx_nodes(G, pos)
    # edges = nx.draw_networkx_edges(G, pos)
    if dfd is not None:
        nx.nx_agraph.write_dot(G, dfd)


def rename(lines: list[str]) -> list[str]:
    op_cnt: dict[str, int] = {
        "add": 0,
        "imm": 0,
        "inselm": 0,
        "insval": 0,
        "ret": 0,
        "sha1c": 0,
        "sha1h": 0,
        "sha1m": 0,
        "sha1p": 0,
        "sha1su0": 0,
        "sha1su1": 0,
        "shuf": 0,
    }
    line_defs = get_line_defs(lines)
    new_line_defs: list[list | None] = [None] * (len(lines) - 1)
    n = 0
    for i in range(len(new_line_defs)):
        od = line_defs[i]
        assert od is not None
        if str.isdigit(od):
            op = get_operation(lines[i])
            new_line_defs[i] = f"{op}_{op_cnt[op]}"
            op_cnt[op] += 1
            n += 1
        else:
            new_line_defs[i] = od
    sorted_renames: list[tuple[str, str]] = sorted(
        [t for t in zip(line_defs, new_line_defs) if t[0] != t[1]], key=lambda x: int(x[0])
    )
    print(f"line_defs: {line_defs}")
    print(f"new_line_defs: {new_line_defs}")
    print(f"sorted_renames: {sorted_renames}")
    o: list[str] = []
    for i, line in enumerate(lines):
        name_map: OrderedDict[str, str] = OrderedDict(reversed(sorted_renames[:i]))
        if line[0] == "%":
            ls = line.split()
            new_name = new_line_defs[i]
            new_line = " ".join(ls[1:])
            new_line = substitute_num_vals(new_line, name_map)
            new_line = f"%{new_name} {new_line}\n"
            o.append(new_line)
        else:
            new_line = substitute_num_vals(line, name_map)
            o.append(new_line)
    assert len(lines) == len(o)
    return o


def parse(
    ifd: typing.TextIO, ofd: typing.TextIO, gfd: typing.TextIO | None, dfd: typing.TextIO | None
) -> None:
    lines = ifd.readlines()
    func_start_line: int | None = None
    func_end_line: int | None = None
    for i in range(len(lines)):
        if "@sha1_arm_unrolled_compress_one" in lines[i]:
            func_start_line = i
            continue
        if lines[i] == "}\n":
            func_end_line = i
            break
    assert func_start_line is not None
    assert func_end_line is not None

    func_lines = lines[func_start_line + 1 : func_end_line]
    for i in range(len(func_lines)):
        assert func_lines[i].startswith("  ")
        func_lines[i] = func_lines[i][2:]
    func_lines = rename(func_lines)
    get_def_use(func_lines, gfd, dfd)
    print("".join(lines[: func_start_line + 1]), end="", file=ofd)
    print("".join(["  " + v for v in func_lines]), end="", file=ofd)
    print("".join(lines[func_end_line:]), end="", file=ofd)


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dag")
    parser.add_argument(
        "-i",
        "--in",
        dest="in_file",
        type=argparse.FileType("r"),
        required=True,
        help="LLVM IR input file.",
    )
    parser.add_argument(
        "-o",
        "--out",
        dest="out_file",
        type=argparse.FileType("w"),
        required=True,
        help="output file.",
    )
    parser.add_argument(
        "-g",
        "--graph",
        dest="graph_svg_file",
        type=argparse.FileType("w"),
        help="output graph SVG file.",
    )
    parser.add_argument(
        "-d",
        "--dot",
        dest="graph_dot_file",
        type=argparse.FileType("wb"),
        help="output graph dot file.",
    )
    return parser


def main(args: argparse.Namespace):
    ifd = args.in_file
    ofd = args.out_file
    gfd = args.graph_svg_file
    dfd = args.graph_dot_file
    parse(ifd, ofd, gfd, dfd)


if __name__ == "__main__":
    parser = get_arg_parser()
    args = parser.parse_args()
    main(args)
