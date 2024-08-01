#undef NDEBUG
#include <cassert>

#include <arm_acle.h>
#include <arm_neon.h>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <type_traits>

// NOLINTNEXTLINE(cppcoreguidelines-macro-usage)
// #define to_from_cast(T, F, V) \
//     __extension__({ \
//         /* NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast) */ \
//         reinterpret_cast<T>(static_cast<F>(V)); \
//     })

constexpr std::size_t align_val = 16;

namespace {

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
constexpr T to_from_cast(const F *__restrict val) { // NOLINT(misc-include-cleaner)
    // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
    return reinterpret_cast<T>(static_cast<F *>(val));
}

template <typename T, typename F>
constexpr T to_from_cast(std::remove_pointer_t<F> *__restrict val) { // NOLINT(misc-include-cleaner)
    // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
    return reinterpret_cast<T>(static_cast<std::remove_pointer_t<F> *>(val));
}
#pragma GCC diagnostic pop

} // namespace

constexpr std::size_t SHA1_BLOCK_SIZE  = 64;
constexpr std::size_t SHA1_OUTPUT_SIZE = 20;

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wpadded"
// NOLINTBEGIN(misc-non-private-member-variables-in-classes)
struct alignas(32) SHA1State {
    SHA1State() {
        abcd = vsetq_lane_u32(0x67452301, vdupq_n_u32(0), 0);
        abcd = vsetq_lane_u32(0xEFCDAB89, abcd, 1);
        abcd = vsetq_lane_u32(0x98BADCFE, abcd, 2);
        abcd = vsetq_lane_u32(0x10325476, abcd, 3);
    }
    uint32x4_t abcd;        // Represents H0, H1, H2, H3
    uint32_t e{0xC3D2E1F0}; // Represents H4
};
// NOLINTEND(misc-non-private-member-variables-in-classes)
#pragma GCC diagnostic pop

struct alignas(SHA1_BLOCK_SIZE) SHA1Block {
    std::array<uint32_t, 16> words;
};

class SHA1 {
public:
    template <std::size_t N>
    // NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
    static std::array<uint8_t, SHA1_OUTPUT_SIZE> hash(const uint8_t (&data)[N]) {
        static_assert(N > 0, "Input data must be non-empty");
        SHA1State state{};
        if constexpr (N <= 32) {
            process_short(data, N, state);
        } else if constexpr (N <= 256) {
            process_medium(data, N, state);
        } else {
            process_large(data, N, state);
        }
        return state_to_bytes(state);
    }

    template <std::size_t N>
    static std::array<uint8_t, SHA1_OUTPUT_SIZE> hash(const std::array<uint8_t, N> &data) {
        static_assert(N > 0, "Input data must be non-empty");
        SHA1State state{};
        if constexpr (N <= 32) {
            process_short(data.data(), N, state);
        } else if constexpr (N <= 256) {
            process_medium(data.data(), N, state);
        } else {
            process_large(data.data(), N, state);
        }
        return state_to_bytes(state);
    }

    // clang-tidy complains about __restrict not being in an included header -_-
    // NOLINTNEXTLINE(misc-include-cleaner)
    static void digest_to_hex(const uint8_t *__restrict digest, char *__restrict hex_str) {
        alignas(align_val) const uint8x16_t mask4 = vdupq_n_u8(0x0F); // Mask for low 4 bits
        alignas(align_val) const uint8x16_t mask8 = vdupq_n_u8(0xF0); // Mask for high 4 bits

        // Load the first 16 bytes of the digest
        alignas(align_val) const uint8x16_t input = vld1q_u8(digest);
        alignas(align_val) const uint8x16_t hi    = vshrq_n_u8(input, 4); // Shift high nibbles down
        alignas(align_val) const uint8x16_t lo    = vandq_u8(input, mask4); // Isolate low nibbles

        alignas(align_val) static constinit std::array<uint8_t, 16> hex_chars = {
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};
        alignas(align_val) const uint8x16_t lut = vld1q_u8(hex_chars.data());

        // Convert to ASCII hex characters
        alignas(align_val) const uint8x16_t hex_hi = vqtbl1q_u8(lut, hi);
        alignas(align_val) const uint8x16_t hex_lo = vqtbl1q_u8(lut, lo);

        // Store the results interleaved
        alignas(align_val) const uint8x16x2_t hex_chars_interleaved = vzipq_u8(hex_hi, hex_lo);
        // vst2q_u8(to_from_cast(uint8_t *, char *, hex_str), hex_chars_interleaved);
        vst2q_u8((to_from_cast<uint8_t *, char *>(hex_str)), hex_chars_interleaved);

        // Handle the remaining 4 bytes using SWAR in GPRs
        // NOLINTBEGIN(cppcoreguidelines-pro-type-reinterpret-cast)
        alignas(align_val) const uint32_t remaining_bytes =
            *reinterpret_cast<const uint32_t *>(digest + 16);
        // NOLINTEND(cppcoreguidelines-pro-type-reinterpret-cast)

        const uint64_t high_nibbles = (remaining_bytes & 0xF0F0F0F0U) >> 4ULL;
        const uint64_t low_nibbles  = remaining_bytes & 0x0F0F0F0FU;

        const uint64_t base_digits = 0x3030303030303030ULL; // '0' * 8
        const uint64_t mask_is_digit =
            0x0707070707070707ULL; // To differentiate digits from letters

        const uint64_t is_digit_high =
            ((high_nibbles + mask_is_digit) & 0x1010101010101010ULL) >> 4ULL;
        const uint64_t high_hex =
            high_nibbles + base_digits +
            ((is_digit_high ^ 0x1010101010101010ULL) >> 1U & 0x2020202020202020ULL);

        const uint64_t is_digit_low =
            ((low_nibbles + mask_is_digit) & 0x1010101010101010ULL) >> 4ULL;
        const uint64_t low_hex =
            low_nibbles + base_digits +
            ((is_digit_low ^ 0x1010101010101010ULL) >> 1ULL & 0x2020202020202020ULL);

        const uint64_t hex_packed = (high_hex << 32ULL) | low_hex;

        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        *reinterpret_cast<uint64_t *>(hex_str + 32) = hex_packed;
        hex_str[SHA1_OUTPUT_SIZE * 2]               = '\0';
    }

