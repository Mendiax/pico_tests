#ifndef TEST_TYPES_HPP
#define TEST_TYPES_HPP

#include <stdint.h>

struct TestCaseStats{
    uint16_t asserts_passed;
    uint16_t asserts_failed;
    uint16_t asserts_checked;
};

#endif