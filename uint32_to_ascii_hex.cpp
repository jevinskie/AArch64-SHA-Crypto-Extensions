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
    for (int i = 0; i < 8; ++i) {
        s[i] = 'a' + i;
    }
    const uint32_t nlo = nibbles_to_hex_swar(n & 0x0f0f'0f0fu);
    std::memcpy(s, &nlo, sizeof(nlo));
    const uint32_t nhi = nibbles_to_hex_swar((n >> 4) & 0x0f0f'0f0fu);
    std::memcpy(s, &nhi, sizeof(nhi));
    s[sizeof(s) - 1] = 0;
}

int main(void) {
    const uint32_t n = 0xDEAD'BEEFu;
    char s[9];
    u32_to_hex(n, s);
    printf("n: 0x%08x s: '%s'\n", n, s);
    return 0;
}
