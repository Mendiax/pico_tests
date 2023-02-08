import serial
import glob


class PicoDevice(serial.Serial):

    def __init__(self) -> None:
        devices = glob.glob('/dev/ttyACM*')
        print('Avaible devices:')
        print(devices)

        # TODO add choosing device
        # now is the first one
        pico_dev = devices[0]
        print('Picked:')
        print(pico_dev)
        super().__init__(pico_dev)