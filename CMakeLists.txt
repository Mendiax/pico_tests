cmake_minimum_required(VERSION 3.13)
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)
project(pico
        VERSION 1.0
        LANGUAGES CXX ASM C)

pico_sdk_init()

if( NOT CMAKE_BUILD_TYPE )
        SET(CMAKE_BUILD_TYPE Debug)
        message("BUILD TYPE NOT SPECIFIED set to ${CMAKE_BUILD_TYPE} on default")
endif()

# DEBUG -> all debug symbols
add_compile_options(
  "$<$<CONFIG:DEBUG>:-O0;-g3;-ggdb>"
)

# RELEASE -> optimization enabled
add_compile_options(
  "$<$<CONFIG:RELEASE>:-O3>"
)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_C_COMPILE_OPTIONS_COLOR_DIAGNOSTICS     -DCOLOR_ON)

# add compiler option for specific compiler
if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
  add_compile_options("-Weverything")
else() # gcc or icc
  add_compile_options("-Wall" "-Wextra")
endif()

add_compile_options(-Wfatal-errors -Werror=return-type)


# Uncomment this line to set verbose mode in makefile
# set(CMAKE_VERBOSE_MAKEFILE ON)


# The compiled library code is under ./src
add_subdirectory(src)

# The executable code is unser ./app
add_subdirectory(app)

# #-----------------------------------------------------------------------------#
# #                             INCLUDE DIRECTORIES                             #
# #-----------------------------------------------------------------------------#

# include_directories(source/lib/common/include)

# ################################ SUBDIRECTORY #################################
# add_subdirectory(source/lib/common)

# #################################### MAIN #####################################






