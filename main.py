from time import sleep
from scripts import reset, get_sensor_data, json_preparation, handle_subscription
from MTTQManager import MTTQManager
from DHTHandler import DHTHandler
from MoistureHandler import MoistureHandler
from config import DEVICE_ID, MQTT_SERVER, DEVICE_ID

# Connect to the MQTT server
manager = MTTQManager(DEVICE_ID, MQTT_SERVER, 1883)
manager.enable_subcsription(handle_subscription)

# Connect to the sensors
dht11 = DHTHandler(16)
moistureSensor = MoistureHandler(XXXXXXXXXX) # TODO

if __name__ == '__main__':
    while True:
        # Read and publish the sensor data
        try: 
            temp, hum = dht11.read_sensor()
            
            # Split the feeds and publish them, helps the Adia dashboard
            json_temp = json_preparation('value', temp)
            json_hum = json_preparation('value', hum)
            manager.publish(json_temp)
            manager.publish(json_hum)

            manager.check_msg()
            sleep(5)
        except OSError as e:
            print(e)
            reset()
        except Exception as e:
            print('An error occurred:', e) # Silently ignore
 