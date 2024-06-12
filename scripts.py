from time import sleep
import machine
import json

led = machine.Pin("LED", machine.Pin.OUT)

def handle_subscription(topic, msg):
    print(topic)
    # TODO add a condition to check if the topic is the same as the one we are subscribing to
    if msg == b'ON':
        led.value(1)
    elif msg == b'OFF':
        led.value(0)

def json_preparation(key, value):
    data = {
        key: value
    }
    return json.dumps(data)

def reset():
    print('Resetting the device...') 
    sleep(5)
    machine.reset()
