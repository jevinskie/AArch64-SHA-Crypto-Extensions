#!/usr/bin/env python3

import abc
import argparse
import colorsys
import typing

import attrs
import colorful as cf
from rich import print as rprint

cf.use_true_colors()
cf.update_palette(
    {
        "slateblue": "#6A5ACD",
        "palegreen": "#98FB98",
        "fuschia": "#FF00FF",
        "lawngreen": "#7CFC00",
    }
)


def rgb_unpack(s: str) -> tuple[float, float, float]:
    r = int(s[1:3], 16) / 255
    g = int(s[3:5], 16) / 255
    b = int(s[5:7], 16) / 255
    return r, g, b


palette = [
    rgb_unpack(c)
    for c in ("#0433ff", "#00fdff", "#00f900", "#ff40ff", "#ff9300", "#942192", "#ff2600")
]


def term_color_hsv(h: float, s: float, v: float) -> str:
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r, g, b = int(round(r * 255)), int(round(g * 255)), int(round(b * 255))
    return f"\x1b[38;2;{r};{g};{b}m"


def num_color(n: int, m: int) -> str:
    assert n < len(palette)
    h, s, v = colorsys.rgb_to_hsv(*palette[n])
    scale = m / 3
    dim_val = scale / 1.5
    s -= dim_val
    if n in (1, 2):
        v -= dim_val
    return term_color_hsv(h, s, v)


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


Integral = type[U32] | type[U128]


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


def f_is_ty(t: type) -> typing.Callable[object, [bool]]:
    def is_ty(obj: object, attr: attrs.Attribute, val: object) -> bool:
        rprint(f"obj: {obj} attr: {attr} val: {val} t: {t}")
        assert attr.type is t
        assert isinstance(val, t)
        return isinstance(val, t)

    return is_ty


def f_is_tys(ts: list[type]) -> typing.Callable[list[object], [bool]]:
    def is_tys(objs: list[object], attr: attrs.Attribute, val: object) -> bool:
        rprint(f"objs: {objs} attr: {attr} val: {val} ts: {ts}")
        assert attr.type is ts
        return all([type(o) is t for o, t in zip(objs, ts)])

    return is_tys


# def opt_instance_of(t: type | list[type]) -> typing.Callable[object | list[object], [bool]]:
#     def f(o: object | list[object], attr: attrs.Attribute, val: object) -> bool:
#         if val is None:
#             return True
#         return attrs.validators.instance_of(t)


@attrs.define(auto_attribs=True)
class Value:
    name: str
    producer: "Instr"
    consumer: "Instr"
    consumer_op: int


@attrs.define(auto_attribs=True)
class U32Value(Value): ...


OptU32Value = U32Value | None


@attrs.define(auto_attribs=True)
class U128Value(Value): ...


OptU128Value = U128Value | None

IntValue = U32Value | U128Value

OptIntValue = IntValue | None


class InstrABC(abc.ABC):
    name: typing.ClassVar[str]


@attrs.define(auto_attribs=True)
class Instr(InstrABC):
    cycle: int | None


@attrs.define(auto_attribs=True)
class U32Input(Instr):
    name = "input32"
    consumes_ty: typing.ClassVar = tuple()
    produces_ty: typing.ClassVar = U32Value
    produces: U32Value = attrs.field(validator=f_is_ty(U32Value))
    consumes: tuple = attrs.field(
        default=tuple(), validator=lambda o: type(o) is tuple and o == tuple()
    )


@attrs.define(auto_attribs=True)
class U128Input(Instr):
    name = "input128"
    consumes_ty: typing.ClassVar = tuple()
    produces_ty: typing.ClassVar = U128Value
    produces: U128Value = attrs.field(validator=f_is_ty(U128Value))
    consumes: tuple = attrs.field(
        default=tuple(), validator=lambda o: isinstance(o, tuple) and o == tuple()
    )


@attrs.define(auto_attribs=True)
class Ru32Iu32(Instr):
    consumes_ty: typing.ClassVar = (U32Value,)
    produces_ty: typing.ClassVar = U32Value
    produces: U32Value = attrs.field(validator=attrs.validators.instance_of(U32Value))
    consumes: tuple[OptU32Value] = attrs.field(
        default=(None,), validator=attrs.validators.instance_of(U32Value)
    )


@attrs.define(auto_attribs=True)
class Ru128Iu128u32u128(Instr):
    consumes_ty: typing.ClassVar = (U128Value, U32Value, U128Value)
    produces_ty: typing.ClassVar = U128Value
    produces: U128Value = attrs.field(validator=attrs.validators.instance_of(U128Value))
    consumes: tuple[OptU128Value, OptU32Value, OptU128Value] = attrs.field(
        default=(None, None, None),
        validator=attrs.validators.instance_of((U128Value, U32Value, U128Value)),
    )


@attrs.define(auto_attribs=True)
class Ru128Iu128u128u128(Instr):
    consumes_ty: typing.ClassVar = (U128Value, U128Value, U128Value)
    produces_ty: typing.ClassVar = U128Value
    produces: U128Value = attrs.field(validator=attrs.validators.instance_of(U128Value))
    consumes: tuple[OptU128Value, OptU128Value, OptU128Value] = attrs.field(
        default=(None, None, None),
        validator=attrs.validators.instance_of((U128Value, OptU128Value, U128Value)),
    )


@attrs.define(auto_attribs=True)
class Ru128Iu128u128(Instr):
    consumes_ty: typing.ClassVar = (U128Value, U128Value)
    produces_ty: typing.ClassVar = U128Value
    produces: U128Value = attrs.field(validator=attrs.validators.instance_of(U128Value))
    consumes: tuple[OptU128Value, OptU128Value] = attrs.field(
        default=(None, None, None), validator=attrs.validators.instance_of((U128Value, U128Value))
    )


@attrs.define(auto_attribs=True)
class Sha1H(Ru32Iu32):
    name = "sha1h"


@attrs.define(auto_attribs=True)
class Sha1C(Ru128Iu128u32u128):
    name = "sha1c"


@attrs.define(auto_attribs=True)
class Sha1M(Ru128Iu128u32u128):
    name = "sha1m"


@attrs.define(auto_attribs=True)
class Sha1P(Ru128Iu128u32u128):
    name = "sha1p"


@attrs.define(auto_attribs=True)
class Sha1SU0(Ru128Iu128u128u128):
    name = "sha1su0"


@attrs.define(auto_attribs=True)
class Sha1SU1(Ru128Iu128u128):
    name = "sha1su1"


@attrs.define(auto_attribs=True)
class Add(Ru128Iu128u128):
    name = "add"


def test_sha1():
    s = SHA1State.make_zeroed()
    rprint(f"s: {s}")
    rprint(f"s.abcd: {s.abcd}")
    rprint(f"s.e: {s.e}")
    s.abcd = 0xDEADBEEF_BAADC0DE
    rprint(f"s.abcd: {hex(s.abcd)}")
    pass


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sha1-arm")
    return parser


def main(args: argparse.Namespace):
    rprint(f"args: {args}")
    test_sha1()
    for i in range(7):
        for j in range(3):
            print(f"{num_color(i, j)}i: {i} j: {j} color{cf.reset}")


if __name__ == "__main__":
    parser = get_arg_parser()
    args = parser.parse_args()
    main(args)
