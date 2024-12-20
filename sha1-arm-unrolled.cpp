#include "sha1-arm-unrolled.h"
#include <_types/_uint32_t.h>

#undef NDEBUG
#include <cassert>

#include <arm_neon.h>
#include <array>
#include <bit>
#include <cstring>
#include <fmt/format.h>

#define ANSI_BOLD_RED_FG    "\x1b[38;5;196m"
#define ANSI_BOLD_GREEN_FG  "\x1b[38;5;34m"
#define ANSI_BOLD_BLUE_FG   "\x1b[38;5;81m"
#define ANSI_BOLD_ORANGE_FG "\x1b[38;5;208m"
#define ANSI_BOLD_VIOLET_FG "\x1b[38;5;207m"
#define ASNI_BOLD_PINK_FG   "\x1b[38;5;223m"
#define ANSI_RESET          "\x1b[1;0m"

#ifdef DO_PRINT_ROUNDS
#define PRND(n) fmt::print("r: {}\n", (n))
#else
#define PRND(n)
#endif

// #include "sha1-wrappers.h"
extern void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32x4_t v);

// https://github.com/RustCrypto/hashes/blob/master/sha1/src/compress/aarch64.rs
// Apache License, Version 2.0
// MIT license

namespace {
constexpr std::array<uint32_t, 4> K = {0x5A827999U, 0x6ED9EBA1U, 0x8F1BBCDCU, 0xCA62C1D6U};
} // namespace

template <size_t N>
static void sha1_arm_unrolled_compress(uint32_t *__restrict _Nonnull state, const uint8_t *__restrict _Nonnull blocks)
#if defined(__clang__)
    __attribute__((no_sanitize("unsigned-integer-overflow"), noinline))
