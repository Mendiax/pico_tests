
// #------------------------------#
// |          includes            |
// #------------------------------#
// pico includes
#include "pico/stdlib.h"

// c/c++ includes
#include <iostream>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/select.h>
#include <string>
// my includes
#include "pico_test.hpp"

// #------------------------------#
// |           macros             |
// #------------------------------#

#define ENDSTDIN	255
#define CR		13
#define LF		10


// #------------------------------#
// | global variables definitions |
// #------------------------------#

// #------------------------------#
// | static variables definitions |
// #------------------------------#

// #------------------------------#
// | static functions declarations|
// #------------------------------#

#ifndef BUILD_FOR_HOST
std::string read_non_block()
{
    char strg[100] = {0};
    unsigned char chr;
    int lp = 0;

    memset(strg, 0, sizeof(strg));

	chr = getchar_timeout_us(0);
	while(chr != ENDSTDIN)
	{
        if (chr != CR)
		    strg[lp++] = chr;
		if(chr == LF || lp == (sizeof(strg) - 1))
		{
			strg[lp] = 0;	//terminate string
			lp = 0;
			break;
		}

		chr = getchar_timeout_us(0);
	}
    return std::string(strg);
}
#endif

// #------------------------------#
// | global function definitions  |
// #------------------------------#
void pico_test_start()
{
    printf("\n\n");
    PICO_TEST_PRINT(CTX_MAIN_FUNC, "starting tests\n");
    #ifndef BUILD_FOR_HOST
    while (1) {
        PICO_TEST_PRINT(CTX_MAIN_FUNC, "waiting for \"START\"\n");
        sleep_ms(1000);

        if (read_non_block() == "START"){
            PICO_TEST_PRINT(CTX_MAIN_FUNC, "received \"START\"\n");
            break;
        }
    }
    #endif
}

void pico_test_end()
{
    PICO_TEST_PRINT(CTX_MAIN_FUNC, "STOP\n");
    printf("\n\n");
}


// #------------------------------#
// | static functions definitions |
// #------------------------------#






