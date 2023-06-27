import sys
from rtc import *
from machine import Pin

"""
Runs on the RPi pico (which is connected to RTC)

Initializes the RTC by:
- enabling trickle charging for backup battery
- disabling unused pins
- changing settings to specify disabling SPI in absence of VCC
- enabling/disabling automatic RC/XT oscillator switching according to user input
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
    

def initialize_rtc(f, a):
    MudwattRTC = RTC()

    # enable trickle charging for the backup battery
    MudwattRTC.enable_trickle()

    # disable unused pins
    disable_pins(MudwattRTC)

    # Enable or disable automatic switch over from the crystal to the internal RC clock
    # Default FOS to 1, AOS to 0, and change them if user used the flags
    osCtrl = MudwattRTC.read_register(0x1C)
    FOSmask = 0b00001000
    if f == True:
        # set FOS to 0
        FOSresult = osCtrl & ~FOSmask
    else:
        # set FOS to 1 (default)
        FOSresult = osCtrl | FOSmask
    MudwattRTC.write_register(0x1C, FOSresult)
    
    AOSmask = 0b00010000
    if a == True:
        # set AOS to 1
        AOSresult = osCtrl | AOSmask
    else:
        # set AOS to 0 (default)
        AOSresult = osCtrl & ~AOSmask
    MudwattRTC.write_register(0x1C, AOSresult)