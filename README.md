![GitHub](https://img.shields.io/github/license/Marcano-Pannuto-ERSP/set-rtc-time)

# Setting RTC to UTC time

## Description
We will program the RTC using a Raspberry Pi Pico that runs with Micropython.

Sets the time of the RTC with accuracy of 0.02 seconds (accuracy can be changed with --range command line argument)

Initializes the RTC by:
- enabling trickle charging for backup battery
- disabling unused pins
- changing settings to specify disabling SPI in absence of VCC
- enabling/disabling automatic RC/XT oscillator switching according to user input
- configuring the RTC alarm
- outputting alarm interrupts to pin FOUT/nIRQ
- writing to register 1 bit 7 to signal that this program initialized the RTC

## Setup
The following files are written in Micropython and need to be uploaded to the RPi Pico:
* `pico_test_time.py`
* `set_time.py`
* `initialize_rtc.py`
* `rtc.py`

To communicate with the RTC, use [adafruit-ampy 1.1.0](https://pypi.org/project/adafruit-ampy/). This is the command to upload files to the Pico: `ampy --port [PORT] put [FILENAME]`

Pin connections:

The RTC's CS pin needs to be connected to the RPI's GP10 pin.

* RTC - Pico
* CS - GP10
* SCK - GP2
* SDO - GP4
* SDI - GP3


## How to run

usage: update_rtc.py [-h] --port PORT [--range RANGE] [--trials TRIALS] [-f] [-a] [--pulse {0,1,2,3}] [-da] [-dt] [--timer TIMER]

Initialize the RTC and sets the time

options:
  -h, --help         show this help message and exit
  --port PORT        sets the port the Raspberry Pi Pico is plugged into
  --range RANGE      sets the new accuracy range to RANGE
  --trials TRIALS    sets the new number of trials to get the average offset to TRIALS
  -f                 set FOS to 0 (no automatic switching when an oscillator failure is detected)
  -a                 set AOS to 1 (automatically switches to RC oscillator when the system is powered from the battery)
  --pulse {0,1,2,3}  sets the length of pulse: 1 means 1/8192 seconds for XT and 1/64 sec for RC; 2 means 1/64 s for both; 3 means 1/4 s for both;
                     0 means level (static)
  -da                disable the RTC alarm
  -dt                disable trickle charging
  --timer TIMER      set repeating timer to TIMER seconds

If no optional arguments are entered, then the program will run 100 trials to determine the average offset, with time accuracy within 0.02 seconds,
FOS is set to 1 (automatic switching when an oscillator failure is detected), AOS is set to 0 (will use XT oscillator when the system is powered
from the battery), the alarm is enabled (and initialize alarm to go off once a second if 0 (default value) is in hundredths alarm register), and
the alarm pulse is 1/8192 seconds for XT or 1/64 sec for RC