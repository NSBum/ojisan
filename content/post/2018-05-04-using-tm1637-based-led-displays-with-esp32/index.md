---
title: Using TM1637-based LED displays with ESP32
date: 2018-05-04 15:56:54
aliases: ['/2018/05/04/Using-TM1637-based-LED-displays-with-ESP32/']
tags:
- c
- electronics
- esp32
- programming
- led
categories:
- electronics
---

There are three main types of 4 digit seven segment displays to be found on the market:

- **Bare displays without any driver.** These come in a variety of colors and with either decimal points or clock-type display with a colon dividing two sets of two digits.
- **74HC595-based displays.** Usually these displays have two daisy-chained 74HC595 shift registers and rely on the host controller to fill the serial registers *and* handle the multiplexing. Depending on the processor speed, this ends up being a significant overhead.
- **TM1637-based displays.** These displays reduce the burden on the host controller because all of the multiplexing is handled on the interface chip.

{{< figure src="images/esp32_led.jpg" title="Getting ESP32 to talk to TM1637-based displays" >}}

This post is about the TM1637 LED displays. The {% asset_link Datasheet_TM1637.pdf TM1637 datasheet %} is terrible, but fortunately there are several libraries for Arduino that provide a little insight into how others have managed to make this work. First things first, the communication protocol for this device is _not_ I2C despite what vendors on Aliexpress frequently claim.

<!-- more -->

{{< figure src="images/led.jpg" title="Old school LED display" >}}

Rather than try to explain this oddball communication protocol, I'll just start with a library that's already been published and that I've modified to display floating point numbers. The original library is [esp-32-tm1637](https://github.com/petrows/esp-32-tm1637) by [Peter Petrovich](https://github.com/petrows). It nicely handles the decimal display, leading zero display for four digit numbers. It works well, but cannot handle floating point numbers.

I've modified the library to display floating point numbers, both positive and negative. My version of the library can be found on [github](https://github.com/NSBum/esp-32-tm1637). To use this component, here's a snippet to get you started:

{{< highlight c >}}
#include "tm1637.h"

tm1637_lcd_t *led;

// application entry point
int app_main(void) {
   //Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    led = tm1637_init(27,26);
    tm1637_set_brightness(led,5);
    //   display a four digit integer
    //tm1637_set_number(led,4402);

    //   display a floating point number
   tm1637_set_float(led,-37.167);
   return 0;
}
{{< /highlight >}}

This version of the component handles positive and negative floating point numbers and correctly handles rounding to the size of the display.

### References

- [TM1637 datasheet](pdf/Datasheet_TM1637.pdf)
- [Improved ESP32 TM1637 component](https://github.com/NSBum/esp-32-tm1637)
- [A somewhat better description of the protocol](https://blog.3d-logic.com/2015/01/21/arduino-and-the-tm1637-4-digit-seven-segment-display/)
- [Source for the TM1637-based displays](https://robotdyn.com/catalog/displays/segment.html) - This company also has presence on Aliexpress.
