#!/usr/bin/env python3

import abc
import argparse
import colorsys
import typing

import attrs
import colorful as cf
import colorspacious as clr
import inflect
from rich import print as rprint

infe = inflect.engine()

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
    assert 0 <= r <= 1
    assert 0 <= g <= 1
    assert 0 <= b <= 1
    return r, g, b


def rgb_unpack_int(s: str) -> tuple[float, float, float]:
    r = int(s[1:3], 16) / 255
    g = int(s[3:5], 16) / 255
    b = int(s[5:7], 16) / 255
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
    return r, g, b


palette_a_8_hex = (
    "#0433ff",
    "#00fdff",
    "#00f900",
    "#ff40ff",
    "#ff9300",
    "#942192",
    "#ff2600",
    "#c6ff4c",
)
palette_a_8 = [rgb_unpack(c) for c in palette_a_8_hex]

# https://colorbrewer2.org/?type=qualitative&scheme=Set3&n=7
palette_b_7_hex = ("#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69")
palette_b_7 = [rgb_unpack(c) for c in palette_b_7_hex]

# https://colorbrewer2.org/?type=qualitative&scheme=Set3&n=8
palette_c_8_hex = (
    "#8dd3c7",
    "#ffffb3",
    "#bebada",
    "#fb8072",
    "#80b1d3",
    "#fdb462",
    "#b3de69",
    "#fccde5",
)
palette_c_8 = [rgb_unpack(c) for c in palette_c_8_hex]

# https://colorbrewer2.org/#type=qualitative&scheme=Paired&n=9
palette_d_9_hex = (
    "#a6cee3",
    "#1f78b4",
    "#b2df8a",
    "#33a02c",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#ff7f00",
    "#cab2d6",
)
palette_d_9 = [rgb_unpack(c) for c in palette_d_9_hex]

palette_hex: tuple[str, ...] = tuple()
# palette_hex = palette_a_8_hex
# palette_hex = palette_b_7_hex
palette_hex = palette_c_8_hex
# palette_hex = palette_d_9_hex

palette = [rgb_unpack(c) for c in palette_hex]


def term_color_rgb_int(r: int, g: int, b: int) -> str:
    assert isinstance(r, int)
    assert isinstance(g, int)
    assert isinstance(b, int)
    assert int(r) == r
    assert int(g) == g
    assert int(b) == b
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
    return f"\x1b[38;2;{r};{g};{b}m"


def term_color_rgb_float(r: float, g: float, b: float) -> str:
    assert isinstance(r, float)
    assert isinstance(g, float)
    assert isinstance(b, float)
    assert 0 <= r <= 1
    assert 0 <= g <= 1
    assert 0 <= b <= 1
    r, g, b = int(round(r * 255)), int(round(g * 255)), int(round(b * 255))
    # r, g, b = int(r * 255), int(g * 255), int(b * 255)
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
    return f"\x1b[38;2;{r};{g};{b}m"


def term_color_hsv(h: float, s: float, v: float) -> str:
    assert 0 <= h <= 1
    assert 0 <= s <= 1
    assert 0 <= v <= 1
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return term_color_rgb_float(r, g, b)


def term_color_jch(j: float, c: float, h: float) -> str:
    assert isinstance(j, float)
    assert isinstance(c, float)
    assert isinstance(h, float)
    assert 0 <= j <= 100
    assert 0 <= c <= 300  # normal max of around 150?
    assert 0 <= h < 360
    # start_to_end_fn = clr.cspace_converter("JCh", "sRGB255")
    # rprint(start_to_end_fn.nodes)
    # rprint(f"start_to_end_fn: {start_to_end_fn}")
    r, g, b = clr.cspace_convert((j, c, h), "JCh", "sRGB255")
    # r, g, b = start_to_end_fn((j, c, h))
    # rprint(f"j: {j:.03} c: {c:.03} h: {h}")
    # rprint(f"r: {r} g: {g} b: {b}")
    # color spaces be weird yo
    r = min(max(r, 0.0), 255.0)
    g = min(max(g, 0.0), 255.0)
    b = min(max(b, 0.0), 255.0)
    r, g, b = int(round(r)), int(round(g)), int(round(b))
    # rprint(f"r: {r} g: {g} b: {b}")
    assert isinstance(r, int)
    assert isinstance(g, int)
    assert isinstance(b, int)
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
    return f"\x1b[38;2;{r};{g};{b}m"


