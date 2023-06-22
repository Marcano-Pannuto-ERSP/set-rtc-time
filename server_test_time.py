import datetime
import serial

"""
test for seeing if we can measure accuracy of time (server side)
"""

PORT = '/dev/ttyACM2'

def server_test_time():
    # Find timestamp for receiving request packet
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 115200

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # Call pico_test_time function
    ser.write(bytearray("\x01import pico_test_time;pico_test_time.pico_test_time();\x04\x02", 'utf-8'))

    line = ser.readline()
    while(line.decode('utf-8')[3:-2] != "this is a request"):
        print(line.decode('utf-8')[3:-2])
        line = ser.readline()
    print(line)
    t1 = datetime.datetime.now()

    # Record timestamp of sending response packet
    # time.sleep(1)
    ser.write(bytearray("this is a response\r\n", 'utf-8'))
    t2 = datetime.datetime.now()

    print(f"t1: {t1}, t2: {t2}")

    print(ser.readline())

    ser.close()

server_test_time()