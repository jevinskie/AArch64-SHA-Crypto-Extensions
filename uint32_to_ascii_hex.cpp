#undef NDEBUG
#include <cassert>

#include <arm_neon.h>
#include <array>
#include <cstdint>
#include <cstdio>

[[gnu::noinline]] void u32_to_hex(const uint32_t n, char (&s)[9]) {
    for (int i = 0; i < 8; ++i) {
        s[i] = 'a' + i;
    }
    s[sizeof(s) - 1] = 0;
}

int main(void) {
    const uint32_t n = 0xDEAD'BEEFu;
    char s[9];
    u32_to_hex(n, s);
    printf("n: 0x%08x s: '%s'\n", n, s);
    return 0;
}
