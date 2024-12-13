#!/usr/bin/env python3

import argparse
import re
import typing
from collections import OrderedDict

import networkx as nx
import xlsxwriter
from rich import print
from rich.pretty import pprint

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


def get_def_use(
    lines: list[str],
    gfd: typing.TextIO | None,
    dfd: typing.BinaryIO | None,
    Dfd: typing.BinaryIO | None,
    sfd: str | None,
) -> tuple[list[str], list[list[str]]]:
    d = get_line_defs(lines)
    u = get_line_uses(lines)
    sz = len(lines)
    G = nx.DiGraph()
    GE = nx.DiGraph()
    GES = nx.DiGraph()
    GEE = nx.DiGraph()
    for i in range(sz):
        ld = d[i]
        for j, lu in enumerate(u[i]):
            G.add_edge(lu, ld)
            GE.add_edge(lu, ld, label=f"op{j}")
            GES.add_edge(lu.split("_")[0], ld.split("_")[0], label=f"op{j}")
            GEE.add_edge(lu, ld, opnum=j)
    assert G.is_directed()
    assert GE.is_directed()
    assert GES.is_directed()
    assert GEE.is_directed()
    print(f"G: {G}")
    print(f"G.nodes(): {G.nodes()}")
    print(f"G.edges(): {G.edges()}")
    print(f"GE: {GE}")
    print(f"GE.nodes(): {GE.nodes()}")
    print(f"GE.edges(): {GE.edges()}")
    print(f"GES: {GES}")
    print(f"GES.nodes(): {GES.nodes()}")
    print(f"GES.edges(): {GES.edges()}")
    print(f"GEE: {GEE}")
    print(f"GEE.nodes(): {GEE.nodes()}")
    print(f"GEE.edges(): {GEE.edges()}")
    print(f"nx.to_dict_of_dicts(GEE): {nx.to_dict_of_dicts(GEE)}")
    batches: list[list[str]] = []
    for i, batch in enumerate(nx.topological_generations(G)):
        batch = sorted(batch)
        print(f"i: {i} batch: {batch}")
        batches.append(batch)
    print(f"batches: {batches}")
    if dfd is not None:
        nx.nx_agraph.write_dot(G, dfd)
    if Dfd is not None:
        nx.nx_agraph.write_dot(GE, Dfd)
    if sfd is not None:
        workbook = xlsxwriter.Workbook(sfd)
        worksheet = workbook.add_worksheet()
        # Widen the first column to make the text clearer.
        worksheet.set_column("A:A", 20)
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({"bold": True})
        # Write some simple text.
        worksheet.write("A1", "Hello")
        # Text with formatting.
        worksheet.write("A2", "World", bold)
        # Write some numbers, with row/column notation.
        worksheet.write(2, 0, 123)
        worksheet.write(3, 0, 123.456)
        workbook.close()
    return d, u


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


def parse_def_use(lines: list[str], defs: list[str], uses: list[list[str]]) -> None:
    assert len(defs) == len(uses)
    assert len(lines) == len(defs)
    sz = len(lines)
    live_outs: list[set[str]] = []
    live_ins: list[set[str]] = []
    for _ in range(sz):
        live_outs.append(set({}))
        live_ins.append(set({}))
    print(f"live_outs: {live_outs}")
    print(f"live_ins: {live_ins}")
    def_uses = tuple(zip(defs, uses))
    print(f"def_uses: {def_uses}")
    live_out: set[str] = set()
    live_in: set[str] = set()
    for i, line in enumerate(reversed(lines)):
        d = defs[i]
        us = uses[i]
        live_out = set(live_in)
        live_in = live_in.difference({d}).union(set(us))
        # print(f"i[{i:2}]: live_in: {live_in}")
        live_outs[i] = live_out
        live_ins[i] = live_in
    print(f"live_outs: {live_outs} len(live_outs): {len(live_outs)}")
    print(f"live_ins: {live_ins}")
    pprint(live_outs)


def parse(
    ifd: typing.TextIO,
    ofd: typing.TextIO,
    gfd: typing.TextIO | None,
    dfd: typing.BinaryIO | None,
    Dfd: typing.BinaryIO | None,
    sfd: str | None,
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
    defs, uses = get_def_use(func_lines, gfd, dfd, Dfd, sfd)
    parse_def_use(func_lines, defs, uses)
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
    parser.add_argument(
        "-D",
        "--deps",
        dest="deps_dot_file",
        type=argparse.FileType("wb"),
        help="output deps graph dot file.",
    )
    parser.add_argument("-s", "--schedule", dest="schedule_xlsx_file", help="output schedule file.")
    return parser


def main(args: argparse.Namespace):
    ifd = args.in_file
    ofd = args.out_file
    gfd = args.graph_svg_file
    dfd = args.graph_dot_file
    Dfd = args.deps_dot_file
    sfd = args.schedule_xlsx_file
    parse(ifd, ofd, gfd, dfd, Dfd, sfd)


if __name__ == "__main__":
    parser = get_arg_parser()
    args = parser.parse_args()
    main(args)
