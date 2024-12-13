// clang-formt: off
#undef NDEBUG
#include <cassert>
// clang-format: on

#include <arm_acle.h>
#include <arm_neon.h>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fmt/format.h>
#include <type_traits>

#include "sha1-arm-unrolled.h"
#include "sha1-wrappers.h"

#if 0
#define USE_TEENY
#endif

#if 1
#define USE_CIFRA
#endif

#ifdef USE_TEENY
extern "C" int sha1digest(uint8_t *digest, char *hexdigest, const uint8_t *data, size_t databytes);
#endif

#if 1
#define DO_DUMP
#endif

#if 0
#define DO_DUMP_8x16
#endif

// clang-format: off
#ifdef USE_CIFRA
#include "sha1-cifra.h"
#endif
// clang-format: on

#ifdef DO_DUMP
#define ANSI_BOLD_RED_FG   "\x1b[1;31m"
#define ANSI_BOLD_GREEN_FG "\x1b[1;32m"
#define ANSI_RESET         "\x1b[1;0m"
#endif

#define DO_MCA

#ifdef DO_MCA
#define MCA_BEGIN(name)                                         \
    do {                                                        \
        __asm volatile("# LLVM-MCA-BEGIN " #name ::: "memory"); \
    } while (0)
#define MCA_END()                                      \
    do {                                               \
        __asm volatile("# LLVM-MCA-END" ::: "memory"); \
    } while (0)
#else
#define MCA_BEGIN(name)
#define MCA_END()
#endif

constexpr size_t SHA1_BLOCK_SIZE  = 64;
constexpr size_t SHA1_OUTPUT_SIZE = 20;

constexpr size_t align_val        = 16;
constexpr size_t digest_align_val = 32;
constexpr size_t block_align_val  = SHA1_BLOCK_SIZE;

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpadded"
struct alignas(digest_align_val) SHA1Digest {
    std::array<uint32_t, 5> words;
    [[nodiscard]] uint32_t *data() {
        return words.data();
    }
    [[nodiscard]] const uint32_t *data() const {
        return words.data();
    }
    [[nodiscard]] uint8_t *bytes() {
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        return reinterpret_cast<uint8_t *>(words.data());
    }
    [[nodiscard]] const uint8_t *bytes() const {
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        return reinterpret_cast<const uint8_t *>(words.data());
    }
    [[nodiscard]] uint8_t &operator[](size_t i) {
        return bytes()[i];
    }
    [[nodiscard]] const uint8_t &operator[](size_t i) const {
        return bytes()[i];
    }
};
#pragma GCC diagnostic pop

namespace {
// ubsan implicit conversion workaround
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wold-style-cast"
#pragma GCC diagnostic ignored "-Wsign-conversion"
template <uint32_t p2>
[[gnu::always_inline]] uint32x4_t my_vsetq_lane_u32(const uint32_t p0, const uint32x4_t p1) noexcept {
    const uint32_t s0    = p0;
    const uint32x4_t s1  = p1;
    const uint32x4_t ret = (uint32x4_t)__builtin_neon_vsetq_lane_i32((int)s0, (int32x4_t)s1, p2);
    return ret;
}
#pragma GCC diagnostic pop

#if defined(__clang__)
#define NOOPT(v) asm volatile("" : "+r,m"((v)) : : "memory")
#else
#define NOOPT(v) asm volatile("" : "+m,r"((v)) : : "memory")
#endif

template <class Tp> [[gnu::always_inline]] inline void DoNotOptimize(Tp &value) {
#if defined(__clang__)
    asm volatile("" : "+r,m"(value) : : "memory");
#else
    asm volatile("" : "+m,r"(value) : : "memory");
#endif
}

} // namespace

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpadded"
// NOLINTBEGIN(misc-non-private-member-variables-in-classes)
class alignas(digest_align_val) SHA1State {
public:
    SHA1State() {
        // abcd = vsetq_lane_u32(0x67452301u, vdupq_n_u32(0u), 0u);
        // abcd = vsetq_lane_u32(0xEFCDAB89u, abcd, 1u);
        // abcd = vsetq_lane_u32(0x98BADCFEu, abcd, 2u);
        // abcd = vsetq_lane_u32(0x10325476u, abcd, 3u);
        abcd = my_vsetq_lane_u32<0u>(0x67452301u, vdupq_n_u32(0u));
        abcd = my_vsetq_lane_u32<1u>(0xEFCDAB89u, abcd);
        abcd = my_vsetq_lane_u32<2u>(0x98BADCFEu, abcd);
        abcd = my_vsetq_lane_u32<3u>(0x10325476u, abcd);
    }
    SHA1State(const uint32x4_t abcd_, const uint32_t e_) : abcd{abcd_}, e{e_} {}
    uint32x4_t abcd;         // Represents H0, H1, H2, H3
    uint32_t e{0xC3D2E1F0u}; // Represents H4
};
// NOLINTEND(misc-non-private-member-variables-in-classes)
#pragma GCC diagnostic pop

class alignas(block_align_val) SHA1Block {
public:
    SHA1Block &operator=(const uint32x4x4_t &block) {
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        *reinterpret_cast<uint32x4x4_t *>(words.data()) = block;
        return *this;
    }
    [[nodiscard]] uint32_t *data() {
        return words.data();
    }
    [[nodiscard]] const uint32_t *data() const {
        return words.data();
    }
    [[nodiscard]] uint8_t *bytes() {
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        return reinterpret_cast<uint8_t *>(words.data());
    }
    [[nodiscard]] const uint8_t *bytes() const {
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        return reinterpret_cast<const uint8_t *>(words.data());
    }

private:
    std::array<uint32_t, 16> words;
};

using SHA1StateScalar = std::array<uint8_t, 20>;
using SHA1BlockScalar = std::array<uint8_t, 64>;

void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i, const SHA1State &state);
void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i, const SHA1StateScalar &state);
extern "C" [[gnu::noinline]] void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i,
                                                  const uint8_t *const _Nonnull state);

