from dep.config import Config
import time

import subprocess
import logging
import sys
from .host_files.host.run_tests import main as run_test_target

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


def run(config : Config) -> int:
    run_cmd('pwd')
    run_cmd('lsusb')
    success = False
    for x in range(5):

        res = run_command(f"picotool load -x -v {config.bin_file} -f")
        print(f'Command exited with code {res}')

        success = res == 0
        if success:
            break
        # time.sleep(1.0)

    if success == False:
        print('Upload failed')
        return 2
    # ret = run_command(config.get_run_cmd(), "tests.log")

    ret = run_test_target()
    res = "PASSED" if ret == 0 else "FAILED"
    print(f"test {res}")
    return ret