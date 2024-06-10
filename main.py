import machine
from time import sleep
import dht
from scripts import reset, get_sensor_data, json_preparation, handle_subscription
from MTTQManager import MTTQManager
from config import DEVICE_ID, MQTT_SERVER, DEVICE_ID, ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY, ADAFRUIT_IO_SUBSCRIBE, ADAFRUIT_IO_HUM, ADAFRUIT_IO_TEMP

manager = MTTQManager(DEVICE_ID, MQTT_SERVER, 1883, ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
manager.enable_subcsription(ADAFRUIT_IO_SUBSCRIBE, handle_subscription)
sensor = dht.DHT11(machine.Pin(16))


if __name__ == '__main__':
    while True:
        try: 
            temp, hum = get_sensor_data(sensor)
            # Split the feeds and publish them, helps the dashboard
            json_temp = json_preparation('value', temp)
            json_hum = json_preparation('value', hum)
            manager.publish(ADAFRUIT_IO_TEMP, json_temp)
            manager.publish(ADAFRUIT_IO_HUM, json_hum)
            manager.check_msg()
            sleep(5)
        except OSError as e:
            print(e)
            reset()
        except Exception as e:
            print('An error occurred:', e) # Silently ignore
 