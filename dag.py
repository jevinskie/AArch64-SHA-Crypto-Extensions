#!/usr/bin/env python3

import argparse
import graphlib
import typing

import networkx


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
        o.append(line)
    assert all(map(lambda o: o is not None, line_defs))
    lds = "\n".join(line_defs)
    print(f"line_defs:\n{lds}")
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
    func_lines = rename(func_lines)
    print("".join(func_lines))


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
