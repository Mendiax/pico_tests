import os
import sys
import yaml
import logging
import paramiko
import shutil
import subprocess

from dep.config import Config
from .run_common import *

CONFIG_FILE_NAME = "config.yaml"
PICO_TESTS_SOURCE = "../pico_tests/"
JSON_DEFINES_DATA = "defines.json"


def copy_folder_recursively(sftp, local_folder, remote_folder):
    # print(f'copy rec {local_folder=} {remote_folder=}')
    # create folder
    try:
        sftp.chdir(remote_folder)  # Test if remote_path exists
    except IOError:
        sftp.mkdir(remote_folder)  # Create remote_path
        sftp.chdir(remote_folder)

    for item in os.listdir(local_folder):
        local_item = os.path.join(local_folder, item)
        remote_item = os.path.join(remote_folder, item)
        if os.path.isfile(local_item):
            sftp.put(local_item, remote_item)
        else:
            copy_folder_recursively(sftp, local_item, remote_item)


def ssh_start(config):
    # Connect to the remote host using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(config.host, username=config.username, password=config.password)
    except Exception as e:
        logging.error("Failed to connect to the host: %s", e)
        sys.exit(1)
    return ssh


def run(config : Config):

    ssh = ssh_start(config)
    sftp = ssh.open_sftp()
    ssh.exec_command("pwd")
    LOG_FILE = "output.log"


    # Copy the bin file to the remote host
    # try:
    #     sftp.chdir(config.destination_folder)  # Test if remote_path exists
    # except IOError:
    #     sftp.mkdir(config.destination_folder)  # Create remote_path
    #     sftp.chdir(config.destination_folder)
    # dest_file_script = config.destination_folder + "/" + os.path.basename(script_filename)
    # dest_test_folder = config.destination_folder # + "/" + os.path.basename(test_folder)

    # generate define file
    dep_folder_path = os.path.abspath(os.path.dirname(__file__))
    print('pwd:',subprocess.getoutput("pwd"))
    print('dep:', dep_folder_path)
    HOST_PYTHON_PATH = f'{dep_folder_path}/host_files'


    path_to_python_host_ssh = f'{config.destination_folder}/host'

    all_bin_files = config.get_bin_list()
    print(f"running tests: {all_bin_files}")

    # copy data
    try:
        print('copying files')
        print(f"{HOST_PYTHON_PATH} -> { config.destination_folder}")
        # copy python scripts and bin file over ssh
        copy_folder_recursively(sftp, HOST_PYTHON_PATH, config.destination_folder)
        print(f'copied python')

        for bin_file in all_bin_files:
            path_to_pico_bin_ssh = f'{config.destination_folder}/{os.path.basename(bin_file)}'
            print(f"{bin_file} -> {path_to_pico_bin_ssh}")
            sftp.put(bin_file, path_to_pico_bin_ssh)
            print(f'copied binary')

    except Exception as e:
        logging.error("Failed to copy the file: %s", e)
        sys.exit(1)
    finally:
        sftp.close()

    # Execute the run.sh script on the remote host
    # command = f"chmod +x {destination_folder}/{script_filename} && {destination_folder}/{script_filename} {dest_file} {password}"
    # print(command)
    # stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    # output_stdout = stdout.read().decode()
    # output_stderr = stderr.read().decode()
    # for line in iter(stdout.readline, ""):
    #     print(line, end="")

    return_values = -1
    # upload binary to pico device and run tests
    with open(LOG_FILE, "w") as output_file:

        def execute_command(command: str):
            print(f'exec {command}')
            # init session
            channel = ssh.get_transport().open_session()
            # set the channel to receive both stdout and stderr
            channel.set_combine_stderr(True)
            channel.exec_command(command)
            while not channel.exit_status_ready():
                if channel.recv_ready():
                    output = channel.recv(1024).decode()
                    print(output, end='')
                    output_file.write(output)
            channel.close()
            exit_code = channel.recv_exit_status()
            return exit_code

        return_values = 0
        # execute_command(f'ls /tmp/pico_test')

        for bin_file in all_bin_files:
            path_to_pico_bin_ssh = f'{config.destination_folder}/{os.path.basename(bin_file)}'
            # load binary file
            execute_command(f'picotool load -x {path_to_pico_bin_ssh} -f')

            # run python host
            test_return_val = execute_command(f'echo "" && cd {path_to_python_host_ssh}/.. ; python3 -u -m host')
            print(f'Host returned {test_return_val}')
            if test_return_val != 0:
                return_values = -1

    # Remove the bin file from the remote host
    remove = True
    if remove:
        ssh.exec_command("rm -rf " + config.destination_folder)
        print("[CLEANUP] rm -rf " + config.destination_folder)

    ssh.close()
    print(f"Tests ended with {return_values}")
    print(f"Tests {passed_bool_to_str(return_values)}")
    return return_values
