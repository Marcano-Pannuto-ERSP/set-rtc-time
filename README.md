![GitHub](https://img.shields.io/github/license/Marcano-Pannuto-ERSP/set-rtc-time)

# Initializing AM1815

## Description
We will program the RTC using a Raspberry Pi Pico that runs with Micropython.

Sets the time of the RTC with accuracy of 0.02 seconds (accuracy can be changed with --range command line argument)

Initializes the RTC by:
- enabling/disabling trickle charging for backup battery
- disabling unused pins
- changing settings to specify disabling SPI in absence of VCC
- enabling/disabling automatic RC/XT oscillator switching according to user input
- configuring the RTC alarm
- configuring the timer to repeat at interval specified by user
- outputting alarm interrupts to pin FOUT/nIRQ
- outputting timer interrupts to pin PSW/nIRQ2
- writing to register 1 bit 7 to signal that this program initialized the RTC

## Setup
The following files are written in Micropython and need to be uploaded to the RPi Pico:
* `pico_test_time.py`
* `set_time.py`
* `initialize_rtc.py`
* `rtc.py`

To communicate with the RTC, use [adafruit-ampy 1.1.0](https://pypi.org/project/adafruit-ampy/). This is the command to upload files to the Pico: `ampy --port PORT put FILENAME`

Pin connections between RTC and RPi Pico:

* RTC - Pico
* CS - GP10
* SCK - GP2
* SDO - GP4
* SDI - GP3

Note that the FOUT and PSW pins on the RTC are open drain, so they need to be connected to a pull up resistor.


## How to run

usage: `update_rtc.py [-h] --port PORT [--range RANGE] [--trials TRIALS] [-f] [-a] [--pulse {0,1,2,3}] [-da] [-dt] [--timer TIMER]`

options:
*  `-h, --help`         show this help message and exit
*  `--port PORT`        set the port the Raspberry Pi Pico is plugged into
*  `--range RANGE`      set the new accuracy range to RANGE
*  `--trials TRIALS`    set the new number of trials to get the average offset to TRIALS
*  `-f`                 set FOS to 0 (no automatic switching when an oscillator failure is detected)
*  `-a`                 set AOS to 1 (automatically switches to RC oscillator when the system is powered from the battery)
*  `--pulse {0,1,2,3}`  sets the length of pulse: 1 means 1/8192 seconds for XT and 1/64 sec for RC; 2 means 1/64 s for both; 3 means 1/4 s for both;
                        0 means level (static)
*  `-da`                disable the RTC alarm
*  `-dt`                disable trickle charging
*  `--timer TIMER`      set repeating timer to TIMER seconds. Maximum value is 15360
*  `--repeat REPEAT`    sets the repeat function for the alarm: 1 means once per year, 2 means once per month, 3 means once per week, 4 means once per day,
                        5 means once per hour, 6 means once per minute, 7 means once per second'

defaults (if no optional arguments are entered):
* the program will run 100 trials to determine the average offset
* time accuracy is within 0.02 seconds
* trickle charging is enabled
* FOS is set to 1 (automatic switching when an oscillator failure is detected)
* AOS is set to 0 (will use XT oscillator when the system is powered from the battery)
* the alarm is enabled (and initialize alarm to go off once a second if 0 (default value) is in hundredths alarm register)
* the alarm pulse is 1/8192 seconds for XT or 1/64 sec for RC
* the timer is disabled
* the alarm repeats every second