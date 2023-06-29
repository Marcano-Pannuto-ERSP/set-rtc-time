"""
Helper file for testing the accuracy of time
To be run on the RPi Pico (called by server_test_time.py)
"""

import sys
import time
from rtc import *


def pico_test_time():
    MudwattRTC = RTC()

    time.sleep(0.005)
    # Request a time from the server
    sys.stdout.write("this is a request\n")
    t0 = MudwattRTC.get_time()

    # Find timestamp for receiving a response
    sys.stdin.readline()
    t3 = MudwattRTC.get_time()

    sys.stdout.write(f"t0: {t0}, t3: {t3}\n")
