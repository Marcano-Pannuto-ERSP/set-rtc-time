import time
from machine import Pin, SPI

class RTC:
    def __init__(self):
        self.init()

    def init(self):
        self.spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4), baudrate=2000000, phase=0)
        self.cs = Pin(5, Pin.OUT, value=1)

    def deinit(self):
        self.spi.deinit()
        self.cs.init(Pin.IN)

    def enable_rc(self):
        tmp = self.read_register(0x1C)
        self.write_register(0x1F, 0xA1)
        self.write_register(0x1C, tmp | 0x80)
        self.write_register(0x1F, 0x00)

    def read_register(self, addr):
        self.cs.value(0)
        self.spi.write(bytes([addr]))
        data = self.spi.read(1)[0]
        self.cs.value(1)
        return data

    def write_register(self, addr, data):
        self.cs.value(0)
        self.spi.write(bytes([0x80 | addr, data]))
        self.cs.value(1)

    def read_bulk(self, addr_start, size):
        self.cs.value(0)
        self.spi.write(bytes([addr_start]))
        data = self.spi.read(size)
        self.cs.value(1)
        return data

    def write_bulk(self, addr_start, data):
        self.cs.value(0)
        self.spi.write(bytes([0x80 | addr_start]) + data)
        self.cs.value(1)

    def enable_trickle(self):
        self.write_register(0x1F, 0x9D)
        # Enable trickle with 3k Ohm resistor, and schottky diode
        self.write_register(0x20, 0xA5)
        self.write_register(0x1F, 0x00)

    def __set_time_calendar(self, calendar):
        tmp_time = bytearray(self.read_bulk(0, 8))

        def to_bcd(value):
            result = 0
            decade = 0
            while value != 0:
                digit = value % 10
                value //= 10
                result |= digit << (4 * decade)
                decade += 1
            return result

        # Hundredths
        tmp_time[0] = to_bcd(calendar[7])
        # Seconds
        tmp_time[1] &= 0x80
        tmp_time[1] |= to_bcd(calendar[6])
        # Minutes
        tmp_time[2] &= 0x80
        tmp_time[2] |= to_bcd(calendar[5])
        # Hours
        tmp_time[3] &= 0xC0
        tmp_time[3] |= to_bcd(calendar[4])
        # Day of month
        tmp_time[4] &= 0xC0
        tmp_time[4] |= to_bcd(calendar[2])
        # Month
        tmp_time[5] &= 0xE0
        tmp_time[5] |= to_bcd(calendar[1])
        # Year
        tmp_time[6] = to_bcd(calendar[0])
        # Day of week
        tmp_time[7] &= 0xF8
        tmp_time[7] |= to_bcd(calendar[3])

        self.write_bulk(0x0, tmp_time)

    def __set_time_seconds(self, time_):
        calendar = time.gmtime(time_[0])
        rtc_calendar = (
            calendar[0] % 100,
            calendar[1],
            calendar[2],
            calendar[6],
            calendar[3],
            calendar[4],
            calendar[5],
            time_[1]
        )
        self.__set_time_calendar(rtc_calendar)

    def set_time(self, time):
        if len(time) == 2:
            self.__set_time_seconds(time)
        elif len(time) == 8:
            self.__set_time_calendar(time)
        else:
            raise TypeError('unknown argument')

    def get_time_seconds(self):
        rtc_calendar = self.get_time()
        calendar = (
            rtc_calendar[0] + 2000,
            rtc_calendar[1],
            rtc_calendar[2],
            rtc_calendar[4],
            rtc_calendar[5],
            rtc_calendar[6],
            rtc_calendar[3],
            0
        )
        return (time.mktime(calendar), rtc_calendar[7])

    def get_time(self):
        tmp_time = bytearray(self.read_bulk(0, 8))

        def from_bcd(value):
            return (((value >> 4) & 0xF) * 10) + (value & 0xF)

        hundredths = from_bcd(tmp_time[0])
        seconds = from_bcd(tmp_time[1] & 0x7F)
        minutes = from_bcd(tmp_time[2] & 0x7F)
        hours = from_bcd(tmp_time[3] & 0x3F)
        date = from_bcd(tmp_time[4] & 0x3F)
        month = from_bcd(tmp_time[5] & 0x3F)
        year = from_bcd(tmp_time[6])
        weekday = from_bcd(tmp_time[7] & 0x07)

        return (year, month, date, weekday, hours, minutes, seconds, hundredths)

    """
    Set the alarm registers to the calendar tuple parameter
    calendar = (month, date, weekday, hours, minutes, seconds, hundredths)
    No year value because there is no alarm year register
    """
    def set_alarm_calendar(self, calendar):
        tmp_time = bytearray(self.read_bulk(8, 7))

        def to_bcd(value):
            result = 0
            decade = 0
            while value != 0:
                digit = value % 10
                value //= 10
                result |= digit << (4 * decade)
                decade += 1
            return result

        # Hundredths
        tmp_time[0] = to_bcd(calendar[6])
        # Seconds
        tmp_time[1] &= 0x80
        tmp_time[1] |= to_bcd(calendar[5])
        # Minutes
        tmp_time[2] &= 0x80
        tmp_time[2] |= to_bcd(calendar[4])
        # Hours
        tmp_time[3] &= 0xC0
        tmp_time[3] |= to_bcd(calendar[3])
        # Day of month
        tmp_time[4] &= 0xC0
        tmp_time[4] |= to_bcd(calendar[1])
        # Month
        tmp_time[5] &= 0xE0
        tmp_time[5] |= to_bcd(calendar[0])
        # Day of week
        tmp_time[6] &= 0xF8
        tmp_time[6] |= to_bcd(calendar[2])

        self.write_bulk(0x8, tmp_time)

    """
    Get the time stored in the alarm registers
    returns (month, date, weekday, hours, minutes, seconds, hundredths)
    """
    def get_alarm_time(self):
        tmp_time = bytearray(self.read_bulk(8, 7))

        def from_bcd(value):
            return (((value >> 4) & 0xF) * 10) + (value & 0xF)

        hundredths = from_bcd(tmp_time[0])
        seconds = from_bcd(tmp_time[1] & 0x7F)
        minutes = from_bcd(tmp_time[2] & 0x7F)
        hours = from_bcd(tmp_time[3] & 0x3F)
        date = from_bcd(tmp_time[4] & 0x3F)
        month = from_bcd(tmp_time[5] & 0x3F)
        weekday = from_bcd(tmp_time[6] & 0x07)

        return (month, date, weekday, hours, minutes, seconds, hundredths)