from dep.config import Config

import subprocess
import logging
import sys
from .host_files.host.run_tests import main as run_test_target

def run_command(cmd: str, file_name: str):
    """Runs a command and captures both stdout and stderr to the same file.

    Args:
        cmd (str): The command to run.
        file_name (str): The name of the file to write the output to.

    Returns:
        None
    """
    try:
        with open(file_name, "w") as output_file:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            for line in iter(proc.stdout.readline, b''):
                sys.stdout.write(line.decode(sys.stdout.encoding))
                output_file.write(line.decode(output_file.encoding))
            proc.wait()
            return proc.returncode
    except Exception as e:
        logging.error("Failed to copy the file: %s", e)
        sys.exit(1)

def run_cmd(cmd:str):
    print(cmd)
    print(subprocess.getoutput(cmd))


def run(config : Config) -> int:
    run_cmd('pwd')
    run_cmd('lsusb')
    for x in range(5):
        success = run_cmd(f"picotool load -x -v {config.bin_file} -f") == 0
        if success:
            break
    # ret = run_command(config.get_run_cmd(), "tests.log")

    ret = run_test_target()
    res = "PASSED" if ret == 0 else "FAILED"
    print(f"test {res}")
    return ret