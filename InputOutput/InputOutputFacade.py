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
        tempReading, humReading = self.dhtSensor.read()

        return self._format_as_json(moistureReading, tempReading, humReading)
    
    def _enable_led(self, moistureReading):
        if moistureReading < 30:
            self.led.turn_on()
        elif self.led.is_on() and moistureReading > 30:
            self.led.turn_off()

    def _format_as_json(self, moisture, temp, hum): 
        data = {
            "moisture": moisture,
            "temperature": temp,
            "humidity": hum
        }
        return data
    
