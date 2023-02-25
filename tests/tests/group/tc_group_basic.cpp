#include "pico_test.hpp"
#include "pico/stdlib.h"
#include <stdio.h>

TEST_CASE_SUB_FUNCTION_DEF(basic_sub_func)
{
    PICO_TEST_ASSERT(1 == 1);

    int x = 13;
    int y = 13;
    PICO_TEST_CHECK_EQ(x,y);
}


TEST_CASE_FUNCTION(tc_group_basic)
{
    printf("Hello, world!\n");

    TEST_CASE_SUB_FUNCTION(basic_sub_func);

    PICO_TEST_ASSERT(1 == 1);
}