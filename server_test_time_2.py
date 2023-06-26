import datetime
import serial
import time
import numpy

"""
test for seeing if we can measure accuracy of time (the client is automaton)
"""

PORT = '/dev/ttyACM5'
TRIALS = 10000
STATUS = 1000

def server_test_time_2():
    offsetAvg = []
    for x in range(TRIALS):
        # Find timestamp for receiving request packet
        ser = serial.Serial(PORT) # open serial port
        ser.baudrate = 115200

        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # Run pico script on automaton
        ser.write(bytearray("\x01import pico_test_time_2;pico_test_time_2.pico_test_time_2();\x04\x02", 'utf-8'))

        # Request a time from the server
        ser.write(bytearray("this is a request\n", 'utf-8'))
        t0 = datetime.datetime.utcnow()

        # Find timestamp for receiving a response
        line = ser.readline()
        while(line.decode('utf-8')[0:-2] != "this is a response"):
            # print(line.decode('utf-8')[0:-2])
            line = ser.readline()
        # print("response")
        # print(line)
        t3 = datetime.datetime.utcnow()

        # Records timestamps from pico
        picoStamps = ser.readline()

        # Prints timestamps
        # print(f"t0: {t0}, t3: {t3}")
        # print(picoStamps)

        ser.close()

        # Gets milliseconds from timestamps
        picoSplit = str(picoStamps)[7:-6]
        picoLists = picoSplit.split("), t2: (")

        t1List = picoLists[0].split(", ")
        t2List = picoLists[1].split(", ")
        t1Tuple = tuple([int(x) for x in t1List])
        t2Tuple = tuple([int(x) for x in t2List])

        t1 = datetime.datetime(t0.year, t1Tuple[1], t1Tuple[2], t1Tuple[4], t1Tuple[5], t1Tuple[6], t1Tuple[7] * 1000)
        t2 = datetime.datetime(t3.year, t2Tuple[1], t2Tuple[2], t2Tuple[4], t2Tuple[5], t2Tuple[6], t2Tuple[7] * 1000)

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

server_test_time_2()