void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i, const SHA1BlockScalar &block);
void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i, const SHA1Block &block);
extern "C" [[gnu::noinline]] void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i,
                                                  const uint8_t *const _Nonnull block);

[[gnu::noinline, gnu::used]] void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32x4_t v);
extern "C" [[gnu::noinline]] void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32_t (&v)[4]);

[[gnu::noinline, gnu::used]] void dump_uint8x16_t(const char *const _Nonnull prefix, const uint8x16_t v);
extern "C" [[gnu::noinline]] void dump_uint8x16_t(const char *const _Nonnull prefix, const uint8_t (&v)[16]);

[[gnu::noinline, gnu::used]] void dump_uint8x16x2_t(const char *const _Nonnull prefix, const uint8x16x2_t v);
extern "C" [[gnu::noinline]] void dump_uint8x16x2_t(const char *const _Nonnull prefix, const uint8_t (&v)[32]);

namespace {

// NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
[[maybe_unused]] const char impl_name[] = "sha1-arm.cpp";

// Helper function to determine the size of the string literal
template <typename T, size_t N>
// NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
consteval std::array<T, N - 1> cstrlit_to_std_array(const char (&str)[N]) {
    std::array<T, N - 1> arr = {};
    auto sit                 = std::begin(str);
    for (auto it = arr.begin(), ite = arr.end(); it != ite; ++it, ++sit) {
        *it = static_cast<uint8_t>(*sit);
    }
    return arr;
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-template"
template <typename T, typename F> constexpr T to_from_cast(const F &val) {
    // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
    return reinterpret_cast<T>(static_cast<F>(val));
}

template <typename T, typename F> constexpr T to_from_cast(const F *_Nonnull val) { // NOLINT(misc-include-cleaner)
    // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
    return reinterpret_cast<T>(static_cast<F *>(val));
}

template <typename T, typename F>
constexpr T to_from_cast(std::remove_pointer_t<F> *_Nonnull val) { // NOLINT(misc-include-cleaner)
    // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
    return reinterpret_cast<T>(static_cast<std::remove_pointer_t<F> *>(val));
}
#pragma GCC diagnostic pop

} // namespace

[[gnu::noinline, maybe_unused]] void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i,
                                                     const SHA1BlockScalar &block) {
#ifdef DO_DUMP
    printf(ANSI_BOLD_RED_FG "block[%10zu]" ANSI_RESET
                            " %10s:%03d %08x%08x%08x%08x%08x%08x%08x%08x%08x%08x%08x%08x%08x%08x%08x%08x\n",
           i, name, line, block[0], block[1], block[2], block[3], block[4], block[5], block[6], block[7], block[8],
           block[9], block[10], block[11], block[12], block[13], block[14], block[15]);
#else
    (void)name;
    (void)line;
    (void)i;
    (void)block;
#endif
}

[[gnu::noinline, maybe_unused]] void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i,
                                                     const SHA1Block &block) {
#ifdef DO_DUMP
    SHA1BlockScalar scalar_block{};
    std::memcpy(scalar_block.data(), &block, sizeof(block));
    dump_sha1_block(name, line, i, scalar_block);
#else
    (void)name;
    (void)line;
    (void)i;
    (void)block;
#endif
}

extern "C" [[gnu::noinline, maybe_unused]] void dump_sha1_block(const char *const _Nonnull name, const int line,
                                                                const size_t i, const uint8_t *const _Nonnull block) {
#ifdef DO_DUMP
    SHA1BlockScalar scalar_block{};
    std::memcpy(scalar_block.data(), block, sizeof(scalar_block));
    dump_sha1_block(name, line, i, scalar_block);
#else
    (void)name;
    (void)line;
    (void)i;
    (void)block;
#endif
}

[[gnu::noinline, maybe_unused]] void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i,
                                                     const SHA1StateScalar &state) {
#ifdef DO_DUMP
    printf(ANSI_BOLD_GREEN_FG "state[%10zu]" ANSI_RESET " %10s:%03d %08x%08x%08x%08x%08x\n", i, name, line, state[0],
           state[1], state[2], state[3], state[4]);
#else
    (void)name;
    (void)line;
    (void)i;
    (void)state;
#endif
}

