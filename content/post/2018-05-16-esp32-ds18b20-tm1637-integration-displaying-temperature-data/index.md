---
title: 'ESP32, DS18B20, TM1637 integration: Displaying temperature data'
date: 2018-05-16 03:37:04
aliases: ['/2018/05/16/ESP32-DS18B20-TM1637-integration-Displaying-temperature-data/']
tags:
- c
- electronics
- esp32
- programming
categories:
- electronics
---
In a [previous post](/2018/05/04/Using-TM1637-based-LED-displays-with-ESP32/) I wrote about displaying arbitrary data on a TM1637-based 4 digit LED display, highlighting an [ESP-IDF component](https://github.com/NSBum/esp-32-tm1637) that I extended to display positive and negative floating point numbers. Now we're going to put that component to use and display actual data from a DS18B20 temperature sensor.

The {% asset_link DS18B20.pdf "DS18B20" %} temperature sensor operates on the Dallas Semiconductor 1-Wire bus. In this application, we aren't powering the devices using parasitic power. Instead we're powering the device from an external supply.

{{< figure src="images/ds18b20power.png" title="Using the DS18B20 with external power supply." >}}

Since we're using a 3.3v bus, the pullup resistor on `DQ` is 2.2KΩ, not 4.7K.

In addition to my modified [TM1637 component](https://github.com/NSBum/esp-32-tm1637), the project uses David Antliff's components for the 1-Wire bus protocol and the DS18B20 digital thermometer. You'll need to follow the instructions in the [project](https://github.com/NSBum/esp32-ds18b20-tm1637) README file to clone the project and recurse the three submodules.

### Usage

After cloning the project, you'll need to configure the GPIO pins in use using `make menuconfig`. One GPIO is used for the 1-Wire bus and two lines are used for each TM1637 display for a total of 5 GPIO pins. Be careful that you do not use pins that are in use for other purposes on your particular board. For example, I initially use GPIO12 for one of the TM1637 displays, but when connected, was unable to flash the ESP32. It appears that GPIO12 is used as a bootstrapping pin. On the particular board I used for this project, I believe that GPIO12 needs to be pulled low at reset but the TM1637 was not permitting it. Moving do another GPIO solved the problem.^[More about GPIO12 [here](https://github.com/espressif/esp-idf/blob/master/examples/storage/sd_card/README.md)]

After completing the hardware connections and specifying them in `make menuconfig`, you can then simply `make flash` to upload the application to the device.

All of the source code is on [github](https://github.com/NSBum/esp32-ds18b20-tm1637).

### References

- [Source code for this project](https://github.com/NSBum/esp32-ds18b20-tm1637)
- [TM1637 datasheet](http://ojisanseiuchi.com/2018/05/04/Using-TM1637-based-LED-displays-with-ESP32/Datasheet_TM1637.pdf)
- [DS18B20 datasheet](pdf/DS18B20.pdf)
- [My improved ESP32 TM1637 component](https://github.com/NSBum/esp-32-tm1637)
- [esp32-owb](https://github.com/DavidAntliff/esp32-owb) - David Antliff's ESP32-compatible C library for the 1-Wire bus protocol
- [esp32-ds18b20](https://github.com/DavidAntliff/esp32-ds18b20) - and his ESP32 C component for the DS18B20 digital thermometer
- [Source for the TM1637-based displays](https://robotdyn.com/catalog/displays/segment.html) - This company also has presence on Aliexpress which is where I ordered these inexpensive displays.^[I prefer these displays to the 74HC595 because the TM1637 handles all of the multiplexing for you, whereas the shift-register displays require the host controller to take on constant refreshing of the display.]
- [Pinout of the Doit ESP32 DEVKIT V1](images/pinoutDOIT32devkitv1.png) - the board used in this project.
