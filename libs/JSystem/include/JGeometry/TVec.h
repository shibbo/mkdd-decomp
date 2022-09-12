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

    template<typename T>
    class TVec3 {
    public:

        void zero() {
            x = 0.0f;
            y = 0.0f;
            z = 0.0f;
        }

        template<typename T>
        void set(const TVec3<T> &rVec) {
            x = rVec.x;
            y = rVec.y;
            z = rVec.z;
        }

        template<typename T>
        void set(T _x, T _y, T _z) {
            x = _x;
            y = _y;
            z = _z;
        }

        f32 length() const {
            return PSVECMag(this->toCVec());
        }

        inline Vec* toVec() {
            return reinterpret_cast<Vec*>(this);
        }

        inline const Vec* toCVec() {
            return reinterpret_cast<const Vec*>(this);
        }

        T x;
        T y;
        T z;
    };
};