[[gnu::noinline, maybe_unused]] void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i,
                                                     const SHA1State &state) {
#ifdef DO_DUMP
    SHA1StateScalar scalar_state{};
    std::memcpy(scalar_state.data(), &state.abcd, sizeof(state.abcd));
    std::memcpy(scalar_state.data() + sizeof(state.abcd), &state.e, sizeof(state.e));
    dump_sha1_state(name, line, i, scalar_state);
#else
    (void)name;
    (void)line;
    (void)i;
    (void)state;
#endif
}

extern "C" [[gnu::noinline, maybe_unused]] void dump_sha1_state(const char *const _Nonnull name, const int line,
                                                                const size_t i, const uint8_t *const _Nonnull state) {
#ifdef DO_DUMP
    SHA1StateScalar scalar_state{};
    std::memcpy(scalar_state.data(), state, sizeof(scalar_state));
    dump_sha1_state(name, line, i, scalar_state);
#else
    (void)name;
    (void)line;
    (void)i;
    (void)state;
#endif
}

[[gnu::noinline, maybe_unused]] void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32x4_t v) {
#ifdef DO_DUMP
    printf("%s v[0]: 0x%08x v[1]: 0x%08x v[2]: 0x%08x v[3]: 0x%08x\n", prefix, v[0], v[1], v[2], v[3]);
#else
    (void)prefix;
    (void)v;
#endif
}

extern "C" [[gnu::noinline, maybe_unused]] void dump_uint32x4_t(const char *const _Nonnull prefix,
                                                                const uint32_t (&v)[4]) {
#ifdef DO_DUMP
    uint32x4_t dv{v[0], v[1], v[2], v[3]};
    dump_uint32x4_t(prefix, dv);
#else
    (void)prefix;
    (void)v;
#endif
}

[[gnu::noinline, maybe_unused]] void dump_uint8x16_t(const char *const _Nonnull prefix, const uint8x16_t v) {
#ifdef DO_DUMP_8x16
    printf("%s v[0]: 0x%02hhx, v[1]: 0x%02hhx, v[2]: 0x%02hhx, v[3]: 0x%02hhx, v[4]: 0x%02hhx, v[5]: 0x%02hhx, v[6]: "
           "0x%02hhx, v[7]: 0x%02hhx, v[8]: 0x%02hhx, v[9]: 0x%02hhx, v[10]: 0x%02hhx, v[11]: 0x%02hhx, v[12]: "
           "0x%02hhx, v[13]: 0x%02hhx, v[14]: 0x%02hhx, v[15]: 0x%02hhx\n",
           prefix, v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10], v[11], v[12], v[13], v[14],
           v[15]);
#else
    (void)prefix;
    (void)v;
#endif
}

extern "C" [[gnu::noinline, maybe_unused]] void dump_uint8x16_t(const char *const _Nonnull prefix,
                                                                const uint8_t (&v)[16]) {
#ifdef DO_DUMP_8x16
    uint8x16_t dv{v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15]};
    dump_uint8x16_t(prefix, dv);
#else
    (void)prefix;
    (void)v;
#endif
}

[[gnu::noinline, maybe_unused]] void dump_uint8x16x2_t(const char *const _Nonnull prefix, const uint8x16x2_t v) {
#ifdef DO_DUMP_8x16
    const uint8x16x2_t mv = v;
    uint8_t b[32];
    static_assert(sizeof(mv) == sizeof(b));
    std::memcpy(b, &mv, sizeof(mv));

    printf("%s v[0]: 0x%02hhx, v[1]: 0x%02hhx, v[2]: 0x%02hhx, v[3]: 0x%02hhx, v[4]: 0x%02hhx, v[5]: 0x%02hhx, v[6]: "
           "0x%02hhx, v[7]: 0x%02hhx, v[8]: 0x%02hhx, v[9]: 0x%02hhx, v[10]: 0x%02hhx, v[11]: 0x%02hhx, v[12]: "
           "0x%02hhx, v[13]: 0x%02hhx, v[14]: 0x%02hhx, v[15]: 0x%02hhx, v[16]: 0x%02hhx, v[17]: 0x%02hhx, v[18]: "
           "0x%02hhx, v[19]: 0x%02hhx, v[20]: 0x%02hhx, v[21]: 0x%02hhx, v[22]: 0x%02hhx, v[23]: 0x%02hhx, v[24]: "
           "0x%02hhx, v[25]: 0x%02hhx, v[26]: 0x%02hhx, v[27]: 0x%02hhx, v[28]: 0x%02hhx, v[29]: 0x%02hhx, v[30]: "
           "0x%02hhx, v[31]: 0x%02hhx\n",
           prefix, b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11], b[12], b[13], b[14], b[15],
           b[16], b[17], b[18], b[19], b[20], b[21], b[22], b[23], b[24], b[25], b[26], b[27], b[28], b[29], b[30],
           b[31]);

    printf("%s v[0]: %c, v[1]: %c, v[2]: %c, v[3]: %c, v[4]: %c, v[5]: %c, v[6]: %c, v[7]: %c, v[8]: %c, v[9]: %c, "
           "v[10]: %c, v[11]: %c, v[12]: %c, v[13]: %c, v[14]: %c, v[15]: %c, v[16]: %c, v[17]: %c, v[18]: %c, v[19]: "
           "%c, v[20]: %c, v[21]: %c, v[22]: %c, v[23]: %c, v[24]: %c, v[25]: %c, v[26]: %c, v[27]: %c, v[28]: %c, "
           "v[29]: %c, v[30]: %c, v[31]: %c",
           prefix, b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11], b[12], b[13], b[14], b[15],
           b[16], b[17], b[18], b[19], b[20], b[21], b[22], b[23], b[24], b[25], b[26], b[27], b[28], b[29], b[30],
           b[31]);
