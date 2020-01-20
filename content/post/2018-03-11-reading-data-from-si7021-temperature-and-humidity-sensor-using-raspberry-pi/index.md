---
title: Reading data from Si7021 temperature and humidity sensor using Raspberry Pi
date: 2018-03-11 18:30:16
tags:
- i2c
- raspberrypi
- electronics
- programming
- c
categories:
- electronics
---
The [Si7021](pdf/Si7021-A20.pdf)is an excellent little device for measuring temperature and humidity, communicating with the host controller over the I2C bus. This is a quick tutorial on using the Raspberry Pi to talk to this device. If you are unfamiliar with the conceptual framework of I2C or how to enable I2C access on the Raspberry Pi, I suggest [starting here](https://www.iot-programmer.com/index.php/books/22-raspberry-pi-and-the-iot-in-c/chapters-raspberry-pi-and-the-iot-in-c/61-raspberry-pi-and-the-iot-in-c-i2c-bus?showall=&limitstart=). Otherwise, let's jump in.

You are probably working with the device mounted on a breakout board. I used [this one](https://www.adafruit.com/product/3251) from Adafruit. There are no surprises on the pins that it breaks out - Vin, 3v out, GND, SCL and SDA. One the 40-pin P1 header of the Raspberry Pi, SDA and SCL for I2C bus 1 occupy pins 2 and 3.

Once you've wired it all up (don't forget common ground connections to the Pi,) then we're ready to write some code. First, we need to study the device a little bit.

### Si7021 Humidity and temperature sensor

The device is quite accurate for temperature, typically ±0.4 degrees C. The humidity is ±3%. It can operate down to -40 degrees C, which is important in Canada where I live!

The I2C implementation on the device is straightforward. It has a fixed I2C hardware address of 0b01000000 (0x40). The instruction set is not large, but there's some nuance which we'll explain. First, let's get some `#define` statements out of the way in our code:

{{< highlight c >}}
#define SI7021_ADDR 0x40

//  I2C COMMANDS
#define SI7021_MRH_HOLD     0xE5
#define SI7021_MRH_NOHOLD   0xF5
#define SI7021_MT_HOLD      0xE3    //  measure temp, hold master
#define SI7021_MT_NOHOLD    0xF3    //  measure temp, no hold master
#define SI7021_RT_PREV      0xE0    //  read temp from last RH measurement
#define SI7021_RESET        0xFE    //  reset
#define SI7021_WR_USER1     0xE6    //  write RH/T user register 1
#define SI7021_RD_USER1     0xE7    //  read RH/T user register 1
#define SI7021_WR_HCTL      0x51    //  write heater control register
#define SI7021_RD_HCTL      0x11    //  read heater control register
#define SI7021_RD_ID1       0xFA 0x0F   //  read electronic ID 1st byte
#define SI7021_RD_ID2       0xFC 0xC9   //  read electronic ID 2nd byte
#define SI7021_RD_REV       0x84 0xB8   //  read firmware revision
{{< /highlight >}}

<!-- more -->

### Simple register read

Let's perform a simple register read on the chip. This is 16 bytes long and requires two separate reads. We can read the first group of bytes by writing `0xFA 0x0F` and the second group of bytes by writing `0xFC 0xC9`. With each opcode, we read in 8 bytes. The BCM2835 C library makes this quite simple. Here's the code:

{{< highlight c >}}
//
//  Read the device serial number and return as string
//
uint8_t readSerialNumber(char *instr) {
    uint8_t buf[8] = {0xFA,0x0F};
    char *str = (char *) malloc(25);
    char *str2 = (char * ) malloc(13);
    if( bcm2835_i2c_write(buf,2) != BCM2835_I2C_REASON_OK ) {
        return SI7021_FAIL;
    }
    if( bcm2835_i2c_read(buf,8) != BCM2835_I2C_REASON_OK ) {
        printf("Read failed\n" );
        return SI7021_FAIL;
    }
    sprintf(str,"%02X %02X %02X %02X ",buf[0],buf[2],buf[4],buf[6]);
    buf[0] = 0xFC; buf[1] = 0xC9;
    bcm2835_i2c_write(buf,2);
    bcm2835_i2c_read(buf,8);
    sprintf(str2,"%02X %02X %02X %02X\0",buf[0],buf[2],buf[4],buf[6]);
    strcpy(instr, strcat(str,str2));
    return SI7021_OK;
}
{{< /highlight >}}

Notice how we allocate memory on the stack for two character pointers that we use as intermediate steps which compiling a string of bytes as characters. To call the function, we need to allocate memory for the pointer to the string on the caller's side, too. Then we pass the pointer to the function:

{{< highlight c >}}
//  read the device serial number
char * sstr = (char *) malloc(26);
readSerialNumber(sstr);
printf("%s\n",sstr);
{{< /highlight >}}

#### Reading the temperature

Notice that we have two I2C commands to read the temperature which we define as `SI7021_MT_HOLD` and `SI7021_MT_NOHOLD`. Since the device cannot take a reading in real-time, there is a delay between receiving the command and writing a value back to the host. To do this, we have two choices. We can either hold the host waiting for the data or we can poll the device to see when the data is ready. For the temperature conversion, we'll opt to wait, so the opcode will be `SI7021_MT_HOLD`. The way to do this is by stretching the clock long enough to cover the conversion latency. But how long do we have to wait? From table 2 in the datasheet, we see that a 12-bit relative humidity measurement takes 10-12 ms. The maximum conversion latency for 14 bit temperature (the default resolution) is almost 11 ms for a total latency of up to 23 ms.

How do we set the clock stretch timeout?

Fortunately, there's a BCM2835 register that we can set. The lower 16 bits of the `CLKT` register represents the `TOUT` field. Here, we can set the number of `SCL` clock cycles (not ms) to wait.

{{< figure src="images/CLKT.png" title="CLKT register" >}}

If we use the default I2C clock divider of 150 (`BCM2835_I2C_CLOCK_DIVIDER_150`) then our clock speed is 1.666 MHz or a period of 60 ns. If we wanted to wait for, say, 40 ms to provide a safety factor, then we would have to wait for 4 x 10^7 ns or 666,666 clock cycles. Since we can only represent numbers in 16 bits, we simply cannot wait that long for the slave device to hold the clock. A different strategy is required. Instead, we'll just slow the clock down even more. By lowering the overall I2C clock rate, we should be able to squeeze the wait cycle count down to the necessary level. So what if we reduced the I2C clock speed using `BCM2835_I2C_CLOCK_DIVIDER_626`? Then we have an I2C clock speed of about 399 kHz with a period of about 2.5 us. At that clock speed, we would wait 40000 us/2.5 us/cycle or 16000 cycles. We can easily manage that in the lower 16 bits of `CLKT`:

{{< highlight c >}}
void setTimeout(uint16_t timeout) {
     volatile uint32_t* stimeout = bcm2835_bsc1 + BCM2835_BSC_CLKT / 4;
     bcm2835_peri_write(stimeout, timeout);
}
{{< /highlight >}}

This code is straight out of [this tutorial](https://www.iot-programmer.com/index.php/books/22-raspberry-pi-and-the-iot-in-c/chapters-raspberry-pi-and-the-iot-in-c/61-raspberry-pi-and-the-iot-in-c-i2c-bus?showall=&start=3). What took me a while to understand is why the offset to the `CLKT` register at the BSC1 base address gets divided by 4. Well, the offset in bytes is 0x1C, but our addresses are 32 bits wide, so we divide the offset by 4 to get the actual address. The rest is self-explanatory.

Now that we've seen how to increase the clock waiting time to compensate for the conversion latency on the slave device, we can actually read the data. We've opted to hold the master. Reading the temperature requires simply writing the appropriate opcode and reading in two bytes of data (and a checksum, which we'll ignore for now.) The conversion to readable data is covered in the {% asset_link Si7021-A20.pdf Si7021 datasheet %}. It requires some floating point calculations:

{{< figure src="images/conversion.png" title="Converting raw data to temperature" >}}

To read the temperature from the device, we'll employ the following function:

{{< highlight c >}}
//
//  Read the current temperature
//
float readTemperature(uint8_t *status) {
    uint8_t buf[4] = { SI7021_MT_HOLD };
    if( bcm2835_i2c_read_register_rs(buf,buf,3) != BCM2835_I2C_REASON_OK ) {
        *status = SI7021_FAIL;
        return 0.0;
    }
    uint8_t msb = buf[0];
    uint8_t lsb = buf[1];
    unsigned int data16 = ((unsigned int) msb << 8) | (unsigned int) (lsb & 0xFC);
    float temp = (float) (-46.85 + (175.72 * data16 / (float) 65536));
    *status = SI7021_OK;
    return temp;
}
{{< /highlight >}}

### Reading the humidity

Reading the relative humidity is not much different, but as with [this tutorial](https://www.iot-programmer.com/index.php/books/22-raspberry-pi-and-the-iot-in-c/chapters-raspberry-pi-and-the-iot-in-c/61-raspberry-pi-and-the-iot-in-c-i2c-bus?showall=&start=3) it's written so as to keep the master "on hold" until the device is ready to read. The conversion of raw data to meaningful RH is also given in the manual.

{{< highlight c >}}
//
//  Read the humidity
//
float readHumidity() {
    uint8_t buf[4] = { SI7021_MRH_NOHOLD };
    bcm2835_i2c_write(buf,1);
    while( bcm2835_i2c_read(buf,3) == BCM2835_I2C_REASON_ERROR_NACK ) {
        bcm2835_delayMicroseconds(500);
    }
    uint8_t msb = buf[0]; uint8_t lsb = buf[1];
    uint16_t data16 = ((unsigned int) msb << 8) | (unsigned int) (lsb & 0xFC);
    float hum = -6 + (125.0 * (float) data16) / 65536;
    return hum;
}
{{< /highlight >}}

Notice here that we keep the master held waiting while we poll the device waiting for a response.

That's it. There's more to the device; but you should now have a good base for exploring more. My entire code is [here].

### References

- [Si7021 datasheet](Si7021-A20.pdf)
- [BCM2835 ARM peripherals](pdf/BCM2835-ARM-Peripherals.pdf)
- [Another (excellent) tutorial on interfacing to the Si7021](https://www.iot-programmer.com/index.php/books/22-raspberry-pi-and-the-iot-in-c/chapters-raspberry-pi-and-the-iot-in-c/61-raspberry-pi-and-the-iot-in-c-i2c-bus?showall=&start=3)
- [My full example code](https://gist.github.com/NSBum/964979dc0be03f737163a030d613504c)
