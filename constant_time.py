from datetime import datetime, timedelta
import time
import serial

"""
Writes current time as a tuple to serial
"""

PORT = '/dev/ttyACM2'
INTERVAL = 10  # in seconds
DELAY = 0.50  # in seconds
OFFSET = 560 # in milliseconds

def constant_time():
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 115200

    startTime = time.monotonic()
    endTime = startTime + INTERVAL
    now = time.monotonic()

    while now < endTime:   # runs for the specified interval
        currTime = datetime.utcnow() + timedelta(milliseconds = OFFSET)
        currWeekday = time.gmtime().tm_wday
        currMillisec = int(currTime.microsecond/10000)  # update this (to be more accurate)
        currTuple = (currTime.year, currTime.month, currTime.day, currWeekday, currTime.hour, currTime.minute, currTime.second, currMillisec)
        # print(currTuple)
        toWrite = bytearray(str(currTuple) + "\n", 'utf-8')
        ser.write(toWrite)

        time.sleep(DELAY)
        now = time.monotonic()

    ser.close() # close serial port

constant_time()