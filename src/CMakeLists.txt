aux_source_directory(. DIR_sources_SRCS)

add_library(srccode ${DIR_sources_SRCS})
target_include_directories(srccode PUBLIC ../include)