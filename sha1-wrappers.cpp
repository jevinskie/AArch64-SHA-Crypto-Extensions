#define SHA1_REDIR_DISABLE
#include "sha1-wrappers.h"

#include <cstdio>
#include <cstdlib>
#include <fmt/format.h>

#define ANSI_BOLD_RED_FG    "\x1b[38;5;196m"
#define ANSI_BOLD_GREEN_FG  "\x1b[38;5;34m"
#define ANSI_BOLD_BLUE_FG   "\x1b[38;5;81m"
#define ANSI_BOLD_ORANGE_FG "\x1b[38;5;208m"
#define ANSI_BOLD_VIOLET_FG "\x1b[38;5;207m"
#define ASNI_BOLD_PINK_FG   "\x1b[38;5;223m"
#define ANSI_RESET          "\x1b[1;0m"

extern void dump_uint32x4_t(const char *const _Nonnull prefix, const uint32x4_t v);

static size_t vsha1pq_u32_cnt;
static size_t vsha1su0q_u32_cnt;
static size_t vsha1su1q_u32_cnt;
static size_t vsha1cq_u32_cnt;
static size_t vsha1mq_u32_cnt;
static size_t vsha1h_u32_cnt;

void sha1_wrappers_reset(void) {
    vsha1pq_u32_cnt = vsha1su0q_u32_cnt = vsha1su1q_u32_cnt = vsha1cq_u32_cnt = vsha1mq_u32_cnt = vsha1h_u32_cnt = 0;
}

uint32x4_t my_vsha1pq_u32(uint32x4_t p0, uint32_t p1, uint32x4_t p2) {
    dump_uint32x4_t(fmt::format(ANSI_BOLD_RED_FG "vsha1pq_u32" ANSI_RESET "  [{:4d}] →  p0", vsha1pq_u32_cnt).c_str(),
                    p0);
    fmt::print(ANSI_BOLD_RED_FG "vsha1pq_u32" ANSI_RESET "  [{:4d}]    p1 {:#010x}\n", vsha1pq_u32_cnt, p1);
    dump_uint32x4_t(fmt::format(ANSI_BOLD_RED_FG "vsha1pq_u32" ANSI_RESET "  [{:4d}]    p2", vsha1pq_u32_cnt).c_str(),
                    p2);
    const auto res = vsha1pq_u32(p0, p1, p2);
    dump_uint32x4_t(fmt::format(ANSI_BOLD_RED_FG "vsha1pq_u32" ANSI_RESET "  [{:4d}] ← res", vsha1pq_u32_cnt).c_str(),
                    res);
    ++vsha1pq_u32_cnt;
    return res;
}

uint32x4_t my_vsha1su0q_u32(uint32x4_t p0, uint32x4_t p1, uint32x4_t p2) {
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_GREEN_FG "vsha1su0q_u32" ANSI_RESET "[{:4d}] →  p0", vsha1su0q_u32_cnt).c_str(), p0);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_GREEN_FG "vsha1su0q_u32" ANSI_RESET "[{:4d}]    p1", vsha1su0q_u32_cnt).c_str(), p1);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_GREEN_FG "vsha1su0q_u32" ANSI_RESET "[{:4d}]    p2", vsha1su0q_u32_cnt).c_str(), p2);
    const auto res = vsha1su0q_u32(p0, p1, p2);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_GREEN_FG "vsha1su0q_u32" ANSI_RESET "[{:4d}] ← res", vsha1su0q_u32_cnt).c_str(), res);
    ++vsha1su0q_u32_cnt;
    return res;
}

uint32x4_t my_vsha1su1q_u32(uint32x4_t p0, uint32x4_t p1) {
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_BLUE_FG "vsha1su1q_u32" ANSI_RESET "[{:4d}] →  p0", vsha1su1q_u32_cnt).c_str(), p0);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_BLUE_FG "vsha1su1q_u32" ANSI_RESET "[{:4d}]    p1", vsha1su1q_u32_cnt).c_str(), p1);
    const auto res = vsha1su1q_u32(p0, p1);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_BLUE_FG "vsha1su1q_u32" ANSI_RESET "[{:4d}] ← res", vsha1su1q_u32_cnt).c_str(), res);
    ++vsha1su1q_u32_cnt;
    return res;
}

uint32x4_t my_vsha1cq_u32(uint32x4_t p0, uint32_t p1, uint32x4_t p2) {
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_VIOLET_FG "vsha1cq_u32" ANSI_RESET "  [{:4d}] →  p0", vsha1cq_u32_cnt).c_str(), p0);
    fmt::print(ANSI_BOLD_VIOLET_FG "vsha1cq_u32" ANSI_RESET "  [{:4d}]    p1 {:#010x}\n", vsha1cq_u32_cnt, p1);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_VIOLET_FG "vsha1cq_u32" ANSI_RESET "  [{:4d}]    p2", vsha1cq_u32_cnt).c_str(), p2);
    const auto res = vsha1cq_u32(p0, p1, p2);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_VIOLET_FG "vsha1cq_u32" ANSI_RESET "  [{:4d}] ← res", vsha1cq_u32_cnt).c_str(), res);
    ++vsha1cq_u32_cnt;
    return res;
}

uint32x4_t my_vsha1mq_u32(uint32x4_t p0, uint32_t p1, uint32x4_t p2) {
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_ORANGE_FG "vsha1mq_u32" ANSI_RESET "  [{:4d}] →  p0", vsha1mq_u32_cnt).c_str(), p0);
    fmt::print(ANSI_BOLD_ORANGE_FG "vsha1mq_u32" ANSI_RESET "  [{:4d}]    p1 {:#010x}\n", vsha1mq_u32_cnt, p1);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_ORANGE_FG "vsha1mq_u32" ANSI_RESET "  [{:4d}]    p2", vsha1mq_u32_cnt).c_str(), p2);
    const auto res = vsha1mq_u32(p0, p1, p2);
    dump_uint32x4_t(
        fmt::format(ANSI_BOLD_ORANGE_FG "vsha1mq_u32" ANSI_RESET "  [{:4d}] ← res", vsha1mq_u32_cnt).c_str(), res);
    ++vsha1mq_u32_cnt;
    return res;
}

uint32_t my_vsha1h_u32(uint32_t p0) {
    fmt::print(ASNI_BOLD_PINK_FG "vsha1h_u32" ANSI_RESET "   [{:4d}] →  p0 {:#010x}\n", vsha1h_u32_cnt, p0);
    const auto res = vsha1h_u32(p0);
    fmt::print(ASNI_BOLD_PINK_FG "vsha1h_u32" ANSI_RESET "   [{:4d}] ← res {:#010x}\n", vsha1h_u32_cnt, res);
    ++vsha1h_u32_cnt;
    return res;
}
