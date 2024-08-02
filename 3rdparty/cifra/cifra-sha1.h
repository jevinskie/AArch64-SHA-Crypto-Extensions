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

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>
#include <stdint.h>

/**
 * General hash function description
 * =================================
 * This allows us to make use of hash functions without depending
 * on a specific one.  This is useful in implementing, for example,
 * :doc:`HMAC <hmac>`.
 */

/* .. c:type:: cf_chash_init
 * Hashing initialisation function type.
 *
 * Functions of this type should initialise the context in preparation
 * for hashing a message with `cf_chash_update` functions.
 *
 * :rtype: void
 * :param ctx: hash function-specific context structure.
 */
typedef void (*cf_chash_init)(void *ctx);

/* .. c:type:: cf_chash_update
 * Hashing data processing function type.
 *
 * Functions of this type hash `count` bytes of data at `data`,
 * updating the contents of `ctx`.
 *
 * :rtype: void
 * :param ctx: hash function-specific context structure.
 * :param data: input data to hash.
 * :param count: number of bytes to hash.
 */
typedef void (*cf_chash_update)(void *ctx, const void *data, size_t count);

/* .. c:type:: cf_chash_digest
 * Hashing completion function type.
 *
 * Functions of this type complete a hashing operation,
 * writing :c:member:`cf_chash.hashsz` bytes to `hash`.
 *
 * This function does not change `ctx` -- any padding which needs doing
 * must be done seperately (in a copy of `ctx`, say).
 *
 * This means you can interlave `_update` and `_digest` calls to
 * learn `H(A)` and `H(A || B)` without hashing `A` twice.
 *
 * :rtype: void
 * :param ctx: hash function-specific context structure.
 * :param hash: location to write hash result.
 */
typedef void (*cf_chash_digest)(const void *ctx, uint8_t *hash);

/* .. c:type:: cf_chash
 * This type describes an incremental hash function in an abstract way.
 *
 * .. c:member:: cf_chash.hashsz
 * The hash function's output, in bytes.
 *
 * .. c:member:: cf_chash.blocksz
 * The hash function's internal block size, in bytes.
 *
 * .. c:member:: cf_chash.init
 * Context initialisation function.
 *
 * .. c:member:: cf_chash:update
 * Data processing function.
 *
 * .. c:member:: cf_chash:digest
 * Completion function.
 *
 */
typedef struct {
    size_t hashsz;
    size_t blocksz;

    cf_chash_init init;
    cf_chash_update update;
    cf_chash_digest digest;
} cf_chash;

/**
 * SHA1
 * ====
 *
 * You shouldn't use this for anything new.
 */

/* .. c:macro:: CF_SHA1_HASHSZ
 * The output size of SHA1: 20 bytes. */
#define CF_SHA1_HASHSZ 20

/* .. c:macro:: CF_SHA1_BLOCKSZ
 * The block size of SHA1: 64 bytes. */
#define CF_SHA1_BLOCKSZ 64

/* .. c:type:: cf_sha1_context
 * Incremental SHA1 hashing context.
 *
 * .. c:member:: cf_sha1_context.H
 * Intermediate values.
 *
 * .. c:member:: cf_sha1_context.partial
 * Unprocessed input.
 *
 * .. c:member:: cf_sha1_context.npartial
 * Number of bytes of unprocessed input.
 *
 * .. c:member:: cf_sha1_context.blocks
 * Number of full blocks processed.
 */
typedef struct {
    uint32_t H[5];                    /* State. */
    uint8_t partial[CF_SHA1_BLOCKSZ]; /* Partial block of input. */
    uint32_t blocks;                  /* Number of full blocks processed into H. */
    size_t npartial;                  /* Number of bytes in prefix of partial. */
} cf_sha1_context;

/* .. c:function:: $DECL
 * Sets up `ctx` ready to hash a new message.
 */
extern void cf_sha1_init(cf_sha1_context *ctx);

/* .. c:function:: $DECL
 * Hashes `nbytes` at `data`.  Copies the data if there isn't enough to make
 * a full block.
 */
extern void cf_sha1_update(cf_sha1_context *ctx, const void *data, size_t nbytes);

/* .. c:function:: $DECL
 * Finishes the hash operation, writing `CF_SHA1_HASHSZ` bytes to `hash`.
 *
 * This leaves `ctx` unchanged.
 */
extern void cf_sha1_digest(const cf_sha1_context *ctx, uint8_t hash[CF_SHA1_HASHSZ]);

/* .. c:function:: $DECL
 * Finishes the hash operation, writing `CF_SHA1_HASHSZ` bytes to `hash`.
 *
 * This destroys `ctx`, but uses less stack than :c:func:`cf_sha1_digest`.
 */
extern void cf_sha1_digest_final(cf_sha1_context *ctx, uint8_t hash[CF_SHA1_HASHSZ]);

/* .. c:var:: cf_sha1
 * Abstract interface to SHA1.  See :c:type:`cf_chash` for more information.
 */
extern const cf_chash cf_sha1;

#ifdef __cplusplus
} // extern "C"
#endif
