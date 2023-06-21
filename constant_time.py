from datetime import datetime
import time
import serial

"""
Writes current time as a tuple to serial
"""

PORT = '/dev/ttyACM2'
# PORT = '/dev/ttyACM3'

def constant_time():
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 19200

    while True: # runs indefinitely
        currTime = datetime.utcnow()
        currWeekday = time.gmtime().tm_wday
        currMillisec = int(currTime.microsecond/10000) # update this (to be more accurate)
        currTuple = (currTime.year, currTime.month, currTime.day, currWeekday, currTime.hour, currTime.minute, currTime.second, currMillisec)
        # print(currTuple)
        toWrite = bytearray(str(currTuple) + "\n", 'utf-8')
        ser.write(toWrite)

    ser.close() # close serial port

constant_time()
