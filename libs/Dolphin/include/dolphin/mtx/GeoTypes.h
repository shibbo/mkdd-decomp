#ifndef GEOTYPES_H
#define GEOTYPES_H

#include <dolphin/types.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    f32 x;
    f32 y;
    f32 z;
} Vec;

typedef f32 Mtx[3][4];
typedef f32 (*MtxPtr)[4];
typedef f32 Mtx44[4][4];
typedef f32 (*Mtx44Ptr)[4];

#ifdef __cplusplus
}
#endif

#endif // GEOTYPES_H