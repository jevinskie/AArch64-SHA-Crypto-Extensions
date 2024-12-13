#pragma once

#include <stdint.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

extern void sha1_arm_unrolled(const uint8_t *buf, const size_t sz, uint8_t hash[20]);

#ifdef __cplusplus
}
#endif
