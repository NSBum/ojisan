---
title: "An alternative method for keyboard input switching on macOS"
date: 2020-01-11T04:59:54-05:00
draft: false
authorbox: false
sidebar: false
categories:
- programming
tags:
- macos
- anki
- applescript
- quicksilver
---
macOS offers a variety of virtual keyboard layouts which are accessible through System Preferences > Keyboard > Input Sources.
Because I spend about half of my time writing in Russian and half in English, rapid switching between keyboard layouts is important. Optionally in the Input Sources preference pane, you can choose to use the Caps lock key to toggle between sources. This almost always works well with the exception of [Anki](https://apps.ankiweb.net/). Presumably Anki's non-standard text management system thwarts the built-in Caps Lock/toggle mechanism for reasons that are not clear to me. Equally unclear is why this worked previously but now does not. I've not updated either Anki or the system software. It's a mystery. Nonetheless, began to search for an alternative method for switching between keyboard layout switching. What I developed relies on several tools:

1. [InputSourceSelector](https://github.com/minoki/InputSourceSelector), a small open-source project that offers command line access to input sources and keyboard layouts.
2. An AppleScript application that uses InputSourceSelector to perform the toggling function.
3. [Quicksilver](https://qsapp.com/index.php), an application that allows you to create keyboard triggers to perform custom tasks. It also requires the Terminal plug-in in Quicksilver.

## InputSourceSelector

[Download](https://github.com/minoki/InputSourceSelector)^[An alternative source that I forked just in case the original goes away is [here](https://github.com/NSBum/InputSourceSelector)] this repository, unzip and run `make` from the terminal. Copy the binary to somewhere in your `$PATH`. I used /usr/local/bin, i.e. `cp InputSourceSelector /usr/local/bin/InputSourceSelector`.

With this command line application in place, you should be able to list your keyboard layouts, select a new keyboard, and perform other similar actions. For example:

{{< highlight bash >}}
Alans-iMac:bin alan$ InputSourceSelector current
com.apple.keylayout.Canadian (Canadian English)
{{< /highlight >}}

To set the keyboard layout, the command is of the form:

{{< highlight bash >}}
com.apple.keylayout.Canadian (Canadian English)
Alans-iMac:bin alan$ InputSourceSelector select com.apple.keylayout.Russian-Phonetic
{{< /highlight >}}

## AppleScript application

I developed an AppleScript application to provide the toggle functionality. It works by reading the current keyboard layout and uses the current configuration to decide on which keyboard layout to select. Since I use only Canadian English and Russian Phonetic keyboards, it's a binary decision, hence the simple logic.

{{< highlight applescript >}}
--
--	Created by: Alan Duncan
--	Created on: 2020-01-11
--
--	Copyright (c) 2020 ОjisanSeiuchi
--	All Rights Reserved
--

-- This script toggles between Russian and Canadian English keyboard layouts.
-- Prerequisite InputSourceSelector can be found here:
-- https://github.com/NSBum/InputSourceSelector


use AppleScript version "2.4" -- Yosemite (10.10) or later
use scripting additions

set res to do shell script "/usr/local/bin/InputSourceSelector current"
set flag to offset of "Canadian" in res
if flag is 0 then
	do shell script "/usr/local/bin/InputSourceSelector select com.apple.keylayout.Canadian"
else
	do shell script "/usr/local/bin/InputSourceSelector select com.apple.keylayout.Russian-Phonetic"
end if
{{< /highlight >}}

Of course, this assumes that you have already enabled both of these keyboard layouts in System Preferences. Save the AppleScript application in a suitable location. The next step in the installation process is to setup a Quicksilver trigger to launch the AppleScript on command.

## Quicksilver

The application [Quicksilver](https://qsapp.com/) has been around for a long time, allowing you to trigger all sorts of actions from keyboard shortcuts. In this case, I simply created a trigger for my AppleScript above, assigned it a keystroke combination, and that's it.

That's all there is - nothing fancy; but if the built-in Caps lock system for keyboard toggling doesn't work or is unsuitable, this is a robust workaround.
