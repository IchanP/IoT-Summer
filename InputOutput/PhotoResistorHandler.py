import machine
from machine import ADC, Pin

class PhotoResistorHandler:
    def __init__(self, pin):
        self.sensor = ADC(Pin(pin))
        
    def read_percentage_light(self):
        # Lower reading = brighter
        raw = self.sensor.read_u16()
         # Pulled from tutorial (https://github.com/iot-lnu/pico-w/blob/main/sensor-examples/P23_LDR_Photo_Resistor/main.py)
         # Normalizes the reading to a percentage since the raw value can be between 0 and 65535
        percentage = round(raw / 65535 * 100, 2)
        return 100 - percentage # Invert the reading since lower value = brighter