from machine import Pin, SPI
​
class RTC:
    def __init__(self):
        self.init()
​
    def init(self):
        self.spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4), baudrate=2000000, phase=0)
        self.cs = Pin(5, Pin.OUT, value=1)
​
    def deinit(self):
        self.spi.deinit()
        self.cs.init(Pin.IN)
​
    def enable_rc(self):
        tmp = self.read_register(0x1C)
        self.write_register(0x1F, 0xA1)
        self.write_register(0x1C, tmp | 0x80)
        self.write_register(0x1F, 0x00)
​
    def read_register(self, addr):
        self.cs.value(0)
        self.spi.write(bytes([addr]))
        data = self.spi.read(1)[0]
        self.cs.value(1)
        return data
​
    def write_register(self, addr, data):
        self.cs.value(0)
        self.spi.write(bytes([0x80 | addr, data]))
        self.cs.value(1)
​
    def read_bulk(self, addr_start, size):
        self.cs.value(0)
        self.spi.write(bytes([addr_start]))
        data = self.spi.read(size)
        self.cs.value(1)
        return data
​
    def write_bulk(self, addr_start, data):
        self.cs.value(0)
        self.spi.write(bytes([0x80 | addr_start]) + data)
        self.cs.value(1)
​
    def enable_trickle(self):
        self.write_register(0x1F, 0x9D)
        # Enable trickle with 3k Ohm resistor, and schottky diode
        self.write_register(0x20, 0xA5)
        self.write_register(0x1F, 0x00)
​
    def set_time(self, time):
        tmp_time = bytearray(self.read_bulk(0, 8))
​
        def to_bcd(value):
            result = 0
            decade = 0
            while value != 0:
                digit = value % 10
                value //= 10
                result |= digit << (4 * decade)
                decade += 1
            return result
​
        # Hundredths
        tmp_time[0] = to_bcd(time[7])
        # Seconds
        tmp_time[1] &= 0x80
        tmp_time[1] |= to_bcd(time[6])
        # Minutes
        tmp_time[2] &= 0x80
        tmp_time[2] |= to_bcd(time[5])
        # Hours
        tmp_time[3] &= 0xC0
        tmp_time[3] |= to_bcd(time[4])
        # Day of month
        tmp_time[4] &= 0xC0
        tmp_time[4] |= to_bcd(time[2])
        # Month
        tmp_time[5] &= 0xE0
        tmp_time[5] |= to_bcd(time[1])
        # Year
        tmp_time[6] = to_bcd(time[0])
        # Day of week
        tmp_time[7] &= 0xF8
        tmp_time[7] |= to_bcd(time[3])
​
        self.write_bulk(0x0, tmp_time)
​
    def get_time(self):
        tmp_time = bytearray(self.read_bulk(0, 8))
​
        def from_bcd(value):
            return (((value >> 4) & 0xF) * 10) + (value & 0xF)
​
        hundredths = from_bcd(tmp_time[0])
        seconds = from_bcd(tmp_time[1] & 0x7F)
        minutes = from_bcd(tmp_time[2] & 0x7F)
        hours = from_bcd(tmp_time[3] & 0x3F)
        date = from_bcd(tmp_time[4] & 0x3F)
        month = from_bcd(tmp_time[5] & 0x3F)
        year = from_bcd(tmp_time[6])
        weekday = from_bcd(tmp_time[7] & 0x07)
​
        return (year, month, date, weekday, hours, minutes, seconds, hundredths)