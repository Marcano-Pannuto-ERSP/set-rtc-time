# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText 2023 Kristin Ebuengan
# SPDX-FileCopyrightText 2023 Melody Gill
# SPDX-FileCopyrightText 2023 Gabriel Marcano

"""
Writes current time as a tuple to serial
"""

from datetime import datetime
import time
import serial


INTERVAL = 0.05  # in seconds
DELAY = 0.05  # in seconds

def constant_time(port):
    ser = serial.Serial(port) # open serial port
    ser.baudrate = 115200

    startTime = time.monotonic()
    endTime = startTime + INTERVAL
    now = time.monotonic()

    while now < endTime:   # runs for the specified interval
        currTime = datetime.utcnow()
        currWeekday = time.gmtime().tm_wday
        currMillisec = int(currTime.microsecond/10000)
        currTuple = (
            currTime.year,
            currTime.month,
            currTime.day,
            currWeekday,
            currTime.hour,
            currTime.minute,
            currTime.second,
            currMillisec
        )
        toWrite = bytearray(str(currTuple) + "\n", 'utf-8')
        ser.write(toWrite)

        time.sleep(DELAY)
        now = time.monotonic()

    ser.close() # close serial port
