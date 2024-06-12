import network, utime
from machine import Pin
from config import WIFI_SSID, WIFI_PASSWORD

pin = Pin("LED", Pin.OUT)

def connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        if not sta_if.isconnected():
            print("Attempting to connect to network...")
            utime.sleep(1)
            connect()
    if sta_if.isconnected():
        print("Connected to network")
        print(sta_if.ifconfig())
        pin.toggle()


print("Connecting to wifi")
connect()
