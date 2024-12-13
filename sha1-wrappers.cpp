#define SHA1_REDIR_DISABLE
#include "sha1-wrappers.h"

#include <cstdio>
#include <cstdlib>

extern "C" void dump_sha1_state(const char *const _Nonnull name, const int line, const size_t i,
                                const uint8_t *const _Nonnull state);
extern "C" void dump_sha1_block(const char *const _Nonnull name, const int line, const size_t i,
                                const uint8_t *const _Nonnull block);

// extern "C" void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32_t (&v)[4]);
// extern "C" void dump_uint8x16_t(const char *const _Nonnull prefix, const uint8_t (&v)[16]);
// extern "C" void dump_uint8x16x2_t(const char *const _Nonnull prefix, const uint8_t (&v)[32]);
extern void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32x4_t v);

static size_t vsha1pq_u32_cnt;
static size_t vsha1su0q_u32_cnt;
static size_t vsha1su1q_u32_cnt;
static size_t vsha1cq_u32_cnt;
static size_t vsha1h_u32_cnt;

void sha1_wrappers_reset(void) {
    vsha1pq_u32_cnt = vsha1su0q_u32_cnt = vsha1su1q_u32_cnt = vsha1cq_u32_cnt = vsha1h_u32_cnt = 0;
}

uint32x4_t my_vsha1pq_u32(uint32x4_t p0, uint32_t p1, uint32x4_t p2) {
    dump_uint32x4_t("vsha1pq_u32 p0", p0);
    printf("vsha1pq_u32 p1: 0x%08x\n", p1);
    dump_uint32x4_t("vsha1pq_u32 p2", p2);
    const auto res = vsha1pq_u32(p0, p1, p2);
    dump_uint32x4_t("vsha1pq_u32 res", res);
    return res;
}

uint32x4_t my_vsha1su0q_u32(uint32x4_t p0, uint32x4_t p1, uint32x4_t p2) {
    dump_uint32x4_t("vsha1su0q_u32 p0", p0);
    dump_uint32x4_t("vsha1su0q_u32 p1", p1);
    dump_uint32x4_t("vsha1su0q_u32 p2", p2);
    const auto res = vsha1su0q_u32(p0, p1, p2);
    dump_uint32x4_t("vsha1su0q_u32 res", res);
    return res;
}

uint32x4_t my_vsha1su1q_u32(uint32x4_t p0, uint32x4_t p1) {
    dump_uint32x4_t("vsha1su1q_u32 p0", p0);
    dump_uint32x4_t("vsha1su1q_u32 p1", p1);
    const auto res = vsha1su1q_u32(p0, p1);
    dump_uint32x4_t("vsha1su1q_u32 res", res);
    return res;
}

uint32x4_t my_vsha1cq_u32(uint32x4_t p0, uint32_t p1, uint32x4_t p2) {
    dump_uint32x4_t("vsha1cq_u32 p0", p0);
    printf("vsha1cq_u32 p1: 0x%08x\n", p1);
    dump_uint32x4_t("vsha1cq_u32 p2", p2);
    const auto res = vsha1cq_u32(p0, p1, p2);
    dump_uint32x4_t("vsha1cq_u32 res", res);
    return res;
}

uint32_t my_vsha1h_u32(uint32_t p0) {
    printf("vsha1h_u32 p1: p0%08x\n", p0);
    const auto res = vsha1h_u32(p0);
    printf("vsha1cq_u32 res: 0x%08x\n", res);
    return res;
}
