#ifndef __PICO_TESTS_HARDWARE_HPP__
#define __PICO_TESTS_HARDWARE_HPP__

#include <stdint.h>

uint32_t time_since_boot_ms();

float time_since_boot_s();

#ifdef BUILD_FOR_HOST
    // not used by host
    char getchar_timeout_us();
#endif



#endif /*__PICO_TESTS_HARDWARE_HPP__*/
