# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText 2023 Kristin Ebuengan
# SPDX-FileCopyrightText 2023 Melody Gill
# SPDX-FileCopyrightText 2023 Gabriel Marcano

"""
Sets the time of the RTC with accuracy of 2 hundredths of seconds
(accuracy can be changed with --range command line argument)
"""

import math
import argparse
import serial
from constant_time import constant_time
from server_test_time import server_test_time

def find_timer(timer):
    if timer <= 0.0625:
        timer = (int(timer * 4096))/4096
    elif timer <= 4:
        timer = (int(timer * 64))/64
    elif timer <= 256:
        timer = int(timer)
    elif timer <= 15360:
        timer = (int(timer/60)) * 60
    else:
        timer = 15360
    if timer == 0:
        print("Timer disabled (set to 0 seconds)")
    else:
        print("Timer set to: " + str(timer))
    return timer

def update_rtc(port, range, trials, f, a, pulse, da, dt, timer, repeat):
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
    timerSet = find_timer(timer)
    ser.write(bytearray(
        "\x01import initialize_rtc;initialize_rtc.initialize_rtc(" + str(f) + ", " + str(a) + \
        "," + str(pulse) + "," + str(da) + "," + str(dt) + "," + str(timerSet) + "," + str(repeat) + ");\x04\x02",
        'utf-8'))

# Command line arguments
parser = argparse.ArgumentParser(
    description='Initialize the RTC and sets the time', \
    epilog='If no optional arguments are entered, then the program will run 100 \
        trials to determine the average offset, with time accuracy within 0.02 seconds, \
        FOS is set to 1 (automatic switching when an oscillator failure is detected), \
        AOS is set to 0 (will use XT oscillator when the system is powered from the battery), \
        the alarm is enabled (and initialize alarm to go off once a second if 0 (default value) \
        is in hundredths alarm register), and the alarm pulse is 1/8192 seconds for XT or \
        1/64 sec for RC')
parser.add_argument(
    '--port',
    type=str,
    required=True,
    help='sets the port the Raspberry Pi Pico is plugged into'
)
parser.add_argument('--range', type=int, default=1, help='sets the new accuracy range to RANGE')
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
    default=0b01,
    choices=range(0,4),
    help='sets the length of pulse: 1 means 1/8192 seconds for XT and 1/64 sec for RC; \
        2 means 1/64 s for both; 3 means 1/4 s for both; 0 means level (static)'
)
parser.add_argument(
    '-da',
    action='store_true',
    help='disable the RTC alarm'
)
parser.add_argument(
    '-dt',
    action='store_true',
    help='disable trickle charging'
)
parser.add_argument(
    '--timer',
    type=float,
    default=0,
    help='set repeating timer to TIMER seconds'
)
parser.add_argument(
    '--repeat',
    type=int,
    default=7,
    choices=range(1,8),
    help='sets the repeat function for the alarm: 1 means once per year, 2 means once per \
    month, 3 means once per week, 4 means once per day, 5 means once per hour, 6 means once \
    per minute, 7 means once per second'
)
args = parser.parse_args()

update_rtc(args.port, args.range, args.trials, args.f, args.a, args.pulse, args.da, args.dt, args.timer, args.repeat)
