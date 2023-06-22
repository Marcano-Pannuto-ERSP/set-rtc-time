import sys
from rtc import *
import time

"""
test for seeing if we can measure accuracy of time
"""

def pico_test_time():
    MudwattRTC = RTC()

    time.sleep(1)
    # Request a time from the server
    sys.stdout.write("this is a request\n")
    t0 = MudwattRTC.get_time()

    # Find timestamp for receiving a response
    response = sys.stdin.readline()
    t3 = MudwattRTC.get_time()

    sys.stdout.write(f"t0: {t0}, t1: {t3}\n")

pico_test_time()