message("PICO_MAIN_FILE=${PICO_MAIN_FILE}")
if( NOT PICO_MAIN_FILE )
SET(PICO_MAIN_FILE pico_main)
message("SET PICO_MAIN_FILE = ${PICO_MAIN_FILE}")
endif()
add_executable( ${PICO_MAIN_FILE} main.cpp)
target_compile_definitions(${PICO_MAIN_FILE} PRIVATE PICO_MALLOC_PANIC=0)
target_include_directories(${PICO_MAIN_FILE} PUBLIC ../inc)

pico_enable_stdio_usb( ${PICO_MAIN_FILE} 1)
pico_enable_stdio_uart( ${PICO_MAIN_FILE} 0)

pico_add_extra_outputs( ${PICO_MAIN_FILE})

target_link_libraries( ${PICO_MAIN_FILE}
        pico_stdlib
        pico_multicore
)