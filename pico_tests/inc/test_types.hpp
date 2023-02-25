#ifndef TEST_TYPES_HPP
#define TEST_TYPES_HPP

#include <stdint.h>

struct TestCaseStats{
    uint16_t asserts_passed;
    uint16_t asserts_failed;
    uint16_t asserts_checked;

    TestCaseStats()
        :asserts_passed(0), asserts_failed(0), asserts_checked(0)
    {

    }
    TestCaseStats operator-(const TestCaseStats& rhs);
    bool check_assert(bool expr);
};

#endif