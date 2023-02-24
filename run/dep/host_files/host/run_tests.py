import serial
import re
import json
import traceback
import os
from datetime import datetime
from enum import Enum
from .device import PicoDevice

# PATH_TO_HEADERS = "../inc"

HOST_PRINT_TOKEN = '[PT-HOST]'
JSON_DEFINES_DATA = "defines.json"

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
    # try:
    with open(file_name, 'r') as json_file:
        defines = json.load(json_file)
        print(defines)
        return defines


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


class Test:

    class TestCase:
        class RunningStatus(Enum):
            NOT_STARTED = 0
            STARTED = 1
            ENDED = 2
        class ResultStatus(Enum):
            NOT_FINISHED = 0
            PASSED = 1
            FAILED = 2

        def __init__(self, name : str, defines : dict) -> None:
            self.name = name
            self.running = self.RunningStatus.NOT_STARTED
            self.result = self.ResultStatus.NOT_FINISHED
            self.pico_define = defines

        def passed(self):
            return self.result == self.ResultStatus.PASSED

        def failed(self):
            return self.result == self.ResultStatus.FAILED

        def correct_ctx(self, ctx : str):
            return (self.name == self.pico_define['CTX_MAIN_FUNC']) or (self.name == ctx)

        def handle_msg(self, msg : str):
            if self.pico_define['PICO_TEST_START'] in msg:
                self.running = self.RunningStatus.STARTED
                self.result.NOT_FINISHED
            elif self.pico_define['PICO_TEST_PASSED'] in msg:
                self.running = self.RunningStatus.ENDED
                self.result = self.ResultStatus.PASSED
            elif self.pico_define['PICO_TEST_FAILED'] in msg:
                self.running = self.RunningStatus.ENDED
                self.result = self.ResultStatus.FAILED

            return self.running

        # def end_test(self):
        #     self.__init__( self.__default_name, self.pico_define)

    def __init__(self, defines : dict) -> None:
        self.pico_define = defines
        self.current_tc = self.TestCase(self.pico_define['CTX_MAIN_FUNC'], defines)
        self.finished_tests = []




    def is_pico_test_print(self, msg :str) -> bool:
        return self.pico_define['PICO_TEST_OUTPUT'] in msg


    def handle_function_context(self, ctx : str,  msg : str):
        if not self.current_tc.correct_ctx(ctx):
            raise Exception('Wrong ctx')

        status = self.current_tc.handle_msg(msg)

        if status == self.TestCase.RunningStatus.ENDED:
            self.finished_tests.append(self.current_tc)
            self.current_tc = self.TestCase(self.pico_define['CTX_MAIN_FUNC'], self.pico_define)


    def pico_test_handle(self, msg: str):
        # [ctx:<name>]
        match = re.search(r'\[ctx:([\w\[\]+*.|()${}\-\"]+)\]', msg)
        if match:
            context = match.group(1)
            # print('handling ctx:', context)
            if context == self.pico_define['CTX_MAIN_FUNC']:
                if "STOP" in msg:
                    failed =  len(self.get_failed_tests())
                    print_host(f'Tests failed:{failed}')
                    passed =  len(self.get_passed_tests())
                    print_host(f'Tests passed:{passed}')
                    return failed
            else:
                # msg from testcase
                self.handle_function_context(context, msg)
        else:
            raise Exception('PICO_TEST_PRINT without context: %s' % msg)
        return None


    def get_failed_tests(self):
        return [tc for tc in self.finished_tests if tc.failed()]
    def get_passed_tests(self):
        return [tc for tc in self.finished_tests if tc.passed()]




def relative_to_absolute_path(path : str) -> str:
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    return f"{current_file_path}/{path}"

def main():

    pico_define = get_defines(relative_to_absolute_path(JSON_DEFINES_DATA))
    test = Test(pico_define)

    try:
        device = PicoDevice()
        print_host(f"starting server", flush=True)
        connect(device)
        while True:
            data = device.get_line()
            # debug


            print(data)
            if test.is_pico_test_print(data):
                # print_host(f"{data}")
                status = test.pico_test_handle(data)

                if status is not None:
                    print_host(f"Closing host with status {status}")
                    return status

    except Exception as e:
        print(f'[MAIN]:{e}')
        traceback.print_exc()
        return -1




