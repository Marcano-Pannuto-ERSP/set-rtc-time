from constant_time import constant_time
import serial

"""
Sets the time of the RTC with the utmost accuracy
(doesn't change the time yet)
"""

PORT = '/dev/ttyACM2'

def update_rtc():
    # Find timestamp for receiving request packet
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 115200

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # Run initialize_rtc()
    ser.write(bytearray("\x01import set_time;set_time.set_time();\x04\x02", 'utf-8'))

    constant_time()

update_rtc()