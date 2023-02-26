#ifndef __PICO_TESTS_PICO_TEST_HPP__
#define __PICO_TESTS_PICO_TEST_HPP__
// #-------------------------------#
// |           includes            |
// #-------------------------------#
// pico includes

// c/c++ includes
#include <string.h>
#include <sstream>
#include <string>
#include <stdint.h>
#include <inttypes.h>


// my includes
#include "escape.hpp"
#include "test_types.hpp"
#include "hardware.hpp"

// #-------------------------------#
// |            macros             |
// #-------------------------------#

// ############### used for communication with host server ###############
#define PICO_TEST_OUTPUT "[PT-SUT]"
#define PICO_TEST_START "[TEST_STARTED]"
#define PICO_TEST_PASSED "[TEST_PASSED]"
#define PICO_TEST_FAILED "[TEST_FAILED]"
// context
#define CTX_MAIN_FUNC "[MAIN_FUNC]"
// ########################################################################

#define MEASURE_TIME(function, ...) do{ \
    auto time_start = time_since_boot_ms(); \
    function( ##__VA_ARGS__ ); \
    auto time_end = time_since_boot_ms(); \
    PICO_TEST_PRINT(__CONTEXT, "function took " PRIu32 "s\n"); \
    }while(0)

#define TEST_CASE_FUNCTION(test_name) \
    void _##test_name(TestCaseStats& stats); \
    static const char* __CONTEXT = #test_name; /* context for asserts */ \
    TestCaseStats test_name(void){\
        printf("\n\n"); \
        PICO_TEST_PRINT(#test_name, PICO_TEST_START " "  "\n"); \
        TestCaseStats stats; \
        auto time_start = time_since_boot_ms(); \
        _##test_name(stats); \
        auto time_end = time_since_boot_ms(); \
        PICO_TEST_PRINT(__CONTEXT, "function took %" PRIu32 "ms\n", time_end - time_start); \
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

#define TEST_CASE_SUB_FUNCTION_DEF(sub_function) \
    void _##sub_function(const char* __CONTEXT, TestCaseStats& __stats)

#define xdd 1

#define TEST_CASE_SUB_FUNCTION(sub_function) do{ \
    PICO_TEST_PRINT(__CONTEXT, ESC_PAINT(ESC_WHITE, "<" #sub_function ">") " start\n"); \
    const TestCaseStats base_stats = /*__stats from main function*/ __stats; \
    _##sub_function(__CONTEXT, __stats); \
    const TestCaseStats sub_func_stats = __stats - base_stats; \
    PICO_TEST_PRINT(__CONTEXT,ESC_PAINT(ESC_WHITE, "<" #sub_function ">") " finished\n"); \
    PICO_TEST_PRINT(__CONTEXT,ESC_PAINT(ESC_WHITE, "<" #sub_function ">") " checks:%3d\n", sub_func_stats.asserts_checked); \
    PICO_TEST_PRINT(__CONTEXT,ESC_PAINT(ESC_WHITE, "<" #sub_function ">") " passed:%3d\n", sub_func_stats.asserts_passed); \
    PICO_TEST_PRINT(__CONTEXT,ESC_PAINT(ESC_WHITE, "<" #sub_function ">") " failed:%3d\n\n", sub_func_stats.asserts_failed); \
    } while(0)


#define PICO_TEST_PRINT(CONTEXT, format, ...) \
    printf(ESC_PAINT(ESC_WHITE, "%8.3f: " PICO_TEST_OUTPUT "[ctx:%s]") " " format, time_since_boot_s(), CONTEXT, ##__VA_ARGS__)

#define PICO_TEST_CHECK_VERBAL(expr, fmt, ...) do{ \
        if (__stats.check_assert(expr)) \
        { \
            /*passed*/ \
            PICO_TEST_PRINT(__CONTEXT, ESC_PAINT(ESC_GREEN, "line %d: Check " #expr " PASSED " fmt ) "\n", __LINE__, ##__VA_ARGS__); \
        } \
        else \
        { \
            /*failed*/ \
            PICO_TEST_PRINT(__CONTEXT, ESC_PAINT(ESC_RED, "line %d: Check " #expr " FAILED " fmt ) "\n", __LINE__, ##__VA_ARGS__); \
        } \
    } while(0)

#define PICO_TEST_CHECK(expr) \
    PICO_TEST_CHECK_VERBAL(expr, "")


#define PICO_TEST_CHECK_EQ(x, y) do{ \
     std::stringstream ss; \
     ss << #x "=" << x << " ?= " #y "=" << y; \
    PICO_TEST_CHECK_VERBAL(x == y, "%s", ss.str().c_str()); \
    } while(0)

#define PICO_TEST_ASSERT_VERBAL(expr, fmt, ...) do{ \
    auto __stats_check = __stats; \
    PICO_TEST_CHECK_VERBAL(expr, fmt, ##__VA_ARGS__); \
    auto  __stats_check_diff = __stats - __stats_check; \
    if(__stats_check_diff.asserts_failed > 0) {\
        PICO_TEST_PRINT(__CONTEXT, ESC_PAINT(ESC_RED, "ASSERT FAILED\n")); \
        return; \
    } \
    } while(0)

#define PICO_TEST_ASSERT(expr) \
    PICO_TEST_ASSERT_VERBAL(expr, "")

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
