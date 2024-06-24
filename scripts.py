from time import sleep
import machine
import json

led = machine.Pin("LED", machine.Pin.OUT)

def format_as_dictionary(moisture, temp, hum, light): 
    data = {
        "moisture": moisture,
        "temperature": temp,
        "humidity": hum,
        "brightness": light
    }
    return data

def reset():
    print('Resetting the device...') 
    machine.reset()

def handle_subscription(topic, msg):
    print(topic)
    # TODO add a condition to check if the topic is the same as the one we are subscribing to
    if msg == b'ON':
        print('Turning on the LED')
    elif msg == b'OFF':
        print('Turning off the LED')
    else:
        print('Invalid message received:', msg)