from constant_time import constant_time
from server_test_time import server_test_time
import serial
import time
import math
import argparse

"""
Sets the time of the RTC with the utmost accuracy
(doesn't change the time yet)
"""

def update_rtc(PORT, RANGE, TRIALS):
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 115200

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # Run set_time()
    ser.write(bytearray("\x01import set_time;set_time.set_time();\x04\x02", 'utf-8'))

    # Gets the timestamps from the server
    constant_time(PORT)

    # Checks the offset
    offset = int(server_test_time(PORT, TRIALS) * 100)

    # If offset is too big keep changing the time
    while math.fabs(offset) > RANGE:
        # Changes the time by the offset
        ser.write(bytearray("\x01import set_time;set_time.change_time(" + str(offset) + ");\x04\x02", 'utf-8'))
        offset = int(server_test_time(PORT, TRIALS) * 100)

    # Initialize the pins
    initialize_rtc()

# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=str, required=True)
parser.add_argument('--range', type=int, default=2)
parser.add_argument('--trials', type=int, default=100)
args = parser.parse_args()

update_rtc(args.port, args.range, args.trials)