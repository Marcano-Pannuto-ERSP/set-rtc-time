import sys
from rtc import *
from machine import Pin

"""
Runs on the RPi pico (which is connected to RTC)

Initializes the RTC by:
- synchronizing time on RTC to time on server
- enabling trickle charging for backup battery
- disabling unused pins
- changing settings to specify disabling SPI in absence of VCC
- enabling/disabling automatic RC/XT oscillator switching according to user input

Run with:
ampy -p <port> run main.py [-f] [-a]
-f means set FOS to 0 (no automatic switching when an oscillator failure is detected)
-a means set AOS to 1 (automatically switches to RC oscillator when the system is powered from the battery)

no flags means FOS is set to 1 (automatic switching when an oscillator failure is detected)
and AOS is set to 0 (will use XT oscillator when the system is powered from the battery)
"""

# disable unused pins (i.e., all pins except SPI and VBAT)
def disable_pins(MudwattRTC):
    # disable EXBM, WDBM, RSEN, O4EN, O3EN, O1EN
    register = MudwattRTC.read_register(0x30)
    mask = 0b11001111
    result = register & ~mask
    MudwattRTC.write_register(0x30, result)

    # disable O4BM
    O4BM = MudwattRTC.read_register(0x3F)
    O4BMmask = 0b10000000
    O4BMresult = O4BM & ~O4BMmask
    MudwattRTC.write_register(0x3F, O4BMresult)

    # disable SPI when we lose Vcc
    # set the BATMODE I/O register's 7th bit to 0
    # which means that the RTC will disable I/O interface in absence of vcc
    IOBM = MudwattRTC.read_register(0x27)
    IOBMmask = 0b10000000
    IOBMresult = IOBM & ~IOBMmask
    MudwattRTC.write_register(0x27, IOBMresult)
    

def initialize_rtc():
    MudwattRTC = RTC()

    # read a line from serial and set the RTC to that time
    line = sys.stdin.readline()

    # parse back into a tuple
    timeTuple = line[1:-2]  # remove parentheses
    splitList = timeTuple.split(", ")
    intTuple = tuple([int(x) for x in splitList])

    MudwattRTC.set_time(intTuple)
    # print(MudwattRTC.get_time())

    # enable trickle charging for the backup battery
    MudwattRTC.enable_trickle()

    # disable unused pins
    disable_pins(MudwattRTC)

    # Enable or disable automatic switch over from the crystal to the internal RC clock
    # Default FOS to 1, AOS to 0, and change them if user used the flags
    osCtrl = MudwattRTC.read_register(0x1C)
    FOSmask = 0b00001000
    if "-f" in sys.argv:
        # set FOS to 0
        FOSresult = osCtrl & ~FOSmask
    else:
        # set FOS to 1 (default)
        FOSresult = osCtrl | FOSmask
    MudwattRTC.write_register(0x1C, FOSresult)
    
    AOSmask = 0b00010000
    if "-a" in sys.argv:
        # set AOS to 1
        AOSresult = osCtrl | AOSmask
    else:
        # set AOS to 0 (default)
        AOSresult = osCtrl & ~AOSmask
    MudwattRTC.write_register(0x1C, AOSresult)

initialize_rtc()