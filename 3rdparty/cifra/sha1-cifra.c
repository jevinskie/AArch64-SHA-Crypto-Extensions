/*
 * cifra - embedded cryptography library
 * Written in 2014 by Joseph Birr-Pixton <jpixton@gmail.com>
 *
 * To the extent possible under law, the author(s) have dedicated all
 * copyright and related and neighboring rights to this software to the
 * public domain worldwide. This software is distributed without any
 * warranty.
 *
 * You should have received a copy of the CC0 Public Domain Dedication
 * along with this software. If not, see
 * <http://creativecommons.org/publicdomain/zero/1.0/>.
 */

#include <arm_neon.h>
#include <assert.h>
#include <string.h>

#include "sha1-cifra.h"

extern void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i,
                            const uint8_t *const _Nonnull state);
extern void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i,
                            const uint8_t *const _Nonnull block);

extern void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32_t(v)[4]);

static const char impl_name[] = "sha1-cifra.c";
static size_t block_cnt;
static size_t state_cnt;

#define CF_MIN(x, y)                                   \
    ({                                                 \
        typeof(x) CF_MIN__x = (x);                     \
        typeof(y) CF_MIN__y = (y);                     \
        CF_MIN__x < CF_MIN__y ? CF_MIN__x : CF_MIN__y; \
    })

/** Circularly rotate left x by n bits.
 *  0 > n > 32. */
#if defined(__clang__)
__attribute__((no_sanitize("unsigned-shift-base")))
#endif
static inline uint32_t
rotl32(uint32_t x, unsigned n) {
    return (x << n) | (x >> (32 - n));
}

/** Read 4 bytes from buf, as a 32-bit big endian quantity. */
static inline uint32_t read32_be(const uint8_t buf[4]) {
    return ((uint32_t)buf[0] << 24) | ((uint32_t)buf[1] << 16) | ((uint32_t)buf[2] << 8) | ((uint32_t)buf[3]);
}

/** Encode v as a 32-bit big endian quantity into buf. */
static inline void write32_be(uint32_t v, uint8_t buf[4]) {
    *buf++ = (v >> 24) & 0xff;
    *buf++ = (v >> 16) & 0xff;
    *buf++ = (v >> 8) & 0xff;
    *buf   = v & 0xff;
}

/** Encode v as a 64-bit big endian quantity into buf. */
static inline void write64_be(uint64_t v, uint8_t buf[8]) {
    *buf++ = (v >> 56) & 0xff;
    *buf++ = (v >> 48) & 0xff;
    *buf++ = (v >> 40) & 0xff;
    *buf++ = (v >> 32) & 0xff;
    *buf++ = (v >> 24) & 0xff;
    *buf++ = (v >> 16) & 0xff;
    *buf++ = (v >> 8) & 0xff;
    *buf   = v & 0xff;
}

typedef void (*cf_blockwise_in_fn)(void *ctx, const uint8_t *data);

static void cf_blockwise_accumulate_final(uint8_t *partial, size_t *npartial, size_t nblock, const void *inp,
                                          size_t nbytes, cf_blockwise_in_fn process, cf_blockwise_in_fn process_final,
                                          void *ctx) {
    const uint8_t *bufin = inp;
    assert(partial && *npartial < nblock);
    assert(inp || !nbytes);
    assert(process && ctx);

    /* If we have partial data, copy in to buffer. */
    if (*npartial && nbytes) {
        size_t space = nblock - *npartial;
        size_t taken = CF_MIN(space, nbytes);

        memcpy(partial + *npartial, bufin, taken);

        bufin += taken;
        nbytes -= taken;
        *npartial += taken;

        /* If that gives us a full block, process it. */
        if (*npartial == nblock) {
            if (nbytes == 0)
                process_final(ctx, partial);
            else
                process(ctx, partial);
            *npartial = 0;
        }
    }

    /* now nbytes < nblock or *npartial == 0. */

    /* If we have a full block of data, process it directly. */
    while (nbytes >= nblock) {
        /* Partial buffer must be empty, or we're ignoring extant data */
        assert(*npartial == 0);

        if (nbytes == nblock)
            process_final(ctx, bufin);
        else
            process(ctx, bufin);
        bufin += nblock;
        nbytes -= nblock;
    }

    /* Finally, if we have remaining data, buffer it. */
    while (nbytes) {
        size_t space = nblock - *npartial;
        size_t taken = CF_MIN(space, nbytes);

        memcpy(partial + *npartial, bufin, taken);

        bufin += taken;
        nbytes -= taken;
        *npartial += taken;

        /* If we started with *npartial, we must have copied it
         * in first. */
        assert(*npartial < nblock);
    }
}