#else
    (void)prefix;
    (void)v;
#endif
}

extern "C" [[gnu::noinline, maybe_unused]] void dump_uint8x16x2_t(const char *const _Nonnull prefix,
                                                                  const uint8_t (&v)[32]) {
#ifdef DO_DUMP_8x16
    uint8x16x2_t dv{v[0],  v[1],  v[2],  v[3],  v[4],  v[5],  v[6],  v[7],  v[8],  v[9],  v[10],
                    v[11], v[12], v[13], v[14], v[15], v[16], v[17], v[18], v[19], v[20], v[21],
                    v[22], v[23], v[24], v[25], v[26], v[27], v[28], v[29], v[30], v[31]};
    dump_uint8x16x2_t(prefix, dv);
#else
    (void)prefix;
    (void)v;
#endif
}

[[maybe_unused]] static size_t block_cnt;
[[maybe_unused]] static size_t state_cnt;

class SHA1 {
public:
    template <size_t N>
    // NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
    static SHA1Digest hash(const uint8_t (&data)[N]) {
        // static_assert(N > 0, "Input data must be non-empty");
        SHA1State state{};
        if constexpr (N <= 32) {
            process_short(data, N, state);
        } else if constexpr (N <= 256) {
            process_medium(data, N, state);
        } else {
            process_large(data, N, state);
        }
        return state_to_digest(state);
    }

