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
Runs on the RPi pico (which is connected to RTC)

Initializes the RTC by:
- enabling trickle charging for backup battery
- disabling unused pins
- changing settings to specify disabling SPI in absence of VCC
- enabling/disabling automatic RC/XT oscillator switching according to user input
- configuring the RTC alarm
- writing to register 1 bit 7 to signal that this program initialized the RTC
"""

from machine import Pin
from rtc import *


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

    # get access to BATMODE I/O register
    MudwattRTC.write_register(0x1F, 0x9D)

    # disable SPI when we lose Vcc
    # set the BATMODE I/O register's 7th bit to 0
    # which means that the RTC will disable I/O interface in absence of vcc
    IOBM = MudwattRTC.read_register(0x27)
    IOBMmask = 0b10000000
    IOBMresult = IOBM & ~IOBMmask
    MudwattRTC.write_register(0x27, IOBMresult)


def initialize_rtc(f, a, pulse, d):
    MudwattRTC = RTC()

    # enable trickle charging for the backup battery
    MudwattRTC.enable_trickle()

    # disable unused pins
    disable_pins(MudwattRTC)

    # get access to oscillator control register
    MudwattRTC.write_register(0x1F, 0xA1)

    # Enable or disable automatic switch over from the crystal to the internal RC clock
    # Default FOS to 1, AOS to 0, and change them if user used the flags
    osCtrl = MudwattRTC.read_register(0x1C)
    FOSmask = 0b00001000
    if f:
        # set FOS to 0
        FOSresult = osCtrl & ~FOSmask
    else:
        # set FOS to 1 (default)
        FOSresult = osCtrl | FOSmask
    MudwattRTC.write_register(0x1C, FOSresult)

    osCtrl = MudwattRTC.read_register(0x1C)

    # get access to oscillator control register
    MudwattRTC.write_register(0x1F, 0xA1)

    AOSmask = 0b00010000
    if a:
        # set AOS to 1
        AOSresult = osCtrl | AOSmask
    else:
        # set AOS to 0 (default)
        AOSresult = osCtrl & ~AOSmask
    MudwattRTC.write_register(0x1C, AOSresult)

    # Configure AIRQ (alarm) interrupt
    # IM (level/pulse) AIE (enables interrupt) 0x12 intmask
    alarm = MudwattRTC.read_register(0x12)
    alarmMask = int(pulse) << 6
    if not d:
        alarmMask += 0b00000100
    alarmResult = alarm | alarmMask
    MudwattRTC.write_register(0x12, alarmResult)

    # Write to bit 7 of register 1 to signal that this program initialized the RTC
    sec = MudwattRTC.read_register(0x01)
    secMask = 0b10000000
    secResult = sec | secMask
    MudwattRTC.write_register(0x01, secResult)
