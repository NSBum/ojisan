---
title: Implementing a simple menu interface on OLED display
date: 2018-04-06 13:45:32
tags:
- electronics
- display
- OLED
- teensy
- i2c
categories:
- electronics
---
{{< vimeo 263554402 >}}

While working on a project to automate environmental control in our greenhouse, I needed to implement a menu interface on a small OLED display. In this sub-project, meant to test the concept, I've used a Teensy 3.1, a small I2C-driven 0.96" monochrome OLED display and a rotary encoder.

### Bill of materials:

- [Teensy 3.1](https://www.pjrc.com/store/teensy32.html) - the Teensy 3.1 is no longer available, but you can easily find the compatible Teensy 3.2.
- [0.96" yellow/blue I2C OLED module](https://www.amazon.ca/Yellow-Moudle-Display-Arduino-Raspberry/dp/B01N78FUH7/ref=sr_1_1_sspa?ie=UTF8&qid=1523037103&sr=8-1-spons&keywords=i2c+oled&psc=1) - I used the version with the yellow band at the top so that it this area could act as the highlighted region of the display.
- [Rotary encoder with push-button switch](https://www.adafruit.com/product/377) - I used this one from Adafruit, but there are many options.
- {% asset_link MC74HC14.pdf 74HC14 Schmitt Trigger inverter %} - to debounce the pushbutton.

### Description

This project is a proof-of-concept for using a rotary encoder to manipulate an on-screen menu of options. A number of electronics design concepts are used here.

<!-- more -->

### Circuit

There's nothing particularly unusual about the schematic, though I'll point out three different methods for debouncing the encoder and switch.

{{< figure src="images/Schematic.png" title="Rotary encoder switch schematic" >}}

First, about the rotary encoder, there are two sides with pins. One side has three pins and the other two pins. The three pin side is for the encoder and the two pin side is for the pushbutton switch. The center pin of the encoder is grounded and remaining two pins are connected to ground via a 0.01 uF capacitor. Together with the internal pullup resistors, this creates an RC filter that removes noise in the square wave pattern that the encoder should generate. It's a form of debouncing, though we still debounce in code. We use an inverting Schmitt trigger inverter to handle debouncing on the switch side.

There's a lot to say about Schmitt trigger debouncing, but since it has been written about extensively, I'll just refer you to [references](#references) at the end of this post for that. Same for the rotary encoder.

### Code

#### Setup

First, we'll initialize the the u8g2 library used to display the menu on our OLED.

{{< highlight cpp >}}

#include <U8g2lib.h>

U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, SCL, SDA, U8X8_PIN_NONE);

void setup() {
    u8g2.begin();
    u8g2.enableUTF8Print();
    u8g2.setFont(u8g2_font_courB12_tr);
    u8g2.setFontMode(0);

    //  initialize our serial interface
    //  initialize our interrupts for the rotary encoder
}
{{< /highlight >}}

Next, we setup our menu items.

{{< highlight cpp >}}
static const uint8_t NUM_MENU_ITEMS = 6;
const char* menu_items[] = {
    "Day lo temp",
    "Day hi temp",
    "Nite lo temp",
    "Nite hi temp",
    "Heat ON",
    "Heat OFF"
};
{{< /highlight >}}

And the interrupts for the rotary encoder/switch. There are many ways to read the rotary encoder. We could simply poll all the device pins, but since we have a robust interrupt capability on the Teensy, why not use that?

{{< highlight cpp >}}
enum PinAssignments {
    encoderPinA = 5,   // right
    encoderPinB = 6,   // left
    selectButton = 7
};

volatile unsigned int encoderPos = 0;  // a counter for the dial
unsigned int lastReportedPos = 1;   // change management
static boolean rotating = false;    // debounce management

// interrupt service routine vars
boolean A_set = false;
boolean B_set = false;

void setup() {
    pinMode(encoderPinA, INPUT);
    pinMode(encoderPinB, INPUT);
    pinMode(selectButton, INPUT);

    // turn on pullup resistors
    digitalWrite(encoderPinA, HIGH);
    digitalWrite(encoderPinB, HIGH);
    digitalWrite(selectButton, HIGH);

    // encoder pin on interrupt A
    attachInterrupt(digitalPinToInterrupt(encoderPinA), doEncoderA, CHANGE);

    // encoder pin on interrupt B
    attachInterrupt(digitalPinToInterrupt(encoderPinB), doEncoderB, CHANGE);

    // interrupt for the switch component
    attachInterrupt(digitalPinToInterrupt(selectButton), doSelect, RISING);
}
{{< /highlight >}}

Here, we make all of the encoder pins inputs and enable the pullup resistors. Then we have to attach the interrupts to each. We use `CHANGE` interrupt on the rotary encoder pins because we're interested in interpreting any change (up or down) whereas with the select button, we just want to know about the `RISING` status when it is pushed.

#### Using the interrupt service routines

Here I used a debounce approach I've adopted in similar projects. I'm not entirely fond of the 1ms delay in the interrupt service routines, but on a practical level, it works.

We interrupt whenever either the A or B inputs from the encoder transition. Then we look to see whether we've preceded or followed the other pulse to determine if which direction the user has rotated.

For the select button, I've debounced solely in hardware using the Schmitt trigger circuit depicted above.

#### Scrolling the menu items

The last task is to scroll the menu items on the screen in response to the encoder movement. There are really two tasks here. The first is to make sure that the encoder value is bounded by the limits of the menu. The value should not go below 0 (or whatever the wraparound value is for the unsigned type.) And it should not go higher than the number of menu items - 1 (for a zero-index array of menu items.) Here's how I do it:

{{< highlight cpp >}}
void loop() {
    rotating = true;  // reset the debouncer

    if (lastReportedPos != encoderPos) {
        encoderPos = (encoderPos > NUM_MENU_ITEMS -1 )?0:encoderPos;
        Serial.print("Index:");
        Serial.println(encoderPos, DEC);
        lastReportedPos = encoderPos;

        uint8_t tempPos = encoderPos;
        u8g2.clearDisplay();
        u8g2.firstPage();
        do {
            u8g2.setCursor(0, 12);
            u8g2.print(menu_items[tempPos++]);
            for( uint8_t i = 0; i < NUM_MENU_ITEMS; i++ ) {
                if( tempPos < NUM_MENU_ITEMS) {
                    u8g2.setCursor(0,16 + (i+1)*14);
                    u8g2.print(menu_items[tempPos++]);
                }
            }

        } while ( u8g2.nextPage() );
    }
}
{{< /highlight >}}

And that's it. The current menu item is shown in the yellow status area of the display, a UI feature that shows its availability for selection.

If you'd like to grab the entire code, you can find it [here](https://gist.github.com/NSBum/9c857a0e10fa5e702f2dff9cf8956e04):


<a id="references"></a>
### References

- [PEC11 12 mm incremental encoder datasheet](pdf/pec11.pdf)
- [Embed with Eliiot: Debounce your noisy buttons, Part I](https://hackaday.com/2015/12/09/embed-with-elliot-debounce-your-noisy-buttons-part-i/) - overview of the problem of switch noise.
- [Embed with Elliot: Debounce your noisy buttons, Part II](https://hackaday.com/2015/12/10/embed-with-elliot-debounce-your-noisy-buttons-part-ii/) - more on software debouncing
- [A Guide to Debouncing by Jack Ganssle](pdf/AGuideToDebouncing.pdf) - a nice pdf guide to debouncing techniques
- [How a rotary encoder works and how to use it with Arduino](https://howtomechatronics.com/tutorials/arduino/rotary-encoder-works-use-arduino/) - a good tutorial on how these devices work.
- [u8g2lib](https://github.com/olikraus/u8g2) - u8g2 library for OLED displays
- [Signal conditioning technical note](pdf/SignalConditioning.pdf) - a technical note from Bourns about debouncing rotary encoders.
