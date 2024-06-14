from InputOutput.MoistureHandler import MoistureHandler
from InputOutput.DHTHandler import DHTHandler
from InputOutput.LEDHandler import LEDHandler

class InputOutputFacade:
    
    def __init__(self):
        self.moistureSensor = MoistureHandler(26)
       # self.dhtSensor = DHTHandler()
       # self.led = LEDHandler()

    def read_all_sensors(self):
        moistureReading = self.moistureSensor.read_percentage_moisture()
       # temp, hum = self.dhtSensor.read()
        # TODO - convert to JSON?
        return moistureReading