    template <size_t N> static SHA1Digest hash(const std::array<uint8_t, N> &data) {
        // static_assert(N > 0, "Input data must be non-empty");
        SHA1State state{};
        if constexpr (N <= 32) {
            process_short(data.data(), N, state);
        } else if constexpr (N <= 256) {
            process_medium(data.data(), N, state);
        } else {
            process_large(data.data(), N, state);
        }
        return state_to_digest(state);
    }

private:
    static constexpr uint8x16_t hex_lut = {'0', '1', '2', '3', '4', '5', '6', '7',
                                           '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
    [[gnu::always_inline]] static void u32_to_hex_ascii_u64(const uint32_t value, char *_Nonnull hex_str) {
        // printf("u32_to_hex_ascii_u64 val: 0x%08x\n", value);
        // assert(!"foo");
        const uint8x16_t mask_lo = vdupq_n_u8(0x0F); // Mask for low 4 bits

        // Load the first 16 bytes of the digest
        const uint8x16_t input = vdupq_n_u32(value);
        const uint8x16_t hi    = vshrq_n_u8(input, 4);     // Shift high nibbles down
        const uint8x16_t lo    = vandq_u8(input, mask_lo); // Isolate low nibbles

        // Convert to ASCII hex characters
        const uint8x16_t hex_hi = vqtbl1q_u8(hex_lut, hi);
        const uint8x16_t hex_lo = vqtbl1q_u8(hex_lut, lo);

        // Store the results interleaved
        const uint8x16x2_t hex_chars_interleaved = vzipq_u8(hex_hi, hex_lo);
        vst1q_lane_u64((to_from_cast<uint64_t *, char *>(hex_str)),
                       static_cast<uint32x4_t>(hex_chars_interleaved.val[0]), 0);
    }

public:
    // clang-tidy complains about __restrict not being in an included header -_-
    // NOLINTNEXTLINE(misc-include-cleaner)
    [[gnu::noinline]] static void digest_to_hex(const uint8_t *__restrict _Nonnull digest,
                                                char *__restrict _Nonnull hex_str) {
        MCA_BEGIN("digest_to_hex");
        const uint8x16_t mask_lo = vdupq_n_u8(0x0F); // Mask for low 4 bits

        // Load the first 16 bytes of the digest
        const uint8x16_t input = vld1q_u8(digest);
        const uint8x16_t hi    = vshrq_n_u8(input, 4);     // Shift high nibbles down
        const uint8x16_t lo    = vandq_u8(input, mask_lo); // Isolate low nibbles

        // Convert to ASCII hex characters
        const uint8x16_t hex_hi = vqtbl1q_u8(hex_lut, hi);
        const uint8x16_t hex_lo = vqtbl1q_u8(hex_lut, lo);

        // Store the results interleaved
        const uint8x16x2_t hex_chars_interleaved = vzipq_u8(hex_hi, hex_lo);
        vst1q_u8_x2((to_from_cast<uint8_t *, char *>(hex_str)), hex_chars_interleaved);

        // Handle the remaining 4 bytes using SWAR in GPRs
        // NOLINTBEGIN(cppcoreguidelines-pro-type-reinterpret-cast)
        const uint32_t remaining_bytes = *reinterpret_cast<const uint32_t *>(digest + 16);
        // NOLINTEND(cppcoreguidelines-pro-type-reinterpret-cast)

        u32_to_hex_ascii_u64(remaining_bytes, hex_str + 32);
        hex_str[SHA1_OUTPUT_SIZE * 2] = '\0';
        MCA_END();
    }

    [[gnu::noinline]] static void digest_to_hex_simple(const uint8_t *__restrict _Nonnull digest,
                                                       char *__restrict _Nonnull hex_str) {
        MCA_BEGIN("digest_to_hex_simple");
#pragma nounroll
        for (size_t i = 0; i < SHA1_OUTPUT_SIZE; ++i, hex_str += 2) {
            // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
            byte_to_ascii_hex(digest[i], reinterpret_cast<std::array<char, 2> &>(*hex_str));
        }
        *hex_str = '\0';
        MCA_END();
    }

private:
    static constexpr std::array<uint32_t, 4> K = {0x5A827999U, 0x6ED9EBA1U, 0x8F1BBCDCU, 0xCA62C1D6U};

#if defined(__clang__)
    __attribute__((no_sanitize("unsigned-integer-overflow")))
#endif
    static void
    process_block_orig(const uint8_t *__restrict _Nonnull block, SHA1State &state) {
        fmt::print("sha1-arm process_block_orig block: {}\n", fmt::ptr(block));
        [[maybe_unused]] SHA1Block db{};
        // dump_sha1_state(impl_name, __LINE__, state_cnt++, state);
        // dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, reinterpret_cast<const SHA1BlockScalar &>(*block));

        uint32x4_t abcd = state.abcd;
        uint32_t e      = state.e;

        // Use aligned loads for the message schedule
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        alignas(block_align_val) uint32x4x4_t w = vld1q_u32_x4(reinterpret_cast<const uint32_t *>(block));

        // dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        // dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        if constexpr (std::endian::native == std::endian::little) {
            // Byte swap the initial words
            // dump_uint32x4_t("w.val[0] before:", w.val[0]);
            w.val[0] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[0])));
            // dump_uint32x4_t("w.val[0] after: ", w.val[0]);
            // dump_uint32x4_t("w.val[1] before:", w.val[1]);
            w.val[1] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[1])));
            // dump_uint32x4_t("w.val[1] after: ", w.val[1]);
            // dump_uint32x4_t("w.val[2] before:", w.val[2]);
            w.val[2] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[2])));
            // dump_uint32x4_t("w.val[2] after: ", w.val[2]);
            // dump_uint32x4_t("w.val[3] before:", w.val[3]);
            w.val[3] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[3])));
            // dump_uint32x4_t("w.val[3] after: ", w.val[3]);
        }

        // dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        // dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        // Constants for each set of 20 rounds
        const uint32x4_t k1 = vdupq_n_u32(K[0]);
        const uint32x4_t k2 = vdupq_n_u32(K[1]);
        const uint32x4_t k3 = vdupq_n_u32(K[2]);
        const uint32x4_t k4 = vdupq_n_u32(K[3]);

        const uint32x4x4_t ks = {
            {{K[0], K[0], K[0], K[0]}, {K[1], K[1], K[1], K[1]}, {K[2], K[2], K[2], K[2]}, {K[3], K[3], K[3], K[3]}}};

        uint32_t e_tmp;

        // First 20 rounds (K1)
        for (size_t i = 0; i < 20 / 4; ++i) {
            if (i < 16) {
                w.val[i % 4] = vsha1su0q_u32(w.val[(i + 2) % 4], w.val[(i + 3) % 4], w.val[i % 4]);
            }

            // uint32x4_t temp = vsha1cq_u32(abcd, e, w.val[i % 4u]);
            // abcd            = vextq_u32(abcd, abcd, 1u); // Rotate the lanes of abcd
            // abcd            = vsetq_lane_u32(e, abcd, 3u);
            // e               = vsha1h_u32(vgetq_lane_u32(temp, 0));

            e_tmp = e;
            e     = vsha1h_u32(vgetq_lane_u32(abcd, 0));
            abcd  = vsha1cq_u32(abcd, e_tmp, w.val[i % 4]);

            if (i < 16) {
                w.val[i % 4] = vsha1su1q_u32(w.val[i % 4], w.val[(i + 1) % 4]);
            }
            w.val[i % 4] = vaddq_u32(w.val[i % 4], k1);

            if (i == 0 || i == 15) {
                // dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
                // dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);
            }
        }

        // dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        // dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        // Rounds 21-40 (K2)
        for (size_t i = 20 / 4; i < 40 / 4; ++i) {
            w.val[i % 4] = vsha1su0q_u32(w.val[(i + 2) % 4], w.val[(i + 3) % 4], w.val[i % 4]);

            const uint32x4_t temp = vsha1pq_u32(abcd, e, w.val[i % 4]);
            abcd                  = vextq_u32(abcd, abcd, 1);
            // abcd            = vsetq_lane_u32(e, abcd, 3);
            abcd = my_vsetq_lane_u32<3u>(e, abcd);
            e    = vsha1h_u32(vgetq_lane_u32(temp, 0));

            w.val[i % 4] = vsha1su1q_u32(w.val[i % 4], w.val[(i + 1) % 4]);
            w.val[i % 4] = vaddq_u32(w.val[i % 4], k2);
        }

        // dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        // dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        // Rounds 41-60 (K3)
        for (size_t i = 40 / 4; i < 60 / 4; ++i) {
            w.val[i % 4] = vsha1su0q_u32(w.val[(i + 2) % 4], w.val[(i + 3) % 4], w.val[i % 4]);

            const uint32x4_t temp = vsha1mq_u32(abcd, e, w.val[i % 4]);
            abcd                  = vextq_u32(abcd, abcd, 1);
            // abcd            = vsetq_lane_u32(e, abcd, 3u);
            abcd = my_vsetq_lane_u32<3u>(e, abcd);
            e    = vsha1h_u32(vgetq_lane_u32(temp, 0));

            w.val[i % 4] = vsha1su1q_u32(w.val[i % 4], w.val[(i + 1) % 4]);
            w.val[i % 4] = vaddq_u32(w.val[i % 4], k3);
        }

        // dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        // dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        // Rounds 61-80 (K4)
        for (size_t i = 60 / 4; i < 80 / 4; ++i) {
            w.val[i % 4] = vsha1su0q_u32(w.val[(i + 2) % 4], w.val[(i + 3) % 4], w.val[i % 4]);

            const uint32x4_t temp = vsha1pq_u32(abcd, e, w.val[i % 4]);
            abcd                  = vextq_u32(abcd, abcd, 1);
            // abcd            = vsetq_lane_u32(e, abcd, 3u);
            abcd = my_vsetq_lane_u32<3u>(e, abcd);
            e    = vsha1h_u32(vgetq_lane_u32(temp, 0));

            w.val[i % 4] = vsha1su1q_u32(w.val[i % 4], w.val[(i + 1) % 4]);
            w.val[i % 4] = vaddq_u32(w.val[i % 4], k4);
        }

        state.abcd = vaddq_u32(state.abcd, abcd);
        state.e += e;

        // dump_sha1_state(impl_name, __LINE__, state_cnt++, state);
        // dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);
    }

    static constexpr auto choose_func = [](size_t r) {
        if (r < 20)
            return vsha1cq_u32;
        else if (r < 40)
            return vsha1pq_u32;
        else if (r < 60)
            return vsha1mq_u32;
        else
            return vsha1pq_u32;
    };

    static constexpr auto choose_key = [](size_t r) {
        if (r < 20)
            return K[0];
        else if (r < 40)
            return K[1];
        else if (r < 60)
            return K[2];
        else
            return K[3];
    };

