import dht
import machine

class DHTHandler:
    def __init__ (self, PIN):
        self.sensor = dht.DHT11(machine.Pin(PIN))
    
    # Returns the temperature and humidity from the sensor in the [temp, hum] format
    def read(self):
        self.sensor.measure()
        temp = self.sensor.temperature()
        hum = self.sensor.humidity()
        return temp, hum

