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
Sets the time of the RTC with accuracy of 2 hundredths of seconds
(accuracy can be changed with --range command line argument)

Initializes the RTC by:
- enabling trickle charging for backup battery
- disabling unused pins
- changing settings to specify disabling SPI in absence of VCC
- enabling/disabling automatic RC/XT oscillator switching according to user input
- configuring the RTC alarm
- writing to register 1 bit 7 to signal that this program initialized the RTC

Run with:
python update_rtc.py [-h] --port PORT [--range RANGE] [--trials TRIALS] [-f] [-a] [--pulse {1,2,3}] [-i]
--port PORT sets the port the Raspberry Pi Pico is plugged into
--range RANGE sets the new accuracy range to RANGE
--trials TRIALS sets the new number of trials to get the average offset to TRIALS
-f means set FOS to 0 (no automatic switching when an oscillator failure is
    detected)
-a means set AOS to 1 (automatically switches to RC oscillator when the system
    is powered from the battery)
--pulse PULSE sets the length of pulse: 1 means 1/8192 seconds for XT and 1/64 sec for RC;
    2 means 1/64 s for both; 3 means 1/4 s for both; 0 means level (static)
-i means enable the RTC alarm

no optional arguments means accuracy is within 2 hundredths of seconds, 100 trials are run to
determine the average offset, FOS is set to 1 (automatic switching when an oscillator failure is
detected), AOS is set to 0 (will use XT oscillator when the system is powered from the battery),
the alarm is disabled, and the alarm pulse is 1/4 seconds
"""

import math
import argparse
import serial
from constant_time import constant_time
from server_test_time import server_test_time


def update_rtc(port, range, trials, f, a, pulse, i):
    ser = serial.Serial(port) # open serial port
    ser.baudrate = 115200

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # Run set_time()
    ser.write(bytearray("\x01import set_time;set_time.set_time();\x04\x02", 'utf-8'))

    # Gets the timestamps from the server
    constant_time(port)

    # Checks the offset
    offset = int(server_test_time(port, trials) * 100)

    # If offset is too big keep changing the time
    while math.fabs(offset) > range:
        # Changes the time by the offset
        ser.write(bytearray(
            "\x01import set_time;set_time.change_time(" + str(offset) + ");\x04\x02",
            'utf-8'
        ))
        offset = int(server_test_time(port, trials) * 100)

    # Initialize the pins
    ser.write(bytearray(
        "\x01import initialize_rtc;initialize_rtc.initialize_rtc(" + str(f) + ", " + str(a) + \
        "," + str(pulse) + "," + str(i) + ");\x04\x02",
        'utf-8'))

# Command line arguments
parser = argparse.ArgumentParser(
    description='Initialize the RTC and sets the time', \
    epilog='no optional arguments means accuracy is within 2 hundredths of seconds, 100 trials are \
        run to determine the average offset, FOS is set to 1 (automatic switching when an \
        oscillator failure is detected), and AOS is set to 0 (will use XT oscillator when the \
        system is powered from the battery)')
parser.add_argument(
    '--port',
    type=str,
    required=True,
    help='sets the port the Raspberry Pi Pico is plugged into'
)
parser.add_argument('--range', type=int, default=2, help='sets the new accuracy range to RANGE')
parser.add_argument(
    '--trials',
    type=int,
    default=100,
    help='sets the new number of trials to get the average offset to TRIALS'
)
parser.add_argument(
    '-f',
    action='store_true',
    help='set FOS to 0 (no automatic switching when an oscillator failure is detected)'
)
parser.add_argument(
    '-a',
    action='store_true',
    help='set AOS to 1 (automatically switches to RC oscillator when the system is powered from \
        the battery)'
)
parser.add_argument(
    '--pulse',
    type=int,
    default=0b11,
    choices=range(0,4),
    help='sets the length of pulse: 1 means 1/8192 seconds for XT and 1/64 sec for RC; \
        2 means 1/64 s for both; 3 means 1/4 s for both; 0 means level (static)'
)
parser.add_argument(
    '-i',
    action='store_true',
    help='enable the RTC alarm'
)
args = parser.parse_args()

update_rtc(args.port, args.range, args.trials, args.f, args.a, args.pulse, args.i)
