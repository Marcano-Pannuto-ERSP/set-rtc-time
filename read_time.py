import sys
from rtc import *
from machine import Pin

"""
Function to easily check the time on the RTC
"""

def read_time():
    MudwattRTC = RTC()
    print(MudwattRTC.get_time())

read_time()