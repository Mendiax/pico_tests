import serial
import glob
import time
import os
import subprocess
import re


class PicoDevice(serial.Serial):

    def get_devices(self):
        devices = []

        try_count = 0
        while len(devices) == 0 and try_count <= 5:
            devices = glob.glob('/dev/ttyACM*')
            print(f'[{try_count}]Avaible devices:', devices)
            try_count += 1
            if len(devices) == 0:
                time.sleep(1)
        return devices

    def __init__(self) -> None:

        try_count = 0
        devices = self.get_devices()
        while len(devices) == 0 and try_count <= 3:
            self.reset()
            try_count += 1
            devices = self.get_devices()



        # TODO add choosing device
        # now is the first one
        pico_dev = devices[0]
        print('Picked:')
        print(pico_dev)
        print(subprocess.getoutput("pwd"))
        # print(subprocess.getoutput(f'stat /dev/'))
        # print(subprocess.getoutput(f'stat {pico_dev}'))
        super().__init__(pico_dev)

    def get_line(self) -> str:
        return self.readline().decode('utf-8').strip()

    def reset(self) -> None:
        print(subprocess.getoutput("picotool reboot -f"))
        time.sleep(5.0)
        self.__init__()