def op_hsv(
    n: int, m: int, p: list[tuple[float, float, float]] = palette
) -> tuple[float, float, float]:
    assert 0 <= n < len(p)
    assert 0 <= m < 3
    h, s, v = colorsys.rgb_to_hsv(*p[n])
    # print(f"h: {h:.03} s: {s:.03} v: {v:.03}")
    scale = m / 3
    # scale = math.exp(max(math.log(m + math.nextafter(0, math.inf)), 0) ** 2 + math.log(1 / 3))
    dim_pct = scale / 1
    s *= 1 - dim_pct
    assert 0 <= h <= 1
    assert 0 <= s <= 1
    assert 0 <= v <= 1
    return h, s, v


def op_jch(
    n: int, m: int, p: list[tuple[float, float, float]] = palette
) -> tuple[float, float, float]:
    assert 0 <= n < len(p)
    assert 0 <= m < 3
    j, c, h = clr.cspace_convert(p[n], "sRGB1", "JCh")
    # rprint(f"j: {j:.03} c: {c:.03} h: {h}")
    scale = m / 3
    # scale = math.exp(max(math.log(m + math.nextafter(0, math.inf)), 0) ** 2 + math.log(1/3))
    dim_pct = scale / 1
    # c *= 1 - dim_pct
    c *= 1 - dim_pct
    # j = max(min(j * (1 - dim_pct/1.5), 100.0), 0.0)
    # j /= (m + 1)
    assert 0 <= j <= 100
    assert 0 <= c <= 300  # normal max of around 150?
    assert 0 <= h < 360
    return j, c, h


def op_rgb(n: int, m: int) -> tuple[int, int, int]:
    j, c, h = op_jch(n, m)
    assert isinstance(j, float)
    assert isinstance(c, float)
    assert isinstance(h, float)
    assert 0 <= j <= 100
    assert 0 <= c <= 300  # normal max of around 150?
    assert 0 <= h < 360
    r, g, b = clr.cspace_convert((j, c, h), "JCh", "sRGB255")
    # color spaces be weird yo
    r = min(max(r, 0.0), 255.0)
    g = min(max(g, 0.0), 255.0)
    b = min(max(b, 0.0), 255.0)
    r, g, b = int(round(r)), int(round(g)), int(round(b))
    assert isinstance(r, int)
    assert isinstance(g, int)
    assert isinstance(b, int)
    assert 0 <= r <= 255
    assert 0 <= g <= 255
    assert 0 <= b <= 255
    return r, g, b


def op_color(n: int, m: int, p: list[tuple[float, float, float]] = palette) -> str:
    # return term_color_hsv(*op_hsv(n, m, p))
    # return term_color_rgb_int(*op_rgb(n, m))
    return term_color_jch(*op_jch(n, m, p))


def dump_palette(pal: tuple[tuple[int, int, int]]) -> None:
    for i, c in enumerate(pal):
        tc = term_color_rgb_float(*c)
        print(f"{tc}number {infe.number_to_words(i)}{cf.reset}")


def dump_palette_ops(pal: tuple[tuple[int, int, int]]) -> None:
    for i in range(len(pal)):
        s = f"pal[{i}]: "
        s += " ".join(f"{op_color(i, j, pal)}operand[{j}]{cf.reset}" for j in range(3))
        print(s)


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
    enum: typing.ClassVar[int]


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
    enum = 0


@attrs.define(auto_attribs=True)
class Sha1C(Ru128Iu128u32u128):
    name = "sha1c"
    enum = 1


@attrs.define(auto_attribs=True)
class Sha1M(Ru128Iu128u32u128):
    name = "sha1m"
    enum = 2


@attrs.define(auto_attribs=True)
class Sha1P(Ru128Iu128u32u128):
    name = "sha1p"
    enum = 3


@attrs.define(auto_attribs=True)
class Sha1SU0(Ru128Iu128u128u128):
    name = "sha1su0"
    enum = 4


@attrs.define(auto_attribs=True)
class Sha1SU1(Ru128Iu128u128):
    name = "sha1su1"
    enum = 5


@attrs.define(auto_attribs=True)
class Add(Ru128Iu128u128):
    name = "add"
    enum = 6


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
    for i in range(len(palette)):
        for j in range(3):
            print(f"{op_color(i, j)}i: {i} j: {j} color{cf.reset}")


if __name__ == "__main__":
    parser = get_arg_parser()
    args = parser.parse_args()
    main(args)
