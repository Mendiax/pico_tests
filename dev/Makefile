PICODIR := ./pico #/mnt/h
BUILD := ../build
PICO_MAIN_FILE := pico_main

PICO_DRIVE_LETTER := H

NPROCS:=$(shell grep -c ^processor /proc/cpuinfo)
PICO_MAIN_FILE_PATH:=$(shell wslpath -w $(BUILD)/$(PICO_MAIN_FILE).uf2)
PICO_TEST_FILE_PATH:=$(shell wslpath -w $(BUILD)/$(PICO_TEST_FILE).uf2)

CMAKE_BUILDER := "Ninja"
# CMAKE_BUILDER := "Unix Makefiles"

all:
	# $(MAKE) -C $(BUILD) -j$(NPROCS) && echo "BUILD FINISHED"
	cmake --build $(BUILD) --parallel $(NPROCS)

main:
	cmake --build $(BUILD) --parallel $(NPROCS) --target $(PICO_MAIN_FILE) && echo "BUILD FINISHED"


CMAKE_ARGS := -G$(CMAKE_BUILDER) -S ../ -B $(BUILD) -DPICO_MAIN_FILE=$(PICO_MAIN_FILE) -DPICO_TEST_FILE=$(PICO_TEST_FILE) -DCMAKE_EXPORT_COMPILE_COMMANDS=1

#-DCMAKE_VERBOSE_MAKEFILE=ON
cmake:
	cmake $(CMAKE_ARGS) -DCMAKE_BUILD_TYPE=Debug

cmaker:
	cmake $(CMAKE_ARGS) -DCMAKE_BUILD_TYPE=Release

cw_all:
	./boot/boot.sh -o b && $(MAKE) main && $(MAKE) write_main && sleep 2 && ./serial.bat

.PHONY: boot
boot:
	./boot/boot.sh -o b

.PHONY: restart
restart:
	./boot/boot.sh -o r

w: write_main
write_main:
	./boot/upload.sh -p '$(PICO_MAIN_FILE_PATH)' -d $(PICO_DRIVE_LETTER)

# compile & write
cw: main write_main
	echo "cw main"
clean:
	rm -rf  $(BUILD)
	mkdir $(BUILD)

reset: clean cmake all
	echo "clean make done!"
