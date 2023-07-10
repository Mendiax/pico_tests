#include "hardware.hpp"

#include "pico/time.h"

uint32_t time_since_boot_ms()
{
    return to_ms_since_boot(get_absolute_time());
}

float time_since_boot_s()
{
    return (float)time_since_boot_ms() / 1000.0f;
}

#ifdef BUILD_FOR_HOST
    // not used by host
    char getchar_timeout_us(){
        return '\0';
    }
#endif