    static void digest_to_hex_simple(const uint8_t *__restrict digest, char *__restrict hex_str) {
        for (size_t i = 0; i < SHA1_OUTPUT_SIZE; ++i, hex_str += 2) {
            // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
            byte_to_ascii_hex(digest[i], reinterpret_cast<std::array<char, 2> &>(*hex_str));
        }
        *hex_str = '\0';
    }

private:
    static constexpr std::array<uint32_t, 4> K = {0x5A827999U, 0x6ED9EBA1U, 0x8F1BBCDCU,
                                                  0xCA62C1D6U};

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
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
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
        alignas(SHA1_BLOCK_SIZE) SHA1Block buffer = {};
        assert(len <= sizeof(buffer));
        std::memcpy(buffer.words.data(), data, len);
        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        reinterpret_cast<uint8_t *>(buffer.words.data())[len] = 0x80;

        if (len >= 56) {
            // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
            process_block(reinterpret_cast<const uint8_t *>(buffer.words.data()), state);
            std::memset(&buffer, 0, sizeof(buffer));
        }

        buffer.words[14] = 0;
        buffer.words[15] = static_cast<uint32_t>(len * 8); // Length in bits

        // NOLINTNEXTLINE(cppcoreguidelines-pro-type-reinterpret-cast)
        process_block(reinterpret_cast<const uint8_t *>(buffer.words.data()), state);
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
        const size_t block_total_sz = len - (len % SHA1_BLOCK_SIZE);
        const size_t remainder_sz   = len - block_total_sz;
        for (size_t i = 0; i < block_total_sz; i += SHA1_BLOCK_SIZE) {
            process_block(&data[i], state);
        }
        pad_and_finalize(&data[block_total_sz], remainder_sz, state);
    }

    static std::array<uint8_t, SHA1_OUTPUT_SIZE> state_to_bytes(const SHA1State &state) {
        std::array<uint8_t, SHA1_OUTPUT_SIZE> hash_output{};

        // Use NEON intrinsics to convert state.abcd to bytes
        const uint8x16_t abcd_bytes = vreinterpretq_u8_u32(state.abcd);
        vst1q_u8(hash_output.data(), abcd_bytes);

        // Convert state.e to bytes and store it
        hash_output[16] = (state.e >> 24U) & 0xFFU;
        hash_output[17] = (state.e >> 16U) & 0xFFU;
        hash_output[18] = (state.e >> 8U) & 0xFFU;
        hash_output[19] = state.e & 0xFFU;

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
    alignas(align_val) static constinit auto str =
        cstrlit_to_std_array<uint8_t>("The quick brown fox jumps over the lazy dog\n");
    alignas(align_val) const std::array<uint8_t, SHA1_OUTPUT_SIZE> h = SHA1::hash(str);
    alignas(align_val) std::array<char, SHA1_OUTPUT_SIZE * 2 + 1> hex_str{};

    printf("SHA-1 Digest dumb:   "
           "%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx%"
           "02hhx%02hhx%02hhx%02hhx%02hhx%02hhx\n",
           h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11], h[12], h[13],
           h[14], h[15], h[16], h[17], h[18], h[19]);

    SHA1::digest_to_hex_simple(h.data(), hex_str.data());
    printf("SHA-1 Digest simple: %s\n", hex_str.data());

    SHA1::digest_to_hex(h.data(), hex_str.data());
    printf("SHA-1 Digest:        %s\n", hex_str.data());

    return 0;
}
