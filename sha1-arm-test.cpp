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
#include <type_traits>

#if 0
#define USE_TEENY
#endif

#if 1
#define USE_CIFRA
#endif

#ifdef USE_TEENY
extern "C" int sha1digest(uint8_t *digest, char *hexdigest, const uint8_t *data, size_t databytes);
#endif

#if 0
#define DO_DUMP
#endif

#define DO_DUMP_8x16

// clang-format: off
#ifdef USE_CIFRA
#include "3rdparty/cifra/cifra-sha1.h"
#endif
// clang-format: on

#ifdef DO_DUMP
#define ANSI_BOLD_RED_FG   "\x1b[1;31m"
#define ANSI_BOLD_GREEN_FG "\x1b[1;32m"
#define ANSI_RESET         "\x1b[1;0m"
#endif

constexpr std::size_t SHA1_BLOCK_SIZE  = 64;
constexpr std::size_t SHA1_OUTPUT_SIZE = 20;

constexpr std::size_t align_val        = 16;
constexpr std::size_t digest_align_val = 32;
constexpr std::size_t block_align_val  = SHA1_BLOCK_SIZE;

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

// NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
const char impl_name[] = "sha1-arm";

using SHA1StateScalar = std::array<uint8_t, 20>;
using SHA1BlockScalar = std::array<uint8_t, 64>;

extern "C" void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i,
                                const SHA1StateScalar &state);
extern "C" void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i,
                                const SHA1BlockScalar &block);

extern "C" void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32_t (&v)[4]);
extern "C" void dump_uint8x16_t(const char *const _Nonnull prefix, const uint8_t (&v)[16]);
extern "C" void dump_uint8x16x2_t(const char *const _Nonnull prefix, const uint8_t (&v)[32]);

// Helper function to determine the size of the string literal
template <typename T, std::size_t N>
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

template <typename T, typename F>
constexpr T to_from_cast(const F *__restrict _Nonnull val) { // NOLINT(misc-include-cleaner)
    // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
    return reinterpret_cast<T>(static_cast<F *>(val));
}

template <typename T, typename F>
constexpr T to_from_cast(std::remove_pointer_t<F> *__restrict _Nonnull val) { // NOLINT(misc-include-cleaner)
    // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
    return reinterpret_cast<T>(static_cast<std::remove_pointer_t<F> *>(val));
}
#pragma GCC diagnostic pop

} // namespace

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpadded"
// NOLINTBEGIN(misc-non-private-member-variables-in-classes)
struct alignas(digest_align_val) SHA1State {
    SHA1State() {
        abcd = vsetq_lane_u32(0x67452301, vdupq_n_u32(0), 0);
        abcd = vsetq_lane_u32(0xEFCDAB89, abcd, 1);
        abcd = vsetq_lane_u32(0x98BADCFE, abcd, 2);
        abcd = vsetq_lane_u32(0x10325476, abcd, 3);
    }
    SHA1State(const uint32x4_t abcd_, const uint32_t e_) : abcd{abcd_}, e{e_} {}
    uint32x4_t abcd;        // Represents H0, H1, H2, H3
    uint32_t e{0xC3D2E1F0}; // Represents H4
};
// NOLINTEND(misc-non-private-member-variables-in-classes)
#pragma GCC diagnostic pop

struct alignas(block_align_val) SHA1Block {
    std::array<uint32_t, 16> words;
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
};

namespace {

extern "C" void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i,
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

void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i, const SHA1Block &block) {
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

extern "C" void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i,
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

void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i, const SHA1State &state) {
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

void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32x4_t v) {
#ifdef DO_DUMP
    printf("%s v[0]: 0x%08x v[1]: 0x%08x v[2]: 0x%08x v[3]: 0x%08x\n", prefix, v[0], v[1], v[2], v[3]);
#else
    (void)prefix;
    (void)v;
#endif
}

extern "C" void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32_t (&v)[4]) {
#ifdef DO_DUMP
    uint32x4_t dv{v[0], v[1], v[2], v[3]};
    dump_uint32x4_t(prefix, dv);
#else
    (void)prefix;
    (void)v;
#endif
}

void dump_uint8x16_t(const char *const _Nonnull prefix, const uint8x16_t v) {
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

extern "C" void dump_uint8x16_t(const char *const _Nonnull prefix, const uint8_t (&v)[16]) {
#ifdef DO_DUMP_8x16
    uint8x16_t dv{v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15]};
    dump_uint8x16_t(prefix, dv);
#else
    (void)prefix;
    (void)v;
#endif
}

void dump_uint8x16x2_t(const char *const _Nonnull prefix, const uint8x16x2_t v) {
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
#else
    (void)prefix;
    (void)v;
#endif
}

