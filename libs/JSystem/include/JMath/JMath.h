#pragma once

#include <dolphin.h>

class JMathInlineVEC {
public:
    static f32 PSVECSquareMag(const register Vec *pVec) {
        register f32 xy, z;

        __asm {
            psq_l   xy, 0(pVec), 0, 0
            lfs     z, 8(pVec)
            ps_mul xy, xy, xy
            ps_madd z, z, z, xy
            ps_sum0 z, z, xy, xy
            blr 
        };
    }

    static void PSVECSubtract(register const Vec *lhs, register const Vec *rhs, register Vec *pDest) {
        __asm {
            psq_l f0, 0(lhs), 0, 0
            psq_l f1, 0(rhs), 0, 0
            psq_l f2, 8(lhs), 1, 0
            ps_sub f0, f0, f1
            psq_l f1, 8(rhs), 1, 0
            ps_sub f1, f2, f1
            psq_st f0, 0(pDest), 0, 0
            psq_st f1, 8(pDest), 1, 0
            blr
        };
    }
};