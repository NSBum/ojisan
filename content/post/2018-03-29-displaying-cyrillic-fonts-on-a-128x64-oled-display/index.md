---
title: Displaying Cyrillic fonts on a 128x64 OLED display
date: 2018-03-29 21:15:56
tags:
- electronics
- arduino
- programming
categories:
- electronics
---
Recently I picked up a couple inexpensive [128x64 pixel OLED displays](https://www.amazon.ca/gp/product/B01N78FUH7/ref=oh_aui_detailpage_o00_s02?ie=UTF8&psc=1) with an I2C interface. It turns out that displaying Russian text on these displays is not difficult. But it's non-obvious. This is a brief description of how to make it work.

{{< figure src="images/display.jpg" >}}

First, there's a variety of these little displays and they're all seemingly configured a little differently. I used [this](https://www.amazon.ca/gp/product/B01N78FUH7/ref=oh_aui_detailpage_o00_s02?ie=UTF8&psc=1) device for this test.

There are two options for libraries to simplify communicating with SSD1306 boards:

- [Adafruit SSD1306 library](https://github.com/adafruit/Adafruit_SSD1306)
- [u8g2 library](https://github.com/olikraus/u8g2)

The u8g2 library has a much more robust mechanism for selecting fonts, so that's what I used.

Here's the code in full:

{{< highlight cpp >}}
#include <Arduino.h>
#include <U8g2lib.h>

#ifdef U8X8_HAVE_HW_SPI
	#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
	#include <Wire.h>
#endif

/*
    Illustrating the use of cyrillic text on the 128x64 OLED display
*/
U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, SCL, SDA, U8X8_PIN_NONE);

void setup(void) {
	u8g2.begin();
	u8g2.enableUTF8Print();        // enable UTF8 support for the Arduino print() function
}

void loop(void) {
	// select a font with 11px height
	u8g2.setFont(u8g2_font_cu12_t_cyrillic);
	u8g2.firstPage();
	do {
		u8g2.setCursor(0, 40);
		u8g2.print("Всем привет!");
		u8g2.setCursor(0,12);
		u8g2.print("Как у вас?");
	} while ( u8g2.nextPage() );
}
{{< /highlight >}}

### References

- [SSD1306 datasheet](pdf/SSD1306.pdf)
