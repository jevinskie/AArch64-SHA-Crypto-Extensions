#pragma once

#include <arm_neon.h>

#ifndef SHA1_REDIR_DISABLE
#define SHA1_REDIR
#endif

#ifdef __cplusplus
extern "C" {
#endif

extern uint32x4_t my_vsha1pq_u32(uint32x4_t p0, uint32_t p1, uint32x4_t p2);
extern uint32x4_t my_vsha1su0q_u32(uint32x4_t p0, uint32x4_t p1, uint32x4_t p2);
extern uint32x4_t my_vsha1su1q_u32(uint32x4_t p0, uint32x4_t p1);
extern uint32x4_t my_vsha1cq_u32(uint32x4_t p0, uint32_t p1, uint32x4_t p2);
extern uint32x4_t my_vsha1mq_u32(uint32x4_t p0, uint32_t p1, uint32x4_t p2);
extern uint32_t my_vsha1h_u32(uint32_t p0);
extern void sha1_wrappers_reset(void);

#ifdef SHA1_REDIR
#define vsha1pq_u32   my_vsha1pq_u32
#define vsha1su0q_u32 my_vsha1su0q_u32
#define vsha1su1q_u32 my_vsha1su1q_u32
#define vsha1cq_u32   my_vsha1cq_u32
#define vsha1mq_u32   my_vsha1mq_u32
#define vsha1h_u32    my_vsha1h_u32
#endif

#ifdef __cplusplus
}
#endif
