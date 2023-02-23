import serial
import re
import json
import sys
import traceback
from datetime import datetime

from .device import PicoDevice

# PATH_TO_HEADERS = "../inc"

HOST_PRINT_TOKEN = '[PT-HOST]'
JSON_DEFINES_DATA = "host/defines.json"

def print_host(*args, **kwargs):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time, HOST_PRINT_TOKEN, *args, **kwargs)

def get_defines(file_name):
    # defines = {}
    # with open(header_file, "r") as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         match = re.search(r"#define\s+(\w+)\s+(\w+)", line)
    #         if match:
    #             defines[match.group(1)] = match.group(2)
    # return defines
    """Reads a JSON file and returns a dictionary

    Args:
        file_name (str): The name of the file to read

    Returns:
        dict: The JSON data in dictionary form
    """
    try:
        with open(file_name, 'r') as json_file:
            return json.load(json_file)
    except:
        print(f"{JSON_DEFINES_DATA} not found")
        return {'PICO_TEST_OUTPUT' : "[PT]"}


def is_pico_test_print(string :str) -> bool:
    return string.startswith(pico_define['PICO_TEST_OUTPUT'])

pico_define = get_defines(JSON_DEFINES_DATA)

def connect(device):
    TIMEOUT_S = 3
    NO_CONNECTIONS = 4
    import time
    print_host("Connecting to device...")
    for x in range(NO_CONNECTIONS):
        t_end = time.time() + TIMEOUT_S
        while time.time() < t_end:
            data = device.get_line()
            print(data)

            if data is not None and "\"START\"" in data:
                print_host("pico connected, starting tests")
                device.write("START".encode())
                return
        print_host(f'restarting device {x}')
        device.reset()



def main():
    try:
        device = PicoDevice()
        print_host(f"starting server", flush=True)
        connect(device)
        while True:
            data = device.get_line()
            print(data)

            if "STOP" in data:
                print_host(f"closing server")
                return 0

    except Exception as e:
        print(f'[MAIN]:{e}')
        traceback.print_exc()
        return -1

if __name__ == '__main__':
    sys.exit(main())


