# Plant Monitor with Raspberry Pi as a controller

## Index

- [Introduction](#introduction)
- [Objective](#objective)
- [Material](#material)
- [Computer Setup](#computer-setup)
- [Putting everything together](#putting-everything-together)
- [Platform](#platform)
- [The code](#the-code)
- [Transmitting the data / connectivity](#transmitting-the-data--connectivity)
- [Presenting the data](#presenting-the-data)
- [Finalizing the Design](#finalizing-the-design)

## Introduction

This tutorial will guide you through the process of creating a plant monitor using a Raspberry Pi as a controller. The project may take approximately 4-7 hours to complete provided you have all the hardware available.

The project creates a notification system that will alert you over Discord when your plant needs watering (or is drowning). The project will use a Raspberry Pi as a controller and as a local server to monitor the soil moisture of the plant and send a message to Discord when the soil moisture is too low or too high.

*Author: ```Pontus Grandin```*

*ID: ```pg222pb```*

## Objective

I often forget to water my plants. A device that would alert me when my plants need attention would therefore be useful. The project reads and stores the soil moisture of the plant as well as the humidity and temperature of the room. Although the moisture levels is what will trigger the alert.

The moisture, humidity and temperature is displayed in a web interface that is accessible on the local network for the user to monitor and interpret.

## Material

| Item | Purpose | Price | Link |
|----------|----------|----------|----------|
| Raspberry Pi 4 Model B (4GB) | Host our IoT Stack and MQTT Broker | 810 SEK | [Amazon.se](https://www.amazon.se/-/en/dp/B09TTNF8BT?ref=ppx_yo2ov_dt_b_product_details&th=1) |
| Geekworm Raspberry Pi 4 Case | Act as cover to protect the Raspberry Pi **(Not necessary to complete the tutorial)** | 166 SEK | [Amazon.se](https://www.amazon.se/-/en/dp/B07ZVJDRF3?ref=ppx_yo2ov_dt_b_product_details&th=1) |
| Raspberry Pi Pico WH| Acts as the microcontroller which reads and sends data | 109 SEK | [Electrokit](https://www.electrokit.com/en/raspberry-pi-pico-wh) |
| SanDisk MobileMate UHS-I microSD Reader | Used for loading the Raspberry Pi OS onto the MicroSD card | 93 SEK | [Amazon.se](https://www.amazon.se/-/en/dp/B07G5JV2B5?ref=ppx_yo2ov_dt_b_product_details&th=1) |
| Sonero Micro HDMI to HDMI Cable | To graphically interact with the Raspberry Pi Desktop | 76 SEK | [Amazon.se](https://www.amazon.se/-/en/dp/B0BWNQ2L3K?ref=ppx_yo2ov_dt_b_product_details&th=1) |
| AZDelivery Ground Moisture Sensor Hygrometer Module V1.2 Capacitive | Reads the moisture in the soil | 69 SEK | [Amazon.se](https://www.amazon.se/-/en/dp/B07HJ6N1S4?ref=ppx_yo2ov_dt_b_product_details&th=1) |
| Solderless Breadboard 840 tie-points | Used for connecting the sensors and LED to the Pico WH | 69 SEK | [Electrokit](https://www.electrokit.com/en/kopplingsdack-840-anslutningar) |
| KIOXIA 32GB EXCERIA microSD | Holds the Raspberry Pi OS, influxDB data and acts as the main memory storage for the Raspberry Pi | 55 SEK | [Amazon.se](https://www.amazon.se/-/en/dp/B088RQCCDJ?psc=1&ref=ppx_yo2ov_dt_b_product_details) |
| Jumper Wires Male/Male | Run electrical currents for giving power/sensor readings | 49 SEK | [Electrokit](https://www.electrokit.com/en/labbsladd-40-pin-30cm-hane/hane) |
| Digital temperature and humidity sensor DHT11 | Reading the temperature and humidity of the air | 49 SEK | [Electrokit](https://www.electrokit.com/en/digital-temperatur-och-fuktsensor-dht11) |
| 2x USB-Cable A-Male to Micro B-Male *Adapter not included* | Powers the Pico and the Raspberry Pi | 28 SEK | [Electrokit](https://www.electrokit.com/en/usb-kabel-a-hane-micro-b-hane-60cm) |
| Photo resistor CdS 4-7 kohm  | Reads the light that the plants receive | 8 SEK | [Electrokit](https://www.electrokit.com/en/fotomotstand-cds-4-7-kohm) |
| LED 5mm Red Diffuse | Lights up when the plant needs attention | 5 SEK | [Electrokit](https://www.electrokit.com/en/led-5mm-rod-diffus-1500mcd) |
| Resistor 0.25W 330R | Limits the current running to the LED | 1 SEK | [Electrokit](https://www.electrokit.com/en/motstand-kolfilm-0.25w-330ohm-330r) |
| Resistor  0.25W 10kohm (10k) | Acts as a voltage divider for the photoresistor | 1 SEK | [Electrokit](https://www.electrokit.com/motstand-kolfilm-0.25w-10kohm-10k) |

The table lists the electrokit items as individual pieces, they were however bought in these two following kits:

- [LNU Start kit](https://www.electrokit.com/lnu-starter)
- [Sensor Kit - 25 Modules](https://www.electrokit.com/sensor-kit-25-moduler)

*Note: The MicroHDMI to HDMI cable is not strictly necessary as you can grab the Raspberry Pi's IP address without graphically interfacing with it. However these steps are not included in this tutorial.*

## Computer Setup

The project was developed on a PC running Windows 10.

### IDE and plugins

The IDE of choice is [Vistual Studio Code](https://code.visualstudio.com/), other options are Tommy and Atom. Visual Studio Code was chosen due to the author already being familiar with the IDE.
The following two extensions were installed in VSC for Python language support, as the Raspberry Pi Pico runs on Micropython in this project, and transferrence of code to the Pico WH. [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python), for its language support, and [Pymakr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr), for its ability to transfer code to the Pico WH.

### Raspberry Pi Pico WH Firmware

Grab the latest firmware from [Micropython's website](https://micropython.org/download/RPI_PICO_W/). The firmware is flashed onto the Pico WH by connecting the Pico WH to your computer using the Micro USB cable and holding down the white BOOTSEL button. A new drive will appear on your computer, drag and drop the firmware onto the drive. The Pico WH will restart and the firmware is now flashed.

### Raspberry Pi OS Installation

To install the Raspberry Pi Operating Systemn we use the MicroSD card and card reader and the official [Raspberry Pi Imager software](https://www.raspberrypi.com/software/). Using the software allows us to easily install the Raspberry Pi OS onto the MicroSD card and preconfigure Wifi and SSH settings, so we can access the Raspberry Pi remotely. The username and password for the Raspberry Pi OS is used when connecting to the Raspberry Pi through SSH if you select the **Use password authentication** option. The author used the Public-key option and could simply SSH into the Raspberry Pi with the following command:

```bash
ssh <username>@<raspberry-ip-address>
```

This requires us to know the IP address of the Raspberry Pi, which can be found by connecting the Raspberry Pi to a monitor and hovering over the Wifi icon in the top right corner of the screen. There are other options of finding the IP address remotely which do not require plugging the Raspberry Pi into a monitor, but they are not covered in this tutorial.

### Installing Mosquitto, Node-Red, InfluxDB and Grafana

IoT-stack was used to quickly setup the visualisation/mqtt stack. The IoT stack program was pulled onto the raspberry pi using the following terminal command:

```cmd
curl -fsSL https://raw.githubusercontent.com/SensorsIot/IOTstack/master/install.sh | bash
```

This downloads the IoT stack program onto the raspberry pi and installs it.

IoT-stack builds a docker-compose file which allows us to quickly launch all of these applications with a single command and not have to worry too much about configuration.

Following this we then enter the menu of the program by opening the menu.sh file located in the IOTstack folder.

```cmd
cd IOTstack/menu.sh
```

We now select the programs we wish to install. This project runs the stack grafana, influxdb, mosquitto as a broker and Node-Red. We select these programs by navigating the menu and selecting them. The program will then build the docker-compose file and launch the applications once the ```Start Stack``` option is selected.

Following this we set up the influxdb database by actually creating the database to which we will write. We will name it "sensor data". To do this we access the command line of the influxdb application by using this command:

```cmd
docker exec -it influxdb influx
```

This tells docker to run the influxdb CLI in interactive mode for us. Meaning we can talk to the influxd application in the command tool.

Here we create the database with the following command:

```cmd
CREATE DATABASE sensor_data
```

These applications are accessible in the browser with the following addresses:

- Grafana: http://< raspberry-ip-address >:3000
- Node-Red: http://< raspberry-ip-address >:1880

InfluxDB and Mosquitto are not accessible through the browser, but they are running on the Raspberry Pi on the following ports:

- InfluxDB: 8086
- Mosquitto: 1883

## Putting everything together

![Circuit Diagram](./img/diagram_bb.png)

The diagram is accurate to real life.

### Wire color coding

- White wires represent power and are connected to the 3V3 pin on the Pico WH.
- Black wires represent ground and are connected to the GND pin on the Pico WH.
- Blue wires represent the data and are connected to the GP pins on the Pico WH.

### GP Connections

- The photoresistor is connected to GP27, or ADC1.
- The moisture sensors data wire is connected to GP26, or ADC0.
- The LED is connected to GP16.
- The temperature and humidity sensors data wire is connected to GP14.

### Resistors and Voltage Dividers

A resistor was required to limit the current running to the LED. The following formula, [Ohm's Law](https://en.wikipedia.org/wiki/Ohm's_law) provided on the IoT Course Discord, was used to calculate the resistance needed:

Resistor Value Required = Supply Voltage - Forward Voltage / Forward Current.

The LED used in this project has a forward voltage of 2V and a forward current of 25mA. The supply voltage is 3.3V. The calculation is as follows:

```js
(3.3 - 2) / 0.025 = 52
```

Meaning we need a resistor with a resistance of 52 Ohms. The closest resistor available was 330 Ohms, which was used in the project.

A resistor was used to create a voltage divider for the photoresistor. This allows the varying resistance of the photoresistor to be read by the Pico WH. The photoresistor has a resistance of 4-7 kOhm. The resistor used in the voltage divider was 10 kOhm. Without this extra resistor we would receive a very constant value, rendering it impossible to read the brightness value. The voltage divider formula is as follows:

```js
 Vin * R2 / (R1 + R2) = Vout  // Vin is the voltage input (3.3V) R1 is the variable resistance of the photoresistor and R2 is the resistance of the resistor.
3.3 * 10000 / (10000 + 5000) = 2.2 // Meaning the output voltage is 2.2V when the photoresistor is at 5 kOhm (Should be bright).
```

*Do not be misled if you cannot find proper documentation on the power requirements of the AZDelivery Moisture Sensor, it works using 3.3V and is not limited to 5V as the technical specification may suggest.*

## Platform

The platform stack runs locally on the Raspberry Pi. The choice to run the stack locally was made due to the authors aversion to cloud services. The stack is also more secure as it does not require any data to be sent outside of the local network.

The stack of choice for this project is as follows:

- [Mosquitto](https://mosquitto.org/) as the MQTT broker for the communication between the Raspberry Pi and the Pico WH.
- [Node-RED](https://nodered.org/) for connecting the MQTT broker to the InfluxDB and Grafana. Node-RED is also used to send messages to Discord and for conditional logic. The conditional logic is more closely examined in the [Code](#the-code) section.
- [InfluxDB](https://www.influxdata.com/) as the database for storing the sensor data.
- [Grafana](https://grafana.com/) for visualizing the data stored in the InfluxDB.

It is entirely possible to scale this project to include more sensors and more functionality. The Raspberry Pi has more than enough computing power to handle more data transmissions and logic in Node-RED. The one consideration is the amount of data stored in the InfluxDB, as the Raspberry Pi has a limited amount of storage space. This can, however, be easily upgraded by using an external hard drive or a larger MicroSD card.

A choice was made between [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/) and Node-RED for the integration between the different parts. Node-RED was chosen due to its graphical interface, making the visualization of the data flow easier to understand. This stack could run using Telegraf as well and is, the author believes, the more orthodox choice.

Following is a visualization of the dataflow between the different parts of the project. It is not meant to be an exhaustive explanation of what happens to the data at each step, but rather a high-level overview of the data flow.

![Flowchart](./img/dataflow.png)

## The code

The code of this project can be divided into two parts, the code running on the microcontroller and the code running on the Raspberry Pi.

### Pico WH Code

The code running on the Pico WH is written in Micropython and can be largely be divided into three parts. The first part being the reading of the sensors, the second part being the sending and receiving of data over MQTT and the third part being the WiFi connectivity. The WiFi connectivity code is largely copied from the IoT LNU Course material accessible [here](https://hackmd.io/@lnu-iot/rJVQizwUh) and will therefore be omitted from this tutorial.

An overview of how the code is ran can be found in the main loop of the code. Data is transmitted and received over MQTT every minute. The 10 second sleep following the publish is to allow the data to be processed by the Node-RED flow and possibly publish a message to our subscribed topic, immediatelly checking the message after publishing would see a full minute delay between Node-RED publishing a message and the Pico WH receiving it.

```js
    moisture, temp, hum, light = IOHandler.get_sensor_data() // Collects and reads the sensor data
    sensorDictionary = format_as_dictionary(moisture, temp, hum, light) // Prepares the data for transmission by converting it to a dictionary
    manager.publish(MQTT_PUBLISH_TOPIC, sensorDictionary) // Publish the data to the MQTT broker
    sleep(10) // Sleep for 10 seconds to allow the Node-RED flow to process the data
    manager.check_msg() // Check for incoming MQTT messages from the Node-RED flow
    sleep(50)
```

None if this is possible without first connecting to the Wifi network. The configuration for the Wifi network is done in the `config.py` file, along with the MQTT broker IP address and the topic to publish and subscribe to. Following is a snippet of the `config.py` file, with omitted details. These variables are imported into the boot sequence and other parts of the code as important constants.

```python
import machine
import ubinascii
WIFI_SSID = 'WIFI NAME 
WIFI_PASSWORD = 'PW'
MQTT_SERVER = 'IP-ADRESS'
MQTT_PUBLISH_TOPIC = '/plant/bedroom'
MQTT_SUBSCRIBE_TOPIC = 'bedroom/led'
```
The connection to the MQTT broker is handled by the `MQTTManager` class which is dependent on the `MQTTClient` library. The library can be accessed [here](./lib/simple.py), or if you would rather grab it from the [source here](https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/umqtt/simple.py). The `MQTTManager` class is responsible for connecting to the MQTT broker, publishing and subscribing to topics and checking for incoming messages.

```py
from lib.simple import MQTTClient 
import ujson

# TODO needs to be reworked slightly.

class MQTTManager:

    def __init__(self, client_id: str, server: str, port: int):
        self.client = MQTTClient(client_id, server, port)
        self.client.connect()

    def enable_subcsription(self, topic, callback):
        self.client.set_callback(callback)
        self.client.subscribe(topic)

    def publish(self, topic: str, msg: str):
        json_msg = ujson.dumps(msg)
        self.client.publish(topic, json_msg)

    def check_msg(self):
        self.client.check_msg()
```

In our ```main.py``` file we pass subscription callback method to the MQTTManager class following the initialization, which simply turns on or off the LED based on the message received from the subscription topic.

**main.py**

```js
# Connect to the MQTT server
manager = MQTTManager(DEVICE_ID, MQTT_SERVER, 1883)
IOHandler = InputOutputFacade()
manager.enable_subcsription(MQTT_SUBSCRIBE_TOPIC, IOHandler.subscription_callback)
```

**InputOutputFacade.py**

```py
def subscription_callback(self, topic, msg):
    parsedMsg = ujson.loads(msg)
    if parsedMsg['msg'] == 'ON':
        print('Turning on LED')
        self.led.turn_on()
    elif parsedMsg['msg'] == 'OFF':
        print('Turning off LED')
        self.led.turn_off()
    else:
        print('Invalid message received:', msg)
```

### Node-RED Code

The Node-RED code is written in Javascript.

The interesting part of the Node-RED code is the conditiona logic that decides when to send a message to Discord and when to turn on/off the LED. This is achieved through the use of the `switch` and `function` nodes. The `switch` node is used to conditionally execute nodes in the flow based on the return value of the `function` node. There are 2 main `function` nodes in the flow, one for checking the moisture of the soil and one for controlling the LED.

#### Moisture Node

```js
const userName = "Bedroom Plant Monitor" // Discord username
const maxMoisture = flow.get('maxMoisture') // Set to 80
const minMoisture = flow.get('minMoisture') // Set to 30

if (msg.payload.moisture < minMoisture || msg.payload.moisture > maxMoisture) {
   return {
      payload: {
          content: `Plant is in danger-zone! Moisture level: ${msg.payload.moisture}`, // Message displayed in Discord
          username: userName,
          needsAttention: true
      }
   }
} else {
   return {
      payload: {
         needsAttention: false
      }
   }
}
```

The if statement will execute if the moisture level is below 30 or above 80. The message will be sent to Discord with the moisture level and the username of the bot. The `needsAttention` variable is used to control the Node-RED flow, the following `switch` node will conditionally execute the following nodes based on the value of `needsAttention`. If `needsAttention` is false the Discord hook will not be executed.

#### LED Node

```js
const currentDate = new Date()
const latestHour = flow.get('ledStopHour') // Set to 21
const earliestHour = flow.get('ledStartHour') // Set to 9
const hour = currentDate.getHours() // Fetch current hour
const isWithinOperableHours = hour < latestHour && hour >= earliestHour // Check if the current hour is within the operable hours
const isLedOn = flow.get('ledOn') // Fetch current LED state

if (isWithinOperableHours && msg.payload.needsAttention && !isLedOn) { // Turn on the LED if the hours are within the operable hours, the plant needs attention and the LED is off
    flow.set('ledOn', true)
    return {
        payload: {
            msg: "ON"
        }
    }
} else if ((!isWithinOperableHours && isLedOn) || (!msg.payload.needsAttention && isLedOn)){ // Turn off the LED if the hours are outside the operable hours and the LED is on, or if the plant does not need attention and the LED is on
    flow.set('ledOn', false)
    return {
        payload: {
            msg: "OFF"
        }
    }
}
return null
```

We use the current hour to determine if the LED should be on or off. The LED should only be on between 9 and 21. The LED should be on if the plant needs attention and the LED is off. The LED should be off if the plant does not need attention and the LED is on, or if the current hour is outside the operable hours and the LED is on. We return `null` if the LED should not be turned on or off, essentially making the function node a no-op and communicating to Node-RED that the flow should terminate.

## Transmitting the data / connectivity

This project utilizes WiFi for transmitting the data from the Pico WH to the Raspberry Pi. The choice of WiFi was chosen due to the local nature of the project, there is no need for the long range communication that LoRaWAN offers. The data is transmitted over MQTT, which was chosen due to its ease of implementation and how lightweight it is. The data is transmitted from the Pico WH to the Raspberry Pi every minute. The data is then processed by the Node-RED flow and stored in the InfluxDB.

The Discord message is transmitted using a webhook. The webhook is created in Discord and the URL is added to the `http request` node in the Node-RED flow. The message is sent to Discord when the plant needs attention.

As no port-forwarding was done the project is only accessible on the local network. That means that the MQTT transmission can only occur on the local network. The same goes for the visualisation of the data in Grafana, the dashboard is only accessible on the local network. To successfully expand the project outside of the WiFi range would require port-forwarding to be enabled on the router. This would allow the MQTT broker to be accessible from the internet and the data to be transmitted from the Pico WH to the Raspberry Pi from anywhere in the world.

// TODO add part about battery consumption (do power calculations)

## Presenting the data

![Node-RED flow](./img/node-red-flow.png)

## Finalizing the design