extern "C" void dump_uint8x16x2_t(const char *const _Nonnull prefix, const uint8_t (&v)[32]) {
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

} // namespace

static size_t block_cnt;
static size_t state_cnt;

class SHA1 {
public:
    template <std::size_t N>
    // NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
    static SHA1Digest hash(const uint8_t (&data)[N]) {
        static_assert(N > 0, "Input data must be non-empty");
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

    template <std::size_t N> static SHA1Digest hash(const std::array<uint8_t, N> &data) {
        static_assert(N > 0, "Input data must be non-empty");
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

    // clang-tidy complains about __restrict not being in an included header -_-
    // NOLINTNEXTLINE(misc-include-cleaner)
    static void digest_to_hex(const uint8_t *__restrict _Nonnull digest, char *__restrict _Nonnull hex_str) {
        alignas(align_val) const uint8x16_t mask4 = vdupq_n_u8(0x0F); // Mask for low 4 bits
        // alignas(align_val) const uint8x16_t mask8 = vdupq_n_u8(0xF0); // Mask for high 4 bits

        // Load the first 16 bytes of the digest
        alignas(align_val) const uint8x16_t input = vld1q_u8(digest);
        alignas(align_val) const uint8x16_t hi    = vshrq_n_u8(input, 4);   // Shift high nibbles down
        alignas(align_val) const uint8x16_t lo    = vandq_u8(input, mask4); // Isolate low nibbles
        dump_uint8x16_t("input", input);
        dump_uint8x16_t("   hi", hi);
        dump_uint8x16_t("   lo", lo);

        alignas(align_val) static constinit std::array<uint8_t, 16> hex_chars = {
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
        alignas(align_val) const uint8x16_t lut = vld1q_u8(hex_chars.data());
        dump_uint8x16_t("  lut", lut);

        // Convert to ASCII hex characters
        alignas(align_val) const uint8x16_t hex_hi = vqtbl1q_u8(lut, hi);
        alignas(align_val) const uint8x16_t hex_lo = vqtbl1q_u8(lut, lo);
        dump_uint8x16_t("hexhi", hex_hi);
        dump_uint8x16_t("hexlo", hex_lo);

        // Store the results interleaved
        alignas(align_val) const uint8x16x2_t hex_chars_interleaved = vzipq_u8(hex_hi, hex_lo);
        dump_uint8x16x2_t("hexil", hex_chars_interleaved);
        // vst2q_u8(to_from_cast(uint8_t *, char *, hex_str), hex_chars_interleaved);
        vst2q_u8((to_from_cast<uint8_t *, char *>(hex_str)), hex_chars_interleaved);

        // Handle the remaining 4 bytes using SWAR in GPRs
        // NOLINTBEGIN(cppcoreguidelines-pro-type-reinterpret-cast)
        alignas(align_val) const uint32_t remaining_bytes = *reinterpret_cast<const uint32_t *>(digest + 16);
        // NOLINTEND(cppcoreguidelines-pro-type-reinterpret-cast)

        const uint64_t high_nibbles = (remaining_bytes & 0xF0F0F0F0U) >> 4ULL;
        const uint64_t low_nibbles  = remaining_bytes & 0x0F0F0F0FU;

        const uint64_t base_digits   = 0x3030303030303030ULL; // '0' * 8
        const uint64_t mask_is_digit = 0x0707070707070707ULL; // To differentiate digits from letters

        const uint64_t is_digit_high = ((high_nibbles + mask_is_digit) & 0x1010101010101010ULL) >> 4ULL;
        const uint64_t high_hex =
            high_nibbles + base_digits + ((is_digit_high ^ 0x1010101010101010ULL) >> 1U & 0x2020202020202020ULL);

        const uint64_t is_digit_low = ((low_nibbles + mask_is_digit) & 0x1010101010101010ULL) >> 4ULL;
        const uint64_t low_hex =
            low_nibbles + base_digits + ((is_digit_low ^ 0x1010101010101010ULL) >> 1ULL & 0x2020202020202020ULL);

        const uint64_t hex_packed = ((high_hex & UINT32_MAX) << 32ULL) | low_hex;

        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        *reinterpret_cast<uint64_t *>(hex_str + 32) = hex_packed;
        hex_str[SHA1_OUTPUT_SIZE * 2]               = '\0';
    }

    static void digest_to_hex_simple(const uint8_t *__restrict _Nonnull digest, char *__restrict _Nonnull hex_str) {
        for (size_t i = 0; i < SHA1_OUTPUT_SIZE; ++i, hex_str += 2) {
            // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
            byte_to_ascii_hex(digest[i], reinterpret_cast<std::array<char, 2> &>(*hex_str));
        }
        *hex_str = '\0';
    }

private:
    static constexpr std::array<uint32_t, 4> K = {0x5A827999U, 0x6ED9EBA1U, 0x8F1BBCDCU, 0xCA62C1D6U};

#if defined(__clang__)
    __attribute__((no_sanitize("unsigned-integer-overflow")))
#endif
    static void
    process_block(const uint8_t *__restrict _Nonnull block, SHA1State &state) {
        SHA1Block db{};
        dump_sha1_state(impl_name, __LINE__, state_cnt++, state);
        dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, reinterpret_cast<const SHA1BlockScalar &>(*block));

        uint32x4_t abcd = state.abcd;
        uint32_t e      = state.e;

        // Use aligned loads for the message schedule
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        alignas(block_align_val) uint32x4x4_t w = vld1q_u32_x4(reinterpret_cast<const uint32_t *>(block));

        dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        if constexpr (std::endian::native == std::endian::little) {
            // Byte swap the initial words
            dump_uint32x4_t("w.val[0] before:", w.val[0]);
            w.val[0] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[0])));
            dump_uint32x4_t("w.val[0] after: ", w.val[0]);
            dump_uint32x4_t("w.val[1] before:", w.val[1]);
            w.val[1] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[1])));
            dump_uint32x4_t("w.val[1] after: ", w.val[1]);
            dump_uint32x4_t("w.val[2] before:", w.val[2]);
            w.val[2] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[2])));
            dump_uint32x4_t("w.val[2] after: ", w.val[2]);
            dump_uint32x4_t("w.val[3] before:", w.val[3]);
            w.val[3] = vreinterpretq_u32_u8(vrev32q_u8(vreinterpretq_u8_u32(w.val[3])));
            dump_uint32x4_t("w.val[3] after: ", w.val[3]);
        }

        dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        // Constants for each set of 20 rounds
        const uint32x4_t k1 = vdupq_n_u32(K[0]);
        const uint32x4_t k2 = vdupq_n_u32(K[1]);
        const uint32x4_t k3 = vdupq_n_u32(K[2]);
        const uint32x4_t k4 = vdupq_n_u32(K[3]);

        // First 20 rounds (K1)
        for (int i = 0; i < 20; ++i) {
            if (i < 16) {
                w.val[i % 4] = vsha1su0q_u32(w.val[(i + 2) % 4], w.val[(i + 3) % 4], w.val[i % 4]);
            }

            // uint32x4_t temp = vsha1cq_u32(abcd, e, w.val[i % 4]);
            // abcd            = vextq_u32(abcd, abcd, 1); // Rotate the lanes of abcd
            // abcd            = vsetq_lane_u32(e, abcd, 3);
            // e               = vsha1h_u32(vgetq_lane_u32(temp, 0));

            abcd = vsha1cq_u32(abcd, e, w.val[i % 4]);
            e    = vsha1h_u32(vgetq_lane_u32(abcd, 0));

            if (i < 16) {
                w.val[i % 4] = vsha1su1q_u32(w.val[i % 4], w.val[(i + 1) % 4]);
            }
            w.val[i % 4] = vaddq_u32(w.val[i % 4], k1);

            if (i == 0 || i == 15) {
                dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
                dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);
            }
        }

        dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        // Rounds 21-40 (K2)
        for (int i = 20; i < 40; ++i) {
            w.val[i % 4] = vsha1su0q_u32(w.val[(i + 2) % 4], w.val[(i + 3) % 4], w.val[i % 4]);

            uint32x4_t temp = vsha1pq_u32(abcd, e, w.val[i % 4]);
            abcd            = vextq_u32(abcd, abcd, 1);
            abcd            = vsetq_lane_u32(e, abcd, 3);
            e               = vsha1h_u32(vgetq_lane_u32(temp, 0));

            w.val[i % 4] = vsha1su1q_u32(w.val[i % 4], w.val[(i + 1) % 4]);
            w.val[i % 4] = vaddq_u32(w.val[i % 4], k2);
        }

        dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        // Rounds 41-60 (K3)
        for (int i = 40; i < 60; ++i) {
            w.val[i % 4] = vsha1su0q_u32(w.val[(i + 2) % 4], w.val[(i + 3) % 4], w.val[i % 4]);

            uint32x4_t temp = vsha1mq_u32(abcd, e, w.val[i % 4]);
            abcd            = vextq_u32(abcd, abcd, 1);
            abcd            = vsetq_lane_u32(e, abcd, 3);
            e               = vsha1h_u32(vgetq_lane_u32(temp, 0));

            w.val[i % 4] = vsha1su1q_u32(w.val[i % 4], w.val[(i + 1) % 4]);
            w.val[i % 4] = vaddq_u32(w.val[i % 4], k3);
        }

        dump_sha1_state(impl_name, __LINE__, state_cnt++, SHA1State{abcd, e});
        dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);

        // Rounds 61-80 (K4)
        for (int i = 60; i < 80; ++i) {
            w.val[i % 4] = vsha1su0q_u32(w.val[(i + 2) % 4], w.val[(i + 3) % 4], w.val[i % 4]);

            uint32x4_t temp = vsha1pq_u32(abcd, e, w.val[i % 4]);
            abcd            = vextq_u32(abcd, abcd, 1);
            abcd            = vsetq_lane_u32(e, abcd, 3);
            e               = vsha1h_u32(vgetq_lane_u32(temp, 0));

            w.val[i % 4] = vsha1su1q_u32(w.val[i % 4], w.val[(i + 1) % 4]);
            w.val[i % 4] = vaddq_u32(w.val[i % 4], k4);
        }

        state.abcd = vaddq_u32(state.abcd, abcd);
        state.e += e;

        dump_sha1_state(impl_name, __LINE__, state_cnt++, state);
        dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, db = w);
    }

    static void pad_and_finalize(const uint8_t *__restrict _Nonnull data, std::size_t len, SHA1State &state) {
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

    static void process_short(const uint8_t *__restrict _Nonnull data, std::size_t len, SHA1State &state) {
        pad_and_finalize(data, len, state);
    }

    static void process_medium(const uint8_t *__restrict _Nonnull data, std::size_t len, SHA1State &state) {
        const uint8_t *__restrict _Nonnull end = data + len - (len % SHA1_BLOCK_SIZE);
        for (const uint8_t *__restrict _Nonnull p = data; p < end; p += SHA1_BLOCK_SIZE) {
            process_block(p, state);
        }
        pad_and_finalize(end, len % SHA1_BLOCK_SIZE, state);
    }

    static void process_large(const uint8_t *__restrict _Nonnull data, std::size_t len, SHA1State &state) {
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
        hash_output.bytes()[16] = (state.e >> 24U) & 0xFFU;
        hash_output[17]         = (state.e >> 16U) & 0xFFU;
        hash_output[18]         = (state.e >> 8U) & 0xFFU;
        hash_output[19]         = state.e & 0xFFU;

        return hash_output;
    }

    static uint8_t nibble_to_ascii_hex(const uint8_t chr) {
        if (chr <= 9) {
            return chr + '0';
        }
        if (chr >= 0xA && chr <= 0xF) {
            return chr - 0xA + 'a';
        }
        __builtin_unreachable();
    }

    static void byte_to_ascii_hex(uint8_t n, std::array<char, 2> &hex) {
        hex[0] = static_cast<char>(nibble_to_ascii_hex(n >> 4U));
        hex[1] = static_cast<char>(nibble_to_ascii_hex(n & 0xFU));
    }
};

