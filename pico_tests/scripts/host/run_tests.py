import serial
import re
import json

from device import PicoDevice

# PATH_TO_HEADERS = "../inc"

HOST_PRINT_TOKEN = '[PT-HOST]'
JSON_DEFINES_DATA = "host/defines.json"

def print_host(*args, **kwargs):
    print(HOST_PRINT_TOKEN, *args, **kwargs)

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
    with open(file_name, 'r') as json_file:
        return json.load(json_file)

pico_define = get_defines(JSON_DEFINES_DATA)

def is_pico_test_print(string :str) -> bool:
    return string.startswith(pico_define['PICO_TEST_OUTPUT'])

ser = PicoDevice()
print_host(f"starting server", flush=True)
while True:
    data = ser.readline().decode('utf-8').strip()
    print(data)

    if "\"START\"" in data:
        print_host("pico connected, starting tests")
        ser.write("START".encode())

    if "STOP" in data:
        break

print_host(f"closing server")

