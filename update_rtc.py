from constant_time import constant_time
from server_test_time import server_test_time
import serial
import time
import math

"""
Sets the time of the RTC with the utmost accuracy
(doesn't change the time yet)
"""

PORT = '/dev/ttyACM2'
RANGE = 2

def update_rtc():
    # Find timestamp for receiving request packet
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 115200

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # Run set_time()
    ser.write(bytearray("\x01import set_time;set_time.set_time();\x04\x02", 'utf-8'))

    # Gets the timestamps from the server
    constant_time()

    # Checks the offset
    offset = int(server_test_time() * 100)

    # print("enter minicom")
    # time.sleep(7)

    # Adjusts time by the offset
    ser.write(bytearray("\x01import set_time;set_time.change_time(" + str(offset) + ");\x04\x02", 'utf-8'))

    # Check the offset again
    offset = int(server_test_time() * 100)

    # If offset is too big keep changing the time
    while math.fabs(offset) > RANGE:
        ser.write(bytearray("\x01import set_time;set_time.change_time(" + str(offset) + ");\x04\x02", 'utf-8'))
        offset = int(server_test_time() * 100)

update_rtc()