#if defined(__clang__)
    __attribute__((no_sanitize("unsigned-integer-overflow")))
#endif
    static void
    process_block(const uint8_t *__restrict _Nonnull block, SHA1State &state) {
        fmt::print("sha1-arm process_block block: {}\n", fmt::ptr(block));

        uint32x4_t abcd = state.abcd;
        uint32_t e      = state.e;

        // Use aligned loads for the message schedule
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        alignas(block_align_val) uint32x4x4_t w = vld1q_u32_x4(reinterpret_cast<const uint32_t *>(block));

        if constexpr (std::endian::native == std::endian::little) {
            // Byte swap the initial words
            w.val[0] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[0])));
            w.val[1] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[1])));
            w.val[2] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[2])));
            w.val[3] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[3])));
        }

        // Constants for each set of 20 rounds
        const uint32x4_t k1 = vdupq_n_u32(K[0]);
        const uint32x4_t k2 = vdupq_n_u32(K[1]);
        const uint32x4_t k3 = vdupq_n_u32(K[2]);
        const uint32x4_t k4 = vdupq_n_u32(K[3]);

        const uint32x4x4_t ks = {
            {{K[0], K[0], K[0], K[0]}, {K[1], K[1], K[1], K[1]}, {K[2], K[2], K[2], K[2]}, {K[3], K[3], K[3], K[3]}}};

        uint32_t e_tmp;
        uint32_t e0, e1;
        uint32x4_t tmp0, tmp1;
        uint32x4_t msg0, msg1, msg2, msg3;

        for (size_t b = 0; b < 20; ++b) {
            const auto r    = b * 4;
            const auto keyf = choose_key(r);
            const auto f    = choose_func(r);
            uint32_t new_e  = vsha1h_u32(vgetq_lane_u32(abcd, 0));
            if ((b & 1) == 0) {
                // even block index: set e1
                e1 = new_e;
            } else {
                // odd block index: set e0
                e0 = new_e;
            }
            if ((b & 1) == 0) {
                abcd = f(abcd, e0, tmp0);
            } else {
                abcd = f(abcd, e1, tmp1);
            }
            const auto key = ks.val[b % 4];
            if ((r & 1) == 0) {
                // Even block: update tmp0
                // Choose correct msgX based on pattern (e.g., msg2 or msg0, etc.)
                // Example for demonstration:
                if (r == 0) {
                    tmp0 = vaddq_u32(msg2, key);
                } else if (r == 2) {
                    tmp0 = vaddq_u32(msg0, key);
                } else if (r == 4) {
                    tmp0 = vaddq_u32(msg2, key);
                } else if (r == 6) {
                    tmp0 = vaddq_u32(msg0, key);
                }
                // Continue pattern as per original code...
            } else {
                // Odd block: update tmp1
                if (r == 1) {
                    tmp1 = vaddq_u32(msg3, key);
                } else if (r == 3) {
                    tmp1 = vaddq_u32(msg1, key);
                } else if (r == 5) {
                    tmp1 = vaddq_u32(msg3, key);
                } else if (r == 7) {
                    tmp1 = vaddq_u32(msg1, key);
                }
                // Continue pattern as per original code...
            }
            switch (r) {
            case 0: // rounds 0-3
                msg0 = vsha1su0q_u32(msg0, msg1, msg2);
                break;
            case 1: // rounds 4-7
                msg0 = vsha1su1q_u32(msg0, msg3);
                msg1 = vsha1su0q_u32(msg1, msg2, msg3);
                break;
            case 2: // rounds 8-11
                msg1 = vsha1su1q_u32(msg1, msg0);
                msg2 = vsha1su0q_u32(msg2, msg3, msg0);
                break;
            case 3: // rounds 12-15
                msg2 = vsha1su1q_u32(msg2, msg1);
                msg3 = vsha1su0q_u32(msg3, msg0, msg1);
                break;
            // Continue for all blocks, following original pattern...
            default:
                // For subsequent blocks (i = 4 to 19), follow the same pattern logic
                // by analyzing the original code snippet and applying the appropriate
                // vsha1su0q_u32 and vsha1su1q_u32 calls.
                break;
            }
        }
    }

    static void pad_and_finalize(const uint8_t *__restrict _Nullable data, size_t len, SHA1State &state) {
        alignas(SHA1_BLOCK_SIZE) SHA1Block buffer = {};
        assert(len <= sizeof(buffer));
        std::memcpy(buffer.data(), data, len);
        buffer.bytes()[len] = 0x80;

        if (len >= 56) {
            process_block(buffer.bytes(), state);
            std::memset(&buffer, 0, sizeof(buffer));
        }

        buffer.data()[14] = 0;
        if constexpr (std::endian::native == std::endian::little) {
            buffer.data()[15] = std::byteswap(static_cast<uint32_t>(len * 8)); // Length in bits
        } else {
            buffer.data()[15] = static_cast<uint32_t>(len * 8); // Length in bits
        }

        process_block(buffer.bytes(), state);
    }

    static void process_short(const uint8_t *__restrict _Nullable data, size_t len, SHA1State &state) {
        pad_and_finalize(data, len, state);
    }

    static void process_medium(const uint8_t *__restrict _Nonnull data, size_t len, SHA1State &state) {
        const uint8_t *__restrict _Nonnull end = data + len - (len % SHA1_BLOCK_SIZE);
        for (const uint8_t *__restrict _Nonnull p = data; p < end; p += SHA1_BLOCK_SIZE) {
            process_block(p, state);
        }
        pad_and_finalize(end, len % SHA1_BLOCK_SIZE, state);
    }

    static void process_large(const uint8_t *__restrict _Nonnull data, size_t len, SHA1State &state) {
        const size_t block_total_sz = len - (len % SHA1_BLOCK_SIZE);
        const size_t remainder_sz   = len - block_total_sz;
        for (size_t i = 0; i < block_total_sz; i += SHA1_BLOCK_SIZE) {
            process_block(&data[i], state);
        }
        pad_and_finalize(&data[block_total_sz], remainder_sz, state);
    }

    static SHA1Digest state_to_digest(const SHA1State &state) {
        SHA1Digest hash_output{};

        // Use NEON intrinsics to convert state.abcd to bytes
        const uint8x16_t abcd_bytes = vreinterpretq_u8_u32(state.abcd);
        vst1q_u8(hash_output.bytes(), abcd_bytes);

        // Convert state.e to bytes and store it
        hash_output[16] = (state.e >> 24U) & 0xFFU;
        hash_output[17] = (state.e >> 16U) & 0xFFU;
        hash_output[18] = (state.e >> 8U) & 0xFFU;
        hash_output[19] = state.e & 0xFFU;

        return hash_output;
    }

    [[gnu::always_inline]] static constexpr uint8_t nibble_to_ascii_hex(const uint8_t chr) {
        if (chr <= 9) {
            return chr + '0';
        }
        if (chr >= 0xA && chr <= 0xF) {
            return chr - 0xA + 'a';
        }
        __builtin_unreachable();
    }

    [[gnu::always_inline]] static constexpr void byte_to_ascii_hex(const uint8_t n, std::array<char, 2> &hex) {
        hex[0] = static_cast<char>(nibble_to_ascii_hex(n >> 4U));
        hex[1] = static_cast<char>(nibble_to_ascii_hex(n & 0xFU));
    }
};

