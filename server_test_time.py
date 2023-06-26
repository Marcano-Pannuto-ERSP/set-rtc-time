import datetime
import serial
import time
import numpy

"""
test for seeing if we can measure accuracy of time (the server is automaton)
"""

PORT = '/dev/ttyACM5'
TRIALS = 100000
STATUS = 1000

def server_test_time():
    offsetAvg = []
    for x in range(TRIALS):
        # Find timestamp for receiving request packet
        ser = serial.Serial(PORT) # open serial port
        ser.baudrate = 115200

        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # Run pico script on automaton
        ser.write(bytearray("\x01import pico_test_time;pico_test_time.pico_test_time();\x04\x02", 'utf-8'))

        # Finds the request
        line = ser.readline()
        while(line.decode('utf-8')[3:-2] != "this is a request"):
            # print(line.decode('utf-8')[3:-2])
            line = ser.readline()
        # print(line)
        t1 = datetime.datetime.utcnow()

        # Record timestamp of sending response packet
        ser.write(bytearray("this is a response\r\n", 'utf-8'))
        t2 = datetime.datetime.utcnow()

        # Record timestamps from pico
        picoStamps = ser.readline()

        # Prints timestamps
        # print(f"t1: {t1}, t2: {t2}")
        # print(picoStamps)

        ser.close()

        # Gets milliseconds from timestamps
        picoSplit = str(picoStamps)[7:-6]
        picoLists = picoSplit.split("), t3: (")

        t0List = picoLists[0].split(", ")
        t3List = picoLists[1].split(", ")
        t0Tuple = tuple([int(x) for x in t0List])
        t3Tuple = tuple([int(x) for x in t3List])

        t0 = datetime.datetime(t1.year, t0Tuple[1], t0Tuple[2], t0Tuple[4], t0Tuple[5], t0Tuple[6], t0Tuple[7] * 1000)
        t3 = datetime.datetime(t2.year, t3Tuple[1], t3Tuple[2], t3Tuple[4], t3Tuple[5], t3Tuple[6], t3Tuple[7] * 1000)

        # Get the offset
        firstHalf = t1 - t0
        secondHalf = t2 - t3
        finalResult = (firstHalf + secondHalf)/2
        offsetAvg.append(finalResult.total_seconds())
        # print(finalResult.total_seconds())

        # Keep track of trials
        if x % STATUS == 0:
            print(x)

    toReturn = sum(offsetAvg)/TRIALS
    print("Average offset in seconds: " + str(toReturn))
    print("Standard Deviation: " + str(numpy.std(offsetAvg)))

server_test_time()