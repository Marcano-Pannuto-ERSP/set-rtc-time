import sys
from rtc import *
import time

"""
Reads the time from the server and uses it to set the time in the RTC
"""

def set_time():
    MudwattRTC = RTC()

    # read a line from serial and set the RTC to that time
    line = sys.stdin.readline()
    # sys.stdout.write("hello!\n")
    # sys.stdout.write(line + "\n")

    # parse back into a tuple
    timeTuple = str(line)[2:-2]  # remove parentheses
    # sys.stdout.write(timeTuple + "\n")
    splitList = timeTuple.split(", ")
    intTuple = tuple([int(x) for x in splitList])

    MudwattRTC.set_time(intTuple)


def change_time(offset):
    MudwattRTC = RTC()

    timeList = list(MudwattRTC.get_time_seconds())
    offsetSec = offset // 100
    offsetHund = offset % 100
    timeList[1] += offsetHund
    if timeList[1] >= 100:
        toAdd = timeList[1] // 100
        timeList[1] -= 100 * toAdd
        timeList[0] += toAdd
    timeList[0] += offsetSec
    MudwattRTC.set_time(timeList)