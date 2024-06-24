from time import sleep
from scripts import reset, format_as_dictionary
from MQTTManager import MQTTManager
from config import DEVICE_ID, MQTT_SERVER, DEVICE_ID, MQTT_PUBLISH_TOPIC, MQTT_SUBSCRIBE_TOPIC
from InputOutput.InputOutputFacade import InputOutputFacade


# Connect to the MQTT server
manager = MQTTManager(DEVICE_ID, MQTT_SERVER, 1883)
IOHandler = InputOutputFacade()
manager.enable_subcsription(MQTT_SUBSCRIBE_TOPIC, IOHandler.subscription_callback)

while True:
    # Read and publish the sensor data
    try: 
        moisture, temp, hum, light = IOHandler.get_sensor_data()
        sensorDictionary = format_as_dictionary(moisture, temp, hum, light)
        manager.publish(MQTT_PUBLISH_TOPIC, sensorDictionary)
        sleep(2)
        manager.check_msg()
        sleep(2)
    except OSError as e:
        print(e)
        sleep(2)
        reset()
    except Exception as e:
        print('An error occurred:', e) # Silently ignore
        sleep(5)
