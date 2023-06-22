import datetime
import serial
import time

"""
test for seeing if we can measure accuracy of time (server side)
"""

PORT = '/dev/ttyACM4'

def server_test_time():
    # Find timestamp for receiving request packet
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 19200
    line = ser.readline()
    t1 = datetime.datetime.now()

    # Record timestamp of sending response packet
    time.sleep(1)
    ser.write(bytearray("this is a response", 'utf-8'))
    t2 = datetime.datetime.now()
    ser.close()

    print(f"t1: {t1}, t2: {t2}")

server_test_time()