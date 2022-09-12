#include "JUTility/JUTAssert.h"

namespace {
    static u32 sDevice = 3;
};

u32 JUTAssertion::getSDevice() {
    return ::sDevice;
}
