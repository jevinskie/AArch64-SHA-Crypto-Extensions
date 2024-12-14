#!/usr/bin/env python3

import argparse
import graphlib
import re
import typing
from collections import OrderedDict

import networkx


def substitute_val(s: str, old: str, new: str) -> str:
    if not str.isdigit(old):
        return s
    pattern = rf"%{old}(?!\d)"
    return re.sub(pattern, f"%{new}", s)


def substitute_vals(s: str, name_map: OrderedDict[str, str]) -> str:
    for on, nn in reversed(name_map.items()):
        if on == "136":
            print(f"on: {on} nn: {nn}")
            s2 = substitute_val(s, on, nn)
            print(f"s2: '{s2}' s: '{s}'")
        s = substitute_val(s, on, nn)
    return s


def rename(lines: list[str]) -> list[str]:
    o: list[str] = []
    names: set[str] = set()
    line_defs: list[str | None] = [None] * (len(lines) - 1)
    for i, line in enumerate(lines):
        assert line[0] == "%" or line.startswith("ret ")
        if line[0] == "%":
            name = line.split()[0][1:]
            line_defs[i] = name
            print(f"name: {name}")
            names.add(name)
    assert all(map(lambda o: o is not None, line_defs))
    new_line_defs: list[list | None] = [None] * (len(lines) - 1)
    n = 0
    for i in range(len(new_line_defs)):
        od = line_defs[i]
        assert od is not None
        if str.isdigit(od):
            new_line_defs[i] = str(n)
            n += 1
        else:
            new_line_defs[i] = od
    sorted_renames: list[tuple[str, str]] = sorted(
        [t for t in zip(line_defs, new_line_defs) if t[0] != t[1]],
        key=lambda x: int(x[0]),
        reverse=True,
    )
    # print(f"sorted: {sorted_renames}")
    # name_map: OrderedDict[str, str] = OrderedDict(sorted_renames)
    # print(f"name_map: {name_map}")
    for i, line in enumerate(lines):
        name_map: OrderedDict[str, str] = OrderedDict(sorted_renames[:i])
        if line[0] == "%":
            ls = line.split()
            new_name = new_line_defs[i]
            new_line = " ".join(ls[1:])
            new_line = substitute_vals(new_line, name_map)
            new_line = f"%{new_name} {new_line}\n"
            o.append(new_line)
        else:
            new_line = substitute_vals(line, name_map)
            o.append(new_line)
    return o


def parse(ifd: typing.TextIO, ofd: typing.TextIO) -> None:
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

    print(f"func_start_line: {func_start_line} func_end_line: {func_end_line}")
    func_lines = lines[func_start_line + 1 : func_end_line]
    for i in range(len(func_lines)):
        assert func_lines[i].startswith("  ")
        func_lines[i] = func_lines[i][2:]
    print(f"len1 func_lines: {len(func_lines)}")
    func_lines = rename(func_lines)
    print(f"len2 func_lines: {len(func_lines)}")
    sl = lines[: func_start_line + 1]
    print(f"sl[-1]: '{sl[-1]}'")
    el = lines[func_end_line:]
    print(f"el[0]: '{el[0]}'")
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
    return parser


def main(args: argparse.Namespace):
    ifd = args.in_file
    ofd = args.out_file
    parse(ifd, ofd)
    networkx
    graphlib
    pass


if __name__ == "__main__":
    parser = get_arg_parser()
    args = parser.parse_args()
    main(args)
