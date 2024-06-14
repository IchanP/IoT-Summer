from time import sleep
from scripts import reset, json_preparation, handle_subscription
from MTTQManager import MTTQManager
from config import DEVICE_ID, MQTT_SERVER, DEVICE_ID
from InputOutput.InputOutputFacade import InputOutputFacade

# Connect to the MQTT server
# manager = MTTQManager(DEVICE_ID, MQTT_SERVER, 1883)
# manager.enable_subcsription(handle_subscription)
IOHandler = InputOutputFacade()

while True:
    # Read and publish the sensor data
    try: 
        moisture = IOHandler.read_all_sensors()
        print("ADC Value --->", moisture)
        # TODO send data over MQTT
        sleep(5)
    except OSError as e:
        print(e)
        reset()
    except Exception as e:
        print('An error occurred:', e) # Silently ignore
        sleep(5)
