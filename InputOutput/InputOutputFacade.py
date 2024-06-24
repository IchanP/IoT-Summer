from InputOutput.MoistureHandler import MoistureHandler
from InputOutput.DHTHandler import DHTHandler
from InputOutput.LEDHandler import LEDHandler
from InputOutput.PhotoResistorHandler import PhotoResistorHandler
import ujson

class InputOutputFacade:
    
    def __init__(self):
        self.moistureSensor = MoistureHandler(26)
        self.dhtSensor = DHTHandler(14)
        self.led = LEDHandler(16)
        self.lightSensor = PhotoResistorHandler(27)

    def get_sensor_data(self):
        moistureReading = self.moistureSensor.read_percentage_moisture()
        tempReading, humReading = self.dhtSensor.read()
        lightReading = self.lightSensor.read_percentage_light()
        return moistureReading, tempReading, humReading, lightReading
    
    def subscription_callback(self, topic, msg):
        print(msg)
        parsedMsg = ujson.loads(msg)
        if parsedMsg['msg'] == 'ON':
            print('Turning on LED')
            self.led.turn_on()
        elif parsedMsg['msg'] == 'OFF':
            print('Turning off LED')
            self.led.turn_off()
        else:
            print('Invalid message received:', msg)


    
