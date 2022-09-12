#pragma once

#include <dolphin.h>
#include <float.h>

namespace JGeometry {
    template<typename T>
    class TUtil {
    public:
        static f32 inv_sqrt(f32 val) {
            if (val <= 0.0f) {
                return val;
            }

            f32 sqr = __frsqrte(val);
            return ((0.5f * sqr) * -((val * (sqr * sqr)) - 3.0f));            
        }

        static f32 epsilon() {
            return 32.0f * *__float_epsilon;
        }
    };
};