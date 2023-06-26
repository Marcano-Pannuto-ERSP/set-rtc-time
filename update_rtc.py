from constant_time import constant_time

PORT = '/dev/ttyACM5'

def update_rtc():
    # Find timestamp for receiving request packet
    ser = serial.Serial(PORT) # open serial port
    ser.baudrate = 115200

    ser.reset_input_buffer()
    ser.reset_output_buffer()

    # Run initialize_rtc()
    ser.write(bytearray("\x01import initialize_rtc;initialize_rtc.initialize_rtc();\x04\x02", 'utf-8'))

    constant_time()
    print(ser.readline())