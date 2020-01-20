---
title: ESP32 reading Si7102 temperature and humidity data via I2C bus
date: 2018-04-26 22:00:22
tags:
- c
- electronics
- esp32
- programming
- i2c
categories:
- electronics
---
Recently I [wrote about](/2018/03/11/Reading-data-from-Si7021-temperature-and-humidity-sensor-using-Raspberry-Pi/) reading Si7021 temperature and humidity data using a Raspberry Pi. Now let's try a completely different platform, the [ESP32](http://www.esp32.net). This is essentially a project to explore using I2C on the ESP32 platform and to understand the build process.

### Project layout

Since we're developing the Si7021 interface code as a reusable component, we need to structure our project in such a way that we can easily refer to it in our main code. Here's how I structured this project:

{{< figure src="images/esp32_component_layout.png" title="Project layout" >}}

<!-- more -->

Carefully note the locations of the `component.mk` files. This is how the build system finds and links our component(s) during the build process. The contents of each `component.mk` file is also important. The outer `component.mk` consists of a single line point to the component directories in use:

{{< highlight c >}}
COMPONENT_SRCDIRS := si7102
{{< /highlight >}}

The `component.mk` inside the `components` directory specifies the entities that should be included there in the build process:

{{< highlight c >}}
#
# Component Makefile
#

COMPONENT_SRCDIRS := .
COMPONENT_ADD_INCLUDEDIRS := .
COMPONENT_PRIV_INCLUDEDIRS :=
{{< /highlight >}}

The final `component.mk` inside the `main` directory is left blank.

### I2C on the ESP32

The ESP32 has a more flexible design than many of the microcontrollers that hobbyists commonly use. Having two I2C controllers, it can serve as both master and slave. It also has the ability to assign the SDA and SCL signals to almost any IO pin. For more on the fundamentals of I2C on the ESP32, see [this excellent post](http://www.lucadentella.it/en/2017/10/09/esp32-23-i2c-basic/) by Luca Dentella.

### Si7021 component

To simplify our `main.c` and to reuse the Si7021-specific code in the future, we broke out that functionality into a component that consists of two files: `si7021.h` and `si7021.c`. The header file contains our register definitions, the slave address of the device and function prototypes. The function implementations are all in `si7021.c`.

To use the Si7021, we must first initialise the I2C bus and determine whether a compatible slave device is waiting:

{{< highlight c >}}
esp_err_t ret;

// setup i2c controller
i2c_config_t conf;
conf.mode = I2C_MODE_MASTER;
conf.sda_io_num = sda_pin;
conf.scl_io_num = scl_pin;
conf.sda_pullup_en = sda_internal_pullup;
conf.scl_pullup_en = scl_internal_pullup;
conf.master.clk_speed = 100000;
ret = i2c_param_config(port, &conf);
if( ret != ESP_OK ) return SI7021_ERR_CONFIG;
{{< /highlight >}}

Here, we simple set up the mode, pins, pullup resistor requirements, and I2C clock speed in a `i2c_config_t` struct and configure one of the two available I2C ports to use that configuration. Next, we have to install the I2C driver

{{< highlight c >}}
// install the driver
ret = i2c_driver_install(port, I2C_MODE_MASTER, 0, 0, 0);
if(ret != ESP_OK) return SI7021_ERR_INSTALL;
{{< /highlight >}}

Finally, we'll just check to see if a Si7021 is sitting on the bus as a slave:

{{< highlight c >}}
// verify if a sensor is present
i2c_cmd_handle_t cmd = i2c_cmd_link_create();
i2c_master_start(cmd);
i2c_master_write_byte(cmd, (SI7021_ADDR << 1) | I2C_MASTER_WRITE, true);
i2c_master_stop(cmd);
if(i2c_master_cmd_begin(port, cmd, 1000 / portTICK_RATE_MS) != ESP_OK)
	return SI7021_ERR_NOTFOUND;
{{< /highlight >}}

The `i2c_cmd_handle_t` is an opaque data type that you can think of as a container for future actions from our master to the Si7021 slave. We have to create this "container" before we can execute any actions on the slave device. After creating the handle, we issue the usual I2C start command on it. To look for the device, we just send the address, look for an ACK and then stop. The function `i2c_master_cmd_begin()` takes the sequence of commands that we've constructed and executes it, waiting here for a timeout of 1000 ms during the initialization process.

#### Reading a value

As I [mentioned previously](/2018/03/11/Reading-data-from-Si7021-temperature-and-humidity-sensor-using-Raspberry-Pi/), we have two different modes of operation for the Si7021. Since the device takes time to do the temperature conversion process, we have to choose whether to keep the master on hold by stretching the clock, or just repeatedly polling the device until we get an `ACK` or the whole operation times out. In this component, we have chosen to simply wait for an `ACK` rather than deal with clock-stretching.

Now that you understand the process flow for I2C operations, it's easy to understand how to read a value (temperature or humidity) from the device. We simple write the device address, the conversion command, wait 50 ms for the result and read out the data and the CRC.

{{< highlight c >}}
uint16_t read_value(uint8_t command) {

	esp_err_t ret;

	// send the command
	i2c_cmd_handle_t cmd = i2c_cmd_link_create();
	i2c_master_start(cmd);
	i2c_master_write_byte(cmd, (SI7021_ADDR << 1) | I2C_MASTER_WRITE, true);
	i2c_master_write_byte(cmd, command, true);
	i2c_master_stop(cmd);
	ret = i2c_master_cmd_begin(_port, cmd, 1000 / portTICK_RATE_MS);
	i2c_cmd_link_delete(cmd);
	if(ret != ESP_OK) return 0;

	// wait for the sensor (50ms)
	vTaskDelay(50 / portTICK_RATE_MS);

	// receive the answer
	uint8_t msb, lsb, crc;
	cmd = i2c_cmd_link_create();
	i2c_master_start(cmd);
	i2c_master_write_byte(cmd, (SI7021_ADDR << 1) | I2C_MASTER_READ, true);
	i2c_master_read_byte(cmd, &msb, 0x00);
	i2c_master_read_byte(cmd, &lsb, 0x00);
	i2c_master_read_byte(cmd, &crc, 0x01);
	i2c_master_stop(cmd);
	ret = i2c_master_cmd_begin(_port, cmd, 1000 / portTICK_RATE_MS);
	i2c_cmd_link_delete(cmd);
	if(ret != ESP_OK) return 0;

	uint16_t raw_value = ((uint16_t) msb << 8) | (uint16_t) lsb;
	if(!is_crc_valid(raw_value, crc)) printf("CRC invalid\r\n");
	return raw_value & 0xFFFC;
}
{{< /highlight >}}

The rest of the code is left as an exercise for the reader. You can find the entire code at its [github repository](https://github.com/NSBum/si7021_test)

### References

- [Si7021 datasheet](/2018/03/11/Reading-data-from-Si7021-temperature-and-humidity-sensor-using-Raspberry-Pi/Si7021-A20.pdf)
- [Reading Si7021/HTU21D on the Raspberry Pi I2C bus](https://www.iot-programmer.com/index.php/books/22-raspberry-pi-and-the-iot-in-c/chapters-raspberry-pi-and-the-iot-in-c/61-raspberry-pi-and-the-iot-in-c-i2c-bus?showall=&start=3) - an excellent article for understanding how to implement clock-stretching and dealing with specifics of the Si7021 device.
