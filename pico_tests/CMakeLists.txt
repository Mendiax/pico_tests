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
