import os
import sys
import yaml
import logging
import paramiko
import shutil
import subprocess


CONFIG_FILE_NAME = "config.yaml"
PICO_TESTS_SOURCE = "../pico_tests/"
JSON_DEFINES_DATA = "defines.json"


def put_dir(sftp, source, target):
    ''' Uploads the contents of the source directory to the target path. The
        target directory needs to exists. All subdirectories in source are
        created under target.
    '''
    for item in os.listdir(source):
        if os.path.isfile(os.path.join(source, item)):
            sftp.put(os.path.join(source, item), '%s/%s' % (target, item))
        else:
            sftp.mkdir('%s/%s' % (target, item), ignore_existing=True)
            sftp.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

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
            # try:
            #     sftp.chdir(remote_item)  # Test if remote_path exists
            # except IOError:
            #     sftp.mkdir(remote_item)  # Create remote_path
            #     sftp.chdir(remote_item)
            copy_folder_recursively(sftp, local_item, remote_item)


# def prepare_data(host_files_path, inc_files_path):
#     defines = dep.pico_test_data.get_defines(inc_files_path)
#     dep.pico_test_data.write_to_file(defines, f"{host_files_path}/{JSON_DEFINES_DATA}")


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




def run(config):

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
    # BINARY_FOLDER_PATH = f'{dep_folder_path}/host_files/bin'
    # prepare_data(f"{config.test_folder}/host", PICO_TESTS_SOURCE)
    # dest_file = config.destination_folder + "/" + os.path.basename(filename)


    path_to_pico_bin_ssh = f'{config.destination_folder}/{os.path.basename(config.bin_file)}'
    path_to_python_host_ssh = f'{config.destination_folder}/host'


    # copy data
    try:
        print('copying files')
        print(f"{HOST_PYTHON_PATH} -> { config.destination_folder}")
        print(f"{config.bin_file} -> {path_to_pico_bin_ssh}")
        # sftp.put(script_filename, dest_file_script)

        # copy python scripts and bin file over ssh
        copy_folder_recursively(sftp, HOST_PYTHON_PATH, config.destination_folder)
        print(f'copied python')
        sftp.put(config.bin_file, path_to_pico_bin_ssh)
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

    #
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


        # execute_command(f'pwd && ls')
        execute_command(f'ls /tmp/pico_test')

        # load binary file
        execute_command(f'picotool load -x {path_to_pico_bin_ssh} -f')

        # run python host
        return_values = execute_command(f'echo "" && cd {path_to_python_host_ssh}/.. ; python3 -u -m host')
        print(f'Host returned {return_values}')


    # print(output_stdout)
    # print("Errors:")
    # print(output_stderr)

    # Remove the bin file from the remote host
    remove = True
    if remove:
        ssh.exec_command("rm -rf " + config.destination_folder)
        print("rm -rf " + config.destination_folder)

    ssh.close()

    return_values = 0
    # with open(LOG_FILE, "r") as output_file:
    #     lines = output_file.readlines()
    #     for l in lines:
    #         if 'failed' in l.lower():
    #             return_values = -1
    #             break



    return return_values
