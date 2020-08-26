---
title: Scripting Indigo with Python
date: 2016-12-26 21:47:28
aliases: ['/2016/12/26/Scripting-Indigo-with-Python/']
authorbox: false
tags:
- programming
- home automation
- python
categories:
- home automation
---
I've used [Indigo](http://www.indigodomo.com) home automation software for a few years. It's a integrated home automation software environment for the Mac and its a solid stable and well-supported platform.

Within Indigo, it's possible to script triggers and actions either AppleScript or Python. It's funny - AppleScript often looks like the easier route to take. It looks more like plain English than Python. But as they say, looks are deceiving. Two bits of bad news put the nail in AppleScript's coffin for me - as least with Indigo.

First, I kept encountering a nasty bug when trying to talk to the Indigo Server via AppleScript run outside of the Indigo environment. You can [read all about it](http://forums.indigodomo.com/viewtopic.php?f=4&t=12857) on the Indigo forums, but basically AppleScript complained that Indigo Server wasn't running when it plainly _was_ running. I'm not usually one for complex workarounds such as thus that were being discussed on the forums.^[For example, some users have reported that restarting the AppleEvents daemon with `sudo killall -9 appleeventsd` can somehow allow external AppleScript applications to address the Indigo Server. It didn't work for me.] So, I began to give Python a consideration.

Then there's the iffy status of AppleScript coming out of Cupertino. The recent departure of Apple's head of Mac automation technologies and the fact that Apple dissolved the whole Mac automation team doesn't bode well for AppleScript.

### Setting up to talk to Indigo via the Indigo Plugin Host (IPH) and Python

To make it easier to address the `indigohost` which is buried ddep in the Application Support directory, you should just create an alias.

{{< highlight bash >}}
~|⇒ echo "alias indigohost='/Library/Application\ Support/Perceptive\ Automation/Indigo\ 7/IndigoPluginHost.app/Contents/MacOS/IndigoPluginHost'" >> ~/.zshrc
~|⇒ source ~/.zshrc
{{< /highlight >}}

I happen to use zsh so your terminal environment may be different.

Now to try out the `indigohost`:

{{< highlight bash >}}
indigohost -e 'return indigo.devices.len()'
{{< /highlight >}}

This should return the number of devices you have. Now you can script Indigo in Python both from _within_ the Indigo client context and as an external application.

To run a Python application as a separate file, it's just:

{{< highlight bash >}}
indigohost -x iphtest.py
{{< /highlight >}}

### Resources

Here are a few resources to get you started:

- [Indigo Scripting Tutorial](http://wiki.indigodomo.com/doku.php?id=indigo_7_documentation:plugin_scripting_tutorial)
- [Indigo Object Model Reference](http://wiki.indigodomo.com/doku.php?id=indigo_7_documentation:object_model_reference)
- [Indigo Devices](http://wiki.indigodomo.com/doku.php?id=indigo_7_documentation:device_class#thermostatdevice) - lots of short snippets in Python showing how you can user the Indigo Object Model (IOM) to work with them.

Good luck and have fun!
