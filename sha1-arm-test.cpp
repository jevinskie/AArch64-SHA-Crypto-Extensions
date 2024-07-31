#undef NDEBUG
#include <cassert>

#include <arm_acle.h>
#include <arm_neon.h>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>

constexpr std::size_t SHA1_BLOCK_SIZE  = 64;
constexpr std::size_t SHA1_OUTPUT_SIZE = 20;

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpadded"
struct alignas(16) SHA1State {
    uint32x4_t abcd; // Represents H0, H1, H2, H3
    uint32_t e;      // Represents H4
};
#pragma GCC diagnostic pop

struct alignas(16) SHA1Block {
    uint32_t words[16];
};

class SHA1 {
public:
    template <std::size_t N>
    static std::array<uint8_t, SHA1_OUTPUT_SIZE> hash(const uint8_t (&data)[N]) {
        static_assert(N > 0, "Input data must be non-empty");
        SHA1State state;
        initialize(state);
        if constexpr (N <= 32) {
            process_short(data, N, state);
        } else if constexpr (N <= 256) {
            process_medium(data, N, state);
        } else {
            process_large(data, N, state);
        }
        return state_to_bytes(state);
    }

    static void digest_to_hex(const uint8_t *__restrict digest, char *__restrict hex_str) {
        alignas(16) const uint8x16_t mask4 = vdupq_n_u8(0x0F); // Mask for low 4 bits
        alignas(16) const uint8x16_t mask8 = vdupq_n_u8(0xF0); // Mask for high 4 bits

        // Load the first 16 bytes of the digest
        alignas(16) const uint8x16_t input = vld1q_u8(digest);
        alignas(16) const uint8x16_t hi    = vshrq_n_u8(input, 4);   // Shift high nibbles down
        alignas(16) const uint8x16_t lo    = vandq_u8(input, mask4); // Isolate low nibbles

        alignas(16) static const uint8_t hex_chars[16] = {'0', '1', '2', '3', '4', '5', '6', '7',
                                                          '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
        alignas(16) static const uint8x16_t lut        = vld1q_u8(hex_chars);

        // Convert to ASCII hex characters
        alignas(16) const uint8x16_t hex_hi = vqtbl1q_u8(lut, hi);
        alignas(16) const uint8x16_t hex_lo = vqtbl1q_u8(lut, lo);

        // Store the results interleaved
        alignas(16) const uint8x16x2_t hex_chars_interleaved = vzipq_u8(hex_hi, hex_lo);
        vst2q_u8(reinterpret_cast<uint8_t *>(hex_str), hex_chars_interleaved);

        // Handle the remaining 4 bytes using SWAR in GPRs
        alignas(16) const uint32_t remaining_bytes =
            *reinterpret_cast<const uint32_t *>(digest + 16);

        const uint64_t high_nibbles = (remaining_bytes & 0xF0F0F0F0) >> 4;
        const uint64_t low_nibbles  = remaining_bytes & 0x0F0F0F0F;

        const uint64_t base_digits   = 0x3030303030303030; // '0' * 8
        const uint64_t mask_is_digit = 0x0707070707070707; // To differentiate digits from letters

        const uint64_t is_digit_high = ((high_nibbles + mask_is_digit) & 0x1010101010101010) >> 4;
        const uint64_t high_hex      = high_nibbles + base_digits +
                                  ((is_digit_high ^ 0x1010101010101010) >> 1 & 0x2020202020202020);

        const uint64_t is_digit_low = ((low_nibbles + mask_is_digit) & 0x1010101010101010) >> 4;
        const uint64_t low_hex      = low_nibbles + base_digits +
                                 ((is_digit_low ^ 0x1010101010101010) >> 1 & 0x2020202020202020);

        const uint64_t hex_packed = (high_hex << 32) | low_hex;

        *reinterpret_cast<uint64_t *>(hex_str + 32) = hex_packed;
        hex_str[SHA1_OUTPUT_SIZE * 2]               = '\0';
    }

private:
    static constexpr uint32_t K[4] = {0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6};

    static void initialize(SHA1State &state) {
        state.abcd = vsetq_lane_u32(0x67452301, vdupq_n_u32(0), 0);
        state.abcd = vsetq_lane_u32(0xEFCDAB89, state.abcd, 1);
        state.abcd = vsetq_lane_u32(0x98BADCFE, state.abcd, 2);
        state.abcd = vsetq_lane_u32(0x10325476, state.abcd, 3);
        state.e    = 0xC3D2E1F0;
    }

    static void process_block(const uint8_t *__restrict block, SHA1State &state) {
        uint32x4_t abcd = state.abcd;
        uint32_t e      = state.e;

        // Use aligned loads for the message schedule
        const uint32x4x4_t w = vld1q_u32_x4(reinterpret_cast<const uint32_t *>(block));

        for (int i = 0; i < 20; ++i) {
            uint32x4_t temp = vsha1cq_u32(abcd, e, w.val[0]);
            abcd            = vextq_u32(abcd, abcd, 1); // Rotate the lanes of abcd
            abcd            = vsetq_lane_u32(e, abcd, 3);
            e               = vgetq_lane_u32(temp, 0);

            temp = vsha1cq_u32(abcd, e, w.val[1]);
            abcd = vextq_u32(abcd, abcd, 1);
            abcd = vsetq_lane_u32(e, abcd, 3);
            e    = vgetq_lane_u32(temp, 0);

            temp = vsha1cq_u32(abcd, e, w.val[2]);
            abcd = vextq_u32(abcd, abcd, 1);
            abcd = vsetq_lane_u32(e, abcd, 3);
            e    = vgetq_lane_u32(temp, 0);

            temp = vsha1cq_u32(abcd, e, w.val[3]);
            abcd = vextq_u32(abcd, abcd, 1);
            abcd = vsetq_lane_u32(e, abcd, 3);
            e    = vgetq_lane_u32(temp, 0);
        }

        state.abcd = vaddq_u32(state.abcd, abcd);
        state.e += e;
    }

    static void pad_and_finalize(const uint8_t *__restrict data, std::size_t len,
                                 SHA1State &state) {
        alignas(16) SHA1Block buffer = {};
        std::memcpy(buffer.words, data, len);
        reinterpret_cast<uint8_t *>(buffer.words)[len] = 0x80;

        if (len >= 56) {
            process_block(reinterpret_cast<const uint8_t *>(buffer.words), state);
            std::memset(&buffer, 0, sizeof(buffer));
        }

        buffer.words[14] = 0;
        buffer.words[15] = static_cast<uint32_t>(len * 8); // Length in bits

        process_block(reinterpret_cast<const uint8_t *>(buffer.words), state);
    }

    static void process_short(const uint8_t *__restrict data, std::size_t len, SHA1State &state) {
        pad_and_finalize(data, len, state);
    }

    static void process_medium(const uint8_t *__restrict data, std::size_t len, SHA1State &state) {
        const uint8_t *__restrict end = data + len - (len % SHA1_BLOCK_SIZE);
        for (const uint8_t *__restrict p = data; p < end; p += SHA1_BLOCK_SIZE) {
            process_block(p, state);
        }
        pad_and_finalize(end, len % SHA1_BLOCK_SIZE, state);
    }

    static void process_large(const uint8_t *__restrict data, std::size_t len, SHA1State &state) {
        const uint8_t *__restrict end = data + len - (len % SHA1_BLOCK_SIZE);
        for (const uint8_t *__restrict p = data; p < end; p += SHA1_BLOCK_SIZE) {
            process_block(p, state);
        }
        pad_and_finalize(end, len % SHA1_BLOCK_SIZE, state);
    }

    static std::array<uint8_t, SHA1_OUTPUT_SIZE> state_to_bytes(const SHA1State &state) {
        std::array<uint8_t, SHA1_OUTPUT_SIZE> hash_output;

        // Use NEON intrinsics to convert state.abcd to bytes
        uint8x16_t abcd_bytes = vreinterpretq_u8_u32(state.abcd);
        vst1q_u8(hash_output.data(), abcd_bytes);

        // Convert state.e to bytes and store it
        hash_output[16] = (state.e >> 24) & 0xFF;
        hash_output[17] = (state.e >> 16) & 0xFF;
        hash_output[18] = (state.e >> 8) & 0xFF;
        hash_output[19] = state.e & 0xFF;

        return hash_output;
    }
};

int main() {
    // Example data
    alignas(16) const uint8_t str[] = "The quick brown fox jumps over the lazy dog\n";
    alignas(16) uint8_t data[sizeof(str) - 1];
    memcpy(data, str, sizeof(data));
    alignas(16) std::array<uint8_t, SHA1_OUTPUT_SIZE> h = SHA1::hash(data);
    alignas(16) char hex_str[SHA1_OUTPUT_SIZE * 2 + 1];
    printf("SHA-1 Digest dumb: "
           "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%"
           "02hhx%02hhx%02hhx%02hhx%02hhx%02hhx\n",
           h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11], h[12], h[13],
           h[14], h[15], h[16], h[17], h[18], h[19]);
    SHA1::digest_to_hex(h.data(), hex_str);

    printf("SHA-1 Digest     : %s\n", hex_str);
    return 0;
}