static void cf_blockwise_accumulate(uint8_t *partial, size_t *npartial, size_t nblock, const void *inp, size_t nbytes,
                                    cf_blockwise_in_fn process, void *ctx) {
    cf_blockwise_accumulate_final(partial, npartial, nblock, inp, nbytes, process, process, ctx);
}

static void cf_blockwise_acc_byte(uint8_t *partial, size_t *npartial, size_t nblock, uint8_t byte, size_t nbytes,
                                  cf_blockwise_in_fn process, void *ctx) {
    /* only memset the whole of the block once */
    int filled = 0;

    while (nbytes) {
        size_t start = *npartial;
        size_t count = CF_MIN(nbytes, nblock - start);

        if (!filled)
            memset(partial + start, byte, count);

        if (start == 0 && count == nblock)
            filled = 1;

        if (start + count == nblock) {
            process(ctx, partial);
            *npartial = 0;
        } else {
            *npartial += count;
        }

        nbytes -= count;
    }
}

static void cf_blockwise_acc_pad(uint8_t *partial, size_t *npartial, size_t nblock, uint8_t fbyte, uint8_t mbyte,
                                 uint8_t lbyte, size_t nbytes, cf_blockwise_in_fn process, void *ctx) {

    switch (nbytes) {
    case 0:
        break;
    case 1:
        fbyte ^= lbyte;
        cf_blockwise_accumulate(partial, npartial, nblock, &fbyte, 1, process, ctx);
        break;
    case 2:
        cf_blockwise_accumulate(partial, npartial, nblock, &fbyte, 1, process, ctx);
        cf_blockwise_accumulate(partial, npartial, nblock, &lbyte, 1, process, ctx);
        break;
    default:
        cf_blockwise_accumulate(partial, npartial, nblock, &fbyte, 1, process, ctx);

        /* If the middle and last bytes differ, then process the last byte separately.
         * Otherwise, just extend the middle block size. */
        if (lbyte != mbyte) {
            cf_blockwise_acc_byte(partial, npartial, nblock, mbyte, nbytes - 2, process, ctx);
            cf_blockwise_accumulate(partial, npartial, nblock, &lbyte, 1, process, ctx);
        } else {
            cf_blockwise_acc_byte(partial, npartial, nblock, mbyte, nbytes - 1, process, ctx);
        }

        break;
    }
}

void cf_sha1_init(cf_sha1_context *ctx) {
    memset(ctx, 0, sizeof *ctx);
    ctx->H[0] = 0x67452301;
    ctx->H[1] = 0xefcdab89;
    ctx->H[2] = 0x98badcfe;
    ctx->H[3] = 0x10325476;
    ctx->H[4] = 0xc3d2e1f0;
}

typedef struct {
    uint32_t a, b, c, d, e;
} dstate_t;

