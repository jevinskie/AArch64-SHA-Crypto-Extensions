#!/usr/bin/env python3

import argparse
import typing

import attrs
from rich import print


@attrs.define(auto_attribs=True)
class U32:
    MAX: typing.ClassVar[int] = 0xFFFF_FFFF
    _v: int = attrs.field()

    @property
    def v(self) -> int:
        r = self._v
        if not 0 <= r <= U32.MAX:
            raise ValueError(r)
        return r

    @v.setter
    def v(self, n: int) -> None:
        if not 0 <= n <= U32.MAX:
            raise ValueError(n)
        self._v = n


@attrs.define(auto_attribs=True)
class U128:
    MAX: typing.ClassVar[int] = 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF
    _v: int = attrs.field()

    @property
    def v(self) -> int:
        r = self._v
        if not 0 <= r <= U128.MAX:
            raise ValueError(r)
        return r

    @v.setter
    def v(self, n: int) -> None:
        if not 0 <= n <= U128.MAX:
            raise ValueError(n)
        self._v = n


@attrs.define(auto_attribs=True)
class SHA1State:
    _a: U32 = attrs.field()
    _b: U32 = attrs.field()
    _c: U32 = attrs.field()
    _d: U32 = attrs.field()
    _e: U32 = attrs.field()

    @classmethod
    def make_zeroed(cls: type) -> typing.Self:
        return cls(U32(0), U32(0), U32(0), U32(0), U32(0))

    def _validate(self) -> None:
        if not 0 <= self._a.v <= U32.MAX:
            raise ValueError(f"a: 0x{self._a:#010x}")
        if not 0 <= self._b.v <= U32.MAX:
            raise ValueError(f"b: 0x{self._b:#010x}")
        if not 0 <= self._c.v <= U32.MAX:
            raise ValueError(f"c: 0x{self._c:#010x}")
        if not 0 <= self._d.v <= U32.MAX:
            raise ValueError(f"d: 0x{self._d:#010x}")
        if not 0 <= self._e.v <= U32.MAX:
            raise ValueError(f"e: 0x{self._e:#010x}")

    @property
    def abcd(self) -> int:
        self._validate()
        return self._a.v | self._b.v << 32 | self._c.v << 64 | self._d.v << 96

    @abcd.setter
    def abcd(self, n: int) -> None:
        if not 0 <= n <= U128.MAX:
            raise ValueError(n)
        self._a.v = n & U32.MAX
        self._b.v = (n >> 32) & U32.MAX
        self._c.v = (n >> 64) & U32.MAX
        self._d.v = (n >> 96) & U32.MAX

    @property
    def e(self) -> int:
        r = self._e.v
        if not 0 <= r <= U32.MAX:
            raise ValueError(r)
        return r

    @e.setter
    def e(self, n: int) -> None:
        if not 0 <= n <= U32.MAX:
            raise ValueError(n)
        self._e.v = n


def sha1h() -> int:
    return 0


def test_sha1():
    s = SHA1State.make_zeroed()
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
