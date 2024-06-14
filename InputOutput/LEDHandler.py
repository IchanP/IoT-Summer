import machine
from machine import Pin

class LEDHandler:
    def __init__(self, pin):
        self.led = machine.Pin(pin, Pin.OUT)

    # TODO change this to check the current time and if it's in operable hours and turned on return true.    
    def is_on(self):
        return self.led.value() == 1

    def turn_on(self):
        self.led.value(1)
    
    def turn_off(self):
        self.led.value(0)