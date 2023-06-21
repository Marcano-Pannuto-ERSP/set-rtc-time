from machine import Pin
from machine import ADC
import time
from rtc import *
from machine import UART

# runs on the pico

if __name__ == "__main__":
    MudwattRTC = RTC()
    # while(True):
    #     currTime = MudwattRTC.get_time()
    #     print(currTime)

    # ntptime.settime()
    # currTime = time.localtime()
    # print(currTime)
    # MudwattRTC = RTC()
    # MudwattRTC.set_time(currTime)

    print("Initializing UART")
    uart = UART(1, 19200)                         # init with given baudrate
    uart.init(19200, bits=8, parity=None, stop=1) # init with given parameters

    # read a line
    line = uart.readline()     # read a line
    print(line)

    """
    uart.read(10)       # read 10 characters, returns a bytes object
    uart.read()         # read all available characters
    uart.readline()     # read a line
    uart.readinto(buf)  # read and store into the given buffer
    uart.write('abc')   # write the 3 characters
    """
