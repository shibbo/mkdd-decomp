#pragma once

#include <dolphin.h>

class JUTAssertion {
public:
    static u32 getSDevice();

    static void showAssert_f(u32, const char *, int, const char *, ...);
};

#define ASSERT_MSG1(line, msg, param1)    \
    JUTAssertion::showAssert_f(JUTAssertion::getSDevice(), __FILE__, line, msg, param1); \
    OSPanic(__FILE__, line, "Halt");

#define ASSERT_MSG2(line, msg, param1, param2)    \
    JUTAssertion::showAssert_f(JUTAssertion::getSDevice(), __FILE__, line, msg, param1, param2); \
    OSPanic(__FILE__, line, "Halt");

#define ASSERT_MSG3(line, msg, param1, param2, param3)    \
    JUTAssertion::showAssert_f(JUTAssertion::getSDevice(), __FILE__, line, msg, param1, param2, param3); \
    OSPanic(__FILE__, line, "Halt");

#define ASSERT_MSG4(line, msg, param1, param2, param3, param4)    \
    JUTAssertion::showAssert_f(JUTAssertion::getSDevice(), __FILE__, line, msg, param1, param2, param3, param4); \
    OSPanic(__FILE__, line, "Halt");