int main() {
    // Example data
    alignas(SHA1_BLOCK_SIZE) static constinit auto str =
        cstrlit_to_std_array<uint8_t>("The quick brown fox jumps over the lazy dog\n");
    const auto h = SHA1::hash(str);
    alignas(align_val) std::array<char, SHA1_OUTPUT_SIZE * 2 + 1> hex_str{};

    printf("SHA-1 Digest dumb:         "
           "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%"
           "02hhx%02hhx%02hhx%02hhx%02hhx%02hhx\n",
           h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11], h[12], h[13], h[14], h[15], h[16],
           h[17], h[18], h[19]);

    SHA1::digest_to_hex_simple(h.bytes(), hex_str.data());
    printf("SHA-1 Digest simple:       %s\n", hex_str.data());

    SHA1::digest_to_hex(h.bytes(), hex_str.data());
    printf("SHA-1 Digest:              %s\n", hex_str.data());
    printf("\n\n\n");

#ifdef USE_TEENY
    SHA1Digest th{};
    assert(!sha1digest(th.bytes(), hex_str.data(), static_cast<const uint8_t *>(str.data()), str.size()));

    printf("SHA-1 Digest dumb teeny:   "
           "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%"
           "02hhx%02hhx%02hhx\n",
           th[0], th[1], th[2], th[3], th[4], th[5], th[6], th[7], th[8], th[9], th[10], th[11], th[12], th[13], th[14],
           th[15], th[16], th[17], th[18], th[19]);

    SHA1::digest_to_hex_simple(th.bytes(), hex_str.data());
    printf("SHA-1 Digest simple teeny: %s\n", hex_str.data());

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

    SHA1::digest_to_hex_simple(ch.bytes(), hex_str.data());
    printf("SHA-1 Digest simple cifra: %s\n", hex_str.data());

    SHA1::digest_to_hex(ch.bytes(), hex_str.data());
    printf("SHA-1 Digest cifra:        %s\n", hex_str.data());
#endif

    return 0;
}
