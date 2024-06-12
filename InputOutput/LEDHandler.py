import machine
from machine import Pin

class LEDHandler:
    def __init__(self, pin):
        self.led = machine.Pin(pin, Pin.OUT)