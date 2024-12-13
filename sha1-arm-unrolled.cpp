#include "sha1-arm-unrolled.h"

#undef NDEBUG
#include <cassert>

#include <arm_neon.h>
#include <array>
#include <bit>
#include <cstring>

#include "sha1-wrappers.h"

// https://github.com/RustCrypto/hashes/blob/master/sha1/src/compress/aarch64.rs
// Apache License, Version 2.0
// MIT license

namespace {
constexpr std::array<uint32_t, 4> K = {0x5A827999U, 0x6ED9EBA1U, 0x8F1BBCDCU, 0xCA62C1D6U};
} // namespace

[[gnu::noinline]] static void sha1_arm_unrolled_compress(uint32_t *__restrict _Nonnull state,
                                                         const uint8_t *__restrict _Nonnull blocks,
                                                         const size_t num_blocks) {
    uint32x4_t abcd = vld1q_u32(state);
    uint32_t e0     = state[4];
    uint32_t e1;
    uint32x4_t tmp0, tmp1;
    const uint32x4_t k0 = vdupq_n_u32(K[0]);
    const uint32x4_t k1 = vdupq_n_u32(K[1]);
    const uint32x4_t k2 = vdupq_n_u32(K[2]);
    const uint32x4_t k3 = vdupq_n_u32(K[3]);

    for (size_t i = 0; i < num_blocks; ++i) {
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
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k0);
        msg0 = vsha1su0q_u32(msg0, msg1, msg2);

        // Rounds 4-7
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k0);
        msg0 = vsha1su1q_u32(msg0, msg3);
        msg1 = vsha1su0q_u32(msg1, msg2, msg3);

        // Rounds 8-11
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg0, k0);
        msg1 = vsha1su1q_u32(msg1, msg0);
        msg2 = vsha1su0q_u32(msg2, msg3, msg0);

        // Rounds 12-15
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg1, k1);
        msg2 = vsha1su1q_u32(msg2, msg1);
        msg3 = vsha1su0q_u32(msg3, msg0, msg1);

        // Rounds 16-19
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1cq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k1);
        msg3 = vsha1su1q_u32(msg3, msg2);
        msg0 = vsha1su0q_u32(msg0, msg1, msg2);

        // Rounds 20-23
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k1);
        msg0 = vsha1su1q_u32(msg0, msg3);
        msg1 = vsha1su0q_u32(msg1, msg2, msg3);

        // Rounds 24-27
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg0, k1);
        msg1 = vsha1su1q_u32(msg1, msg0);
        msg2 = vsha1su0q_u32(msg2, msg3, msg0);

        // Rounds 28-31
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg1, k1);
        msg2 = vsha1su1q_u32(msg2, msg1);
        msg3 = vsha1su0q_u32(msg3, msg0, msg1);

        // Rounds 32-35
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k2);
        msg3 = vsha1su1q_u32(msg3, msg2);
        msg0 = vsha1su0q_u32(msg0, msg1, msg2);

        // Rounds 36-39
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k2);
        msg0 = vsha1su1q_u32(msg0, msg3);
        msg1 = vsha1su0q_u32(msg1, msg2, msg3);

        // Rounds 40-43
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg0, k2);
        msg1 = vsha1su1q_u32(msg1, msg0);
        msg2 = vsha1su0q_u32(msg2, msg3, msg0);

        // Rounds 44-47
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg1, k2);
        msg2 = vsha1su1q_u32(msg2, msg1);
        msg3 = vsha1su0q_u32(msg3, msg0, msg1);

        // Rounds 48-51
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k2);
        msg3 = vsha1su1q_u32(msg3, msg2);
        msg0 = vsha1su0q_u32(msg0, msg1, msg2);

        // Rounds 52-55
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k3);
        msg0 = vsha1su1q_u32(msg0, msg3);
        msg1 = vsha1su0q_u32(msg1, msg2, msg3);

        // Rounds 56-59
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1mq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg0, k3);
        msg1 = vsha1su1q_u32(msg1, msg0);
        msg2 = vsha1su0q_u32(msg2, msg3, msg0);

        // Rounds 60-63
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg1, k3);
        msg2 = vsha1su1q_u32(msg2, msg1);
        msg3 = vsha1su0q_u32(msg3, msg0, msg1);

        // Rounds 64-67
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e0, tmp0);
        tmp0 = vaddq_u32(msg2, k3);
        msg3 = vsha1su1q_u32(msg3, msg2);

        // Rounds 68-71
        e0   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e1, tmp1);
        tmp1 = vaddq_u32(msg3, k3);

        // Rounds 72-75
        e1   = vsha1h_u32(vgetq_lane_u32(abcd, 0));
        abcd = vsha1pq_u32(abcd, e0, tmp0);

        // Rounds 76-79
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
    alignas(64) uint8_t buffer[64] = {};
    assert(len <= sizeof(buffer));
    std::memcpy(buffer, data, len);
    buffer[len] = 0x80;

    if (len >= 56) {
        sha1_arm_unrolled_compress(state, buffer, 1);
        std::memset(buffer, 0, sizeof(buffer));
    }

    reinterpret_cast<uint32_t *>(buffer)[14] = 0;
    if constexpr (std::endian::native == std::endian::little) {
        reinterpret_cast<uint32_t *>(buffer)[15] = std::byteswap(static_cast<uint32_t>(len * 8)); // Length in bits
    } else {
        reinterpret_cast<uint32_t *>(buffer)[15] = static_cast<uint32_t>(len * 8); // Length in bits
    }

    sha1_arm_unrolled_compress(state, buffer, 1);
}

static void process(const uint8_t *__restrict _Nullable data, size_t len, uint32_t *__restrict _Nonnull state) {
    const size_t block_total_sz = len - (len % 64);
    const size_t remainder_sz   = len - block_total_sz;
    for (size_t i = 0; i < block_total_sz; i += 64) {
        sha1_arm_unrolled_compress(state, &data[i], 1);
    }
    pad_and_finalize(&data[block_total_sz], remainder_sz, state);
}

void sha1_arm_unrolled(const uint8_t *_Nullable buf, const size_t sz, uint8_t *__restrict _Nonnull hash) {
    uint32_t state[5];
    process(buf, sz, state);
    static_assert(sizeof(state) == 20);
    std::memcpy(hash, state, sizeof(state));
}
