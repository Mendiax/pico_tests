#ifndef __PICO_TESTS_PICO_TEST_HPP__
#define __PICO_TESTS_PICO_TEST_HPP__
// #-------------------------------#
// |           includes            |
// #-------------------------------#
// pico includes

// c/c++ includes
#include <string.h>

// my includes
#include "escape.hpp"
#include "test_types.hpp"

// #-------------------------------#
// |            macros             |
// #-------------------------------#

#define PICO_TEST_OUTPUT "[PT-SUT]"
#define PICO_TEST_START "[TEST_STARTED]"
#define PICO_TEST_PASSED "[TEST_PASSED]"
#define PICO_TEST_FAILED "[TEST_FAILED]"

// context
#define CTX_MAIN_FUNC "[MAIN_FUNC]"


#define TEST_CASE_FUNCTION(test_name) \
    void _##test_name(TestCaseStats& stats); \
    static const char* __CONTEXT = #test_name; /* context for asserts */ \
    TestCaseStats test_name(void){\
        printf("\n\n"); \
        PICO_TEST_PRINT(#test_name, PICO_TEST_START " "  "\n"); \
        TestCaseStats stats; \
        memset(&stats, 0 ,sizeof(stats)); \
        _##test_name(stats); \
        PICO_TEST_PRINT(#test_name, "finished\n"); \
        PICO_TEST_PRINT(#test_name, "checks:%3d\n", stats.asserts_checked); \
        PICO_TEST_PRINT(#test_name, "passed:%3d\n", stats.asserts_passed); \
        PICO_TEST_PRINT(#test_name, "failed:%3d\n", stats.asserts_failed); \
        if (stats.asserts_failed == 0) \
        { \
            PICO_TEST_PRINT(#test_name, ESC_PAINT(ESC_GREEN, PICO_TEST_PASSED " " #test_name "\n")); \
        } \
        else \
        { \
            stats.asserts_failed++; \
            PICO_TEST_PRINT(#test_name, ESC_PAINT(ESC_RED, PICO_TEST_FAILED " " #test_name " \n")); \
        } \
        printf("\n\n"); \
        return stats; \
    } \
    void _##test_name(TestCaseStats& __stats)

#define PICO_TEST_PRINT(CONTEXT, format, ...) \
    printf(ESC_PAINT(ESC_WHITE, PICO_TEST_OUTPUT "[ctx:%s]") " " format, CONTEXT, ##__VA_ARGS__)

#define PICO_TEST_ASSERT(expr) do{ \
        if (expr) \
        { \
            /*passed*/ \
            __stats.asserts_passed++; \
            PICO_TEST_PRINT(__CONTEXT, ESC_PAINT(ESC_GREEN, "Assert " #expr " PASSED\n")); \
        } \
        else \
        { \
            /*failed*/ \
            __stats.asserts_failed++; \
            PICO_TEST_PRINT(__CONTEXT, ESC_PAINT(ESC_RED, "Assert " #expr " FAILED\n")); \
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
