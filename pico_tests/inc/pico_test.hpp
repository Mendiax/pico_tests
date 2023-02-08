#ifndef __PICO_TESTS_PICO_TEST_HPP__
#define __PICO_TESTS_PICO_TEST_HPP__
// #-------------------------------#
// |           includes            |
// #-------------------------------#
// pico includes

// c/c++ includes

// my includes
#include "escape.hpp"
#include "test_types.hpp"

// #-------------------------------#
// |            macros             |
// #-------------------------------#

#define PICO_TEST_OUTPUT "[PT-TARGET]"

#define TEST_CASE_FUNCTION(test_name) \
    void _##test_name(TestCaseStats& stats); \
    TestCaseStats test_name(void){\
        printf("\n\n"); \
        PICO_TEST_PRINT(#test_name " started\n"); \
        TestCaseStats stats = {0}; \
        _##test_name(stats); \
        PICO_TEST_PRINT(#test_name " finished\n"); \
        PICO_TEST_PRINT(#test_name " checks:%3d\n", stats.asserts_checked); \
        PICO_TEST_PRINT(#test_name " passed:%3d\n", stats.asserts_passed); \
        PICO_TEST_PRINT(#test_name " failed:%3d\n", stats.asserts_failed); \
        printf("\n\n"); \
        return stats; \
    } \
    void _##test_name(TestCaseStats& __stats)

#define PICO_TEST_PRINT(format, ...) \
    printf(ESC_PAINT(ESC_WHITE, PICO_TEST_OUTPUT) " " format, ##__VA_ARGS__)

#define PICO_TEST_ASSERT(expr) do{ \
        if (expr) \
        { \
            /*passed*/ \
            __stats.asserts_passed++; \
            PICO_TEST_PRINT(ESC_PAINT(ESC_GREEN, "Assert " #expr " PASSED\n")); \
        } \
        else \
        { \
            /*failed*/ \
            __stats.asserts_failed++; \
            PICO_TEST_PRINT(ESC_PAINT(ESC_RED, "Assert " #expr " FAILED\n")); \
        } \
    } while(0)

// #-------------------------------#
// | global types declarations     |
// #-------------------------------#

// #-------------------------------#
// | global variables declarations |
// #-------------------------------#

// #-------------------------------#
// | global function declarations  |
// #-------------------------------#

void pico_test_start();
void pico_test_end();


#endif
