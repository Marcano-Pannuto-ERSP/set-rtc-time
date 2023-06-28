# Setting RTC to UTC time

## Description
We will program the RTC using a Raspberry Pi Pico that runs with Micropython.

Sets the time of the RTC with accuracy of 0.02 seconds (accuracy can be changed with --range command line argument)

Initializes the RTC by:
- enabling trickle charging for backup battery
- disabling unused pins
- changing settings to specify disabling SPI in absence of VCC
- enabling/disabling automatic RC/XT oscillator switching according to user input
- writing to register 1 bit 7 to signal that this program initialized the RTC

## Setup
The following files are written in Micropython and need to be uploaded to the RPi Pico:
* `pico_test_time.py`
* `set_time.py`
* `initialize_rtc.py`
* `rtc.py`

To communicate with the RTC, use [adafruit-ampy 1.1.0](https://pypi.org/project/adafruit-ampy/). This is the command to upload files to the Pico: `ampy --port [PORT] put [FILENAME]`


## How to run
Run with:

`python update_rtc.py [-h] --port PORT [--range RANGE] [--trials TRIALS] [-f] [-a]`

* `--port PORT` sets the port the Raspberry Pi Pico is plugged into
* `--range RANGE` sets the new accuracy range to RANGE (in hundredths of seconds). Default is 2
* `--trials TRIALS` sets the new number of trials to get the average offset to TRIALS. Default is 100
* `-f` means set FOS to 0 (no automatic switching when an oscillator failure is detected)
* `-a` means set AOS to 1 (automatically switches to RC oscillator when the system is powered from the battery)

If no optional arguments are entered, then the program will run 100 trials to determine the average offset, with time accuracy within 0.02 seconds, 
FOS is set to 1 (automatic switching when an oscillator failure is detected),
and AOS is set to 0 (will use XT oscillator when the system is powered from the battery)
