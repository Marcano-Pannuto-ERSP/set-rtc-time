# Setting RTC to UTC time

## How to set RTC time
We will program the RTC using a Raspberry Pi Pico that runs with Micropython.
In order to run Micropython on the Raspberry Pi Pico, we have to install `adafruit-ampy 1.1.0`. Refer to this [link](https://pypi.org/project/adafruit-ampy/) to see installation instructions.

1. Run `python constant_time.py` on the server
2. While constant_time.py is running, run `ampy --port [PORT] run main.py`

