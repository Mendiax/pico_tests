add_library(pico_test INTERFACE)

aux_source_directory(src DIR_src_SRCS)
# aux_source_directory(inc DIR_inc_SRCS)


target_sources(pico_test INTERFACE
    ${DIR_src_SRCS}
)
target_include_directories(pico_test INTERFACE
    inc
)
target_link_libraries(pico_test INTERFACE
    pico_stdlib
)


# generate header file

if(NOT DEFINED PICO_TEST_SOURCE_DIR)
    message(FATAL_ERROR "PICO_TEST_SOURCE_DIR is not defined")
endif()

message("PICO_TEST_SOURCE_DIR is defined.")
set(PICO_TEST_PATH "${CMAKE_CURRENT_SOURCE_DIR}/..")
# gen header
set(PICO_TEST_SRC_PATH "${PICO_TEST_PATH}/pico_tests")
set(PICO_TEST_RUN_PATH "${PICO_TEST_PATH}/run")
# Define the path to the Python script
set(PYTHON_SCRIPT_FILE "${PICO_TEST_SRC_PATH}/scripts/generate_header.py")

# Define the source and header directories
set(HEADER_DIR ${PICO_TEST_SOURCE_DIR})

# Define the full path to the header file
set(HEADER_FILE "${HEADER_DIR}/test_cases.h")

# Define the command to generate the header file
add_custom_command(
OUTPUT ${HEADER_FILE}
COMMAND python3 -u ${PYTHON_SCRIPT_FILE} ${HEADER_FILE} ${PICO_TEST_SOURCE_DIR}
DEPENDS ${PYTHON_SCRIPT_FILE} # List any dependencies of the command here
COMMENT "Generating header file"
)

  # Add the header file as a target
  add_custom_target(
  generate_header_file ALL
  DEPENDS ${HEADER_FILE}
  )
  # Add the header file as an include directory for the target
#   include_directories(${HEADER_DIR})
  # Depend the target on the header file generation target
  add_dependencies(pico_test generate_header_file)

#   # add sources
#   aux_source_directory(${PICO_TEST_SOURCE_DIR} DIR_src_SRCS)
#   target_sources(${PICO_TEST_FILE} PRIVATE  ${DIR_src_SRCS})






message("------------------------------- picotest cmake --------------------------------")