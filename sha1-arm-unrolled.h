#pragma once

#include <stdint.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

extern void sha1_arm_unrolled(const uint8_t *_Nullable buf, const size_t sz, uint8_t *_Nonnull hash);

#ifdef __cplusplus
}
#endif
