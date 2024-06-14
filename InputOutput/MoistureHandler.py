import machine
from machine import ADC, Pin

class MoistureHandler:

    MAX_DRY = 43500 # Highest value measured when in dry air
    MAX_WET = 14000 # Lowest value measured when submerged in water

    def __init__(self, pin):
        self.sensor = ADC(Pin(pin))

    
    def read_percentage_moisture(self):
        adc_value = self._read_raw()
        return self._calculate_percent(adc_value)
        
    def _read_raw(self):
        return self.sensor.read_u16()
    
    def _calculate_percent(self, raw_value):
        if raw_value > self.MAX_DRY:
            return 100
        elif raw_value < self.MAX_WET:
            return 0
        else:
            adjusted_max = self.MAX_DRY - self.MAX_WET
            adjusted_reading = raw_value - self.MAX_WET
            return round((adjusted_reading) / (adjusted_max) * 100, 2)
