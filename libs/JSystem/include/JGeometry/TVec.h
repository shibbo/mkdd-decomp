#pragma once

#include <dolphin.h>

namespace JGeometry {
    template<typename T>
    class TVec2 {
    public:

        void scale(T scalar) {
            x *= scalar;
            y *= scalar;
        }

        T squared() const {
            return dot(this);
        }

        T dot(const TVec2<T> &rVec) const {
            return (x * rVec.x) + (y * rVec.y);
        }

        void set<T>(T _x, T _y) {
            x = _x;
            y = _y;
        }

        T x;
        T y;
    };
};