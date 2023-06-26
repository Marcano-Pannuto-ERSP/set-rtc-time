import datetime
import serial
import time

"""
test for seeing if we can measure accuracy of time (the client is automaton)
"""

PORT = '/dev/ttyACM5'

def server_test_time_2():
    # Find timestamp for receiving request packet
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 115200

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    ser.write(bytearray("\x01import pico_test_time_2;pico_test_time_2.pico_test_time_2();\x04\x02", 'utf-8'))
    time.sleep(1)

    # Request a time from the server
    ser.write(bytearray("this is a request\n", 'utf-8'))
    t0 = datetime.datetime.utcnow()

    # Find timestamp for receiving a response
    line = ser.readline()
    while(line.decode('utf-8')[0:-2] != "this is a response"):
        print(line.decode('utf-8')[0:-2])
        line = ser.readline()
    print("response")
    print(line)
    t3 = datetime.datetime.utcnow()

    print(f"t0: {t0}, t3: {t3}")
    print(ser.readline())

    ser.close()

server_test_time_2()