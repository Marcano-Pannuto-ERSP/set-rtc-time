import sys
from rtc import *

"""
test for seeing if we can measure accuracy of time
"""

def pico_test_time():
    MudwattRTC = RTC()

    # Request a time from the server
    sys.stdout.write("this is a request")
    t0 = MudwattRTC.get_time()

    # Find timestamp for receiving a response
    response = sys.stdin.readline()
    t3 = MudwattRTC.get_time()

    print(f"t0: {t0}, t1: {t3}")

pico_test_time()