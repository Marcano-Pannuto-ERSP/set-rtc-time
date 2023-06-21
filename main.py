import time
from rtc import *
import sys

# runs on the pico

if __name__ == "__main__":
    MudwattRTC = RTC()

    # read a line from serial
    line = sys.stdin.readline()
    print(line)
    MudwattRTC.set_time(line)
    MudwattRTC.enable_trickle()
