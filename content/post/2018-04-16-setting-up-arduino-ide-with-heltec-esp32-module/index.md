---
title: Setting up Arduino IDE with Heltec ESP32 module for macOS
date: 2018-04-16 21:41:27
tags:
- electronics
- display
- OLED
- wifi
- wireless
- ESP32
- arduino
- macOS
categories:
- electronics
---
{{< figure src="images/module.jpg" title="Heltec WiFi Kit 32 ESP32 module" >}}

The [Heltec WIFI Kit 32](https://robotzero.one/heltec-wifi-kit-32/) is an interesting little module that integrates a WiFi/MCU SoC and a small OLED display on a single board. If you want to set up the Arduino IDE to work with this device and you're on macOS, this is for you. This particular ESP32 module has a number of impressive features: 240 MHz processor speed and 4 MB of flash memory. The onboard OLED display can be conveniently used for debugging.

### Install command line development tools

If you haven't already installed the command line dev tools, you'll need to do so.

{{< highlight bash >}}
xcode-select --install
{{< /highlight >}}

For some reason, I had to do this twice before it would install. It eventually succeeded.

### Install the Arduino support files

{{< highlight bash >}}
mkdir -p ~/Documents/Arduino/hardware/espressif
cd ~/Documents/Arduino/hardware/espressif
git clone https://github.com/espressif/arduino-esp32.git esp32
cd esp32
git submodule update --init --recursive
cd tools
python get.py
{{< /highlight >}}

With the last command `python get.py` I got an SSL error. I was able to workaround it but downloading the mkspiffs archive [here](https://github.com/igrr/mkspiffs/releases). My target machine is still on 10.11, and I downloaded [mkspiffs-0.2.1-osx.tar.gz](https://github.com/igrr/mkspiffs/releases/download/0.2.1/mkspiffs-0.2.1-osx.tar.gz). Then I just moved the archive (not unzipped) to `~/Arduino/hardware/espressif/esp32/tools/dist`. Then I reran:

{{< highlight bash >}}
python get.py
{{< /highlight >}}

It still threw an error related to openssl, so I updated the Python distribution with [Homebrew](https://brew.sh/)^[Homebrew is an excellent package manager for macOS. It's incredibly easy to install. See the link provided.], and updated openssl:

{{< highlight bash >}}
brew install openssl
brew install python
{{< /highlight >}}

Then I was able to run `get.py`:

{{< highlight bash >}}
python3.6 get.py
{{< /highlight >}}

Now you're setup to use the Arduino IDE to develop for this powerful little board.

{{< figure src="images/modulepins.jpg" title="Heltec WiFi Kit 32 pin diagram" >}}

### References

- [Source for this board](https://www.aliexpress.com/item/ESP32-Bluetooth-WIFI-Kit-OLED-Blue-0-96-inch-Display-Module-CP2102-32M-Flash-3-3V/32822005748.html)
- [IoT with ESP32](http://esp32.net/) - a trove of data and links about all things ESP32
- [ESP32 on Reddit](https://www.reddit.com/r/esp32/) - community discussion about ESP32
- [U.S.-based source of ESP32 boards](https://www.ezsbc.com/index.php/featured-products-list-home-page/wifi01-32.html#.WsuwtH8h2po) - these are U.S. made with prices that are competitive with Chinese sources.
- [ESP32 board comparison](https://www.youtube.com/watch?v=-769_YIeGmI) - a video comparison of ESP32 boards (only those without a display, though.)
- [Windows installation of ESP32 Arduino IDE support](https://robotzero.one/heltec-wifi-kit-32/)
