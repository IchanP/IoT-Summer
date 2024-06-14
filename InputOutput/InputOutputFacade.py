from InputOutput.MoistureHandler import MoistureHandler
from InputOutput.DHTHandler import DHTHandler
from InputOutput.LEDHandler import LEDHandler

class InputOutputFacade:
    
    def __init__(self):
        self.moistureSensor = MoistureHandler(26)
        self.dhtSensor = DHTHandler(14)
        self.led = LEDHandler(16)

    def read_all_sensors(self):
        moistureReading = self.moistureSensor.read_percentage_moisture()
        self._enable_led(moistureReading)
        temp, hum = self.dhtSensor.read()
        print("temp: ", temp, "hum: ", hum)
        return moistureReading, temp, hum
    
    def _enable_led(self, moistureReading):
        if moistureReading < 30:
            self.led.turn_on()
        elif self.led.is_on() and moistureReading > 30:
            self.led.turn_off()
