from datetime import datetime
import time
import serial

"""
Writes current time as a tuple to serial
"""

PORT = '/dev/ttyACM2'
# PORT = '/dev/ttyACM3'
INTERVAL = 60  # in seconds

def constant_time():
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 19200

    start_time = time.monotonic()
    end_time = start_time + INTERVAL
    now = time.monotonic()

    while now < end_time:   # runs for the specified interval
        currTime = datetime.utcnow()
        currWeekday = time.gmtime().tm_wday
        currMillisec = int(currTime.microsecond/10000)  # update this (to be more accurate)
        currTuple = (currTime.year, currTime.month, currTime.day, currWeekday, currTime.hour, currTime.minute, currTime.second, currMillisec)
        print(currTuple)
        toWrite = bytearray(str(currTuple) + "\n", 'utf-8')
        ser.write(toWrite)

        now = time.monotonic()

    ser.close() # close serial port

constant_time()
