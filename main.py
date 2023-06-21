import time
from rtc import *
import sys
from machine import Pin

# runs on the pico

if __name__ == "__main__":
    MudwattRTC = RTC()

    # read a line from serial
    line = sys.stdin.readline()
    print(line)
    MudwattRTC.set_time(line)

    # enable trickle charging for the backup battery
    MudwattRTC.enable_trickle()

    # HAVE TO CHANGE TO USING REGISTERS
    # disable unused pins (i.e., all pins except SPI and VBAT)
    
    # disable EXBM
    EXBM = MudwattRTC.read_register(0x30)
    EXBMmask = 0b01000000
    EXBMmasked = EXBM & EXBMmask
    EXBMread = EXBMmasked >> 6
    if EXBMread == 1:
        EXBMwritemask = 0b01000000
        EXBMresult = EXBM ^ EXBMwritemask
        MudwattRTC.write_register(0x30, EXBMresult)

    # disable SPI when we lose Vcc
    # set the BATMODE I/O register's 7th bit to 0
    # which means that the RTC will disable I/O interface in absence of vcc
    IOBM = MudwattRTC.read_register(0x27)
    IOBMmask = 0b00000000
    IOBMresult = IOBM & IOBMmask
    MudwattRTC.write_register(0x27, IOBMresult)