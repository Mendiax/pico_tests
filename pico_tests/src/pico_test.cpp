
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

// #------------------------------#
// | global function definitions  |
// #------------------------------#
void pico_test_start()
{
    printf("\n\n");
    PICO_TEST_PRINT("starting tests\n");
    while (1) {
        PICO_TEST_PRINT("waiting for \"START\"\n");
        sleep_ms(1000);

        if (read_non_block() == "START"){
            PICO_TEST_PRINT("received \"START\"\n");
            break;
        }
    }
}

void pico_test_end()
{
    PICO_TEST_PRINT("STOP\n");
    printf("\n\n");
}


// #------------------------------#
// | static functions definitions |
// #------------------------------#






