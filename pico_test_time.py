"""
SPDX-FileCopyrightText 2023 Kristin Ebuengan
SPDX-FileCopyrightText 2023 Melody Gill
SPDX-FileCopyrightText 2023 Gabriel Marcano

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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
