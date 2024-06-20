from time import sleep
from scripts import reset, json_preparation, handle_subscription
from MQTTManager import MQTTManager
from config import DEVICE_ID, MQTT_SERVER, DEVICE_ID
from InputOutput.InputOutputFacade import InputOutputFacade

# Connect to the MQTT server
manager = MQTTManager(DEVICE_ID, MQTT_SERVER, 1883)
# manager.enable_subcsription(handle_subscription)
IOHandler = InputOutputFacade()

while True:
    # Read and publish the sensor data
    try: 
        sensorDictionary = IOHandler.get_sensor_dictionary()
        print(sensorDictionary)
        manager.publish('/plant/bedroom', sensorDictionary)
        sleep(5)
    except OSError as e:
        print(e)
        sleep(2)
        reset()
    except Exception as e:
        print('An error occurred:', e) # Silently ignore
        sleep(5)