#endif
{
    uint32x4_t abcd = vld1q_u32(state);
    uint32_t e0     = state[4];
    uint32_t e1;
    uint32x4_t tmp0, tmp1;
    const uint32x4_t k0 = vdupq_n_u32(K[0]);
    const uint32x4_t k1 = vdupq_n_u32(K[1]);
    const uint32x4_t k2 = vdupq_n_u32(K[2]);
    const uint32x4_t k3 = vdupq_n_u32(K[3]);

    for (size_t i = 0; i < N; ++i) {
        const uint8_t *block      = blocks + (i * 64);
        const uint32x4_t abcd_cpy = abcd;
        const uint32_t e0_cpy     = e0;

        // Load and reverse byte order
        uint32x4_t msg0 = vreinterpretq_u32_u8(vrev32q_u8(vld1q_u8(block + 16 * 0)));
        uint32x4_t msg1 = vreinterpretq_u32_u8(vrev32q_u8(vld1q_u8(block + 16 * 1)));
        uint32x4_t msg2 = vreinterpretq_u32_u8(vrev32q_u8(vld1q_u8(block + 16 * 2)));
        uint32x4_t msg3 = vreinterpretq_u32_u8(vrev32q_u8(vld1q_u8(block + 16 * 3)));

        tmp0 = vaddq_u32(msg0, k0);
        tmp1 = vaddq_u32(msg1, k0);

        // Rounds 0-3
        PRND("r: 0\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k0);
        msg0 = vsha1su0q_u32(msg0, msg1, msg2);

        // Rounds 4-7
        PRND("r: 4\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k0);
        msg0 = vsha1su1q_u32(msg0, msg3);
        msg1 = vsha1su0q_u32(msg1, msg2, msg3);

        // Rounds 8-11
        PRND("r: 8\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg0, k0);
        msg1 = vsha1su1q_u32(msg1, msg0);
        msg2 = vsha1su0q_u32(msg2, msg3, msg0);

        // Rounds 12-15
        PRND("r: 12\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg1, k1);
        msg2 = vsha1su1q_u32(msg2, msg1);
        msg3 = vsha1su0q_u32(msg3, msg0, msg1);

        // Rounds 16-19
        PRND("r: 16\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k1);
        msg3 = vsha1su1q_u32(msg3, msg2);
        msg0 = vsha1su0q_u32(msg0, msg1, msg2);

        // Rounds 20-23
        PRND("r: 20\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k1);
        msg0 = vsha1su1q_u32(msg0, msg3);
        msg1 = vsha1su0q_u32(msg1, msg2, msg3);

        // Rounds 24-27
        PRND("r: 24\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg0, k1);
        msg1 = vsha1su1q_u32(msg1, msg0);
        msg2 = vsha1su0q_u32(msg2, msg3, msg0);

        // Rounds 28-31
        PRND("r: 28\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg1, k1);
        msg2 = vsha1su1q_u32(msg2, msg1);
        msg3 = vsha1su0q_u32(msg3, msg0, msg1);

        // Rounds 32-35
        PRND("r: 32\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k2);
        msg3 = vsha1su1q_u32(msg3, msg2);
        msg0 = vsha1su0q_u32(msg0, msg1, msg2);

        // Rounds 36-39
        PRND("r: 36\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k2);
        msg0 = vsha1su1q_u32(msg0, msg3);
        msg1 = vsha1su0q_u32(msg1, msg2, msg3);

        // Rounds 40-43
        PRND("r: 40\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg0, k2);
        msg1 = vsha1su1q_u32(msg1, msg0);
        msg2 = vsha1su0q_u32(msg2, msg3, msg0);

        // Rounds 44-47
        PRND("r: 44\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg1, k2);
        msg2 = vsha1su1q_u32(msg2, msg1);
        msg3 = vsha1su0q_u32(msg3, msg0, msg1);

        // Rounds 48-51
        PRND("r: 48\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k2);
        msg3 = vsha1su1q_u32(msg3, msg2);
        msg0 = vsha1su0q_u32(msg0, msg1, msg2);

        // Rounds 52-55
        PRND("r: 52\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k3);
        msg0 = vsha1su1q_u32(msg0, msg3);
        msg1 = vsha1su0q_u32(msg1, msg2, msg3);

        // Rounds 56-59
        PRND("r: 56\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg0, k3);
        msg1 = vsha1su1q_u32(msg1, msg0);
        msg2 = vsha1su0q_u32(msg2, msg3, msg0);

        // Rounds 60-63
        PRND("r: 60\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg1, k3);
        msg2 = vsha1su1q_u32(msg2, msg1);
        msg3 = vsha1su0q_u32(msg3, msg0, msg1);

        // Rounds 64-67
        PRND("r: 64\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k3);
        msg3 = vsha1su1q_u32(msg3, msg2);

        // Rounds 68-71
        PRND("r: 68\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k3);

        // Rounds 72-75
        PRND("r: 72\n");
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e0, tmp0);

        // Rounds 76-79
        PRND("r: 76\n");
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);

        // Update state
        abcd = vaddq_u32(abcd_cpy, abcd);
        e0 += e0_cpy;
    }

    // Save state
    vst1q_u32(state, abcd);
    state[4] = e0;
}

static void pad_and_finalize(const uint8_t *__restrict _Nullable data, size_t len,
                             uint32_t *__restrict _Nonnull state) {
    fmt::print("pad_and_finalize len: {} data: {}\n", len, fmt::ptr(data));
    alignas(64) uint8_t buffer[64] = {};
    assert(len <= sizeof(buffer));
    std::memcpy(buffer, data, len);
    buffer[len] = 0x80;

    if (len >= 56) {
        fmt::print("pad_and_finalize len >= 56 sha1_arm_unrolled_compress data: {}\n", fmt::ptr(buffer));
        sha1_arm_unrolled_compress<1>(state, buffer);
        std::memset(buffer, 0, sizeof(buffer));
    }

    reinterpret_cast<uint32_t *>(buffer)[14] = 0;
    if constexpr (std::endian::native == std::endian::little) {
        reinterpret_cast<uint32_t *>(buffer)[15] = std::byteswap(static_cast<uint32_t>(len * 8)); // Length in bits
    } else {
        reinterpret_cast<uint32_t *>(buffer)[15] = static_cast<uint32_t>(len * 8); // Length in bits
    }

    fmt::print("pad_and_finalize final sha1_arm_unrolled_compress data: {}\n", fmt::ptr(buffer));
    sha1_arm_unrolled_compress<1>(state, buffer);
}

static void process(const uint8_t *__restrict _Nullable data, size_t len, uint32_t *__restrict _Nonnull state) {
    const size_t block_total_sz = len - (len % 64);
    const size_t remainder_sz   = len - block_total_sz;
    fmt::print("process sz: {} block_total_sz: {} remainder_sz: {}\n", len, block_total_sz, remainder_sz);
    for (size_t i = 0; i < block_total_sz; i += 64) {
        fmt::print("process sha1_arm_unrolled_compress i: {} data: {}\n", i, fmt::ptr(&data[i]));
        sha1_arm_unrolled_compress<1>(state, &data[i]);
    }
    fmt::print("process pad_and_finalize block_total_sz: {} remainder_sz: {} data: {}\n", block_total_sz, remainder_sz,
               fmt::ptr(&data[block_total_sz]));
    pad_and_finalize(&data[block_total_sz], remainder_sz, state);
}

void sha1_arm_unrolled(const uint8_t *_Nullable buf, const size_t sz, uint8_t *__restrict _Nonnull hash) {
    uint32_t state[5] = {0x67452301u, 0xEFCDAB89u, 0x98BADCFEu, 0x10325476u, 0xC3D2E1F0u};
    process(buf, sz, state);
    static_assert(sizeof(state) == 20);
    for (size_t i = 0; i < 5; ++i) {
        state[i] = std::byteswap(state[i]);
    }
    std::memcpy(hash, state, sizeof(state));
}

struct CoolSHA1Digest {
    uint32x4_t abcd;
    uint32_t e;
};

extern "C" CoolSHA1Digest sha1_arm_unrolled_compress_one(const uint32x4_t abcd_p, const uint32_t e_p,
                                                         const uint32x4x4_t blocks_p);

extern "C" CoolSHA1Digest sha1_arm_unrolled_compress_one(const uint32x4_t abcd_p, const uint32_t e_p,
                                                         const uint32x4x4_t blocks_p)
#if defined(__clang__)
    __attribute__((no_sanitize("unsigned-integer-overflow"), noinline))
#endif
{
    uint32x4_t abcd = abcd_p;
    uint32_t e0     = e_p;
    uint32_t e1;
    uint32x4_t tmp0, tmp1;
    const uint32x4_t k0 = vdupq_n_u32(K[0]);
    const uint32x4_t k1 = vdupq_n_u32(K[1]);
    const uint32x4_t k2 = vdupq_n_u32(K[2]);
    const uint32x4_t k3 = vdupq_n_u32(K[3]);

    const uint32x4_t abcd_cpy = abcd;
    const uint32_t e0_cpy     = e0;

    // Load and reverse byte order
    uint32x4_t msg0 = vreinterpretq_u32_u8(vrev32q_u8(blocks_p.val[0]));
    uint32x4_t msg1 = vreinterpretq_u32_u8(vrev32q_u8(blocks_p.val[1]));
    uint32x4_t msg2 = vreinterpretq_u32_u8(vrev32q_u8(blocks_p.val[2]));
    uint32x4_t msg3 = vreinterpretq_u32_u8(vrev32q_u8(blocks_p.val[3]));

    tmp0 = vaddq_u32(msg0, k0);
    tmp1 = vaddq_u32(msg1, k0);

    // Rounds 0-3
    PRND("r: 0\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1cq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg2, k0);
    msg0 = vsha1su0q_u32(msg0, msg1, msg2);

    // Rounds 4-7
    PRND("r: 4\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1cq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg3, k0);
    msg0 = vsha1su1q_u32(msg0, msg3);
    msg1 = vsha1su0q_u32(msg1, msg2, msg3);

    // Rounds 8-11
    PRND("r: 8\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1cq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg0, k0);
    msg1 = vsha1su1q_u32(msg1, msg0);
    msg2 = vsha1su0q_u32(msg2, msg3, msg0);

    // Rounds 12-15
    PRND("r: 12\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1cq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg1, k1);
    msg2 = vsha1su1q_u32(msg2, msg1);
    msg3 = vsha1su0q_u32(msg3, msg0, msg1);

    // Rounds 16-19
    PRND("r: 16\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1cq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg2, k1);
    msg3 = vsha1su1q_u32(msg3, msg2);
    msg0 = vsha1su0q_u32(msg0, msg1, msg2);

    // Rounds 20-23
    PRND("r: 20\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg3, k1);
    msg0 = vsha1su1q_u32(msg0, msg3);
    msg1 = vsha1su0q_u32(msg1, msg2, msg3);

    // Rounds 24-27
    PRND("r: 24\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg0, k1);
    msg1 = vsha1su1q_u32(msg1, msg0);
    msg2 = vsha1su0q_u32(msg2, msg3, msg0);

    // Rounds 28-31
    PRND("r: 28\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg1, k1);
    msg2 = vsha1su1q_u32(msg2, msg1);
    msg3 = vsha1su0q_u32(msg3, msg0, msg1);

    // Rounds 32-35
    PRND("r: 32\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg2, k2);
    msg3 = vsha1su1q_u32(msg3, msg2);
    msg0 = vsha1su0q_u32(msg0, msg1, msg2);

    // Rounds 36-39
    PRND("r: 36\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg3, k2);
    msg0 = vsha1su1q_u32(msg0, msg3);
    msg1 = vsha1su0q_u32(msg1, msg2, msg3);

    // Rounds 40-43
    PRND("r: 40\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1mq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg0, k2);
    msg1 = vsha1su1q_u32(msg1, msg0);
    msg2 = vsha1su0q_u32(msg2, msg3, msg0);

    // Rounds 44-47
    PRND("r: 44\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1mq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg1, k2);
    msg2 = vsha1su1q_u32(msg2, msg1);
    msg3 = vsha1su0q_u32(msg3, msg0, msg1);

    // Rounds 48-51
    PRND("r: 48\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1mq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg2, k2);
    msg3 = vsha1su1q_u32(msg3, msg2);
    msg0 = vsha1su0q_u32(msg0, msg1, msg2);

    // Rounds 52-55
    PRND("r: 52\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1mq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg3, k3);
    msg0 = vsha1su1q_u32(msg0, msg3);
    msg1 = vsha1su0q_u32(msg1, msg2, msg3);

    // Rounds 56-59
    PRND("r: 56\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1mq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg0, k3);
    msg1 = vsha1su1q_u32(msg1, msg0);
    msg2 = vsha1su0q_u32(msg2, msg3, msg0);

    // Rounds 60-63
    PRND("r: 60\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg1, k3);
    msg2 = vsha1su1q_u32(msg2, msg1);
    msg3 = vsha1su0q_u32(msg3, msg0, msg1);

    // Rounds 64-67
    PRND("r: 64\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e0, tmp0);
    tmp0 = vaddq_u32(msg2, k3);
    msg3 = vsha1su1q_u32(msg3, msg2);

    // Rounds 68-71
    PRND("r: 68\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e1, tmp1);
    tmp1 = vaddq_u32(msg3, k3);

    // Rounds 72-75
    PRND("r: 72\n");
    e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e0, tmp0);

    // Rounds 76-79
    PRND("r: 76\n");
    e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
    abcd = vsha1pq_u32(abcd, e1, tmp1);

    // Update state
    abcd = vaddq_u32(abcd_cpy, abcd);
    e0 += e0_cpy;

    return {abcd, e0};
}

extern "C" CoolSHA1Digest sha1_arm_unrolled_compress_one_microcoded(const uint32x4_t abcd_p, const uint32_t e_p,
                                                                    const uint32x4x4_t blocks_p,
                                                                    const uint16_t *_Nonnull microcode_p,
                                                                    const size_t microcode_sz_p);

extern "C" CoolSHA1Digest
sha1_arm_unrolled_compress_one_microcoded(const uint32x4_t abcd_p, const uint32_t e_p, const uint32x4x4_t blocks_p,
                                          const uint16_t *_Nonnull microcode_p, const size_t microcode_sz_p)
#if defined(__clang__)
    __attribute__((no_sanitize("unsigned-integer-overflow"), noinline))
#endif
{

    constexpr uint8_t microcode[] = {0};
    uint32x4_t pres{}, pop0{}, pop2{};
    uint32_t pop1{};
    uint32x4_t su0res{}, su0op0{}, su0op1{}, su0op2{};
    uint32x4_t su1res{}, su1op0{}, su1op1{};
    uint32x4_t cres{}, cop0{}, cop2{};
    uint32_t cop1{};
    uint32x4_t mres{}, mop0{}, mop2{};
    uint32_t mop1{};
    uint32_t hres{}, hop0{};
    uint32x4_t aXres{}, aXop0{}, aXop1{}, aYres{}, aYop0{}, aYop1{};
    uint32x4_t aXYres{};

    // microcoded loop
    // for (size_t i = 0; i < std::size(microcode); ++i) {
    for (size_t i = 0; i < microcode_sz_p; ++i) {
        // const uint16_t c = microcode[i];
        const uint16_t c = microcode_p[i];
        if (c & (1 << 0)) {
            pres = vsha1pq_u32(pop0, pop1, pop2);
        }
        if (c & (1 << 1)) {
            su0res = vsha1su0q_u32(su0op0, su0op1, su0op2);
        }
        if (c & (1 << 2)) {
            su1res = vsha1su1q_u32(su1op0, su1op1);
        }
        if (c & (1 << 3)) {
            cres = vsha1cq_u32(cop0, cop1, cop2);
        }
        if (c & (1 << 4)) {
            mres = vsha1mq_u32(mop0, mop1, mop2);
        }
        if (c & (1 << 5)) {
            hres = vsha1h_u32(hop0);
        }
        if (c & (1 << 6)) {
            aXres = vaddq_u32(aXop0, aXop1);
        }
        if (c & (1 << 7)) {
            aYres = vaddq_u32(aYop0, aYop1);
        }
        if (c & (1 << 8)) {
            pop0 += rand() & 0xff;
            pop1 += rand() & 0xff;
            pop2 += rand() & 0xff;
            su0op0 += rand() & 0xff;
            su0op1 += rand() & 0xff;
            su0op2 += rand() & 0xff;
            su1op0 += rand() & 0xff;
            su1op1 += rand() & 0xff;
            cop0 += rand() & 0xff;
            cop1 += rand() & 0xff;
            cop2 += rand() & 0xff;
            mop0 += rand() & 0xff;
            mop1 += rand() & 0xff;
            mop2 += rand() & 0xff;
            hop0 += rand() & 0xff;
            aXop0 += rand() & 0xff;
            aXop1 += rand() & 0xff;
            aYop0 += rand() & 0xff;
            aYop1 += rand() & 0xff;
        }
    }
    dump_uint32x4_t(ANSI_BOLD_RED_FG "pres" ANSI_RESET "  ", pres);
    dump_uint32x4_t(ANSI_BOLD_ORANGE_FG "su0res" ANSI_RESET, su0res);
    dump_uint32x4_t(ANSI_BOLD_VIOLET_FG "su1res" ANSI_RESET, su1res);
    dump_uint32x4_t(ASNI_BOLD_PINK_FG "cres" ANSI_RESET "  ", cres);
    dump_uint32x4_t(ANSI_BOLD_BLUE_FG "mres" ANSI_RESET "  ", mres);
    fmt::print(ANSI_BOLD_GREEN_FG "hres" ANSI_RESET "  {:#010x}", hres);
    dump_uint32x4_t(ANSI_BOLD_RED_FG "aXres" ANSI_RESET "  ", aXres);
    dump_uint32x4_t(ANSI_BOLD_RED_FG "aYres" ANSI_RESET "  ", aYres);
    dump_uint32x4_t(ANSI_BOLD_RED_FG "pres" ANSI_RESET "  ", pres);

    return {};
}