int main() {
    // Example data
    alignas(SHA1_BLOCK_SIZE) static constinit auto str =
        // cstrlit_to_std_array<uint8_t>("The quick brown fox jumps over the lazy dog\n");
        cstrlit_to_std_array<uint8_t>("");

    sha1_wrappers_reset();
    const auto h = SHA1::hash(str);
    sha1_wrappers_reset();
    alignas(align_val) std::array<char, SHA1_OUTPUT_SIZE * 2 + 1> hex_str{};

    printf("SHA-1 Digest dumb:         "
           "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%"
           "02hhx%02hhx%02hhx%02hhx%02hhx%02hhx\n",
           h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11], h[12], h[13], h[14], h[15], h[16],
           h[17], h[18], h[19]);

    std::memset(hex_str.data(), 0, sizeof(hex_str));
    SHA1::digest_to_hex_simple(h.bytes(), hex_str.data());
    printf("SHA-1 Digest simple:       %s\n", hex_str.data());

    std::memset(hex_str.data(), 0, sizeof(hex_str));
    SHA1::digest_to_hex(h.bytes(), hex_str.data());
    printf("SHA-1 Digest:              %s\n", hex_str.data());
    printf("\n\n\n");

    SHA1Digest uh{};
    sha1_wrappers_reset();
    sha1_arm_unrolled(str.data(), str.size(), uh.bytes());
    sha1_wrappers_reset();

    printf("SHA-1 Digest dumb unrolled: "
           "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%"
           "02hhx%02hhx%02hhx\n",
           uh[0], uh[1], uh[2], uh[3], uh[4], uh[5], uh[6], uh[7], uh[8], uh[9], uh[10], uh[11], uh[12], uh[13], uh[14],
           uh[15], uh[16], uh[17], uh[18], uh[19]);

    std::memset(hex_str.data(), 0, sizeof(hex_str));
    SHA1::digest_to_hex_simple(uh.bytes(), hex_str.data());
    printf("SHA-1 Digest simple unrolled: %s\n", hex_str.data());

    std::memset(hex_str.data(), 0, sizeof(hex_str));
    SHA1::digest_to_hex(uh.bytes(), hex_str.data());
    printf("SHA-1 Digest unrolled: %s\n", hex_str.data());
    printf("\n\n\n");

