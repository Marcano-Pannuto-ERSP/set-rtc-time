import sys
from rtc import *
import time

"""
test for seeing if we can measure accuracy of time
"""

def pico_test_time_2():
    MudwattRTC = RTC()

    line = sys.stdin.readline()
    while(line.find("this is a request") == -1):
        sys.stdout.write(line)
        line = sys.stdin.readline()
    sys.stdout.write(line)
    t1 = MudwattRTC.get_time()

    # Record timestamp of sending response packet
    sys.stdout.write("this is a response\n")
    t2 = MudwattRTC.get_time()
    
    sys.stdout.write(f"t1: {t1}, t2: {t2}\n")
    print(sys.stdin.readline())

pico_test_time_2()