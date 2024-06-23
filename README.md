## Plant Monitor with Raspberry Pi as a controller

This tutorial will guide you through the process of creating a plant monitor using a Raspberry Pi as a controller. The project may take approximately 4-7 hours to complete provided you have all the hardware available.

The project creates a notification system that will alert you over Discord when your plant needs watering (or is drowning). The project will use a Raspberry Pi as a controller and local server to monitor the soil moisture of the plant and send a message to Discord when the soil moisture is too low or too high.

*Author: Pontus Grandin*
*ID: pg222pb*

### Objective

I often forget to water my plants. A device that would alert me when my plants need attention would therefore be useful. The project reads and stores the soil moisture of the plant as well as the humidity and temperature of the room. Although the moisture levels is what will trigger the alert.

The moisture, humidity and temperature is displayed in a web interface that is accessible on the local network for the user to monitor and interpet.

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

// TODO Does the Raspberry Pi installation go here?

### Putting everything together

![Circuit Diagram](./img/diagram_bb.png)

The diagram is accurate to real life.

#### Wire color coding

- White wires represent power and are connected to the 3V3 pin on the Pico WH.
- Black wires represent ground and are connected to the GND pin on the Pico WH.
- Blue wires represent the data and are connected to the GP pins on the Pico WH.

#### GP Connections

The moisture sensors data wire is connected to GP26, or ADC0.
The temperature and humidity sensors data wire is connected to GP14.
The LED is connected to GP16.

A resistor was required to limit the current running to the LED. The following formula, [Ohm's Law](https://en.wikipedia.org/wiki/Ohm's_law) provided on the IoT Course Discord, was used to calculate the resistance needed:

Resistor Value Required = Supply Voltage - Forward Voltage / Forward Current.

The LED used in this project has a forward voltage of 2V and a forward current of 25mA. The supply voltage is 3.3V. The calculation is as follows:

```js
(3.3 - 2) / 0.025 = 52
```

Meaning we need a resistor with a resistance of 52 Ohms. The closest resistor available was 330 Ohms, which was used in the project.

*Do not be misled if you cannot find proper documentation on the power requirements of the AZDelivery Moisture Sensor, it works using 3.3V and is not limited to 5V as the technical specification may suggest.*

### Platform

### The code

### Transmitting the data / connectivity

### Presenting the data

### Finalizing the design