#ifdef USE_TEENY
    SHA1Digest th{};
    assert(!sha1digest(th.bytes(), hex_str.data(), static_cast<const uint8_t *>(str.data()), str.size()));

    printf("SHA-1 Digest dumb teeny:   "
           "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%"
           "02hhx%02hhx%02hhx\n",
           th[0], th[1], th[2], th[3], th[4], th[5], th[6], th[7], th[8], th[9], th[10], th[11], th[12], th[13], th[14],
           th[15], th[16], th[17], th[18], th[19]);

    std::memset(hex_str.data(), 0, sizeof(hex_str));
    SHA1::digest_to_hex_simple(th.bytes(), hex_str.data());
    printf("SHA-1 Digest simple teeny: %s\n", hex_str.data());

    std::memset(hex_str.data(), 0, sizeof(hex_str));
    SHA1::digest_to_hex(th.bytes(), hex_str.data());
    printf("SHA-1 Digest teeny:        %s\n", hex_str.data());
    printf("\n\n\n");
#endif

#ifdef USE_CIFRA
    SHA1Digest ch{};
    cf_sha1_context cifra_ctx{};
    cf_sha1_init(&cifra_ctx);
    cf_sha1_update(&cifra_ctx, str.data(), str.size());
    cf_sha1_digest_final(&cifra_ctx, ch.bytes());

    printf("SHA-1 Digest dumb cifra:   "
           "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%"
           "02hhx%02hhx%02hhx\n",
           ch[0], ch[1], ch[2], ch[3], ch[4], ch[5], ch[6], ch[7], ch[8], ch[9], ch[10], ch[11], ch[12], ch[13], ch[14],
           ch[15], ch[16], ch[17], ch[18], ch[19]);

    std::memset(hex_str.data(), 0, sizeof(hex_str));
    SHA1::digest_to_hex_simple(ch.bytes(), hex_str.data());
    printf("SHA-1 Digest simple cifra: %s\n", hex_str.data());

    std::memset(hex_str.data(), 0, sizeof(hex_str));
    SHA1::digest_to_hex(ch.bytes(), hex_str.data());
    printf("SHA-1 Digest cifra:        %s\n", hex_str.data());
#endif

    return 0;
}
