import re
import os
import json
import sys

PATH_TO_INC = '../pico_tests'
PATH_TO_HOST = 'dep/host_files/host'


def get_defines_from_file(header_file: str) -> dict:
    """Extracts all defines from header_file and returns them
    as a dictionary where keys are defines names and values are values of defines.
    """
    defines = {}
    with open(header_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(r"#define\s+(\w+)\s+([\w\[\]+*.|()${}\-\"]+)", line)
            if match:
                key = match.group(1)
                val = match.group(2)
                if val.startswith(r'"'):
                    val = val[1:]
                if val.endswith(r'"'):
                    val = val[:-1]
                defines[key] = val
    return defines

def get_defines(path_to_inc=PATH_TO_INC) -> dict:
    """Scans path_to_inc recursively and extract all defines from .h and .hpp files
    using get_defines_from_file(header_file) function. Returns dictionary with all
    defines where keys are defines names and values are values of defines.
    """
    defines = {}
    for root, dirs, files in os.walk(path_to_inc):
        print(files)
        for file in files:
            if file.endswith((".h", ".hpp")):
                header_file = os.path.join(root, file)
                defines.update(get_defines_from_file(header_file))
    print(defines)
    return defines

def write_to_file(dictionary :dict, file_name :str):
    """Writes all values from dictionary to file file_name in JSON format.
    """
    with open(file_name, 'w') as f:
        json.dump(dictionary, f, indent=4)

if __name__ == "__main__":
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    path_to_host = f"{current_file_path}/{PATH_TO_HOST}/defines.json"
    write_to_file(get_defines(PATH_TO_INC), path_to_host)