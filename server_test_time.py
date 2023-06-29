"""
SPDX-FileCopyrightText 2023 Kristin Ebuengan
SPDX-FileCopyrightText 2023 Melody Gill
SPDX-FileCopyrightText 2023 Gabriel Marcano

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

"""
Measure accuracy of the time that was set on the RTC
The server is automaton and the client is the RTC
"""

import datetime
import serial
import numpy


def server_test_time(port, trials):
    STATUS = trials // 5
    offsetAvg = []
    for x in range(trials):
        # Find timestamp for receiving request packet
        ser = serial.Serial(port) # open serial port
        ser.baudrate = 115200

        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # Run pico script on automaton
        ser.write(bytearray(
            "\x01import pico_test_time;pico_test_time.pico_test_time();\x04\x02",
            'utf-8'
            ))

        # Finds the request
        line = ser.readline()
        while line.decode('utf-8')[3:-2] != "this is a request":
            line = ser.readline()
        t1 = datetime.datetime.utcnow()

        # Record timestamp of sending response packet
        ser.write(bytearray("this is a response\r\n", 'utf-8'))
        t2 = datetime.datetime.utcnow()

        # Record timestamps from pico
        picoStamps = ser.readline()

        ser.close()

        # Gets milliseconds from timestamps
        picoSplit = str(picoStamps)[7:-6]
        picoLists = picoSplit.split("), t3: (")

        t0List = picoLists[0].split(", ")
        t3List = picoLists[1].split(", ")
        t0Tuple = tuple([int(x) for x in t0List])
        t3Tuple = tuple([int(x) for x in t3List])

        t0 = datetime.datetime(
            t1.year,
            t0Tuple[1],
            t0Tuple[2],
            t0Tuple[4],
            t0Tuple[5],
            t0Tuple[6],
            t0Tuple[7] * 1000
        )
        t3 = datetime.datetime(
            t2.year,
            t3Tuple[1],
            t3Tuple[2],
            t3Tuple[4],
            t3Tuple[5],
            t3Tuple[6],
            t3Tuple[7] * 1000
        )

        # Get the offset
        firstHalf = t1 - t0
        secondHalf = t2 - t3
        finalResult = (firstHalf + secondHalf)/2
        offsetAvg.append(finalResult.total_seconds())

        # Keep track of trials
        if x % STATUS == 0:
            print(str(x) + " trials to check time accuracy completed")

    toReturn = sum(offsetAvg)/trials
    print("Average offset in seconds: " + str(toReturn))
    print("Standard Deviation: " + str(numpy.std(offsetAvg)))
    return toReturn
