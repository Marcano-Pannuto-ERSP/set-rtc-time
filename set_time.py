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

    # parse back into a tuple
    timeTuple = str(line)[2:-2]  # remove parentheses
    splitList = timeTuple.split(", ")
    intTuple = tuple([int(x) for x in splitList])

    MudwattRTC.set_time(intTuple)

"""
Change the time of the RTC according to the offset given
"""

def change_time(offset):
    MudwattRTC = RTC()

    # gets the time in seconds
    timeList = list(MudwattRTC.get_time_seconds())

    # gets the offsets
    offsetSec = offset // 100
    offsetHund = offset % 100

    # adds hundredths to the time
    timeList[1] += offsetHund

    # if there's a carry over
    if timeList[1] >= 100:
        toAdd = timeList[1] // 100
        timeList[1] -= 100 * toAdd
        timeList[0] += toAdd

    # adds seconds to the time
    timeList[0] += offsetSec

    # sets the time with the offset
    MudwattRTC.set_time(timeList)