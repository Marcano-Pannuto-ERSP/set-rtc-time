# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText 2023 Kristin Ebuengan
# SPDX-FileCopyrightText 2023 Melody Gill
# SPDX-FileCopyrightText 2023 Gabriel Marcano

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

# Set up registers that control the alarm
def configure_alarm(MudwattRTC, pulse, d, repeat):
    # Configure AIRQ (alarm) interrupt
    # IM (level/pulse) AIE (enables interrupt) 0x12 intmask
    alarm = MudwattRTC.read_register(0x12)
    alarm = alarm & ~(0b01100100)
    alarmMask = int(pulse) << 5
    if not d:
        alarmMask += 0b00000100
    alarmResult = alarm | alarmMask
    MudwattRTC.write_register(0x12, alarmResult)

    # Set Control2 register bits so that FOUT/nIRQ pin outputs nAIRQ
    out = MudwattRTC.read_register(0x11)
    outMask = 0b00000011
    outResult = out | outMask
    MudwattRTC.write_register(0x11, outResult)

    # Set RPT bits in Countdown Timer Control register to control how often the alarm interrupt repeats.
    timerControl = MudwattRTC.read_register(0x18)
    timerControl = timerControl & ~(0b00011100)
    timerMask = int(repeat) << 2
    timerResult = timerControl | timerMask
    MudwattRTC.write_register(0x18, timerResult)

def configure_countdown(MudwattRTC, timer):
    # Configure TIRQ (countdown timer) interrupt
    # TIE (enables interrupt) 0x12 intmask
    countdown = MudwattRTC.read_register(0x12)
    countdownMask = 0b00001000
    countdownResult = countdown | countdownMask
    MudwattRTC.write_register(0x12, countdownResult)

    # TE (enables countdown timer)
    # Sets the Countdown Timer Frequency and
    # the Timer Initial Value
    countdowntimer = MudwattRTC.read_register(0x18)
    # clear TE first
    MudwattRTC.write_register(0x18, countdowntimer & ~0b10000000)
    RPT = countdowntimer & 0b00011100
    timerResult = 0b10100000 + RPT
    timerinitial = 0
    if timer <= 0.0625:
        timerResult += 0b00
        timerinitial = int((timer * 4096) - 1)
    elif timer <= 4:
        timerResult += 0b01
        timerinitial = int((timer * 64) - 1)
    elif timer <= 256:
        timerResult += 0b10
        timerinitial = int(timer - 1)
    else:
        timerResult += 0b11
        timerinitial = int((timer * (1/60)) - 1)
    MudwattRTC.write_register(0x19, timerinitial)
    MudwattRTC.write_register(0x1A, timerinitial)
    MudwattRTC.write_register(0x18, timerResult)

    # Set Control2 register bits so that PSW/nIRQ2 pin outputs nTIRQ
    out = MudwattRTC.read_register(0x11)
    outMask = 0b00010100
    outResult = out | outMask
    outMask = 0b00001000
    outResult = outResult & ~outMask
    MudwattRTC.write_register(0x11, outResult)

def initialize_rtc(f, a, pulse, da, dt, timer, repeat):
    MudwattRTC = RTC()

    # enable/disable trickle charging for the backup battery
    if not dt:
        MudwattRTC.enable_trickle()

    if dt:
        MudwattRTC.disable_trickle()

    # disable unused pins
    disable_pins(MudwattRTC)

    # get access to oscillator control register
    MudwattRTC.write_register(0x1F, 0xA1)

    # clear the OF bit so that a failure isn't detected on start up
    OF = MudwattRTC.read_register(0x1D)
    OFmask = 0b00000010
    OFresult = OF & ~OFmask
    MudwattRTC.write_register(0x1D, OFresult)

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

    # Configure alarm
    configure_alarm(MudwattRTC, pulse, da, repeat)

    # Configure countdown timer
    if timer != 0:
        configure_countdown(MudwattRTC, timer)
    else:
        countdowntimer = MudwattRTC.read_register(0x18)
        MudwattRTC.write_register(0x18, countdowntimer & ~0b10000000)

    # Write to bit 7 of register 1 to signal that this program initialized the RTC
    sec = MudwattRTC.read_register(0x01)
    secMask = 0b10000000
    secResult = sec | secMask
    MudwattRTC.write_register(0x01, secResult)
