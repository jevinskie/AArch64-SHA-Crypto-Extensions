#undef NDEBUG
#include <cassert>

#include <arm_neon.h>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>

// Wojciech Muła
// https://web.archive.org/web/20240913163942/https://0x80.pl/articles/convert-to-hex.html

constexpr uint32_t packed(uint8_t b) {
    return b * 0x01010101u;
}

uint32_t nibbles_to_hex_swar(uint32_t nibbles) {
    assert((nibbles & 0xf0f0'f0f0u) == 0);

    const uint32_t ascii09    = nibbles + packed('0');
    const uint32_t correction = packed('a' - '0' - 10);

    const uint32_t tmp  = nibbles + packed(128 - 10);
    const uint32_t msb  = tmp & packed(0x80);
    const uint32_t mask = msb - (msb >> 7);

    return ascii09 + (mask & correction);
}

constexpr uint32_t nibble_expand32_naive(const uint32_t x) {
    if ((uint32_t)x > (uint32_t)UINT16_MAX) {
        __builtin_unreachable();
    }

    const uint32_t n0 = x & 0x0f;
    const uint32_t n1 = (x >> 4) & 0x0f;
    const uint32_t n2 = (x >> 8) & 0x0f;
    const uint32_t n3 = (x >> 12) & 0x0f;

    return n3 | (n2 << 8) | (n1 << 16) | (n0 << 24);
}

constexpr uint64_t nibble_expand64_naive(const uint32_t x) {
    if ((uint64_t)x > (uint64_t)UINT32_MAX) {
        __builtin_unreachable();
    }

    const uint64_t n0 = x & 0x0f;
    const uint64_t n1 = (x >> 4) & 0x0f;
    const uint64_t n2 = (x >> 8) & 0x0f;
    const uint64_t n3 = (x >> 12) & 0x0f;
    const uint64_t n4 = (x >> 16) & 0x0f;
    const uint64_t n5 = (x >> 20) & 0x0f;
    const uint64_t n6 = (x >> 24) & 0x0f;
    const uint64_t n7 = (x >> 28) & 0x0f;

    return n7 | (n6 << 8) | (n5 << 16) | (n4 << 24) | (n3 << 32) | (n2 << 40) | (n1 << 48) | (n0 << 56);
}

[[gnu::noinline]] void u32_to_hex(const uint32_t n, char (&s)[9]) {
    const uint64_t mask_lo = 0x00ff'00ff'00ff'00ffllu;
    const uint64_t mask_hi = 0xff00'ff00'ff00'ff00llu;
    printf("mask_lo: 0x%016llx\n", mask_lo);
    printf("mask_hi: 0x%016llx\n", mask_hi);
#if 0
    for (int i = 0; i < 8; ++i) {
        s[i] = 'a' + i;
    }
#endif
#if 0
    const uint32_t nlo = nibbles_to_hex_swar(n & 0x0f0f'0f0fu);
    std::memcpy(s, &nlo, sizeof(nlo));
#endif
#if 1
    const uint32_t nhi = nibbles_to_hex_swar((n >> 4) & 0x0f0f'0f0fu);
    std::memcpy(s, &nhi, sizeof(nhi));
#endif
#if 0
    std::memset(s, 'x', sizeof(uint64_t));

    const uint64_t foo = nhi * 0x0101'0101'0101'0101llu;
    printf("foo:   0x%016llx\n", foo);
    const uint64_t foom = foo & mask_lo;
    printf("foom:  0x%016llx\n", foom);

    const uint64_t sx = *(uint64_t *)&s & mask_hi;
    printf("sx:    0x%016llx\n", sx);
    // const uint64_t sx = *(uint64_t *)&s;
    const uint64_t bar = foom | sx;
    // const uint64_t bar = sx;
    printf("bar:   0x%016llx\n", bar);
    std::memcpy(s, &bar, sizeof(bar));
#endif

    s[sizeof(s) - 1] = 0;
}

int main(void) {
    // const uint32_t n = 0xDEAD'BEEFu;
    // const uint32_t n = 0x0D0E'0A0Du;
    const uint32_t n    = 0xD0E0'A0D0u;
    const uint32_t nexp = nibble_expand32_naive(0xDEAD);
    printf("nexp: 0x%08x\n", nexp);
    const uint32_t nfull     = 0xDEAD'BEEFu;
    const uint64_t nfull_exp = nibble_expand64_naive(nfull);
    printf("nfull_exp: 0x%016llx\n", nfull_exp);
    char s[9] = {};
    u32_to_hex(n, s);
    printf("n: 0x%08x s: '%s'\n", n, s);
    return 0;
}
