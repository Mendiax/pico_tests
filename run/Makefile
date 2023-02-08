BUILD := ../tests/build
SOURCE := ../tests
PICO_MAIN_FILE := pico_main

NPROCS:=$(shell grep -c ^processor /proc/cpuinfo)
PICO_MAIN_FILE_PATH:=$(BUILD)/$(PICO_MAIN_FILE).uf2
PICO_TEST_FILE_PATH:=$(BUILD)/$(PICO_TEST_FILE).uf2

# CMAKE_BUILDER := "Ninja"
CMAKE_BUILDER := "Unix Makefiles"

all: cmaker
	# $(MAKE) -C $(BUILD) -j$(NPROCS) && echo "BUILD FINISHED"
	cmake --build $(BUILD) --parallel $(NPROCS)

### CMAKE BUILD CONFIGS
CMAKE_ARGS := -G$(CMAKE_BUILDER) -S $(SOURCE) -B $(BUILD) -DPICO_MAIN_FILE=$(PICO_MAIN_FILE) -DPICO_TEST_FILE=$(PICO_TEST_FILE) -DCMAKE_EXPORT_COMPILE_COMMANDS=1
#-DCMAKE_VERBOSE_MAKEFILE=ON
cmake:
	cmake $(CMAKE_ARGS) -DCMAKE_BUILD_TYPE=Debug

cmaker:
	cmake $(CMAKE_ARGS) -DCMAKE_BUILD_TYPE=Release


# build target main
main:
	cmake --build $(BUILD) --parallel $(NPROCS) --target $(PICO_MAIN_FILE) && echo "BUILD FINISHED"

run_main:
	python3 run_ssh.py

build_run_main: cmaker main run_main
	echo "build_run_main DONE"




clean:
	rm -rf  $(BUILD)
	mkdir $(BUILD)

# rebuilds project
rebuild: clean all
	echo "clean make done!"
