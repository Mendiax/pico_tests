from dep.config import Config
import time

import subprocess
import logging
import sys
from .host_files.host.run_tests import main as run_test_target
from .run_common import *

def run_command(cmd: str):
    print(f'run_command {cmd}')
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    for line in iter(proc.stdout.readline, b''):
        sys.stdout.write(line.decode(sys.stdout.encoding))
    proc.wait()
    return proc.returncode

def run_cmd(cmd:str):
    print(cmd)
    print(subprocess.getoutput(cmd))

def load_binary(bin_file):
    success = False
    for x in range(5):
        res = run_command(f"picotool load -x -v {bin_file} -f")
        print(f'Command exited with code {res}')

        success = res == 0
        if success:
            break
        # time.sleep(1.0)
    return success

def run(config : Config) -> int:
    print('[DEBUG] current dir')
    run_cmd('pwd')
    print('[DEBUG] usb devices connected')
    run_cmd('lsusb')

    all_bin_files = config.get_bin_list()
    print(f"running tests: {all_bin_files}")

    return_values = 0
    for bin_file in all_bin_files:
        if load_binary(bin_file) == False:
            print('Upload failed')
            return 2

        test_return_val = run_test_target()
        print(f'Test finished with {test_return_val}')
        if test_return_val != 0:
                return_values = -1

    print(f"Tests ended with {return_values}")
    print(f"Tests {passed_bool_to_str(return_values)}")
    return return_values