## Plant Monitor with Raspberry Pi as a controller

This tutorial will guide you through the process of creating a plant monitor using a Raspberry Pi as a controller. The project may take approximately 4-7 hours to complete provided you have all the hardware available.

The project creates a notification system that will alert you over Discord when your plant needs watering (or is drowning). The project will use a Raspberry Pi as a controller and as a local server to monitor the soil moisture of the plant and send a message to Discord when the soil moisture is too low or too high.

*Author: Pontus Grandin*
*ID: pg222pb*

### Objective

I often forget to water my plants. A device that would alert me when my plants need attention would therefore be useful. The project reads and stores the soil moisture of the plant as well as the humidity and temperature of the room. Although the moisture levels is what will trigger the alert.

The moisture, humidity and temperature is displayed in a web interface that is accessible on the local network for the user to monitor and interpret.

### Material

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
| LED 5mm Red Diffuse | Lights up when the plant needs attention | 5 SEK | [Electrokit](https://www.electrokit.com/en/led-5mm-rod-diffus-1500mcd) |
| Resistor 0.25W 330R | Limits the current running to the LED | 1 SEK | [Electrokit](https://www.electrokit.com/en/motstand-kolfilm-0.25w-330ohm-330r) |
| Resistor  0.25W 10kohm (10k) | Acts as a voltage divider for the photoresistor | 1 SEK | [Electrokit](https://www.electrokit.com/motstand-kolfilm-0.25w-10kohm-10k) |
| Photo resistor CdS 4-7 kohm  | Reads the light that the plants receive | 8 SEK | [Electrokit](https://www.electrokit.com/en/fotomotstand-cds-4-7-kohm) |

The table lists the electrokit items as individual pieces, they were however bought in these two following kits:

- [LNU Start kit](https://www.electrokit.com/lnu-starter)
- [Sensor Kit - 25 Modules](https://www.electrokit.com/sensor-kit-25-moduler)

*Note: The MicroHDMI to HDMI cable is not strictly necessary as you can grab the Raspberry Pi's IP address without graphically interfacing with it. However these steps are not included in this tutorial.*

### Computer Setup

The project was developed on a PC running Windows 10.

#### IDE and plugins

The IDE of choice is [Vistual Studio Code](https://code.visualstudio.com/), other options are Tommy and Atom. Visual Studio Code was chosen due to the author already being familiar with the IDE.
The following two extensions were installed in VSC for Python language support, as the Raspberry Pi Pico runs on Micropython in this project, and transferrence of code to the Pico WH. [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python), for its language support, and [Pymakr](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr), for its ability to transfer code to the Pico WH.

#### Raspberry Pi Pico WH Firmware

Grab the latest firmware from [Micropython's website](https://micropython.org/download/RPI_PICO_W/). The firmware is flashed onto the Pico WH by connecting the Pico WH to your computer using the Micro USB cable and holding down the white BOOTSEL button. A new drive will appear on your computer, drag and drop the firmware onto the drive. The Pico WH will restart and the firmware is now flashed.

#### Raspberry Pi OS Installation

To install the Raspberry Pi Operating Systemn we use the MicroSD card and card reader and the official [Raspberry Pi Imager software](https://www.raspberrypi.com/software/). Using the software allows us to easily install the Raspberry Pi OS onto the MicroSD card and preconfigure Wifi and SSH settings, so we can access the Raspberry Pi remotely. The username and password for the Raspberry Pi OS is used when connecting to the Raspberry Pi through SSH if you select the **Use password authentication** option. The author used the Public-key option and could simply SSH into the Raspberry Pi with the following command:

```bash
ssh <username>@<raspberry-ip-address>
```

This requires us to know the IP address of the Raspberry Pi, which can be found by connecting the Raspberry Pi to a monitor and hovering over the Wifi icon in the top right corner of the screen. There are other options of finding the IP address remotely which do not require plugging the Raspberry Pi into a monitor, but they are not covered in this tutorial.

// TODO Explain how to setup Node-RED, InfluxDB and Grafana on the Raspberry Pi.

### Putting everything together

![Circuit Diagram](./img/diagram_bb.png)

The diagram is accurate to real life.

#### Wire color coding

- White wires represent power and are connected to the 3V3 pin on the Pico WH.
- Black wires represent ground and are connected to the GND pin on the Pico WH.
- Blue wires represent the data and are connected to the GP pins on the Pico WH.

#### GP Connections

- The moisture sensors data wire is connected to GP26, or ADC0.
- The temperature and humidity sensors data wire is connected to GP14.
- The LED is connected to GP16.
- The photoresistor is connected to GP27, or ADC1.

#### Resistors and Voltage Dividers

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

### Platform

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

### The code

### Transmitting the data / connectivity

### Presenting the data

### Finalizing the design
