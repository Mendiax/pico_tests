import os
import sys
import yaml
import logging
import paramiko
import shutil

import pico_test_data

CONFIG_FILE_NAME = "config.yaml"
HOST_PYTHON_SCRIPT = "../pico_tests/scripts/host"
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
    for item in os.listdir(local_folder):
        local_item = os.path.join(local_folder, item)
        remote_item = os.path.join(remote_folder, item)
        if os.path.isfile(local_item):
            sftp.put(local_item, remote_item)
        else:
            try:
                sftp.chdir(remote_item)  # Test if remote_path exists
            except IOError:
                sftp.mkdir(remote_item)  # Create remote_path
                sftp.chdir(remote_item)
            copy_folder_recursively(sftp, local_item, remote_item)


def prepare_data(host_files_path):
    defines = pico_test_data.get_defines()
    pico_test_data.write_to_file(defines, f"{host_files_path}/{JSON_DEFINES_DATA}")

def main(argv):

    # Load config from YAML file
    with open(CONFIG_FILE_NAME, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error("Failed to load config: %s", exc)
            sys.exit(1)

    host = config['host']
    username = config['username']
    password = config['password']
    # path to folder on target that will be holding temporary files for testing
    destination_folder = config['destination_folder']
    # name of file with pico executable
    filename = config['bin_file']
    # folder name with all files needed to run test
    test_folder = config['test_folder']
    # script with file execution
    script_filename = config['script_file']


    host_files_folder = os.path.basename(HOST_PYTHON_SCRIPT)
    # copy host scripts
    test_folder_host = f"{test_folder}/{host_files_folder}"
    if os.path.exists(test_folder_host):
        shutil.rmtree(test_folder_host)
    shutil.copytree(HOST_PYTHON_SCRIPT, test_folder_host)

    # Connect to the remote host using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
    except Exception as e:
        logging.error("Failed to connect to the host: %s", e)
        sys.exit(1)

    # Copy the bin file to the remote host
    sftp = ssh.open_sftp()
    try:
        sftp.chdir(destination_folder)  # Test if remote_path exists
    except IOError:
        sftp.mkdir(destination_folder)  # Create remote_path
        sftp.chdir(destination_folder)
    dest_file = destination_folder + "/" + os.path.basename(filename)
    dest_file_script = destination_folder + "/" + os.path.basename(script_filename)
    dest_test_folder = destination_folder # + "/" + os.path.basename(test_folder)


    prepare_data(test_folder_host)

    try:
        print('copying files')
        print(f"{filename} -> {dest_file}")
        print(f"{test_folder} -> {dest_test_folder}")
        # sftp.put(script_filename, dest_file_script)
        copy_folder_recursively(sftp, test_folder, dest_test_folder)
        sftp.put(filename, dest_file)

    except Exception as e:
        logging.error("Failed to copy the file: %s", e)
        sys.exit(1)
    finally:
        sftp.close()

    # Execute the run.sh script on the remote host
    command = f"chmod +x {destination_folder}/{script_filename} && {destination_folder}/{script_filename} {dest_file} {password}"
    print(command)
    # stdin, stdout, stderr = ssh.exec_command(command, get_pty=True)
    # output_stdout = stdout.read().decode()
    # output_stderr = stderr.read().decode()
    # for line in iter(stdout.readline, ""):
    #     print(line, end="")

    # create a new channel
    with open("output.log", "w") as output_file:
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
    # print(output_stdout)
    # print("Errors:")
    # print(output_stderr)

    ssh.close()

    # Remove the bin file from the remote host
    remove = False
    if remove:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, username=username, password=password)
            ssh.exec_command("rm " + dest_file)
            ssh.exec_command("rm " + dest_file_script)
            print("rm " + dest_file)
        except Exception as e:
            logging.error("Failed to remove the bin file: %s", e)
            sys.exit(1)
        finally:
            ssh.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv)
