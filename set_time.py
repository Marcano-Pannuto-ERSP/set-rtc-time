import sys
from rtc import *
from machine import Pin 

"""
Reads the time from the server and uses it to set the time in the RTC
"""

def set_time():
    MudwattRTC = RTC()

    # read a line from serial and set the RTC to that time
    line = sys.stdin.readline()

    # parse back into a tuple
    timeTuple = line[1:-2]  # remove parentheses
    splitList = timeTuple.split(", ")
    intTuple = tuple([int(x) for x in splitList])

    MudwattRTC.set_time(intTuple)

set_time()