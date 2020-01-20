---
title: An easier way to automate synchronization of Anki profiles with AppleScript
date: 2016-04-05 21:38:04
aliases: ['/2016/04/05/An-easier-way-to-automate-synchronization-of-Anki-profiles-with-AppleScript/']
tags:
- anki
- programming
- applescript
- mac os
- os x
- automation
categories:
- anki
---
After waking up this morning with my mouse locked onto the Anki icon in the dock and trying to figure out how to get Activity Monitor up and running so I could force quite my Automator application that I [described yesterday](2016/04/04/Scheduling-synchronization-of-Anki-databases-on-OS-X/) I figured it was back-to-the-drawing board.

I'd like to have used the Accessibility Inspector to manipulate the PyQt objects in Anki's windows, they aren't exposed in a may that you can script them. But System Events rules all.

When Anki launches it offers a dialog box with profiles to sync (assuming you have multiple profiles.) Using AppleScript and System Events scripting, you can drive the keyboard as it manipulates the PyQt interface. Here's my solution. Yours may vary depending on where the profile in question lies in the list.

{{< highlight applescript >}}
tell application "Anki" to launch
delay 2.0

tell application "System Events"
	key code 125 -- down arrow to point at the profile to sync
	key code 36 -- Enter key
	delay 10.0 -- time to sync
	key code 12 using {command down} -- quit
end tell
{{< /highlight >}}

 Much less painless than Automator.
