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

[[gnu::noinline]] void u32_to_hex(const uint32_t n, char (&s)[9]) {
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
    const uint64_t foo = nhi * 0x0000'0000'0101'0101llu;
    printf("foo:  0x%016llx\n", foo);
    std::memset(s, 'x', sizeof(foo));
    // const uint64_t mask = 0x00ff'00ff'00ff'00ffllu;
    const uint64_t mask = 0xff00'ff00'ff00'ff00llu;
    printf("mask: 0x%016llx\n", mask);
    const uint64_t sx = *(uint64_t *)&s & mask;
    printf("sx:   0x%016llx\n", sx);
    // const uint64_t sx = *(uint64_t *)&s;
    const uint64_t bar = foo | sx;
    // const uint64_t bar = sx;
    printf("bar:  0x%016llx\n", bar);
    std::memcpy(s, &bar, sizeof(bar));
    s[sizeof(s) - 1] = 0;
}

int main(void) {
    const uint32_t n = 0xDEAD'BEEFu;
    char s[9]        = {};
    u32_to_hex(n, s);
    printf("n: 0x%08x s: '%s'\n", n, s);
    return 0;
}
