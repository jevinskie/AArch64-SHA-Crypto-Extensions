#!/usr/bin/env python3

import argparse

import attrs
from rich import print

U32_MAX = 0xFFFF_FFFF
U128_MAX = 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF


@attrs.define(auto_attribs=True)
class SHA1State:
    _a: int = attrs.field(default=0)
    _b: int = attrs.field(default=0)
    _c: int = attrs.field(default=0)
    _d: int = attrs.field(default=0)
    _e: int = attrs.field(default=0)

    def _validate(self) -> None:
        if not 0 <= self._a <= U32_MAX:
            raise ValueError(f"a: 0x{self._a:#010x}")
        if not 0 <= self._b <= U32_MAX:
            raise ValueError(f"b: 0x{self._b:#010x}")
        if not 0 <= self._c <= U32_MAX:
            raise ValueError(f"c: 0x{self._c:#010x}")
        if not 0 <= self._d <= U32_MAX:
            raise ValueError(f"d: 0x{self._d:#010x}")
        if not 0 <= self._e <= U32_MAX:
            raise ValueError(f"e: 0x{self._e:#010x}")

    @property
    def abcd(self) -> int:
        self._validate()
        return self._a | self._b << 32 | self._c << 64 | self._d << 96

    @abcd.setter
    def abcd(self, n: int) -> None:
        if not 0 <= n <= U128_MAX:
            raise ValueError(n)
        self._a = n & U32_MAX
        self._b = (n >> 32) & U32_MAX
        self._c = (n >> 64) & U32_MAX
        self._d = (n >> 96) & U32_MAX

    @property
    def e(self) -> int:
        r = self._e
        if not 0 <= r <= U32_MAX:
            raise ValueError(r)
        return r

    @e.setter
    def e(self, n: int) -> None:
        if not 0 <= n <= U128_MAX:
            raise ValueError(n)
        self._s[4] = n


def sha1h() -> int:
    return 0


def test_sha1():
    s = SHA1State()
    print(f"s: {s}")
    print(f"s.abcd: {s.abcd}")
    print(f"s.e: {s.e}")
    s.abcd = 0xDEADBEEF_BAADC0DE
    print(f"s.abcd: {hex(s.abcd)}")
    pass


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sha1-arm")
    return parser


def main(args: argparse.Namespace):
    print(f"args: {args}")
    test_sha1()


if __name__ == "__main__":
    parser = get_arg_parser()
    args = parser.parse_args()
    main(args)
