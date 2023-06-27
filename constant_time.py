from datetime import datetime, timedelta
import time
import serial

"""
Writes current time as a tuple to serial
"""

INTERVAL = 0.05  # in seconds
DELAY = 0.05  # in seconds

def constant_time(PORT):
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 115200

    startTime = time.monotonic()
    endTime = startTime + INTERVAL
    now = time.monotonic()

    while now < endTime:   # runs for the specified interval
        currTime = datetime.utcnow()
        currWeekday = time.gmtime().tm_wday
        currMillisec = int(currTime.microsecond/10000)
        currTuple = (currTime.year, currTime.month, currTime.day, currWeekday, currTime.hour, currTime.minute, currTime.second, currMillisec)
        toWrite = bytearray(str(currTuple) + "\n", 'utf-8')
        ser.write(toWrite)

        time.sleep(DELAY)
        now = time.monotonic()

    ser.close() # close serial port