#if defined(__clang__)
__attribute__((no_sanitize("unsigned-integer-overflow")))
#endif
static void
sha1_update_block(void *vctx, const uint8_t *inp) {
    cf_sha1_context *ctx = vctx;

    dump_sha1_state(impl_name, __LINE__, state_cnt++, (const uint8_t *)ctx->H);
    dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, inp);

    /* This is a 16-word window into the whole W array. */
    uint32_t W[16];

    uint32_t a = ctx->H[0], b = ctx->H[1], c = ctx->H[2], d = ctx->H[3], e = ctx->H[4], Wt;

    dump_sha1_state(impl_name, __LINE__, state_cnt++, (const uint8_t *)ctx->H);
    dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, inp);

    for (size_t t = 0; t < 80; t++) {
        /* For W[0..16] we process the input into W.
         * For W[16..79] we compute the next W value:
         *
         * W[t] = (W[t - 3] ^ W[t - 8] ^ W[t - 14] ^ W[t - 16]) <<< 1
         *
         * But all W indices are reduced mod 16 into our window.
         */
        if (t < 16) {
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wcast-align"
            if (t == 0) {
                dump_uint32x4_t("w.val[0] before:", (const uint32_t *)inp);
            } else if (t == 4) {
                dump_uint32x4_t("w.val[1] before:", (const uint32_t *)inp);
            } else if (t == 8) {
                dump_uint32x4_t("w.val[2] before:", (const uint32_t *)inp);
            } else if (t == 12) {
                dump_uint32x4_t("w.val[3] before:", (const uint32_t *)inp);
            }
#pragma GCC diagnostic pop
            W[t] = Wt = read32_be(inp);
            if (t == 3) {
                dump_uint32x4_t("w.val[0] after: ", &W[0]);
            } else if (t == 7) {
                dump_uint32x4_t("w.val[1] after: ", &W[4]);
            } else if (t == 11) {
                dump_uint32x4_t("w.val[2] after: ", &W[8]);
            } else if (t == 15) {
                dump_uint32x4_t("w.val[3] after: ", &W[12]);
            }
            inp += 4;
        } else {
            Wt        = W[(t - 3) % 16] ^ W[(t - 8) % 16] ^ W[(t - 14) % 16] ^ W[(t - 16) % 16];
            Wt        = rotl32(Wt, 1);
            W[t % 16] = Wt;
        }

        uint32_t f, k;

        if (t <= 19) {
            f = (b & c) | (~b & d);
            k = 0x5a827999;
        } else if (t <= 39) {
            f = b ^ c ^ d;
            k = 0x6ed9eba1;
        } else if (t <= 59) {
            f = (b & c) | (b & d) | (c & d);
            k = 0x8f1bbcdc;
        } else {
            f = b ^ c ^ d;
            k = 0xca62c1d6;
        }

        uint32_t temp = rotl32(a, 5) + f + e + k + Wt;
        e             = d;
        d             = c;
        c             = rotl32(b, 30);
        b             = a;
        a             = temp;
        if (t == 15 || t == 19 || t == 39 || t == 59 || t == 79) {
            dump_sha1_state(impl_name, __LINE__, state_cnt++, (const uint8_t *)&(dstate_t){a, b, c, d, e});
            dump_sha1_block(impl_name, __LINE__ - 2, block_cnt++, (const uint8_t *)W);
        }
    }

    ctx->H[0] += a;
    ctx->H[1] += b;
    ctx->H[2] += c;
    ctx->H[3] += d;
    ctx->H[4] += e;

    dump_sha1_state(impl_name, __LINE__, state_cnt++, (const uint8_t *)ctx->H);
    dump_sha1_block(impl_name, __LINE__ - 1, block_cnt++, (const uint8_t *)W);

    ctx->blocks++;
}

void cf_sha1_update(cf_sha1_context *ctx, const void *data, size_t nbytes) {
    cf_blockwise_accumulate(ctx->partial, &ctx->npartial, sizeof ctx->partial, data, nbytes, sha1_update_block, ctx);
}

void cf_sha1_digest(const cf_sha1_context *ctx, uint8_t hash[CF_SHA1_HASHSZ]) {
    cf_sha1_context ours = *ctx;
    cf_sha1_digest_final(&ours, hash);
}

void cf_sha1_digest_final(cf_sha1_context *ctx, uint8_t hash[CF_SHA1_HASHSZ]) {
    uint64_t digested_bytes = ctx->blocks;
    digested_bytes          = digested_bytes * CF_SHA1_BLOCKSZ + ctx->npartial;
    uint64_t digested_bits  = digested_bytes * 8;

    size_t padbytes = CF_SHA1_BLOCKSZ - ((digested_bytes + 8) % CF_SHA1_BLOCKSZ);

    /* Hash 0x80 00 ... block first. */
    cf_blockwise_acc_pad(ctx->partial, &ctx->npartial, sizeof ctx->partial, 0x80, 0x00, 0x00, padbytes,
                         sha1_update_block, ctx);

    /* Now hash length. */
    uint8_t buf[8];
    write64_be(digested_bits, buf);
    cf_sha1_update(ctx, buf, 8);

    /* We ought to have got our padding calculation right! */
    assert(ctx->npartial == 0);

    write32_be(ctx->H[0], hash + 0);
    write32_be(ctx->H[1], hash + 4);
    write32_be(ctx->H[2], hash + 8);
    write32_be(ctx->H[3], hash + 12);
    write32_be(ctx->H[4], hash + 16);

    memset(ctx, 0, sizeof *ctx);
}
