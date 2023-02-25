cmake_minimum_required(VERSION 3.13)
message("PICO_SDK_PATH=$ENV{PICO_SDK_PATH}")
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
project(pico
        VERSION 3.0
        LANGUAGES CXX ASM C)

pico_sdk_init()

if( NOT CMAKE_BUILD_TYPE )
        SET(CMAKE_BUILD_TYPE Debug)
        message("BUILD TYPE NOT SPECIFIED set to ${CMAKE_BUILD_TYPE} on default")
endif()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17")


add_compile_options(-Wfatal-errors -Werror=return-type)

if (TARGET tinyusb_device)
        message("PICO_MAIN_FILE=${PICO_MAIN_FILE}")
        if( NOT PICO_MAIN_FILE )
                SET(PICO_MAIN_FILE pico_main)
                message("SET PICO_MAIN_FILE = ${PICO_MAIN_FILE}")
        endif()

        set(PICO_TEST_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/tests")
        set(PICO_TEST_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../pico_tests")
        add_subdirectory(${PICO_TEST_PATH} build)

        add_executable( ${PICO_MAIN_FILE} main.cpp )
        target_compile_definitions(${PICO_MAIN_FILE} PRIVATE PICO_MALLOC_PANIC=0)



        # Define the source and header directories
        set(HEADER_DIR "${CMAKE_CURRENT_SOURCE_DIR}/tests")
        set(SOURCE_DIR ${HEADER_DIR})

        # Define the full path to the header file
        set(HEADER_FILE "${HEADER_DIR}/test_cases.h")

        # Add the header file as an include directory for the target
        include_directories(${HEADER_DIR})
        # Depend the target on the header file generation target
        add_dependencies(${PICO_MAIN_FILE} generate_header_file)



        file(GLOB_RECURSE PICO_TEST_SRC_FILES "${SOURCE_DIR}/*.cpp")
        # aux_source_directory({SOURCE_DIR} DIR_src_SRCS)
        target_sources(${PICO_MAIN_FILE} PRIVATE  ${PICO_TEST_SRC_FILES})

        pico_enable_stdio_usb( ${PICO_MAIN_FILE} 1)
        pico_enable_stdio_uart( ${PICO_MAIN_FILE} 0)

        pico_add_extra_outputs( ${PICO_MAIN_FILE})

        target_link_libraries( ${PICO_MAIN_FILE}
            pico_stdlib
            pico_test
        )
elseif(PICO_ON_DEVICE)
        message(FATAL_ERROR "not building hello_usb because TinyUSB submodule is not initialized in the SDK")
endif()
